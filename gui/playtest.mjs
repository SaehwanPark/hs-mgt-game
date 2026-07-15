export const PLAYTEST_CAPTURE_SCHEMA = "gui-playtest-v1";

export const PLAYTEST_FAILURE_CLASSES = Object.freeze([
  "adapter_error",
  "submit_rejected",
  "unsupported_schema",
  "missing_control",
  "semantic_gap",
  "capture_invalid",
  "task_incomplete",
]);

const EVENT_FIELDS = Object.freeze({
  onboarding_opened: ["campaign", "next_action"],
  onboarding_next: ["target"],
  settings_changed: ["setting", "value"],
  recovery_retry: ["target"],
  semantic_snapshot: ["sections", "controls", "status"],
  session_loaded: ["campaign", "turn", "done", "schema"],
  command_submitted: ["campaign", "command", "turn"],
  validation_result: ["valid", "code", "message"],
  audio_cue: ["id", "source", "equivalent"],
  history_observed: ["turn", "state_hash", "transition_count"],
  failure: ["class", "message", "recoverable"],
  task_completed: ["role", "task", "result"],
});

const SESSION_FIELDS = [
  "session_id",
  "campaign",
  "seed",
  "role",
  "task",
  "viewport",
  "interface_mode",
  "accessibility_mode",
  "capture_method",
  "screenshot_refs",
];

const SNAPSHOT_IDS = [
  "onboarding-panel",
  "presentation-state",
  "campaign-coverage-panel",
  "campaign-decision-list",
  "action-builder",
  "resolution-panel",
  "audio-panel",
  "settings-panel",
  "recovery-panel",
];

function safeScalar(value) {
  if (typeof value === "string") return value.slice(0, 320);
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "boolean") return value;
  return undefined;
}

function safeValue(value) {
  const scalar = safeScalar(value);
  if (scalar !== undefined) return scalar;
  if (!Array.isArray(value)) return undefined;
  return value
    .map(safeScalar)
    .filter((entry) => entry !== undefined)
    .slice(0, 64);
}

function pickFields(fields, names) {
  const picked = {};
  for (const name of names) {
    const value = safeValue(fields?.[name]);
    if (value !== undefined) picked[name] = value;
  }
  return picked;
}

function pickEventFields(type, fields) {
  if (type === "semantic_snapshot") {
    return {
      sections: (Array.isArray(fields?.sections) ? fields.sections : []).slice(0, 32).map((section) => ({
        id: safeScalar(section?.id) ?? "section",
        hidden: Boolean(section?.hidden),
        text: safeScalar(section?.text) ?? "",
      })),
      controls: (Array.isArray(fields?.controls) ? fields.controls : []).slice(0, 128).map((control) => ({
        id: safeScalar(control?.id) ?? "control",
        role: safeScalar(control?.role) ?? "control",
        label: safeScalar(control?.label) ?? "",
        disabled: Boolean(control?.disabled),
        hidden: Boolean(control?.hidden),
      })),
      status: safeScalar(fields?.status) ?? "",
    };
  }
  return pickFields(fields, EVENT_FIELDS[type]);
}

function normalizeSession(metadata) {
  return pickFields(metadata, SESSION_FIELDS);
}

export function semanticSnapshot(root = globalThis.document) {
  const sections = [];
  const controls = [];
  for (const id of SNAPSHOT_IDS) {
    const node = root?.querySelector?.(`#${id}`);
    if (!node) continue;
    const sectionHidden = Boolean(node.hidden);
    sections.push({ id, hidden: sectionHidden, text: sectionHidden ? "" : String(node.textContent ?? "").trim().slice(0, 320) });
    for (const control of node.querySelectorAll?.("button, input, select, textarea") ?? []) {
      controls.push({
        id: control.id || `${id}-control`,
        role: control.getAttribute?.("role") ?? control.tagName?.toLowerCase() ?? "control",
        label: control.hidden || sectionHidden ? "" : String(control.getAttribute?.("aria-label") ?? control.textContent ?? control.name ?? "").trim().slice(0, 160),
        disabled: Boolean(control.disabled),
        hidden: Boolean(control.hidden),
      });
    }
  }
  const status = String(root?.querySelector?.("#presentation-state")?.textContent ?? "").trim().slice(0, 320);
  return { sections, controls, status };
}

export function createPlaytestRecorder({ metadata = {}, maxEvents = 512 } = {}) {
  const session = normalizeSession(metadata);
  const events = [];
  let detach = null;

  function record(type, fields = {}) {
    const names = EVENT_FIELDS[type];
    if (!names || events.length >= maxEvents) return { ok: false, code: "unsupported_or_full_capture" };
    events.push({ sequence: events.length, type, ...pickEventFields(type, fields) });
    return { ok: true, sequence: events.length - 1 };
  }

  function recordFailure(failure) {
    const failureClass = PLAYTEST_FAILURE_CLASSES.includes(failure?.class)
      ? failure.class
      : "capture_invalid";
    return record("failure", {
      class: failureClass,
      message: failure?.message ?? "Unclassified playtest failure.",
      recoverable: failure?.recoverable !== false,
    });
  }

  function recordSnapshot(root) {
    const snapshot = semanticSnapshot(root);
    return record("semantic_snapshot", snapshot);
  }

  function attach(root = globalThis.document) {
    detach?.();
    if (!root?.addEventListener) return () => {};
    const eventName = (node) => node?.dataset?.playtestEvent ?? null;
    const onClick = (event) => {
      if (event.__hsMgtPlaytestRecorded) return;
      const node = event.target?.closest?.("[data-playtest-event]");
      const type = eventName(node);
      if (type === "onboarding_next") record(type, { target: node.id || "briefing" });
      if (type === "recovery_retry") record(type, { target: node.id || "current-read" });
    };
    const onChange = (event) => {
      if (event.__hsMgtPlaytestRecorded) return;
      const node = event.target?.closest?.("[data-playtest-setting]");
      if (node) record("settings_changed", { setting: node.dataset.playtestSetting, value: node.checked ?? node.value });
    };
    const onSubmit = (event) => {
      const form = event.target;
      if (form?.dataset?.playtestEvent === "command_submitted") {
        record("command_submitted", { command: form.dataset.command ?? "", turn: form.dataset.turn ?? "" });
      }
    };
    root.addEventListener("click", onClick);
    root.addEventListener("change", onChange);
    root.addEventListener("submit", onSubmit);
    detach = () => {
      root.removeEventListener("click", onClick);
      root.removeEventListener("change", onChange);
      root.removeEventListener("submit", onSubmit);
      detach = null;
    };
    return detach;
  }

  function capture() {
    const evidence = {
      commands: events.filter((event) => event.type === "command_submitted").map(({ sequence, ...event }) => ({ sequence, ...event })),
      validations: events.filter((event) => event.type === "validation_result"),
      audio_cues: events.filter((event) => event.type === "audio_cue"),
      history_hashes: events.filter((event) => event.type === "history_observed"),
      failures: events.filter((event) => event.type === "failure"),
    };
    return {
      schema_version: PLAYTEST_CAPTURE_SCHEMA,
      session: { ...session },
      events: events.map((event) => ({ ...event })),
      evidence,
    };
  }

  function toJSON() {
    return JSON.stringify(capture());
  }

  return {
    attach,
    capture,
    record,
    recordAudio: (event) => record("audio_cue", event),
    recordFailure,
    recordHistory: (entry) => record("history_observed", entry),
    recordSnapshot,
    recordValidation: (result) => record("validation_result", result),
    toJSON,
    get eventCount() { return events.length; },
  };
}
