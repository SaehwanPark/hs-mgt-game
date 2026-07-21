export const AUDIO_CUE_CONTRACT_SCHEMA = "audio-cue-contract-v1";

export const AUDIO_CUE_POLICY = Object.freeze({
  normalization_gain: 0.08,
  peak_ceiling_dbfs: -3,
  interface_duration_ms: 90,
  event_duration_ms: 150,
  maximum_cue_voices: 1,
  cues_only_channels: Object.freeze(["interface", "event"]),
  written_equivalent_rule: "Every cue retains its visible source/status/effect text.",
});

const CUE_DEFINITIONS = [
  ["ui.action-confirm", "Confirm a visible draft or validation result", "routine", 90, 700, "Confirmed draft or host validation status", "confirm-tone", "visible-ui-or-host-validation"],
  ["ui.action-reject", "Mark a visible rejected draft or validation result", "major", 120, 900, "Error text and unchanged-session marker", "reject-tone", "host-rejection"],
  ["ui.action-add", "A local action entered the visible draft queue", "routine", 90, 500, "Draft-batch row added", "draft-add-tone", "local-draft-add"],
  ["ui.action-remove", "A local action left the visible draft queue", "routine", 90, 500, "Draft-batch row removed", "draft-remove-tone", "local-draft-remove"],
  ["ui.submit", "The host accepted a visible command batch for resolution", "major", 100, 900, "Submitted/awaiting-resolution status", "submit-tone", "host-accepted-submit"],
  ["ui.advance-month", "A committed transition advanced the visible month", "major", 110, 1200, "Month-resolution control and date change", "month-advance-tone", "committed-transition"],
  ["ui.report-received", "A committed visible report or refreshed observation arrived", "major", 110, 1200, "New report or briefing item with source and timing", "report-arrival-tone", "committed-visible-report"],
  ["ui.save-complete", "The host reported a visible save result", "major", 100, 1200, "Save/session status", "save-result-tone", "host-save-result"],
  ["event.project-complete", "A host-reported project reached a visible completion state", "major", 150, 1800, "Project completion event and changed process marker", "project-complete-tone", "committed-visible-project"],
  ["event.staffing-constraint", "A visible staffing constraint or workforce effect was reported", "major", 150, 1800, "Staffing status and affected capacity explanation", "staffing-constraint-tone", "actor-visible-workforce-result"],
  ["event.operating-loss", "A visible operating result reports a negative margin", "critical", 180, 2200, "Margin/cost result with direct visible contributors", "operating-loss-tone", "actor-visible-operating-result"],
  ["event.operating-recovery", "A visible operating result reports an improved margin", "major", 150, 1800, "Improved margin/result with direct visible contributors", "operating-recovery-tone", "actor-visible-operating-result"],
  ["event.payer-decision", "A host-committed payer decision is visible", "major", 150, 1800, "Payer response text and commitment/result marker", "payer-decision-tone", "committed-visible-payer-event"],
  ["event.regulatory-decision", "A host-committed regulatory decision is visible", "critical", 180, 2200, "Regulatory response text and status marker", "regulatory-decision-tone", "committed-visible-regulatory-event"],
  ["event.rival-expansion", "A public rival expansion signal is visible", "major", 150, 1800, "Public rival action/intelligence line with timing", "rival-expansion-tone", "public-visible-rival-event"],
  ["event.affiliation-milestone", "A committed affiliation stage milestone is visible", "major", 150, 1800, "Affiliation stage/status marker", "affiliation-milestone-tone", "committed-visible-affiliation-event"],
].map(([id, purpose, priority, duration_ms, cooldown_ms, equivalent, distinction, trigger_source]) => ({
  id,
  channel: id.startsWith("ui.") ? "interface" : "event",
  semantic_purpose: purpose,
  priority_class: priority,
  duration_ms,
  loudness_target_db: -18,
  peak_ceiling_dbfs: AUDIO_CUE_POLICY.peak_ceiling_dbfs,
  normalization_gain: AUDIO_CUE_POLICY.normalization_gain,
  cooldown_ms,
  text_equivalent: equivalent,
  distinction,
  visible_trigger_source: trigger_source,
  cues_only: true,
})).map((entry) => Object.freeze(entry));

const CUE_BY_ID = new Map(CUE_DEFINITIONS.map((entry) => [entry.id, entry]));

export const AUDIO_CUE_CONTRACT = Object.freeze({
  schema_version: AUDIO_CUE_CONTRACT_SCHEMA,
  policy: AUDIO_CUE_POLICY,
  entries: Object.freeze(CUE_DEFINITIONS),
});

export function audioCueContractFor(cueId) {
  return CUE_BY_ID.get(String(cueId ?? "").trim()) ?? null;
}

export function orderedAudioCueContracts() {
  return [...CUE_DEFINITIONS].sort((left, right) => left.id.localeCompare(right.id));
}

export function validateAudioCueContracts(entries = CUE_DEFINITIONS) {
  const errors = [];
  const seen = new Set();
  for (const entry of Array.isArray(entries) ? entries : []) {
    if (!entry?.id || seen.has(entry.id)) errors.push(`duplicate-or-missing-id:${entry?.id ?? ""}`);
    seen.add(entry?.id);
    if (!entry?.semantic_purpose || !entry?.priority_class || !entry?.duration_ms) errors.push(`missing-purpose-or-timing:${entry?.id ?? ""}`);
    if (!Number.isFinite(entry?.loudness_target_db) || !Number.isFinite(entry?.peak_ceiling_dbfs)) errors.push(`missing-levels:${entry?.id ?? ""}`);
    if (!Number.isFinite(entry?.cooldown_ms) || entry.cooldown_ms < 0) errors.push(`invalid-cooldown:${entry?.id ?? ""}`);
    if (!entry?.text_equivalent || !entry?.distinction || !entry?.visible_trigger_source) errors.push(`missing-equivalent-source:${entry?.id ?? ""}`);
    if (entry?.peak_ceiling_dbfs > AUDIO_CUE_POLICY.peak_ceiling_dbfs) errors.push(`peak-over-ceiling:${entry?.id ?? ""}`);
  }
  return Object.freeze(errors);
}

export function cueTriggerContract(cueId) {
  const entry = audioCueContractFor(cueId);
  if (!entry) return null;
  return Object.freeze({
    id: entry.id,
    channel: entry.channel,
    source: entry.visible_trigger_source,
    text_equivalent: entry.text_equivalent,
    trigger_is_visible_only: true,
  });
}
