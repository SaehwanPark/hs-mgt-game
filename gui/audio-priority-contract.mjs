import { AUDIO_CUE_CONTRACT } from "./audio-cue-contract.mjs";

export const AUDIO_PRIORITY_MANAGER_SCHEMA = "audio-priority-manager-v1";

export const AUDIO_PRIORITY_LEVELS = Object.freeze([
  "critical",
  "major",
  "routine",
  "ambient",
]);

export const AUDIO_PRIORITY_POLICY = Object.freeze({
  schema_version: AUDIO_PRIORITY_MANAGER_SCHEMA,
  priority_order: AUDIO_PRIORITY_LEVELS,
  priority_values: Object.freeze({ critical: 4, major: 3, routine: 2, ambient: 1 }),
  maximum_critical_per_batch: 1,
  maximum_batch_cues: 4,
  maximum_queued_cues: 4,
  maximum_simultaneous_cue_voices: 1,
  routine_aggregation_minimum: 2,
  duplicate_window_ms: 300,
  duck_attack_ms: 40,
  duck_release_ms: 140,
  ducking_db: Object.freeze({ major: -8, critical: -12 }),
  storage_key: "hs-mgt-audio-preferences-v1",
});

const DEFAULT_CUE_ENTRIES = new Map(AUDIO_CUE_CONTRACT.entries.map((entry) => [entry.id, entry]));

export function priorityValue(priority) {
  return AUDIO_PRIORITY_POLICY.priority_values[String(priority ?? "routine")] ?? 0;
}

function entryMap(entries) {
  return new Map((Array.isArray(entries) ? entries : []).map((entry) => [entry.id, entry]));
}

export function planAudioCueBatch(requests = [], entries = AUDIO_CUE_CONTRACT.entries) {
  const catalog = entries === AUDIO_CUE_CONTRACT.entries ? DEFAULT_CUE_ENTRIES : entryMap(entries);
  const normalized = (Array.isArray(requests) ? requests : [])
    .map((request, index) => {
      const id = String(request?.id ?? request ?? "").trim();
      const entry = catalog.get(id);
      if (!entry) return null;
      return {
        id,
        entry,
        index,
        priority: entry.priority_class,
        priority_value: priorityValue(entry.priority_class),
      };
    })
    .filter(Boolean);
  const duplicateIds = [];
  const unique = [];
  const seen = new Set();
  for (const request of normalized) {
    if (seen.has(request.id)) {
      duplicateIds.push(request.id);
      continue;
    }
    seen.add(request.id);
    unique.push(request);
  }
  const ordered = [...unique].sort((left, right) => right.priority_value - left.priority_value || left.index - right.index);
  const critical = ordered.filter((request) => request.priority === "critical");
  const major = ordered.filter((request) => request.priority === "major");
  const routine = ordered.filter((request) => request.priority !== "critical" && request.priority !== "major");
  const selected = [];
  if (critical[0]) selected.push({ ...critical[0], batch_reason: "highest-critical" });
  selected.push(...major.map((request) => ({ ...request, batch_reason: "major-visible-consequence" })));
  if (routine[0]) {
    selected.push({
      ...routine[0],
      batch_reason: routine.length >= AUDIO_PRIORITY_POLICY.routine_aggregation_minimum ? "routine-aggregate" : "routine-visible-result",
      aggregated_count: routine.length,
    });
  }
  const bounded = selected.slice(0, AUDIO_PRIORITY_POLICY.maximum_batch_cues);
  return Object.freeze({
    selected: Object.freeze(bounded.map((request) => Object.freeze(request))),
    duplicate_ids: Object.freeze(duplicateIds),
    critical_suppressed_count: Math.max(0, critical.length - AUDIO_PRIORITY_POLICY.maximum_critical_per_batch),
    routine_aggregated_count: routine.length >= AUDIO_PRIORITY_POLICY.routine_aggregation_minimum ? routine.length : 0,
    overflow_count: Math.max(0, selected.length - bounded.length),
    request_count: normalized.length,
  });
}

export function validateAudioPriorityPolicy(policy = AUDIO_PRIORITY_POLICY) {
  const errors = [];
  if (policy?.schema_version !== AUDIO_PRIORITY_MANAGER_SCHEMA) errors.push("invalid-schema");
  if (JSON.stringify(policy?.priority_order) !== JSON.stringify(AUDIO_PRIORITY_LEVELS)) errors.push("invalid-priority-order");
  if (policy?.maximum_critical_per_batch !== 1) errors.push("critical-limit-must-be-one");
  for (const key of ["maximum_batch_cues", "maximum_queued_cues", "maximum_simultaneous_cue_voices"]) {
    if (!Number.isInteger(policy?.[key]) || policy[key] < 1) errors.push(`invalid-${key}`);
  }
  for (const key of ["duck_attack_ms", "duck_release_ms", "duplicate_window_ms"]) {
    if (!Number.isFinite(policy?.[key]) || policy[key] < 0) errors.push(`invalid-${key}`);
  }
  for (const priority of ["critical", "major"]) {
    if (!Number.isFinite(policy?.ducking_db?.[priority]) || policy.ducking_db[priority] >= 0) errors.push(`invalid-ducking-${priority}`);
  }
  return Object.freeze(errors);
}
