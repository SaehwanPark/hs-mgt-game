export const AMBIENCE_CONTRACT_SCHEMA = "ambience-library-v1";

const TARGETS = [
  ["ambience.executive-office", "Executive office", 0.18, 0.0, 24, 196, "Muted office air and distant HVAC; no speech or clinical signal."],
  ["ambience.hospital-lobby", "Hospital lobby", 0.16, 0.0, 28, 220, "Subtle public-space room tone; no speech, alarm, or clinical severity."],
  ["ambience.hospital-campus-exterior", "Hospital campus exterior", 0.14, -58, 32, 174, "Distant exterior air and traffic bed; no identifying speech or siren focus."],
  ["ambience.construction-site", "Construction site", 0.17, -54, 36, 147, "Distant bounded worksite texture; no danger, urgency, or project outcome claim."],
  ["ambience.boardroom", "Boardroom", 0.15, 0.0, 26, 208, "Quiet room tone around a meeting; no speech or decision outcome claim."],
  ["ambience.press-policy-event", "Press or policy event", 0.15, -60, 30, 233, "Distant public-event room tone; no speech, slogans, or political outcome claim."],
  ["ambience.regional-city-bed", "Regional city bed", 0.13, -56, 40, 165, "Optional fictional city bed for the visible competitive month; no geography or acuity claim."],
].map(([id, label, gain, noise_floor_db, loop_seconds, cutoff_hz, equivalent]) => ({
  id,
  label,
  channel: "ambience",
  source_or_generation: "Hand-authored deterministic Web Audio oscillator recipe in this repository",
  license: "project-generated",
  source_hash_basis: "gui/ambience-contract.mjs",
  release_derivative: "runtime-generated from the same approved recipe; no release audio file",
  noise_floor_db,
  loop: Object.freeze({ start_ms: 0, end_ms: loop_seconds * 1000, seamless: true, reviewed: true, crossfade_ms: 80 }),
  loudness_target_db: -24,
  peak_ceiling_dbfs: -6,
  normalization_gain: gain,
  no_identifying_speech: true,
  no_copyrighted_music: true,
  no_real_institution_names: true,
  no_clinical_alarm: true,
  siren_policy: "rare-and-distant; not encoded in this recipe",
  reduced_audio: "Suppress or reduce to silence without removing written context.",
  text_equivalent: equivalent,
  visible_source: "Explicit presentation setting or active competitive-month context",
  fallback: "Ambience unavailable; written setting and decision-relevant text remain complete.",
  recipe: Object.freeze({
    waveform: "noise",
    filter: "lowpass",
    cutoff_hz,
    noise_floor_db,
    noise_amplitude: Math.max(0.03, Math.min(0.18, 0.03 + ((noise_floor_db + 60) / 60) * 0.15)),
    seed: [...id].reduce((value, character) => ((value * 33) + character.charCodeAt(0)) >>> 0, 5381),
    crossfade_ms: 80,
    duration_ms: loop_seconds * 1000,
  }),
})).map((entry) => Object.freeze(entry));

const AMBIENCE_BY_ID = new Map(TARGETS.map((entry) => [entry.id, entry]));

export const AMBIENCE_CONTRACT = Object.freeze({
  schema_version: AMBIENCE_CONTRACT_SCHEMA,
  default_id: "ambience.regional-city-bed",
  entries: Object.freeze(TARGETS),
});

export function ambienceFor(id) {
  return AMBIENCE_BY_ID.get(String(id ?? "").trim()) ?? null;
}

export function defaultAmbience() {
  return ambienceFor(AMBIENCE_CONTRACT.default_id);
}

export function validateAmbienceContracts(entries = TARGETS) {
  const errors = [];
  const ids = new Set();
  for (const entry of Array.isArray(entries) ? entries : []) {
    if (!entry?.id || ids.has(entry.id)) errors.push(`duplicate-or-missing-id:${entry?.id ?? ""}`);
    ids.add(entry?.id);
    if (!entry?.source_or_generation || !entry?.license || !entry?.source_hash_basis || !entry?.release_derivative) errors.push(`missing-provenance:${entry?.id ?? ""}`);
    if (!Number.isFinite(entry?.noise_floor_db) || !Number.isFinite(entry?.loudness_target_db) || !Number.isFinite(entry?.peak_ceiling_dbfs)) errors.push(`missing-levels:${entry?.id ?? ""}`);
    if (!entry?.loop?.seamless || !entry?.loop?.reviewed || entry.loop.end_ms <= entry.loop.start_ms || entry.loop.crossfade_ms <= 0) errors.push(`invalid-loop:${entry?.id ?? ""}`);
    if (entry?.recipe?.waveform !== "noise" || entry?.recipe?.filter !== "lowpass" || !Number.isFinite(entry?.recipe?.cutoff_hz) || entry.recipe.noise_floor_db !== entry.noise_floor_db || entry.recipe.crossfade_ms !== entry.loop.crossfade_ms || !Number.isFinite(entry.recipe?.seed)) errors.push(`invalid-recipe:${entry?.id ?? ""}`);
    if (!entry?.no_identifying_speech || !entry?.no_copyrighted_music || !entry?.no_real_institution_names || !entry?.no_clinical_alarm) errors.push(`rights-or-safety-gap:${entry?.id ?? ""}`);
    if (!entry?.reduced_audio || !entry?.text_equivalent || !entry?.visible_source || !entry?.fallback) errors.push(`missing-equivalent-fallback:${entry?.id ?? ""}`);
  }
  return Object.freeze(errors);
}
