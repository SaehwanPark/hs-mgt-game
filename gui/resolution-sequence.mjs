export const RESOLUTION_SEQUENCE_SCHEMA = "competitive-first-month-resolution-v1";

const STAGE_CONTRACTS = Object.freeze([
  Object.freeze({
    id: "submitted",
    label: "Submitted batch",
    fallback: "Submitted batch unavailable.",
    attention_priority: 30,
    surface_sync: "action-queue",
    audio_cue: "ui.submit",
  }),
  Object.freeze({
    id: "responses",
    label: "Visible institutional responses",
    fallback: "No visible institutional responses.",
    attention_priority: 10,
    surface_sync: "regional-board,reports",
    audio_cue: "ui.report-received",
  }),
  Object.freeze({
    id: "processes",
    label: "Process advancement",
    fallback: "Pending-process advancement unavailable.",
    attention_priority: 40,
    surface_sync: "pending-processes",
    audio_cue: null,
  }),
  Object.freeze({
    id: "operations",
    label: "Operating result",
    fallback: "Visible operating result unavailable.",
    attention_priority: 20,
    surface_sync: "metric-summary",
    audio_cue: "ui.advance-month",
  }),
  Object.freeze({
    id: "resources",
    label: "Resource changes",
    fallback: "Visible resource change unavailable.",
    attention_priority: 50,
    surface_sync: "resource-header",
    audio_cue: null,
  }),
  Object.freeze({
    id: "effects",
    label: "Direct committed effects",
    fallback: "No direct committed effects.",
    attention_priority: 5,
    surface_sync: "consequence-links,after-action-report",
    audio_cue: null,
  }),
  Object.freeze({
    id: "information",
    label: "Newly visible information",
    fallback: "No new visible information.",
    attention_priority: 15,
    surface_sync: "briefing,reports",
    audio_cue: "ui.report-received",
  }),
  Object.freeze({
    id: "pending",
    label: "Updated pending processes",
    fallback: "No pending processes.",
    attention_priority: 45,
    surface_sync: "pending-processes",
    audio_cue: null,
  }),
]);

const CONTRACT_BY_ID = new Map(STAGE_CONTRACTS.map((entry) => [entry.id, entry]));

function text(value, fallback) {
  const normalized = String(value ?? "").trim();
  return normalized || fallback;
}

function items(value, fallback) {
  const values = Array.isArray(value)
    ? value.map((entry) => text(entry, "Visible detail unavailable.")).filter(Boolean)
    : [];
  return values.length ? values : [fallback];
}

function stableStageId(value, index) {
  const id = String(value ?? "").trim().toLowerCase();
  return id || `unknown-${index + 1}`;
}

function contractFor(id) {
  return CONTRACT_BY_ID.get(id) ?? {
    id,
    label: "Additional visible resolution detail",
    fallback: "Visible resolution detail unavailable.",
    attention_priority: 60,
    surface_sync: "resolution-review",
    audio_cue: null,
  };
}

export function resolutionStageContracts() {
  return Object.freeze(STAGE_CONTRACTS.map((entry) => ({ ...entry })));
}

export function planResolutionSequence(envelope = {}, options = {}) {
  const sourceSteps = Array.isArray(envelope?.steps) ? envelope.steps : [];
  const byId = new Map();
  const unknown = [];
  sourceSteps.forEach((step, index) => {
    const id = stableStageId(step?.id, index);
    if (CONTRACT_BY_ID.has(id) && !byId.has(id)) byId.set(id, step);
    else if (!CONTRACT_BY_ID.has(id)) unknown.push({ step, index, id });
  });
  const planned = STAGE_CONTRACTS.map((contract, index) => {
    const step = byId.get(contract.id);
    return {
      stage_id: contract.id,
      label: contract.label,
      source: text(step?.source, "Host resolution source unavailable."),
      items: items(step?.items, contract.fallback),
      attention_priority: contract.attention_priority,
      priority_semantics: "display-order-only; not severity or hidden state",
      surface_sync: contract.surface_sync.split(","),
      audio_cue: contract.audio_cue,
      replay_order: index,
      present: Boolean(step),
      reduced_motion: Boolean(options.reduced_motion),
    };
  });
  unknown.forEach(({ step, id }) => {
    const contract = contractFor(id);
    planned.push({
      stage_id: contract.id,
      label: contract.label,
      source: text(step?.source, "Host resolution source unavailable."),
      items: items(step?.items, contract.fallback),
      attention_priority: contract.attention_priority,
      priority_semantics: "display-order-only; not severity or hidden state",
      surface_sync: contract.surface_sync.split(","),
      audio_cue: contract.audio_cue,
      replay_order: planned.length,
      present: true,
      reduced_motion: Boolean(options.reduced_motion),
    });
  });
  return Object.freeze(planned.map((entry) => Object.freeze({
    ...entry,
    items: Object.freeze([...entry.items]),
    surface_sync: Object.freeze([...entry.surface_sync]),
  })));
}

export function sequenceForReplay(envelope = {}, options = {}) {
  return planResolutionSequence(envelope, options).map((entry) => ({
    stage_id: entry.stage_id,
    attention_priority: entry.attention_priority,
    audio_cue: entry.audio_cue,
    surface_sync: [...entry.surface_sync],
    replay_order: entry.replay_order,
  }));
}

export function sequenceFingerprint(envelope = {}, options = {}) {
  return JSON.stringify(sequenceForReplay(envelope, options));
}

export function sequenceForSkip(envelope = {}, options = {}) {
  const sequence = planResolutionSequence(envelope, options);
  return Object.freeze({
    active_index: Math.max(sequence.length - 1, 0),
    written_stage_count: sequence.length,
    skipped: true,
    report_text_retained: sequence.every((entry) => entry.items.length > 0),
  });
}
