export const MUSIC_STEM_CONTRACT_SCHEMA = "adaptive-music-stem-contract-v1";

export const MUSIC_STEM_ROLES = Object.freeze([
  "base_pulse",
  "institutional_motif",
  "pressure_layer",
  "policy_layer",
  "transition_cadence",
]);

function stem(waveform, frequency, duration_ms, offset_ms = 0) {
  return Object.freeze({
    waveform,
    frequency,
    duration_ms,
    offset_ms,
    crossfade_ms: 260,
  });
}

function state(id, label, semantic_purpose, visible_trigger_source, text_equivalent, frequencies, loop_duration_ms = 4200) {
  const [base, motif, pressure, policy, cadence] = frequencies;
  return Object.freeze({
    id,
    label,
    channel: "music",
    semantic_purpose,
    visible_trigger_source,
    text_equivalent,
    fallback: "Music unavailable or suppressed; the visible heading, status, source, and result remain complete.",
    normalization_gain: 0.07,
    crossfade_ms: 260,
    loop_duration_ms,
    stem_order: MUSIC_STEM_ROLES,
    stems: Object.freeze({
      base_pulse: stem("sine", base, loop_duration_ms),
      institutional_motif: stem("triangle", motif, loop_duration_ms),
      pressure_layer: stem("sine", pressure, loop_duration_ms),
      policy_layer: stem("triangle", policy, loop_duration_ms),
      transition_cadence: stem("sine", cadence, 900, loop_duration_ms - 900),
    }),
  });
}

const ENTRIES = [
  state(
    "menu",
    "Menu and planning",
    "Orient the player to an open planning surface without urgency.",
    "Explicit menu or planning page stage",
    "Menu heading, campaign choice, and planning controls",
    [196, 246.94, 293.66, 220, 392],
    3600,
  ),
  state(
    "stable_operations",
    "Stable operations",
    "Support a readable operating summary when visible pressure is not dominant.",
    "Actor-visible operating summary and status with no stronger state marker",
    "Stable operating summary, current status, and visible briefing",
    [174.61, 220, 261.63, 196, 349.23],
  ),
  state(
    "pressure",
    "Visible pressure",
    "Mark visible operating pressure without turning it into moral judgment or outcome certainty.",
    "Visible negative margin, unmet demand, runway signal, or pressure language",
    "Source-linked pressure banner and affected metric",
    [146.83, 185, 110, 174.61, 293.66],
    3200,
  ),
  state(
    "regulatory_scrutiny",
    "Regulatory scrutiny",
    "Mark a visible regulatory or policy review context without predicting its result.",
    "Actor-visible regulatory, oversight, mandate, or policy-review report/stage",
    "Regulatory letter, policy report, and current review status",
    [164.81, 207.65, 123.47, 246.94, 329.63],
    4400,
  ),
  state(
    "competitive_escalation",
    "Competitive escalation",
    "Mark a visible public-market or rival-action context without exposing private intent.",
    "Actor-visible public rival action, market escalation, or competitive report",
    "Public market signal, observed rival line, and source timing",
    [155.56, 233.08, 138.59, 207.65, 311.13],
    4000,
  ),
  state(
    "affiliation_negotiation",
    "Affiliation or negotiation",
    "Mark a visible partner, coalition, or negotiation context without implying agreement.",
    "Actor-visible affiliation, partner, coalition, or negotiation stage/report",
    "Partner, coalition, negotiation, and commitment status text",
    [185, 277.18, 155.56, 246.94, 369.99],
    4600,
  ),
  state(
    "debrief",
    "Debrief",
    "Close a completed session with a reflective transition rather than a victory signal.",
    "Explicit debrief page stage or completed visible session",
    "Debrief heading, committed timeline, and educational summary",
    [130.81, 196, 164.81, 220, 261.63],
    4800,
  ),
].map((entry) => Object.freeze(entry));

const BY_ID = new Map(ENTRIES.map((entry) => [entry.id, entry]));
const PRESSURE_WORDS = /watch|strained|pressure|shortage|constraint|unmet|negative|runway/i;
const REGULATORY_WORDS = /regulat|oversight|mandate|compliance|policy review|review letter/i;
const COMPETITIVE_WORDS = /rival|competitive|competition|market escalation|public expansion/i;
const AFFILIATION_WORDS = /affiliation|partner|coalition|negotiat|commitment review/i;
const VISIBLE_SCALAR_KEYS = Object.freeze([
  "title",
  "kind",
  "detail",
  "status",
  "status_label",
  "summary",
  "label",
  "value",
  "unit",
  "text",
  "message",
  "source",
  "equivalent",
  "public_signal",
]);

function visibleString(value) {
  return JSON.stringify(value ?? "").toLowerCase();
}

function visibleScalar(value) {
  if (value == null || (typeof value !== "string" && typeof value !== "number" && typeof value !== "boolean")) return "";
  return String(value);
}

function visibleValues(value) {
  if (Array.isArray(value)) return value.flatMap((entry) => visibleValues(entry));
  const scalar = visibleScalar(value);
  if (scalar) return [scalar];
  if (!value || typeof value !== "object") return [];
  return VISIBLE_SCALAR_KEYS.map((key) => visibleScalar(value[key])).filter(Boolean);
}

function visibleText(input = {}) {
  const observation = input.observation ?? input.after?.observation ?? {};
  const operations = observation.operations ?? {};
  return visibleString([
    visibleScalar(input.stage ?? input.page_stage ?? input.session?.stage),
    ...visibleValues(input.briefing),
    ...visibleValues(input.reports),
    ...visibleValues(input.processes),
    ...visibleValues(input.actors),
    ...visibleValues(input.decisions),
    ...visibleValues(observation.market_bullets),
    ...visibleValues(observation.policy_bullets),
    ...visibleValues(observation.cash_runway_signal),
    ...visibleValues(observation.workforce_trust),
    ...visibleValues(observation.in_flight_projects),
    visibleScalar(operations.margin),
    visibleScalar(operations.unmet_demand),
  ]);
}

export function musicStateFor(id) {
  return BY_ID.get(String(id ?? "").trim()) ?? null;
}

export function classifyVisibleMusicState(input = {}) {
  const stage = String(input.stage ?? input.page_stage ?? input.session?.stage ?? "").trim().toLowerCase();
  if (stage === "menu" || stage === "planning") return "menu";
  if (stage === "debrief" || input.done === true || input.session?.done === true) return "debrief";
  const text = visibleText(input);
  if (REGULATORY_WORDS.test(text)) return "regulatory_scrutiny";
  if (AFFILIATION_WORDS.test(text)) return "affiliation_negotiation";
  if (COMPETITIVE_WORDS.test(text)) return "competitive_escalation";
  const operations = input.observation?.operations ?? input.after?.observation?.operations ?? {};
  if (Number(operations.margin) < 0 || Number(operations.unmet_demand) > 0 || PRESSURE_WORDS.test(text)) return "pressure";
  return "stable_operations";
}

export function musicPlanFromVisible(input = {}) {
  const id = classifyVisibleMusicState(input);
  const entry = musicStateFor(id) ?? musicStateFor("stable_operations");
  return Object.freeze({
    state: entry.id,
    visible_source: entry.visible_trigger_source,
    text_equivalent: entry.text_equivalent,
    fallback: entry.fallback,
    crossfade_ms: entry.crossfade_ms,
    stem_order: entry.stem_order,
  });
}

export function musicReplaySequence(inputs = []) {
  return Object.freeze((Array.isArray(inputs) ? inputs : []).map((input) => classifyVisibleMusicState(input)));
}

export const MUSIC_STEM_CONTRACT = Object.freeze({
  schema_version: MUSIC_STEM_CONTRACT_SCHEMA,
  stem_roles: MUSIC_STEM_ROLES,
  entries: Object.freeze(ENTRIES),
});

export function validateMusicStemContracts(entries = ENTRIES) {
  const errors = [];
  const ids = new Set();
  for (const entry of Array.isArray(entries) ? entries : []) {
    if (!entry?.id || ids.has(entry.id)) errors.push(`duplicate-or-missing-id:${entry?.id ?? ""}`);
    ids.add(entry?.id);
    if (!entry?.semantic_purpose || !entry?.visible_trigger_source || !entry?.text_equivalent || !entry?.fallback) errors.push(`missing-meaning:${entry?.id ?? ""}`);
    if (!Number.isFinite(entry?.crossfade_ms) || entry.crossfade_ms <= 0 || !Number.isFinite(entry?.loop_duration_ms) || entry.loop_duration_ms <= entry.crossfade_ms) errors.push(`invalid-timing:${entry?.id ?? ""}`);
    if (JSON.stringify(entry?.stem_order) !== JSON.stringify(MUSIC_STEM_ROLES)) errors.push(`invalid-stem-order:${entry?.id ?? ""}`);
    for (const role of MUSIC_STEM_ROLES) {
      const recipe = entry?.stems?.[role];
      if (!recipe || !Number.isFinite(recipe.frequency) || !Number.isFinite(recipe.duration_ms) || recipe.crossfade_ms <= 0) errors.push(`invalid-stem:${entry?.id ?? ""}:${role}`);
    }
  }
  return Object.freeze(errors);
}
