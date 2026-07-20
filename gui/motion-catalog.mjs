export const MOTION_CATALOG_SCHEMA = "motion-catalog-v1";

export const MOTION_POLICY = Object.freeze({
  max_simultaneous_animations: 3,
  default_duration_ms: 240,
  baseline_frame_budget_ms: 16,
  ordering_rule: "Replay order, then explicit sequence, then category ID and target ID.",
  input_rule: "Motion never owns focus, blocks input, or delays a host command.",
  hidden_information_rule: "Motion may emphasize only information already visible in text or state.",
  reduced_motion_rule: "Use an immediate static replacement with the same written information.",
  interruption_rule: "Cancel or replace local presentation motion without changing host state.",
});

const CATALOG = [
  {
    id: "focus-transition",
    label: "Focus transition",
    semantic_purpose: "Show where local keyboard or board focus moved.",
    duration_ms: 160,
    easing: "ease-out",
    reduced_motion_replacement: "Move focus immediately and retain the visible focus ring.",
    interruption_behavior: "Cancel the prior local focus effect and keep the latest focus target.",
    replay_behavior: "Replay in explicit sequence order; never animate a hidden target.",
    deterministic_order: 10,
    input_behavior: "Does not capture focus or delay input.",
    performance_budget_ms: 16,
  },
  {
    id: "report-arrival",
    label: "Report arrival",
    semantic_purpose: "Signal that a new actor-visible report is available.",
    duration_ms: 240,
    easing: "ease-out",
    reduced_motion_replacement: "Insert the report and expose its written source/status immediately.",
    interruption_behavior: "Keep the report in the DOM even when its arrival cue is interrupted.",
    replay_behavior: "Replay only the visible report order recorded for the turn.",
    deterministic_order: 20,
    input_behavior: "Does not block report review or command input.",
    performance_budget_ms: 16,
  },
  {
    id: "month-transition",
    label: "Month transition",
    semantic_purpose: "Orient the player to a committed month change.",
    duration_ms: 360,
    easing: "ease-in-out",
    reduced_motion_replacement: "Replace the month marker and written summary immediately.",
    interruption_behavior: "Stop the local transition and retain the committed month text.",
    replay_behavior: "Replay after host-committed order, never before the turn is available.",
    deterministic_order: 30,
    input_behavior: "Does not hold the command boundary or host resolution.",
    performance_budget_ms: 16,
  },
  {
    id: "project-progress",
    label: "Project progress",
    semantic_purpose: "Make a visible project commitment’s reported progress easier to scan.",
    duration_ms: 300,
    easing: "linear",
    reduced_motion_replacement: "Show the current reported progress and timing text statically.",
    interruption_behavior: "Keep the latest host-reported progress without interpolation.",
    replay_behavior: "Replay only reported progress points in recorded order.",
    deterministic_order: 40,
    input_behavior: "Does not disable project review or action controls.",
    performance_budget_ms: 16,
  },
  {
    id: "project-completion",
    label: "Project completion",
    semantic_purpose: "Mark a host-reported project completion as a visible conclusion.",
    duration_ms: 420,
    easing: "ease-out",
    reduced_motion_replacement: "Show the completion label, source, and consequence text immediately.",
    interruption_behavior: "Retain the completion report if the local emphasis is interrupted.",
    replay_behavior: "Replay after the host reports completion; do not predict it.",
    deterministic_order: 50,
    input_behavior: "Does not gate the next command or host transition.",
    performance_budget_ms: 16,
  },
  {
    id: "new-visible-rival-action",
    label: "New visible rival action",
    semantic_purpose: "Draw attention to a newly observed public rival action.",
    duration_ms: 280,
    easing: "ease-out",
    reduced_motion_replacement: "Show the public action, observation timing, and missing private detail in text.",
    interruption_behavior: "Keep the public action and its timing when emphasis stops.",
    replay_behavior: "Replay only the recorded actor-visible observation order.",
    deterministic_order: 60,
    input_behavior: "Does not reveal private rival activity or block review.",
    performance_budget_ms: 16,
  },
  {
    id: "status-change",
    label: "Status change",
    semantic_purpose: "Emphasize a visible status label change without adding severity.",
    duration_ms: 220,
    easing: "ease-out",
    reduced_motion_replacement: "Replace the status label and non-color pattern immediately.",
    interruption_behavior: "Keep the latest visible status and text equivalent.",
    replay_behavior: "Replay statuses in committed or observed order only.",
    deterministic_order: 70,
    input_behavior: "Does not disable status review or local navigation.",
    performance_budget_ms: 16,
  },
  {
    id: "metric-delta-reveal",
    label: "Metric delta reveal",
    semantic_purpose: "Guide attention to an explicit visible metric change.",
    duration_ms: 260,
    easing: "ease-out",
    reduced_motion_replacement: "Show the exact before value, after value, and delta in text.",
    interruption_behavior: "Keep both exact values and the delta when emphasis stops.",
    replay_behavior: "Replay the host-reported metric order without recomputing values.",
    deterministic_order: 80,
    input_behavior: "Does not delay command validation or input.",
    performance_budget_ms: 16,
  },
  {
    id: "relationship-line-change",
    label: "Relationship-line change",
    semantic_purpose: "Orient the player to a visible relationship presentation change.",
    duration_ms: 180,
    easing: "ease-out",
    reduced_motion_replacement: "Replace the line pattern and written relationship label immediately.",
    interruption_behavior: "Keep the latest visible line pattern; do not interpolate a relationship.",
    replay_behavior: "Replay explicit visible line updates in deterministic order.",
    deterministic_order: 90,
    input_behavior: "Does not capture board input or assert direction/cause.",
    performance_budget_ms: 16,
  },
].map((entry) => Object.freeze({ ...entry }));

const CATALOG_BY_ID = new Map(CATALOG.map((entry) => [entry.id, entry]));

export const MOTION_CATALOG = Object.freeze({
  schema_version: MOTION_CATALOG_SCHEMA,
  policy: MOTION_POLICY,
  entries: Object.freeze(CATALOG),
});

function text(value, fallback = "Unavailable") {
  const normalized = String(value ?? "").trim();
  return normalized || fallback;
}

function number(value, fallback = 0) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

export function motionFor(id) {
  return CATALOG_BY_ID.get(String(id ?? "").trim().toLowerCase()) ?? null;
}

export function orderedMotionCatalog() {
  return [...CATALOG].sort((left, right) => left.deterministic_order - right.deterministic_order || left.id.localeCompare(right.id));
}

function normalizeEvent(event, index) {
  const contract = motionFor(event?.motion_id ?? event?.id) ?? motionFor("status-change");
  return {
    motion_id: contract.id,
    sequence: number(event?.sequence, index),
    batch: Math.max(0, number(event?.batch, 0)),
    target_id: text(event?.target_id, "visible-surface"),
    visible_label: text(event?.visible_label, contract.label),
    source: text(event?.source, "Visible presentation source unavailable"),
    contract,
  };
}

export function replayMotionSequence(events = [], options = {}) {
  const reducedMotion = Boolean(options.reduced_motion);
  const normalized = (Array.isArray(events) ? events : [])
    .map(normalizeEvent)
    .sort((left, right) => left.batch - right.batch || left.sequence - right.sequence || left.contract.deterministic_order - right.contract.deterministic_order || left.target_id.localeCompare(right.target_id));
  return Object.freeze(normalized.map((event, index) => Object.freeze({
    ...event,
    replay_index: index,
    duration_ms: reducedMotion ? 0 : event.contract.duration_ms,
    easing: reducedMotion ? "step-end" : event.contract.easing,
    replacement: reducedMotion ? event.contract.reduced_motion_replacement : null,
  })));
}

export function interruptMotion(activeMotionId, nextMotionId) {
  const active = motionFor(activeMotionId);
  const next = motionFor(nextMotionId);
  return Object.freeze({
    interrupted: active?.id ?? null,
    replacement: next?.id ?? null,
    host_state_changed: false,
    written_information_retained: true,
  });
}

export function motionLoadReport(events = []) {
  const replay = replayMotionSequence(events);
  const batches = new Map();
  for (const event of replay) batches.set(event.batch, (batches.get(event.batch) ?? 0) + 1);
  const maximum = Math.max(0, ...batches.values());
  return Object.freeze({
    maximum_simultaneous: maximum,
    allowed_maximum: MOTION_POLICY.max_simultaneous_animations,
    within_simultaneous_budget: maximum <= MOTION_POLICY.max_simultaneous_animations,
    declared_frame_budget_ms: MOTION_POLICY.baseline_frame_budget_ms,
    entries: replay.length,
  });
}
