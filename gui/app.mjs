import { AUDIO_CATALOG, createAudioClient, visibleEventCues } from "./audio.mjs";
import { ASSET_CREDITS } from "./asset-credits.mjs";
import { renderAssetCredits } from "./asset-credits-renderer.mjs";
import { consequenceLinkContext, consequenceLinkDelta, consequenceLinksForTarget, regionalWorldConsequenceLinks, resolutionConsequenceLinks, resolutionResponseLinks } from "./consequence-links.mjs";
import { facilityComponentFor } from "./facility-components.mjs";
import { CAMPAIGN_COVERAGE_FLOW_SCHEMA, FIRST_MONTH_FLOW_SCHEMA, createFirstMonthFlow } from "./first-month.mjs";
import { PLAYTEST_CAPTURE_SCHEMA, createPlaytestRecorder } from "./playtest.mjs";
import { presentationFixtureToSceneData, regionalWorldToSceneData } from "./regional-board.mjs";
import { renderRegionalSvg } from "./scene.mjs";
import { renderMetricVisualizationSvg } from "./metric-visualizations.mjs";
import { VISUAL_CATALOG, visualIdentityFor, visualMarkerFor, visualStatusFor } from "./visual.mjs";
import { planResolutionSequence, sequenceForSkip } from "./resolution-sequence.mjs";
import { DEFAULT_VISIBLE_COUNTS, WORKSPACE_IDS, createWorkspaceController, workspaceForEvent } from "./workspace.mjs";

const presentationFixture = {
  header_metrics: [
    { label: "Month", value: "Year 1 · January" },
    { label: "Cash", value: "60 units", visualization: { visualization_kind: "capacity-bar", value: 60, max: 100, exact_text: "Cash: 60 units", source: "PlayerObservation.cash" } },
    { label: "Monthly margin", value: "+12 units", visualization: { visualization_kind: "sparkline", exact_text: "Monthly margin: +9, +12, +12 units", source: "PlayerObservation.monthly_margin", values: [{ period: "Nov", value: 9, display: "+9 units" }, { period: "Dec", value: 12, display: "+12 units" }, { period: "Jan", value: 12, display: "+12 units" }] } },
    { label: "Action points", value: "3 AP" },
    { label: "Political capital", value: "10" },
    { label: "Workforce trust", value: "Moderate", visualization: { visualization_kind: "trust-trend", exact_text: "Workforce trust: moderate, moderate, moderate", source: "PlayerObservation.workforce_trust_summary", values: [{ period: "Nov", value: 1, display: "Moderate" }, { period: "Dec", value: 1, display: "Moderate" }, { period: "Jan", value: 1, display: "Moderate" }] } },
    { label: "Session", value: "Injected fixture" },
  ],
  briefing: [
    {
      kind: "Workforce",
      title: "Nursing vacancy is the immediate bottleneck",
      detail: "Vacancy pressure is visible before a staffing action; added capacity remains delayed.",
      status: "watch",
      source: "PlayerObservation.workforce_trust_summary",
      target_id: "riverside",
    },
    {
      kind: "Rival intelligence",
      title: "Summit Care expanded outpatient capacity",
      detail: "This is a public rival signal. Private rival activity remains unavailable.",
      status: "uncertain",
      source: "PlayerObservation.market_bullets",
      target_id: "summit",
    },
    {
      kind: "Operations",
      title: "Demand exceeded staffed capacity last month",
      detail: "Review the direct volume, access, and margin contributors before acting.",
      status: "constrained",
      source: "PlayerObservation.monthly_unmet_demand",
      target_id: "riverside",
    },
  ],
  entities: [
    {
      id: "riverside",
      icon: "▣",
      type: "Player system",
      name: "Riverside Community Health",
      status: "watch",
      status_label: "Watch",
      summary: "Safety-net-leaning system with visible nursing and capacity pressure.",
      public_signal: "Player-visible operating and workforce context",
      metrics: [
        { label: "Access", value: "68" },
        { label: "Quality", value: "72" },
        { label: "Workforce", value: "Moderate trust" },
        { label: "Margin", value: "+12 units" },
      ],
      facilities: [
        { icon: "▥", name: "Riverside Medical Center", kind: "Inpatient", status: "constrained", detail: "118 staffed beds · 24 nurses · capacity is visible" },
        { icon: "◇", name: "Riverside Clinics", kind: "Outpatient", status: "stable", detail: "100 outpatient capacity · treated volume is visible" },
      ],
    },
    {
      id: "northlake",
      icon: "◇",
      type: "Public rival",
      name: "Northlake Health",
      status: "stable",
      status_label: "Stable",
      summary: "Publicly visible market participant; private actions are not shown.",
      public_signal: "Public signal: held capacity last month",
      metrics: [
        { label: "Public signal", value: "Held capacity" },
        { label: "Observation", value: "Reported" },
        { label: "Private actions", value: "Unavailable" },
        { label: "Source", value: "Market briefing" },
      ],
      facilities: [
        { icon: "▥", name: "Northlake facilities", kind: "Public summary", status: "stable", detail: "No private facility detail is displayed" },
      ],
    },
    {
      id: "summit",
      icon: "◈",
      type: "Public rival",
      name: "Summit Care",
      status: "improving",
      status_label: "Improving",
      summary: "Public rival signal shows expanded outpatient capacity.",
      public_signal: "Public signal: outpatient expansion reported",
      metrics: [
        { label: "Public signal", value: "Expansion" },
        { label: "Observation", value: "Reported" },
        { label: "Private actions", value: "Unavailable" },
        { label: "Source", value: "Market briefing" },
      ],
      facilities: [
        { icon: "▥", name: "Summit facilities", kind: "Public summary", status: "improving", detail: "Only the reported public signal is available" },
      ],
    },
  ],
  selected_entity_id: "riverside",
  actions: [
    {
      label: "Recruit nurses",
      command: "recruit role=nurse headcount=<n>",
      cost: "1 AP · cash per head",
      delay: "1 month",
      uncertainty: "Candidate response and capacity effect remain uncertain",
      constraint: "Host validates headcount and resources",
      source: "CompetitiveCommand::Recruit",
    },
    {
      label: "Invest in beds",
      command: "invest domain=beds amount=<n>",
      cost: "1 AP · cash amount",
      delay: "Immediate spend; capacity effect is modeled",
      uncertainty: "Operating result is not promised by the preview",
      constraint: "Host validates amount and available cash",
      source: "CompetitiveCommand::Invest",
    },
    {
      label: "Monitor a rival",
      command: "monitor target=northlake depth=1",
      cost: "1 AP · no cash",
      delay: "Information may arrive later",
      uncertainty: "Private activity can remain unobserved",
      constraint: "Target and depth are host-validated",
      source: "CompetitiveCommand::Monitor",
    },
  ],
  pending: [
    {
      title: "Nursing recruitment",
      status: "delayed",
      status_label: "Delayed",
      timing: "Role-specific resolution delay",
      detail: "Visible commitment; future staffing and operating outcome are not guaranteed.",
      source: "PlayerObservation.in_flight_projects",
    },
    {
      title: "Annual policy review",
      status: "uncertain",
      status_label: "Uncertain",
      timing: "Next visible policy calendar milestone",
      detail: "The client shows timing and source, not a hidden result.",
      source: "PlayerObservation.annual_policy_review",
    },
  ],
  monthly_result: {
    status: "watch",
    status_label: "Watch",
    headline: "Prior month operated below reported demand",
    metrics: [
      "Treated volume: 96 / 110 demand units",
      "Unmet demand: 14 units",
      "Revenue: 84 units · cost: 72 units · margin: +12 units",
    ],
    effects: [
      "Direct visible driver: staffed capacity and nursing availability",
      "Observation boundary: rival private activity remains unavailable",
    ],
    source: "TransitionSummary.effects → next PlayerObservation",
  },
};

const demoEnvelope = {
  campaign: "competitive-regional-v1",
  turn: 1,
  max_turns: 24,
  done: false,
  observation: [
    "Year 1, Month 1 (January)",
    "Organization: Riverside Community Health",
    "Workforce trust: moderate; vacancy rate elevated in nursing",
    "Staffing: nurses 24, physicians 10, admins 11",
    "Physical capacity: staffed beds 118, outpatient 100, emergency 0, ICU 0, obstetrics 0, psychiatric 0, cardiology 0, oncology 0, infusion 0, neurology 0, ASC 0",
    "Cash runway: COMFORTABLE",
  ],
  legal_commands: [
    "Available resources: AP 3, cash 60, political capital 10",
    "invest domain=beds amount=<n>",
    "recruit role=nurse headcount=<n>",
    "hold",
  ],
  history: [
    { turn: 0, command: "genesis", state_hash: "genesis" },
  ],
  debrief: [
    "The debrief will retain the committed decisions and actor responses.",
    "Decision quality and outcome quality remain separate.",
  ],
  presentation_fixture: presentationFixture,
};

const READ_ONLY_PRESENTATION_SCHEMA = "competitive-read-only-v1";
const END_SESSION_SCHEMA = "competitive-end-session-v1";
const HISTORY_SCHEMA = "competitive-history-v1";
const HISTORY_CAMPAIGN = "competitive-regional-v1";
const REPLAY_SCHEMA = "competitive-replay-v1";
const SAVE_SCHEMA = "competitive-save-v1";
const CHECKPOINT_DISCOVERY_SCHEMA = "gui-checkpoint-discovery-v1";
export const CHECKPOINT_REFERENCE_SCHEMA = "gui-checkpoint-reference-v1";
const REGIONAL_WORLD_SCHEMA = "competitive-regional-world-v1";
const CAMPAIGN_COVERAGE_SCHEMA = "campaign-coverage-v1";
export const ACTIVE_SESSION_STORAGE_KEY = "hs-mgt-active-session-id";
export const SESSION_RESUME_POLICY = Object.freeze({
  schema_version: "gui-session-resume-policy-v1",
  automatic_source: "browser-refresh-opaque-session-id",
  max_host_restore_attempts: 1,
  stored_value: "opaque-session-id-only",
  manual_load_auto_restore: false,
  transient_failure_preserves_id: true,
  unknown_session_clears_id: true,
});
let selectedEntityId = null;
let selectedBoardId = null;
let currentMapEntities = [];
let currentBoardScene = null;
let currentBriefingItems = [];
let briefingFocusEntityId = null;
let currentRegionalLinks = [];
let currentResolutionLinks = [];
let currentResolutionSessionId = null;
let visualHelpCounter = 0;

function workspaceController(root) {
  return root?.__hsMgtWorkspace ?? null;
}

function workspaceEvent(root, event, options = {}) {
  return workspaceController(root)?.goForEvent?.(event, options) ?? null;
}

function openContextDrawer(root) {
  const drawer = root?.querySelector?.("#context-drawer");
  if (!drawer) return false;
  const controller = workspaceController(root);
  if (controller?.openDialog) {
    controller.openDialog(drawer);
    return true;
  }
  if (typeof drawer.showModal === "function") drawer.showModal();
  else drawer.open = true;
  drawer.hidden = false;
  return true;
}

function bindWorkspaceFlow(firstMonthFlow, root) {
  const controller = workspaceController(root);
  if (!controller || !firstMonthFlow || firstMonthFlow.__hsMgtWorkspaceBound) return;
  firstMonthFlow.__hsMgtWorkspaceBound = true;
  controller.subscribe(({ workspace, reason }) => {
    if (workspace === "decide" && reason === "briefing-reviewed") {
      firstMonthFlow.update({ briefingReviewed: true });
    }
    if (workspace === "brief" && reason === "resolution-continue") {
      firstMonthFlow.update({
        briefingReviewed: false,
        resolutionReviewed: true,
        submitted: false,
        decisionSubmitted: false,
        resolutionVisible: false,
        refreshed: false,
      });
    }
  });
}

export function createSessionIdStorage({ storage } = {}) {
  function target() {
    try {
      return storage ?? globalThis.localStorage;
    } catch {
      return null;
    }
  }

  return {
    get() {
      try {
        const value = target()?.getItem?.(ACTIVE_SESSION_STORAGE_KEY);
        const sessionId = String(value ?? "").trim();
        return sessionId || null;
      } catch {
        return null;
      }
    },
    set(sessionId) {
      const value = String(sessionId ?? "").trim();
      if (!value) return false;
      try {
        const store = target();
        if (!store?.setItem) return false;
        store.setItem(ACTIVE_SESSION_STORAGE_KEY, value);
        return true;
      } catch {
        return false;
      }
    },
    clear() {
      try {
        const store = target();
        if (!store?.removeItem) return false;
        store.removeItem(ACTIVE_SESSION_STORAGE_KEY);
        return true;
      } catch {
        return false;
      }
    },
  };
}

function isUnknownSessionResult(result) {
  const detail = `${result?.code ?? ""} ${result?.message ?? result?.error ?? ""}`.toLowerCase();
  return detail.includes("unknown session") || detail.includes("session_not_found");
}

function boardEntityFor(id) {
  return currentBoardScene?.entities?.find((entity) => entity.id === id || entity.source_id === id);
}

function boardIdFor(id) {
  return boardEntityFor(id)?.id ?? id;
}

function appendText(parent, text) {
  const node = document.createElement("p");
  node.textContent = String(text);
  parent.append(node);
}

function emptyState(parent, message) {
  const node = document.createElement("li");
  node.className = "empty";
  node.textContent = message;
  parent.append(node);
}

function setStatus(root, message) {
  const node = root.querySelector("#session-status");
  if (node) node.textContent = message;
}

function setPresentationState(root, message) {
  setStatus(root, message);
  const node = root.querySelector("#presentation-state");
  if (node) node.textContent = message;
}

function bindSkipNavigation(root) {
  const link = root.querySelector("#skip-to-content");
  const target = root.querySelector("#briefing-region");
  if (!link || !target || link.__hsMgtSkipNavigationBound) return;
  link.__hsMgtSkipNavigationBound = true;
  link.addEventListener("click", () => {
    const result = workspaceController(root)?.setWorkspace?.("brief", { focus: false });
    if (result?.ok) target.focus?.({ preventScroll: true });
  });
}

function configureRecovery(root, retry, recorder) {
  const button = root.querySelector("#recovery-retry");
  if (!button) return;
  button.onclick = async (event) => {
    event.__hsMgtPlaytestRecorded = true;
    recorder?.record("recovery_retry", { target: "current-read" });
    await retry?.();
  };
}

function showRecovery(root, message) {
  const panel = root.querySelector("#recovery-panel");
  const detail = root.querySelector("#recovery-detail");
  if (detail) detail.textContent = String(message);
  if (panel) panel.hidden = false;
}

function clearRecovery(root) {
  const panel = root.querySelector("#recovery-panel");
  if (panel) panel.hidden = true;
}

function renderOnboarding(envelope, root, recorder) {
  // Evidence marker retained for the terminal-debrief boundary: const targetSelectors = session.done.
  // Workspace routing now owns the handoff so inactive controls stay hidden.
  const panel = root.querySelector("#onboarding-panel");
  const campaign = root.querySelector("#onboarding-campaign");
  const next = root.querySelector("#onboarding-next");
  if (!panel || !campaign || !next) return;
  const session = envelope?.session ?? envelope ?? {};
  const campaignId = session.campaign ?? "the current campaign";
  campaign.textContent = `${campaignId} · start with the visible briefing and choose an action.`;
  next.textContent = session.done ? "Review the debrief" : "Review the current briefing";
  next.onclick = (event) => {
    event.__hsMgtPlaytestRecorded = true;
    recorder?.record("onboarding_next", { target: session.done ? "campaign-debrief-list" : "briefing-list" });
    workspaceEvent(root, session.done ? "session_ended" : "session_loaded");
  };
  panel.hidden = false;
  recorder?.record("onboarding_opened", { campaign: campaignId, next_action: next.textContent });
  recorder?.recordSnapshot(root);
}

function recordVisibleEnvelope(recorder, envelope) {
  if (!recorder || !envelope) return;
  const session = envelope.session ?? {};
  recorder.record("session_loaded", {
    campaign: session.campaign ?? envelope.campaign,
    turn: session.turn ?? envelope.turn,
    done: session.done ?? envelope.done,
    schema: envelope.schema_version,
  });
  const history = Array.isArray(envelope.history) ? envelope.history : [];
  const replay = envelope.replay ?? {};
  const latest = history[history.length - 1];
  if (latest || replay.state_hash || replay.latest_state_hash) {
    recorder.recordHistory({
      turn: latest?.turn ?? session.turn ?? envelope.turn,
      state_hash: latest?.state_hash ?? replay.state_hash ?? replay.latest_state_hash,
      transition_count: replay.transition_count ?? history.length,
    });
  }
}

function recordPlaytestFailure(recorder, code, message, recoverable = true) {
  if (!recorder) return;
  const failureClass = code?.includes("unsupported") ? "unsupported_schema"
    : code?.includes("submit") ? "submit_rejected"
      : code?.includes("adapter") ? "adapter_error"
        : code?.includes("schema") ? "unsupported_schema" : "capture_invalid";
  recorder.recordFailure({ class: failureClass, message, recoverable });
}

export function createPresentationSettings({ root = document, recorder, storage, audio } = {}) {
  if (root.__hsMgtPresentationSettings) return root.__hsMgtPresentationSettings;
  bindSkipNavigation(root);
  let persisted = {};
  try {
    persisted = JSON.parse((storage ?? globalThis.localStorage)?.getItem?.("hs-mgt-presentation-settings") ?? "{}");
  } catch {
    persisted = {};
  }
  const persistedLowAudioState = persisted.low_distraction_audio_snapshot;
  const hasPersistedLowAudioState = persistedLowAudioState
    && typeof persistedLowAudioState.muted === "boolean"
    && typeof persistedLowAudioState.reducedNotifications === "boolean";
  const state = {
    low_distraction: Boolean(persisted.low_distraction && hasPersistedLowAudioState),
    reduced_motion: persisted.reduced_motion ?? Boolean(globalThis.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches),
    text_equivalents: persisted.text_equivalents ?? true,
    text_scale: persisted.text_scale === "large" ? "large" : "standard",
  };
  let lowDistractionAudioState = state.low_distraction ? { ...persistedLowAudioState } : null;
  const save = () => {
    try {
      const persistedState = {
        ...state,
        low_distraction_audio_snapshot: state.low_distraction && lowDistractionAudioState
          ? {
            muted: lowDistractionAudioState.muted,
            reducedNotifications: lowDistractionAudioState.reducedNotifications,
          }
          : null,
      };
      (storage ?? globalThis.localStorage)?.setItem?.("hs-mgt-presentation-settings", JSON.stringify(persistedState));
    } catch {
      // Settings remain session-local when storage is unavailable.
    }
  };
  const applyLowDistractionAudio = () => {
    if (!audio) return;
    if (state.low_distraction && !lowDistractionAudioState) {
      lowDistractionAudioState = typeof audio.state === "function" ? audio.state() : {};
      audio.setMuted?.(true);
      audio.setReducedNotifications?.(true);
    } else if (!state.low_distraction && lowDistractionAudioState) {
      if (typeof lowDistractionAudioState.muted === "boolean") audio.setMuted?.(lowDistractionAudioState.muted);
      if (typeof lowDistractionAudioState.reducedNotifications === "boolean") {
        audio.setReducedNotifications?.(lowDistractionAudioState.reducedNotifications);
      }
      lowDistractionAudioState = null;
    }
  };
  const apply = () => {
    applyLowDistractionAudio();
    const effectiveReducedMotion = state.reduced_motion || state.low_distraction;
    const effectiveTextEquivalents = state.text_equivalents || state.low_distraction;
    const effectiveTextScale = state.low_distraction ? "large" : state.text_scale;
    root.documentElement?.dataset && (root.documentElement.dataset.lowDistraction = String(state.low_distraction));
    root.documentElement?.dataset && (root.documentElement.dataset.reducedMotion = String(effectiveReducedMotion));
    root.documentElement?.dataset && (root.documentElement.dataset.textEquivalents = String(effectiveTextEquivalents));
    root.documentElement?.dataset && (root.documentElement.dataset.textScale = effectiveTextScale);
    const low = root.querySelector("#settings-low-distraction");
    const motion = root.querySelector("#settings-reduced-motion");
    const text = root.querySelector("#settings-text-equivalents");
    const scale = root.querySelector("#settings-text-scale");
    if (low) low.checked = state.low_distraction;
    if (motion) {
      motion.checked = effectiveReducedMotion;
      motion.disabled = state.low_distraction;
    }
    if (text) {
      text.checked = effectiveTextEquivalents;
      text.disabled = state.low_distraction;
    }
    if (scale) {
      scale.value = effectiveTextScale;
      scale.disabled = state.low_distraction;
    }
    for (const control of root.querySelectorAll?.("#audio-panel button, #audio-panel input, #audio-panel select") ?? []) {
      control.disabled = state.low_distraction;
    }
    const status = root.querySelector("#settings-state");
    if (status) {
      const modeLabel = state.low_distraction ? "Low-distraction mode is active." : "Low-distraction mode is off.";
      const motionLabel = effectiveReducedMotion ? "Reduced motion is active." : "Standard motion is active.";
      const cueLabel = effectiveTextEquivalents ? "Optional cue explanations are visible." : "Optional cue explanations are hidden.";
      const scaleLabel = effectiveTextScale === "large" ? "Large text is active." : "Standard text is active.";
      status.textContent = `${modeLabel} ${motionLabel} ${scaleLabel} ${cueLabel} Written results remain complete.`;
    }
  };
  root.querySelector("#settings-low-distraction")?.addEventListener("change", (event) => {
    event.__hsMgtPlaytestRecorded = true;
    state.low_distraction = Boolean(event.target.checked);
    recorder?.record("settings_changed", { setting: "low_distraction", value: state.low_distraction });
    apply();
    save();
  });
  root.querySelector("#settings-reduced-motion")?.addEventListener("change", (event) => {
    event.__hsMgtPlaytestRecorded = true;
    state.reduced_motion = Boolean(event.target.checked);
    recorder?.record("settings_changed", { setting: "reduced_motion", value: state.reduced_motion });
    save();
    apply();
  });
  root.querySelector("#settings-text-equivalents")?.addEventListener("change", (event) => {
    event.__hsMgtPlaytestRecorded = true;
    state.text_equivalents = Boolean(event.target.checked);
    recorder?.record("settings_changed", { setting: "text_equivalents", value: state.text_equivalents });
    save();
    apply();
  });
  root.querySelector("#settings-text-scale")?.addEventListener("change", (event) => {
    event.__hsMgtPlaytestRecorded = true;
    state.text_scale = event.target.value === "large" ? "large" : "standard";
    recorder?.record("settings_changed", { setting: "text_scale", value: state.text_scale });
    save();
    apply();
  });
  apply();
  const client = { apply, get state() { return { ...state }; } };
  root.__hsMgtPresentationSettings = client;
  return client;
}

function setReadOnlyControls(root, readOnly) {
  const form = root.querySelector("#command-form");
  if (form) form.hidden = readOnly;
  const technical = root.querySelector("#technical-controls");
  if (technical) {
    technical.hidden = readOnly;
    if (readOnly) technical.open = false;
  }
  const commands = root.querySelector("#legal-command-list");
  if (readOnly && commands) {
    commands.replaceChildren();
    emptyState(commands, "Submission is unavailable in this view.");
  }
}

function setEndSessionControl(root, enabled) {
  const button = root.querySelector("#session-end");
  if (button) button.disabled = !enabled;
}

function setCheckpointControls(root, enabled, busy = false) {
  for (const selector of ["#session-save", "#session-restore"]) {
    const button = root.querySelector(selector);
    if (button) button.disabled = !enabled || busy;
  }
}

function createStatus(status, label) {
  const node = document.createElement("span");
  const normalizedStatus = String(status ?? "uncertain").toLowerCase();
  const text = String(label ?? status ?? "Uncertain");
  node.className = `status status--${normalizedStatus}`;
  node.dataset.status = normalizedStatus;
  node.dataset.symbol = visualStatusFor(normalizedStatus)?.symbol ?? "?";
  node.setAttribute("aria-label", text);
  node.textContent = text;
  return node;
}

function createVisualToken(entry, role = "marker", root = document) {
  const documentRef = root?.ownerDocument
    ?? (typeof root?.createElement === "function" ? root : globalThis.document);
  const node = documentRef.createElement("span");
  node.className = `visual-token visual-token--${role} ${entry.token_class}`;
  node.dataset.visualId = entry.id;
  node.setAttribute("aria-label", `${entry.label}: ${entry.equivalent}`);
  node.tabIndex = 0;
  const helpId = `visual-help-${visualHelpCounter += 1}`;
  node.setAttribute("aria-describedby", helpId);
  node.dataset.tooltipOpen = "false";
  const symbol = documentRef.createElement("span");
  symbol.className = "visual-token-symbol";
  symbol.setAttribute("aria-hidden", "true");
  symbol.textContent = entry.symbol;
  const label = documentRef.createElement("span");
  label.className = "visual-token-label";
  label.textContent = entry.label;
  const help = documentRef.createElement("span");
  help.className = "visual-token-help";
  help.id = helpId;
  help.setAttribute("role", "tooltip");
  help.textContent = String(entry.equivalent ?? `${entry.label} symbol`);
  node.addEventListener?.("click", () => {
    const drawerRoot = root?.querySelector ? root : documentRef;
    const drawer = drawerRoot?.querySelector?.("#context-drawer");
    const detail = drawerRoot?.querySelector?.("#entity-detail");
    const heading = drawerRoot?.querySelector?.("#entity-heading");
    if (!drawer || !detail || !heading) {
      node.dataset.tooltipOpen = node.dataset.tooltipOpen === "true" ? "false" : "true";
      return;
    }
    heading.textContent = `${entry.label} explanation`;
    detail.replaceChildren();
    const explanation = documentRef.createElement("p");
    explanation.textContent = String(entry.equivalent ?? `${entry.label} symbol`);
    detail.append(explanation);
    appendSource(detail, entry.source ?? "Visual catalog");
    openContextDrawer(drawerRoot);
  });
  node.addEventListener?.("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault?.();
      node.dataset.tooltipOpen = node.dataset.tooltipOpen === "true" ? "false" : "true";
    }
  });
  node.append(symbol, label, help);
  return node;
}

function prependOrInsertBefore(parent, node) {
  if (typeof parent.prepend === "function") parent.prepend(node);
  else parent.insertBefore(node, parent.firstChild);
}

function appendSource(parent, source) {
  if (!source) return;
  const node = document.createElement("small");
  node.className = "source";
  node.textContent = `Source: ${source}`;
  parent.append(node);
}

function renderBoundedCollection({ list, overflow, details, items, limit, label, renderItem, emptyMessage }) {
  if (!list) return;
  const entries = Array.isArray(items) ? items : [];
  if (list.dataset) list.dataset.collectionTotal = String(entries.length);
  list.setAttribute?.("aria-label", `${label}; ${entries.length} total`);
  list.replaceChildren();
  for (const [index, entry] of entries.slice(0, limit).entries()) list.append(renderItem(entry, index));
  if (!entries.length) emptyState(list, emptyMessage);
  if (!overflow || !details) return;
  overflow.replaceChildren();
  for (const [index, entry] of entries.slice(limit).entries()) overflow.append(renderItem(entry, index + limit));
  const remaining = Math.max(entries.length - limit, 0);
  details.hidden = remaining === 0;
  if (remaining > 0) {
    const summary = details.querySelector?.("summary");
    if (summary) summary.textContent = `Show remaining ${remaining} ${label} (${entries.length} total)`;
  } else {
    details.open = false;
  }
}

function renderMetricList(metrics, root) {
  const list = root.querySelector("#header-metrics");
  const renderMetric = (metric) => {
    const item = document.createElement("div");
    item.className = "metric";
    const label = document.createElement("dt");
    label.textContent = String(metric.label ?? "Metric");
    const value = document.createElement("dd");
    value.textContent = String(metric.value ?? "Unavailable");
    item.append(label, value);
    if (metric.visualization?.visualization_kind) {
      const visual = document.createElement("div");
      visual.className = "metric-visual-container";
      visual.innerHTML = renderMetricVisualizationSvg(metric.visualization, metric.visualization.visualization_kind);
      item.append(visual);
    }
    appendSource(item, metric.source);
    return item;
  };
  renderBoundedCollection({
    list,
    overflow: root.querySelector("#header-metrics-overflow"),
    details: root.querySelector("#header-metrics-more"),
    items: metrics,
    limit: 6,
    label: "additional metrics",
    renderItem: renderMetric,
    emptyMessage: "No executive metrics available.",
  });
}

function renderBriefing(items, root) {
  currentBriefingItems = items ?? [];
  const list = root.querySelector("#briefing-list");
  const visibleItems = briefingFocusEntityId
    ? currentBriefingItems.filter((entry) => !entry.target_id || entry.target_id === briefingFocusEntityId)
    : currentBriefingItems;
  const renderBriefingItem = (entry) => {
    const item = document.createElement("li");
    item.className = "briefing-item";
    const heading = document.createElement("div");
    heading.className = "action-heading";
    const title = document.createElement("strong");
    title.textContent = String(entry.kind ?? "Briefing");
    heading.append(title, createStatus(entry.status, entry.status_label));
    const detail = document.createElement("p");
    detail.textContent = String(entry.title ?? "Untitled briefing");
    const explanation = document.createElement("p");
    explanation.textContent = String(entry.detail ?? "No further visible detail.");
    item.append(heading, detail, explanation);
    if (entry.target_id) {
      const focus = document.createElement("button");
      focus.type = "button";
      focus.className = "briefing-focus";
      focus.textContent = "View on regional board";
      focus.addEventListener("click", () => {
        selectedEntityId = String(entry.target_id);
        selectedBoardId = boardIdFor(selectedEntityId);
        briefingFocusEntityId = selectedEntityId;
        renderMap(currentMapEntities, root);
        renderSelectedEntity(currentMapEntities, root);
        renderBriefing(currentBriefingItems, root);
        renderRegionalBoard(currentBoardScene, root);
        openContextDrawer(root);
      });
      item.append(focus);
    }
    appendSource(item, entry.source);
    return item;
  };
  renderBoundedCollection({
    list,
    overflow: root.querySelector("#briefing-overflow-list"),
    details: root.querySelector("#briefing-more"),
    items: visibleItems,
    limit: DEFAULT_VISIBLE_COUNTS.signals,
    label: "additional signals",
    renderItem: renderBriefingItem,
    emptyMessage: "No briefing items are linked to the selected institution.",
  });
}

function renderMap(entities, root) {
  currentMapEntities = entities ?? [];
  const list = root.querySelector("#map-list");
  list.replaceChildren();
  for (const entity of entities ?? []) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "entity-card";
    card.dataset.entityId = entity.id;
    card.setAttribute("aria-current", entity.id === selectedEntityId ? "true" : "false");
    const icon = createVisualToken(visualIdentityFor(entity), "identity", root);
    icon.classList.add("entity-icon");
    const type = document.createElement("small");
    type.className = "source";
    type.textContent = String(entity.type ?? "Institution");
    const name = document.createElement("strong");
    name.textContent = String(entity.name ?? "Unnamed institution");
    const summary = document.createElement("p");
    summary.textContent = String(entity.public_signal ?? entity.summary ?? "No public signal available.");
    card.append(icon, type, name, summary, createStatus(entity.status, entity.status_label));
    card.addEventListener("click", () => {
      selectedEntityId = entity.id;
      selectedBoardId = boardIdFor(entity.id);
      briefingFocusEntityId = entity.id;
      renderMap(entities, root);
      renderSelectedEntity(entities, root);
      renderBriefing(currentBriefingItems, root);
      renderRegionalBoard(currentBoardScene, root);
      openContextDrawer(root);
    });
    list.append(card);
  }
  if (!entities?.length) emptyState(list, "No regional institutions available.");
}

function renderRegionalBoard(scene, root) {
  const mount = root.querySelector("#regional-board");
  if (!mount) return;
  currentBoardScene = scene;
  mount.replaceChildren();
  if (!scene) return;
  mount.innerHTML = renderRegionalSvg(scene, { selectedId: boardIdFor(selectedBoardId ?? selectedEntityId) });
  if (mount.dataset.bound === "true") return;
  mount.dataset.bound = "true";
  const selectTarget = (event) => {
    const target = event.target.closest?.("[data-entity-id], [data-facility-id]");
    if (!target) return;
    event.preventDefault();
    const boardOwnerId = target.dataset.entityId
      ?? target.parentElement?.closest?.("[data-entity-container-id]")?.dataset.entityContainerId;
    const boardEntity = boardEntityFor(boardOwnerId);
    selectedEntityId = boardEntity?.source_id ?? boardOwnerId;
    selectedBoardId = target.dataset.facilityId ?? boardEntity?.id ?? boardOwnerId;
    briefingFocusEntityId = selectedEntityId;
    if (!currentMapEntities.some((entity) => entity.id === selectedEntityId)) return;
    renderMap(currentMapEntities, root);
    renderSelectedEntity(currentMapEntities, root);
    renderBriefing(currentBriefingItems, root);
    renderRegionalBoard(currentBoardScene, root);
    openContextDrawer(root);
  };
  mount.addEventListener("click", selectTarget);
  mount.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") selectTarget(event);
  });
}

function renderConsequenceLinks(links, root) {
  const list = root.querySelector("#consequence-link-list");
  if (!list) return;
  list.replaceChildren();
  for (const link of links ?? []) {
    const item = document.createElement("li");
    item.className = "consequence-link";
    const heading = document.createElement("div");
    heading.className = "timeline-row";
    const title = document.createElement("strong");
    title.textContent = String(link.label ?? "Visible consequence");
    heading.append(title);
    if (link.kind === "visible-response") {
      const reported = visualStatusFor("reported");
      if (reported) prependOrInsertBefore(heading, createVisualToken(reported, "status", root));
    }
    if (link.target_id && currentMapEntities.some((entity) => entity.id === link.target_id)) {
      const focus = document.createElement("button");
      focus.type = "button";
      focus.textContent = "Focus board";
      focus.addEventListener("click", () => {
        selectedEntityId = link.target_id;
        selectedBoardId = boardIdFor(link.target_id);
        briefingFocusEntityId = link.target_id;
        renderMap(currentMapEntities, root);
        renderSelectedEntity(currentMapEntities, root);
        renderBriefing(currentBriefingItems, root);
        renderRegionalBoard(currentBoardScene, root);
        openContextDrawer(root);
      });
      heading.append(focus);
    }
    const detail = document.createElement("p");
    detail.textContent = String(link.detail ?? "No visible consequence detail available.");
    const deltaText = consequenceLinkDelta(link);
    const delta = document.createElement("small");
    delta.className = "consequence-delta";
    delta.textContent = deltaText;
    const context = document.createElement("small");
    context.className = "consequence-context";
    context.textContent = consequenceLinkContext(link);
    item.append(heading, detail);
    if (deltaText) item.append(delta);
    item.append(context);
    appendSource(item, link.source);
    list.append(item);
  }
  if (!links?.length) emptyState(list, "No linked visible consequences are available.");
}

function renderSelectedEntity(entities, root) {
  const detail = root.querySelector("#entity-detail");
  detail.replaceChildren();
  const entity = (entities ?? []).find((candidate) => candidate.id === selectedEntityId);
  if (!entity) {
    emptyState(detail, "Select an actor-visible system or facility.");
    return;
  }
  const heading = document.createElement("div");
  heading.className = "entity-heading";
  const icon = createVisualToken(visualIdentityFor(entity), "identity", root);
  icon.classList.add("entity-icon");
  const title = document.createElement("h3");
  title.textContent = String(entity.name);
  heading.append(icon, title, createStatus(entity.status, entity.status_label));
  const summary = document.createElement("p");
  summary.className = "detail-summary";
  summary.textContent = String(entity.summary ?? "No visible summary available.");
  const related = [
    ...consequenceLinksForTarget(currentRegionalLinks, entity.id),
    ...consequenceLinksForTarget(currentResolutionLinks, entity.id),
  ];
  if (related.length || currentBriefingItems.some((entry) => entry.target_id === entity.id)) {
    const reports = document.createElement("button");
    reports.type = "button";
    reports.textContent = "Show related reports and consequences";
    reports.addEventListener("click", () => {
      briefingFocusEntityId = entity.id;
      renderBriefing(currentBriefingItems, root);
      renderConsequenceLinks([...currentRegionalLinks, ...currentResolutionLinks], root);
      root.querySelector("#briefing-list")?.scrollIntoView?.({ behavior: "auto", block: "start" });
    });
    summary.append(document.createTextNode(" "), reports);
  }
  const metrics = document.createElement("dl");
  metrics.className = "detail-metrics";
  for (const metric of entity.metrics ?? []) {
    const item = document.createElement("div");
    const label = document.createElement("dt");
    label.textContent = String(metric.label ?? "Metric");
    const value = document.createElement("dd");
    value.textContent = String(metric.value ?? "Unavailable");
    item.append(label, value);
    metrics.append(item);
  }
  const facilitiesHeading = document.createElement("h3");
  facilitiesHeading.textContent = "Facility cards";
  const facilities = document.createElement("ul");
  facilities.className = "facility-list";
  for (const facility of entity.facilities ?? []) {
    const item = document.createElement("li");
    item.className = "facility-card";
    const row = document.createElement("div");
    row.className = "timeline-row";
    const name = document.createElement("strong");
    name.textContent = String(facility.name ?? "Facility");
    row.append(name, createStatus(facility.status, facility.status_label));
    const marker = createVisualToken(visualMarkerFor(facility.kind), "marker", root);
    const kind = document.createElement("small");
    kind.className = "source";
    kind.textContent = String(facility.kind ?? "Facility");
    const component = document.createElement("small");
    component.className = "source";
    component.textContent = `Visual component: ${String(facility.component_label ?? "Facility")}`;
    const componentDetail = document.createElement("p");
    componentDetail.textContent = String(facility.component_equivalent ?? "Facility component equivalent unavailable.");
    const detailText = document.createElement("p");
    detailText.textContent = String(facility.detail ?? "No visible facility detail.");
    item.append(row, marker, kind, component, componentDetail, detailText);
    appendSource(item, facility.component_source);
    appendSource(item, facility.source);
    facilities.append(item);
  }
  if (!entity.facilities?.length) emptyState(facilities, "No visible facility detail available.");
  detail.append(heading, summary, metrics, facilitiesHeading, facilities);
  if (entity.processes || entity.missing) {
    const processHeading = document.createElement("h3");
    processHeading.textContent = "Visible processes";
    const processes = document.createElement("ul");
    processes.className = "facility-list";
    for (const process of entity.processes ?? []) {
      const item = document.createElement("li");
      item.className = "facility-card";
      const marker = createVisualToken(visualMarkerFor(process.marker ?? process.label), "marker", root);
      const title = document.createElement("strong");
      title.textContent = String(process.label ?? "Visible process");
      const processDetail = document.createElement("p");
      processDetail.textContent = String(process.detail ?? "No visible process detail.");
      item.append(marker, title, processDetail);
      appendSource(item, process.source);
      processes.append(item);
    }
    if (!entity.processes?.length) emptyState(processes, "No visible process reported.");
    detail.append(processHeading, processes);
  }
  if (entity.missing?.length) {
    const missingHeading = document.createElement("h3");
    missingHeading.textContent = "Unavailable detail";
    const missing = document.createElement("ul");
    missing.className = "facility-list";
    for (const entry of entity.missing) {
      const item = document.createElement("li");
      item.className = "facility-card";
      const title = document.createElement("strong");
      title.textContent = String(entry.label ?? "Unavailable detail");
      const missingDetail = document.createElement("p");
      missingDetail.textContent = String(entry.detail ?? "Detail is unavailable.");
      item.append(title, missingDetail);
      appendSource(item, entry.source);
      missing.append(item);
    }
    detail.append(missingHeading, missing);
  }
}

function regionalEntitiesToFixture(envelope) {
  const missingByEntity = new Map();
  for (const missing of envelope.missing ?? []) {
    const entityId = String(missing.id ?? "").replace(/-(?:private-detail|public-signal|process)$/, "");
    if (!entityId) continue;
    const entries = missingByEntity.get(entityId) ?? [];
    entries.push(missing);
    missingByEntity.set(entityId, entries);
  }
  return (envelope.entities ?? []).map((entity) => ({
    id: entity.id,
    icon: entity.visibility === "owned" ? "▣" : "◇",
    type: entity.role,
    name: entity.name,
    status: entity.status,
    status_label: entity.status_label,
    summary: entity.visibility === "owned"
      ? `Owned detail · ${entity.source}`
      : "Public identity only; private rival detail remains unavailable.",
    public_signal: entity.signals?.length
      ? entity.signals.map((signal) => `${signal.text} (observed month ${signal.observed_month})`).join(" · ")
      : entity.visibility === "owned"
        ? "Player-owned facilities and processes are shown in selected detail."
        : "No public signal reported for the observed month.",
    metrics: [],
    facilities: (entity.facilities ?? []).map((facility) => {
      const component = facilityComponentFor(facility.component_id);
      return {
        icon: "▥",
        name: facility.name,
        kind: facility.kind,
        status: entity.status,
        status_label: entity.status_label,
        detail: (facility.metrics ?? []).map((metric) => `${metric.label}: ${metric.value}`).join(" · ") || "No visible facility metric.",
        source: facility.source,
        component_id: component.id,
        component_label: component.label,
        component_source: component.source,
        component_equivalent: component.equivalent,
        component_release_path: component.release_path ?? null,
      };
    }),
    processes: (entity.processes ?? []).map((process) => ({
      label: process.label,
      detail: process.detail,
      source: process.source,
    })),
    missing: missingByEntity.get(entity.id) ?? [],
  }));
}

export function renderRegionalOverlays(overlays, root) {
  const list = root.querySelector("#regional-overlay-list");
  if (!list) return;
  list.replaceChildren();
  for (const overlay of overlays ?? []) {
    const item = document.createElement("li");
    item.dataset.overlayId = String(overlay.id ?? "");
    item.dataset.operationalOverlayId = String(overlay.operational_overlay_id ?? "");
    const catalogSemantics = overlay.operational_overlay_id
      ? `; Catalog source: ${overlay.operational_source ?? "Unavailable"}; Non-color pattern: ${overlay.operational_pattern ?? "Unavailable"}`
      : "";
    item.setAttribute(
      "aria-label",
      `${overlay.label ?? "Visible overlay"}; ${overlay.value ?? "Unavailable"}; ${overlay.equivalent ?? "Visible source-linked overlay."}${catalogSemantics}`,
    );
    const marker = createVisualToken(visualMarkerFor(overlay.marker ?? overlay.kind ?? overlay.label), "marker", root);
    const headingRow = document.createElement("div");
    headingRow.className = "timeline-row";
    const heading = document.createElement("strong");
    heading.textContent = String(overlay.label ?? "Visible overlay");
    const value = document.createElement("span");
    value.textContent = `${overlay.value ?? "Unavailable"} ${overlay.unit ?? ""}`.trim();
    const equivalent = document.createElement("p");
    equivalent.textContent = String(overlay.equivalent ?? "Visible source-linked overlay.");
    headingRow.append(marker, heading);
    item.append(headingRow, value, equivalent);
    if (overlay.operational_overlay_id) {
      const semantics = document.createElement("p");
      semantics.className = "source";
      semantics.textContent = catalogSemantics.slice(2);
      item.append(semantics);
    }
    appendSource(item, overlay.source);
    list.append(item);
  }
  if (!overlays?.length) emptyState(list, "No visible regional overlays available.");
}

function renderRegionalNavigation(navigation, root) {
  const nav = root.querySelector("#regional-navigation");
  if (!nav) return;
  nav.replaceChildren();
  for (const entry of navigation ?? []) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = String(entry.label ?? entry.id ?? "View");
    button.addEventListener("click", () => {
      const target = root.querySelector(entry.target);
      target?.scrollIntoView?.({ behavior: "smooth", block: "start" });
      target?.focus?.({ preventScroll: true });
    });
    nav.append(button);
  }
  if (!navigation?.length) emptyState(nav, "Regional navigation is unavailable.");
}

export function campaignMusicStateId(envelope = {}) {
  const state = envelope?.audio?.music_state_id;
  return typeof state === "string" && state.trim() ? state.trim() : null;
}

export function campaignAudioCueIds(envelope = {}) {
  if (!Array.isArray(envelope?.audio?.audio_cue_ids)) return null;
  const allowed = new Set(AUDIO_CATALOG.cues.map((entry) => entry.id));
  return envelope.audio.audio_cue_ids
    .filter((cueId) => typeof cueId === "string" && allowed.has(cueId.trim()))
    .map((cueId) => cueId.trim());
}

function campaignAudioInput(envelope) {
  return {
    campaign: envelope?.session?.campaign,
    done: envelope?.session?.done,
    music_state_id: campaignMusicStateId(envelope),
    observation: {
      market_bullets: (envelope?.briefing ?? []).map((entry) => entry.detail),
      workforce_trust: (envelope?.actors ?? []).map((entry) => entry.status).join(" "),
      in_flight_projects: (envelope?.processes ?? []).map((entry) => entry.detail).join(" "),
    },
  };
}

function renderCampaignCoverageBriefing(items, root) {
  const list = root.querySelector("#campaign-briefing-list");
  if (!list) return;
  const renderItem = (entry) => {
    const item = document.createElement("li");
    const title = document.createElement("strong");
    title.textContent = String(entry.title ?? entry.kind ?? "Briefing");
    const detail = document.createElement("p");
    detail.textContent = String(entry.detail ?? "No visible campaign detail.");
    item.append(title, detail);
    appendSource(item, entry.source);
    return item;
  };
  renderBoundedCollection({
    list,
    overflow: root.querySelector("#campaign-briefing-overflow-list"),
    details: root.querySelector("#campaign-briefing-more"),
    items,
    limit: DEFAULT_VISIBLE_COUNTS.signals,
    label: "additional campaign signals",
    renderItem,
    emptyMessage: "No campaign briefing is available.",
  });
}

function renderCampaignCoverageMetrics(metrics, root) {
  const list = root.querySelector("#campaign-metric-list");
  if (!list) return;
  const renderItem = (metric) => {
    const item = document.createElement("div");
    const label = document.createElement("dt");
    label.textContent = String(metric.label ?? "Metric");
    const value = document.createElement("dd");
    value.textContent = `${metric.value ?? "Unavailable"} ${metric.unit ?? ""}`.trim();
    item.append(label, value);
    appendSource(item, `${metric.source ?? "Visible campaign source"} · ${metric.equivalent ?? "Written equivalent"}`);
    return item;
  };
  renderBoundedCollection({
    list,
    overflow: root.querySelector("#campaign-metric-overflow-list"),
    details: root.querySelector("#campaign-metric-more"),
    items: metrics,
    limit: 4,
    label: "additional metrics",
    renderItem,
    emptyMessage: "No visible campaign metrics are available.",
  });
}

function renderCampaignCoverageActors(actors, root) {
  const list = root.querySelector("#campaign-actor-list");
  if (!list) return;
  const renderItem = (actor) => {
    const item = document.createElement("li");
    item.className = "campaign-actor-card";
    const heading = document.createElement("div");
    heading.className = "timeline-row";
    const title = document.createElement("strong");
    title.textContent = String(actor.label ?? "Actor");
    heading.append(title);
    const status = document.createElement("p");
    status.textContent = `• ${actor.status ?? "Status unavailable"}`;
    const role = document.createElement("small");
    role.className = "source";
    role.textContent = String(actor.role ?? "Actor");
    const detail = document.createElement("p");
    detail.textContent = String(actor.detail ?? "No visible actor detail.");
    item.append(heading, status, role, detail);
    appendSource(item, actor.source);
    return item;
  };
  renderBoundedCollection({
    list,
    overflow: root.querySelector("#campaign-actor-overflow-list"),
    details: root.querySelector("#campaign-actor-more"),
    items: actors,
    limit: DEFAULT_VISIBLE_COUNTS.actors,
    label: "additional actors",
    renderItem,
    emptyMessage: "No campaign actor signals are available.",
  });
}

function renderCampaignCoverageProcesses(processes, root) {
  const list = root.querySelector("#campaign-process-list");
  if (!list) return;
  const renderItem = (process) => {
    const item = document.createElement("li");
    const marker = createVisualToken(visualMarkerFor(process.marker ?? process.label), "marker", root);
    const heading = document.createElement("div");
    heading.className = "timeline-row";
    const title = document.createElement("strong");
    title.textContent = String(process.label ?? "Process");
    heading.append(marker, title, createStatus(process.status, process.status));
    const detail = document.createElement("p");
    detail.textContent = String(process.detail ?? "No visible process detail.");
    item.append(heading, detail);
    appendSource(item, process.source);
    return item;
  };
  renderBoundedCollection({
    list,
    overflow: root.querySelector("#campaign-process-overflow-list"),
    details: root.querySelector("#campaign-process-more"),
    items: processes,
    limit: DEFAULT_VISIBLE_COUNTS.processes,
    label: "additional processes",
    renderItem,
    emptyMessage: "No campaign process is available.",
  });
}

function renderCampaignCoverageHistory(entries, root) {
  const list = root.querySelector("#campaign-history-list");
  if (!list) return;
  const renderItem = (entry) => {
    const item = document.createElement("li");
    const turn = document.createElement("strong");
    turn.textContent = `Turn ${entry.turn ?? "—"}`;
    const command = document.createElement("span");
    command.textContent = ` · ${entry.command ?? "—"}`;
    const hash = document.createElement("small");
    hash.className = "hash";
    hash.textContent = ` · state hash: ${entry.state_hash ?? "—"}`;
    item.append(turn, command, hash);
    if (Array.isArray(entry.observation) && entry.observation.length) {
      const details = document.createElement("details");
      const summary = document.createElement("summary");
      summary.textContent = "Decision-time observation";
      const observation = document.createElement("ul");
      observation.className = "campaign-observation-list";
      for (const line of entry.observation) {
        const observationLine = document.createElement("li");
        observationLine.textContent = String(line);
        observation.append(observationLine);
      }
      details.append(summary, observation);
      item.append(details);
    }
    return item;
  };
  renderBoundedCollection({
    list,
    overflow: root.querySelector("#campaign-history-overflow-list"),
    details: root.querySelector("#campaign-history-more"),
    items: entries,
    limit: DEFAULT_VISIBLE_COUNTS.history,
    label: "additional campaign history rows",
    renderItem,
    emptyMessage: "No committed campaign transitions yet.",
  });
}

function renderCampaignCoverageResolution(envelope, root) {
  const list = root.querySelector("#campaign-resolution-list");
  const status = root.querySelector("#campaign-resolution-status");
  const source = root.querySelector("#campaign-resolution-source");
  const continueButton = root.querySelector("#campaign-resolution-continue");
  if (!list) return;
  const history = Array.isArray(envelope?.history) ? envelope.history : [];
  const latest = history.at?.(-1) ?? history[history.length - 1] ?? null;
  const lines = [];
  if (latest) {
    lines.push({
      label: `Committed turn ${latest.turn ?? "—"}`,
      detail: `Host command: ${latest.command ?? "Unavailable"}`,
      source: "CampaignCoverage.history",
    });
    for (const event of latest.events ?? []) {
      lines.push({ label: "Visible event", detail: String(event), source: "CampaignCoverage.history.events" });
    }
    for (const effect of latest.effects ?? []) {
      lines.push({ label: "Direct visible effect", detail: String(effect), source: "CampaignCoverage.history.effects" });
    }
    if (Array.isArray(latest.observation) && latest.observation.length) {
      lines.push({
        label: "Decision-time observation",
        detail: latest.observation.join(" · "),
        source: "CampaignCoverage.history.observation",
      });
    }
  } else {
    lines.push({
      label: "No committed transition yet",
      detail: "The host has not supplied a campaign transition for this session.",
      source: "CampaignCoverage.history",
    });
  }
  for (const process of Array.isArray(envelope?.processes) ? envelope.processes : []) {
    lines.push({
      label: `Pending or uncertain process · ${process.label ?? "Unavailable"}`,
      detail: `${process.status ?? "Status unavailable"}: ${process.detail ?? "No visible process detail available."}`,
      source: process.source ?? "CampaignCoverage.processes",
    });
  }
  renderBoundedCollection({
    list,
    overflow: null,
    details: null,
    items: lines,
    limit: Math.max(DEFAULT_VISIBLE_COUNTS.processes, 3),
    label: "additional resolution details",
    renderItem: (line) => {
      const item = document.createElement("li");
      const heading = document.createElement("strong");
      heading.textContent = String(line.label ?? "Resolution detail");
      const detail = document.createElement("span");
      detail.textContent = String(line.detail ?? "No visible resolution detail available.");
      item.append(heading, detail);
      appendSource(item, line.source);
      return item;
    },
    emptyMessage: "No visible campaign resolution detail is available.",
  });
  if (status) {
    status.textContent = latest
      ? `Turn ${latest.turn ?? "—"} committed; direct effects and pending processes remain host-reported.`
      : "No committed campaign transition is loaded; direct effects remain unavailable.";
  }
  if (source) source.textContent = latest
    ? "Sources: CampaignCoverage.history, CampaignCoverage.history.effects, and CampaignCoverage.processes."
    : "Source: CampaignCoverage.history; no transition was supplied.";
  if (continueButton) continueButton.disabled = !latest;
}

function setCampaignCoverageReviewSurface(root, active) {
  for (const selector of ["#history-panel", "#debrief-region"]) {
    const panel = root.querySelector(selector);
    if (panel) panel.hidden = Boolean(active);
  }
}

function normalizeActionParameter(parameter = {}) {
  const options = (parameter.options ?? []).map((option) => {
    const value = String(option?.value ?? option?.label ?? option ?? "");
    return { value, label: String(option?.label ?? value) };
  });
  const name = String(parameter.name ?? "parameter");
  return {
    name,
    label: String(parameter.label ?? name),
    inputType: String(parameter.input_type ?? "text"),
    options,
    min: parameter.min,
    max: parameter.max,
  };
}

export function normalizeActionViewModel(spec = {}, submissionMode = "draft", source = null) {
  const id = String(spec.id ?? spec.action_id ?? "action");
  const details = {
    timing: spec.delay_label ?? spec.delay ?? spec.timing ?? null,
    constraint: spec.constraint_label ?? spec.constraint ?? null,
    uncertainty: spec.uncertainty_label ?? spec.uncertainty ?? null,
    cost: spec.cost ?? null,
    commandTemplate: spec.command_template ?? spec.command ?? null,
    source: source ?? spec.source ?? null,
  };
  return {
    id,
    label: String(spec.label ?? spec.title ?? id),
    parameters: (spec.parameters ?? []).map(normalizeActionParameter),
    submissionMode,
    details,
  };
}

export function normalizeCampaignDecision(decision = {}) {
  return normalizeActionViewModel(decision, "commit", decision.source ?? null);
}

function commandForParameters(action, params) {
  return String(action?.details?.commandTemplate ?? "").replace(/\{\{(.*?)\}\}/g, (_, name) => String(params[name] ?? ""));
}

function collectActionParameters(form, action) {
  const params = {};
  for (const parameter of action.parameters ?? []) {
    const input = form?.elements?.namedItem?.(parameter.name);
    params[parameter.name] = String(input?.value ?? "");
  }
  const missing = (action.parameters ?? []).find((parameter) => !params[parameter.name]);
  return missing
    ? { ok: false, message: `Enter ${missing.label}.` }
    : { ok: true, params };
}

export function renderCampaignCoverage(envelope, root = document, onSubmit = null) {
  const panel = root.querySelector("#campaign-coverage-panel");
  if (!envelope || envelope.schema_version !== CAMPAIGN_COVERAGE_SCHEMA) {
    return { ok: false, code: envelope ? "unsupported_campaign_coverage_schema" : "empty_campaign_coverage" };
  }
  if (panel) panel.hidden = false;
  if (panel) panel.dataset.workspaceReady = "true";
  if (panel) panel.dataset.workspaceAreas = "brief resolve review";
  setCampaignCoverageReviewSurface(root, true);
  const role = root.querySelector("#campaign-role");
  const stage = root.querySelector("#campaign-stage");
  const meta = root.querySelector("#campaign-coverage-meta");
  if (role) role.textContent = String(envelope.campaign_role ?? "Campaign coverage");
  if (stage) stage.textContent = `${envelope.stage?.label ?? "Current stage"}: ${envelope.stage?.detail ?? "Visible stage detail unavailable."}`;
  if (meta) meta.textContent = `${envelope.session?.campaign ?? "campaign"} · turn ${envelope.session?.turn ?? "—"}/${envelope.session?.max_turns ?? "—"}`;
  renderCampaignCoverageBriefing(envelope.briefing, root);
  renderCampaignCoverageMetrics(envelope.metrics, root);
  renderCampaignCoverageActors(envelope.actors, root);
  renderCampaignCoverageProcesses(envelope.processes, root);
  if (envelope.session?.campaign !== "competitive-regional-v1") {
    renderUnifiedActionSurface(
      (envelope.decisions ?? []).map(normalizeCampaignDecision),
      root,
      {
        onSubmit: typeof onSubmit === "function" && envelope.session?.done !== true
          ? (action, params, form, command, item) => onSubmit(command, action, params, form, item)
          : null,
        submissionMode: "commit",
      },
    );
  }
  renderCampaignCoverageResolution(envelope, root);
  renderCampaignCoverageHistory(envelope.history, root);
  const debrief = root.querySelector("#campaign-debrief-list");
  if (debrief) {
    const renderItem = (line) => {
      const item = document.createElement("li");
      item.textContent = String(line);
      return item;
    };
    renderBoundedCollection({
      list: debrief,
      overflow: root.querySelector("#campaign-debrief-overflow-list"),
      details: root.querySelector("#campaign-debrief-more"),
      items: envelope.debrief,
      limit: DEFAULT_VISIBLE_COUNTS.history,
      label: "additional debrief lines",
      renderItem,
      emptyMessage: "Campaign debrief becomes available after completion.",
    });
  }
  workspaceController(root)?.sync?.();
  return { ok: true, envelope };
}

export function createCampaignCoverageClient({
  adapter = globalThis.HsMgtGameCampaignAdapter ?? globalThis.HsMgtGameActionAdapter ?? globalThis.HsMgtGameReadOnlyAdapter,
  root = document,
  audio,
  recorder,
  autosave,
  onCommitted = () => {},
} = {}) {
  let currentEnvelope = null;
  const audioClient = audio ?? createAudioClient({ root, recorder });
  const settings = createPresentationSettings({ root, recorder, audio: audioClient });

  function applyCoverageEnvelope(envelope, onSubmit, clearExistingRecovery = true) {
    setReadOnlyControls(root, true);
    const result = renderCampaignCoverage(envelope, root, onSubmit);
    if (!result.ok) return result;
    currentEnvelope = envelope;
    if (clearExistingRecovery) clearRecovery(root);
    renderOnboarding(envelope, root, recorder);
    recordVisibleEnvelope(recorder, envelope);
    const audioInput = campaignAudioInput(envelope);
    const musicStateId = campaignMusicStateId(envelope);
    if (musicStateId) audioClient.setMusicState(musicStateId, audioInput);
    else audioClient.setMusicFromVisible(audioInput);
    audioClient.setAmbienceFromVisible(audioInput);
    return result;
  }

  async function load(sessionId = adapter?.sessionId) {
    configureRecovery(root, () => load(sessionId), recorder);
    if (!adapter || typeof adapter.getCampaignCoverage !== "function") {
      recordPlaytestFailure(recorder, "campaign_coverage_adapter_missing", "Campaign coverage adapter is unavailable.");
      showRecovery(root, "Campaign coverage is unavailable. Load a campaign adapter, then retry the current read.");
      return { ok: false, code: "campaign_coverage_adapter_missing" };
    }
    try {
      const envelope = await adapter.getCampaignCoverage(sessionId);
      const result = applyCoverageEnvelope(
        envelope,
        envelope?.session?.campaign === "competitive-regional-v1" ? null : submit,
      );
      if (!result.ok) {
        recordPlaytestFailure(recorder, result.code, "Campaign coverage schema is unavailable.");
        setPresentationState(root, "Campaign coverage is unavailable; existing presentation remains active.");
        showRecovery(root, "Campaign coverage could not be read. Retry the current host read when the adapter is available.");
        return result;
      }
      return result;
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      recordPlaytestFailure(recorder, "campaign_coverage_adapter_error", message);
      setPresentationState(root, `Campaign coverage adapter error: ${message}`);
      showRecovery(root, `Campaign coverage could not be read: ${message}`);
      return { ok: false, code: "campaign_coverage_adapter_error", message };
    }
  }

  async function loadCompanion(sessionId = adapter?.sessionId) {
    configureRecovery(root, () => loadCompanion(sessionId), recorder);
    if (!adapter || typeof adapter.getCampaignCoverage !== "function") {
      recordPlaytestFailure(recorder, "campaign_coverage_companion_missing", "Campaign coverage adapter is unavailable.");
      showRecovery(root, "Competitive campaign context is unavailable; the action surface remains usable.");
      return { ok: false, code: "campaign_coverage_companion_missing" };
    }
    try {
      const envelope = await adapter.getCampaignCoverage(sessionId);
      const result = applyCoverageEnvelope(envelope, null, false);
      if (!result.ok) {
        recordPlaytestFailure(recorder, "campaign_coverage_companion_schema", "Campaign coverage companion schema is unavailable.");
        showRecovery(root, "Competitive campaign context could not be read; the action surface remains usable.");
        return result;
      }
      return result;
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      recordPlaytestFailure(recorder, "campaign_coverage_companion_error", message);
      showRecovery(root, `Competitive campaign context could not be read; the action surface remains usable: ${message}`);
      return { ok: false, code: "campaign_coverage_companion_error", message };
    }
  }

  async function submit(command) {
    if (currentEnvelope?.session?.campaign === "competitive-regional-v1") {
      const message = "Competitive campaign coverage is a read-only projection; use the action plan.";
      setPresentationState(root, message);
      recordPlaytestFailure(recorder, "competitive_coverage_read_only", message);
      showRecovery(root, message);
      audioClient.playCue("ui.action-reject");
      return { ok: false, code: "competitive_coverage_read_only", message };
    }
    if (!adapter || typeof adapter.submitTurn !== "function") {
      setPresentationState(root, "No campaign submit adapter configured; no transition was attempted.");
      recordPlaytestFailure(recorder, "campaign_submit_adapter_missing", "Campaign submit adapter is unavailable.");
      showRecovery(root, "Campaign submission is unavailable. Review the current read or load a submit-capable host adapter.");
      audioClient.playCue("ui.action-reject");
      return { ok: false, code: "campaign_submit_adapter_missing" };
    }
    try {
      setPresentationState(root, "Submitting the canonical campaign decision…");
      recorder?.record("command_submitted", { campaign: currentEnvelope?.session?.campaign, command, turn: currentEnvelope?.session?.turn });
      const response = await adapter.submitTurn(command);
      if (response?.error) throw new Error(response.error);
      if (typeof autosave === "function") await autosave(adapter.sessionId);
      audioClient.playCue("ui.submit");
      const result = await load(adapter.sessionId);
      if (!result.ok) return result;
      audioClient.playCue("ui.report-received");
      audioClient.playCue("ui.advance-month");
      const cueIds = campaignAudioCueIds(result.envelope);
      if (cueIds) {
        for (const cueId of cueIds) audioClient.playCue(cueId);
      } else if (result.envelope.session?.campaign === "regional-affiliation-v1") {
        audioClient.playCue("event.affiliation-milestone");
      }
      onCommitted(result.envelope);
      setPresentationState(root, "Campaign decision committed; current stage refreshed from the host.");
      return { ok: true, envelope: result.envelope };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      recordPlaytestFailure(recorder, "campaign_submit_rejected", message);
      audioClient.playCue("ui.action-reject");
      setPresentationState(root, `Campaign decision rejected; current stage remains active: ${message}`);
      showRecovery(root, "The host rejected this decision. Review the visible constraints, then retry the current read or choose another decision.");
      return { ok: false, code: "campaign_submit_rejected", message };
    }
  }

  return { load, loadCompanion, submit, audio: audioClient, settings, get envelope() { return currentEnvelope; } };
}

export function renderRegionalWorld(envelope, root = document) {
  if (!envelope || envelope.schema_version !== REGIONAL_WORLD_SCHEMA) {
    renderRegionalOverlays([], root);
    renderRegionalNavigation([], root);
    return { ok: false, code: envelope ? "unsupported_regional_world_schema" : "empty_regional_world" };
  }
  const entities = regionalEntitiesToFixture(envelope);
  if (!entities.some((entity) => entity.id === selectedEntityId)) selectedEntityId = entities[0]?.id;
  selectedBoardId = selectedEntityId;
  const regionalSessionId = envelope.session?.session_id;
  if (currentResolutionSessionId && regionalSessionId !== currentResolutionSessionId) {
    currentResolutionLinks = [];
    currentResolutionSessionId = null;
  }
  currentRegionalLinks = regionalWorldConsequenceLinks(envelope);
  renderMap(entities, root);
  renderSelectedEntity(entities, root);
  renderRegionalBoard(regionalWorldToSceneData(envelope), root);
  renderConsequenceLinks([...currentRegionalLinks, ...currentResolutionLinks], root);
  renderRegionalOverlays(envelope.overlays, root);
  renderRegionalNavigation(envelope.navigation, root);
  return { ok: true, envelope };
}

export function createRegionalWorldClient({ adapter = globalThis.HsMgtGameReadOnlyAdapter, root = document } = {}) {
  let currentEnvelope = null;

  async function load(sessionId = adapter?.sessionId) {
    if (!adapter || typeof adapter.getRegionalWorld !== "function") {
      return { ok: false, code: "regional_world_adapter_missing" };
    }
    try {
      const envelope = await adapter.getRegionalWorld(sessionId);
      const result = renderRegionalWorld(envelope, root);
      currentEnvelope = result.ok ? envelope : null;
      if (!result.ok) {
        const state = root.querySelector("#presentation-state");
        if (state) state.textContent = "Regional world presentation is unavailable; base presentation remains active.";
      }
      return result;
    } catch (error) {
      currentEnvelope = null;
      renderRegionalOverlays([], root);
      renderRegionalNavigation([], root);
      const state = root.querySelector("#presentation-state");
      if (state) state.textContent = `Regional world adapter error: ${error instanceof Error ? error.message : String(error)}`;
      return { ok: false, code: "regional_world_adapter_error" };
    }
  }

  return { load, get envelope() { return currentEnvelope; } };
}

function actionDocument(root) {
  return root?.ownerDocument?.createElement
    ? root.ownerDocument
    : root?.createElement
      ? root
      : root?.documentElement?.ownerDocument ?? globalThis.document;
}

function actionState(root) {
  return root?.dataset ?? root?.documentElement?.dataset ?? (root.__hsMgtActionState ??= {});
}

function actionNode(root, tag, text, className, attrs = {}) {
  const node = actionDocument(root).createElement(tag);
  if (text != null) node.textContent = String(text);
  if (className) node.className = className;
  for (const [key, value] of Object.entries(attrs)) {
    if (key.includes("-")) node.setAttribute(key, String(value));
    else node[key] = value;
  }
  return node;
}

function renderActionDetails(action, root) {
  const drawer = root.querySelector("#context-drawer");
  const detail = root.querySelector("#entity-detail");
  const heading = root.querySelector("#entity-heading");
  if (!drawer || !detail || !heading) return false;
  heading.textContent = `${action.label} details`;
  detail.replaceChildren();
  detail.append(actionNode(root, "p", "These details come from the current host read."));
  const rows = [
    ["Timing", action.details.timing],
    ["Rules", action.details.constraint],
    ["Uncertainty", action.details.uncertainty],
    ["Cost", action.details.cost],
    ["Canonical command", action.details.commandTemplate],
  ];
  const list = actionNode(root, "dl", null, "detail-metrics");
  for (const [label, value] of rows) {
    list.append(actionNode(root, "dt", label), actionNode(root, "dd", value ?? "Not provided by the host."));
  }
  detail.append(list);
  appendSource(detail, action.details.source ?? "Not provided by the host.");
  openContextDrawer(root);
  return true;
}

function renderUnifiedActionSurface(actions, root, { onSubmit = null, onChange = null, submissionMode = "read-only" } = {}) {
  const list = root.querySelector("#action-preview-list");
  if (!list) return { ok: false, code: "action_surface_missing" };
  const surfaceRoot = root.querySelector("#action-builder");
  if (surfaceRoot) surfaceRoot.hidden = false;
  const cards = new Map();
  const editingSnapshots = new Map();
  let expandedId = null;
  const normalizedActions = Array.isArray(actions) ? actions : [];

  const setExpanded = (id, focus = false) => {
    expandedId = id;
    for (const [actionId, card] of cards) {
      const open = actionId === id;
      card.element.dataset.expanded = String(open);
      card.body.hidden = !open;
      card.toggle.setAttribute("aria-expanded", String(open));
    }
    if (focus && id) cards.get(id)?.toggle.focus?.({ preventScroll: true });
  };

  const renderItem = (action) => {
    const item = actionNode(root, "article", null, "action-card");
    item.dataset.actionId = action.id;
    item.dataset.expanded = "false";
    const header = actionNode(root, "div", null, "action-card-header");
    const bodyId = `action-body-${action.id.replace(/[^A-Za-z0-9_-]/g, "-")}`;
    const toggle = actionNode(root, "button", null, "action-toggle", {
      type: "button", "aria-expanded": false, "aria-controls": bodyId,
    });
    toggle.append(actionNode(root, "strong", action.label), actionNode(root, "span", action.details.timing ?? "Details available", "muted"));
    const detailsButton = actionNode(root, "button", "Details", "action-details visual-token", { type: "button" });
    detailsButton.title = "Timing, rules, uncertainty, command, and source";
    const tooltip = actionNode(root, "span", "Timing, rules, uncertainty, command, and source", "visual-token-help");
    tooltip.id = `${bodyId}-details-help`;
    tooltip.setAttribute("role", "tooltip");
    detailsButton.setAttribute("aria-describedby", tooltip.id);
    detailsButton.append(tooltip);
    detailsButton.addEventListener?.("click", (event) => {
      event.stopPropagation?.();
      detailsButton.dataset.tooltipOpen = "true";
      renderActionDetails(action, root);
    });
    toggle.addEventListener?.("click", () => setExpanded(expandedId === action.id ? null : action.id, true));
    toggle.addEventListener?.("keydown", (event) => {
      if (["Enter", " ", "Spacebar"].includes(event.key)) {
        event.preventDefault?.();
        toggle.click?.();
      }
    });
    header.append(toggle, detailsButton);

    const body = actionNode(root, "div", null, "action-card-body");
    body.id = bodyId;
    body.hidden = true;
    const form = actionNode(root, "form", null, "action-card-form");
    form.dataset.actionId = action.id;
    for (const parameter of action.parameters ?? []) {
      const label = actionNode(root, "label", parameter.label);
      const input = actionNode(root, parameter.inputType === "select" ? "select" : "input", null, null, {
        name: parameter.name, required: true,
      });
      if (parameter.inputType !== "select") {
        input.type = parameter.inputType;
        if (parameter.min != null) input.min = String(parameter.min);
        if (parameter.max != null) input.max = String(parameter.max);
        if (parameter.inputType === "number") input.inputMode = "numeric";
      } else for (const option of parameter.options) {
        input.append(actionNode(root, "option", option.label, null, { value: option.value }));
      }
      label.append(input);
      form.append(label);
    }
    const submitButton = actionNode(
      root,
      "button",
      submissionMode === "draft" ? "Add" : submissionMode === "commit" ? "Commit decision" : "Read only",
      null,
      { type: "submit", disabled: submissionMode === "read-only" || typeof onSubmit !== "function" },
    );
    form.append(submitButton);
    if (submissionMode === "draft" && typeof onChange === "function") {
      form.addEventListener?.("input", () => onChange(action, form));
      form.addEventListener?.("change", () => onChange(action, form));
    }
    form.addEventListener?.("submit", (event) => {
      event.preventDefault?.();
      if (submitButton.disabled) return;
      const result = collectActionParameters(form, action);
      if (!result.ok) {
        setPresentationState(root, result.message);
        return;
      }
      onSubmit(action, result.params, form, commandForParameters(action, result.params), item);
    });
    body.append(form);
    item.append(header, body);
    cards.set(action.id, { action, element: item, body, form, submitButton, toggle });
    return item;
  };

  renderBoundedCollection({
    list,
    overflow: root.querySelector("#action-preview-overflow-list"),
    details: root.querySelector("#action-preview-more"),
    items: normalizedActions,
    limit: DEFAULT_VISIBLE_COUNTS.actions,
    label: "more actions",
    renderItem,
    emptyMessage: submissionMode === "commit" ? "No campaign action is available." : "No action is available.",
  });
  const actionMore = root.querySelector("#action-preview-more");
  if (actionMore && normalizedActions.length > DEFAULT_VISIBLE_COUNTS.actions) {
    const remaining = normalizedActions.length - DEFAULT_VISIBLE_COUNTS.actions;
    const summary = actionMore.querySelector?.("summary");
    if (summary) summary.textContent = `Show ${remaining} more`;
  }
  actionState(root).actionSubmissionMode = submissionMode;
  const surface = {
    expand(id, focus = true) {
      const card = cards.get(id);
      if (!card) return false;
      setExpanded(id, focus);
      return true;
    },
    edit(id, params = {}) {
      surface.cancelEditing();
      const card = cards.get(id);
      if (!card) {
        const more = root.querySelector("#action-preview-more");
        if (more) more.open = true;
        return false;
      }
      const overflow = card.element.closest?.("#action-preview-more");
      if (overflow) overflow.open = true;
      const original = {};
      for (const parameter of card.action.parameters ?? []) {
        const input = card.form.elements?.namedItem?.(parameter.name);
        original[parameter.name] = String(input?.value ?? "");
      }
      editingSnapshots.set(id, original);
      setExpanded(id);
      for (const [name, value] of Object.entries(params)) {
        const input = card.form.elements?.namedItem?.(name);
        if (input) input.value = value;
      }
      card.submitButton.textContent = "Save";
      card.form.dataset.editing = "true";
      card.toggle.focus?.({ preventScroll: true });
      return true;
    },
    resetEditing() {
      editingSnapshots.clear();
      for (const card of cards.values()) {
        card.submitButton.textContent = "Add";
        card.form.dataset.editing = "false";
      }
    },
    cancelEditing() {
      for (const [id, original] of editingSnapshots) {
        const card = cards.get(id);
        for (const [name, value] of Object.entries(original ?? {})) {
          const input = card?.form.elements?.namedItem?.(name);
          if (input) input.value = value;
        }
      }
      editingSnapshots.clear();
      for (const card of cards.values()) {
        card.submitButton.textContent = "Add";
        card.form.dataset.editing = "false";
      }
    },
  };
  root.__hsMgtActionSurface = surface;
  return { ok: true, actions: normalizedActions, surface };
}

function renderActions(actions, root) {
  const normalized = (actions ?? []).map((action, index) => normalizeActionViewModel({
    id: action.id ?? action.action_id ?? `action-${index + 1}`,
    label: action.label ?? "Action",
    command: action.command,
    cost: action.cost,
    delay: action.delay,
    constraint: action.constraint,
    uncertainty: action.uncertainty,
    source: action.source,
  }, "read-only", action.source));
  const result = renderUnifiedActionSurface(normalized, root, { submissionMode: "read-only" });
  if (!normalized.length) {
    const surfaceRoot = root.querySelector("#action-builder");
    if (surfaceRoot) surfaceRoot.hidden = true;
  }
  return result;
}

function renderPending(items, root) {
  const list = root.querySelector("#pending-list");
  list.replaceChildren();
  for (const entry of items ?? []) {
    const item = document.createElement("li");
    item.className = "timeline-item";
    const row = document.createElement("div");
    row.className = "timeline-row";
    const marker = createVisualToken(visualMarkerFor(entry.marker ?? entry.title), "marker", root);
    const title = document.createElement("strong");
    title.textContent = String(entry.title ?? "Pending process");
    row.append(marker, title, createStatus(entry.status, entry.status_label));
    const timing = document.createElement("p");
    timing.textContent = String(entry.timing ?? "Visible timing unavailable.");
    const detail = document.createElement("p");
    detail.textContent = String(entry.detail ?? "No visible detail available.");
    item.append(row, timing, detail);
    appendSource(item, entry.source);
    list.append(item);
  }
  if (!items?.length) emptyState(list, "No pending processes available.");
}

function renderMonthlyResult(result, root) {
  const list = root.querySelector("#result-list");
  list.replaceChildren();
  if (!result) {
    emptyState(list, "No monthly result available.");
    return;
  }
  const headline = document.createElement("li");
  headline.className = "result-item";
  const row = document.createElement("div");
  row.className = "timeline-row";
  const title = document.createElement("strong");
  title.textContent = String(result.headline ?? "Monthly result");
  row.append(title, createStatus(result.status, result.status_label));
  headline.append(row);
  for (const line of [...(result.metrics ?? []), ...(result.effects ?? [])]) {
    const detail = document.createElement("p");
    detail.textContent = String(line);
    headline.append(detail);
  }
  appendSource(headline, result.source);
  list.append(headline);
}

function replayDetailText(entry) {
  const details = [];
  if (Array.isArray(entry?.observation) && entry.observation.length) details.push(`observation: ${entry.observation.join(" | ")}`);
  if (Array.isArray(entry?.events) && entry.events.length) details.push(`events: ${entry.events.join(" | ")}`);
  if (Array.isArray(entry?.effects) && entry.effects.length) details.push(`effects: ${entry.effects.join(" | ")}`);
  return details.join(" · ");
}

function renderHistory(entries, root, selectedIndex = -1) {
  const list = root.querySelector("#history-list");
  const renderItem = (entry, index) => {
    const item = document.createElement("li");
    item.className = "history-item";
    if (index === selectedIndex) item.setAttribute("aria-current", "true");
    const turn = document.createElement("strong");
    turn.textContent = `Turn ${entry.turn ?? "—"}`;
    const command = document.createElement("span");
    command.textContent = String(entry.command ?? "—");
    const hash = document.createElement("span");
    hash.className = "hash";
    hash.textContent = `state hash: ${entry.state_hash ?? "—"}`;
    item.append(turn, command, hash);
    if (index === selectedIndex) {
      const detail = document.createElement("span");
      detail.className = "history-detail";
      detail.textContent = replayDetailText(entry) || "No additional visible row detail was supplied.";
      item.append(detail);
    }
    return item;
  };
  renderBoundedCollection({
    list,
    overflow: root.querySelector("#history-overflow-list"),
    details: root.querySelector("#history-more"),
    items: entries,
    limit: DEFAULT_VISIBLE_COUNTS.history,
    label: "additional committed transitions",
    renderItem,
    emptyMessage: "No committed transitions yet.",
  });
}

export function validateHistoryEnvelope(envelope) {
  if (!envelope || typeof envelope !== "object") {
    return { ok: false, code: "empty_history", message: "No host history envelope was supplied." };
  }
  if (envelope.schema_version !== HISTORY_SCHEMA) {
    return { ok: false, code: "unsupported_history_schema", message: "Unsupported host history schema." };
  }
  if (envelope.campaign !== HISTORY_CAMPAIGN) {
    return { ok: false, code: "unsupported_history_campaign", message: "History is outside the supported competitive campaign." };
  }
  if (
    typeof envelope.session_id !== "string"
    || !envelope.session_id.trim()
    || typeof envelope.campaign !== "string"
    || !envelope.campaign.trim()
    || !Array.isArray(envelope.transitions)
    || !Number.isInteger(envelope.transition_count)
    || envelope.transition_count < 0
    || envelope.transition_count !== envelope.transitions.length
    || envelope.transitions.some((entry) => (
      !entry
      || typeof entry !== "object"
      || !Number.isInteger(entry.turn)
      || entry.turn < 0
      || typeof entry.state_hash !== "string"
      || !entry.state_hash.trim()
    ))
  ) {
    return { ok: false, code: "incomplete_history", message: "Host history is missing aligned transition summaries." };
  }
  return { ok: true, envelope };
}

export function renderHistoryEnvelope(envelope, root = document) {
  const validation = validateHistoryEnvelope(envelope);
  if (!validation.ok) return validation;
  renderHistory(envelope.transitions, root);
  const meta = root.querySelector("#session-meta");
  if (meta) {
    const latestHash = envelope.transitions.at(-1)?.state_hash ?? "no committed hash";
    meta.textContent = `${envelope.campaign} · ${envelope.transition_count} committed transitions · hash ${latestHash}`;
  }
  return validation;
}

export function validateReplayEnvelope(envelope) {
  if (!envelope || typeof envelope !== "object") {
    return { ok: false, code: "empty_replay", message: "No host replay envelope was supplied." };
  }
  if (envelope.schema_version !== REPLAY_SCHEMA) {
    return { ok: false, code: "unsupported_replay_schema", message: "Unsupported host replay schema." };
  }
  const transitions = Array.isArray(envelope.transitions) ? envelope.transitions : [];
  const latestHash = transitions.at(-1)?.state_hash ?? null;
  if (
    typeof envelope.session_id !== "string"
    || !envelope.session_id.trim()
    || typeof envelope.campaign !== "string"
    || !envelope.campaign.trim()
    || !Number.isInteger(envelope.seed)
    || envelope.seed < 0
    || !Array.isArray(envelope.transitions)
    || !Number.isInteger(envelope.transition_count)
    || envelope.transition_count < 0
    || envelope.transition_count !== transitions.length
    || (envelope.latest_state_hash !== null
      && (typeof envelope.latest_state_hash !== "string" || !envelope.latest_state_hash.trim()))
    || (transitions.length === 0 && envelope.latest_state_hash !== null)
    || (transitions.length > 0 && envelope.latest_state_hash !== latestHash)
    || transitions.some((entry) => (
      !entry
      || typeof entry !== "object"
      || typeof entry.state_hash !== "string"
      || !entry.state_hash.trim()
    ))
  ) {
    return { ok: false, code: "misaligned_replay", message: "Host replay metadata is not aligned with committed history." };
  }
  return { ok: true, envelope };
}

export function renderReplayEnvelope(envelope, root = document) {
  const validation = validateReplayEnvelope(envelope);
  if (!validation.ok) return validation;
  renderHistory(envelope.transitions, root);
  const meta = root.querySelector("#session-meta");
  if (meta) {
    meta.textContent = `${envelope.campaign} · replay ${envelope.transition_count} committed transitions · hash ${envelope.latest_state_hash ?? "no committed hash"}`;
  }
  return validation;
}

function renderReplayPlaybackState(entry, index, total, playing, root) {
  const status = root.querySelector("#replay-playback-status");
  if (status) {
    if (!entry) {
      status.textContent = "No committed replay rows yet.";
    } else {
      const detail = replayDetailText(entry);
      status.textContent = `Reviewing replay row ${index + 1} of ${total} · Turn ${entry.turn ?? "—"} · command ${entry.command ?? "—"} · ${detail || "no additional visible row detail"} · state hash ${entry.state_hash ?? "—"}. ${playing ? "Playing." : "Paused."}`;
    }
  }
  const previous = root.querySelector("#replay-previous");
  const play = root.querySelector("#replay-play");
  const pause = root.querySelector("#replay-pause");
  const next = root.querySelector("#replay-next");
  if (previous) previous.disabled = !entry || index <= 0;
  if (play) play.disabled = !entry || playing;
  if (pause) pause.disabled = !playing;
  if (next) next.disabled = !entry || index >= total - 1;
}

export function validateSaveEnvelope(envelope) {
  if (!envelope || typeof envelope !== "object") {
    return { ok: false, code: "empty_save", message: "No host checkpoint envelope was supplied." };
  }
  if (envelope.schema_version !== SAVE_SCHEMA) {
    return { ok: false, code: "unsupported_save_schema", message: "Unsupported host checkpoint schema." };
  }
  const latestHash = envelope.latest_state_hash;
  if (
    !["saved", "loaded"].includes(envelope.operation)
    || typeof envelope.session_id !== "string"
    || !envelope.session_id.trim()
    || typeof envelope.campaign !== "string"
    || !envelope.campaign.trim()
    || !Number.isInteger(envelope.seed)
    || envelope.seed < 0
    || !Number.isInteger(envelope.transition_count)
    || envelope.transition_count < 0
    || (latestHash !== null && (typeof latestHash !== "string" || !latestHash.trim()))
    || (envelope.transition_count === 0 && latestHash !== null)
    || (envelope.transition_count > 0 && typeof latestHash !== "string")
  ) {
    return { ok: false, code: "incomplete_save", message: "Host checkpoint metadata is incomplete or misaligned." };
  }
  return { ok: true, envelope };
}

const checkpointError = (code, message) => ({ ok: false, code, message });

export function validateCheckpointDiscoveryEnvelope(envelope) {
  if (!envelope || typeof envelope !== "object") return checkpointError("empty_checkpoint_discovery", "No checkpoint list was supplied.");
  if (envelope.schema_version !== CHECKPOINT_DISCOVERY_SCHEMA) return checkpointError("unsupported_checkpoint_discovery_schema", "Unsupported checkpoint schema.");
  if (!Array.isArray(envelope.checkpoints) || !Number.isInteger(envelope.invalid_entry_count) || envelope.invalid_entry_count < 0) {
    return checkpointError("incomplete_checkpoint_discovery", "Checkpoint metadata is incomplete.");
  }
  if (envelope.checkpoints.some((checkpoint) => (
    !checkpoint
    || typeof checkpoint.session_id !== "string"
    || !/^[A-Za-z0-9_-]+$/.test(checkpoint.session_id)
    || !SESSION_LAUNCH_CAMPAIGNS.has(checkpoint.campaign)
    || !Number.isSafeInteger(checkpoint.seed)
    || checkpoint.seed < 0
    || !Number.isInteger(checkpoint.transition_count)
    || checkpoint.transition_count < 0
    || !["archive", "legacy"].includes(checkpoint.storage)
  ))) return checkpointError("invalid_checkpoint_discovery_entry", "Invalid checkpoint metadata.");
  return { ok: true, envelope };
}

const CHECKPOINT_REFERENCE_FIELDS = [
  "schema_version",
  "session_id",
  "campaign",
  "seed",
  "transition_count",
  "storage",
];

function checkpointReferenceError(code, message) {
  return { ok: false, code, message };
}

export function validateCheckpointReference(reference) {
  if (!reference || typeof reference !== "object" || Array.isArray(reference)) {
    return checkpointReferenceError("empty_checkpoint_reference", "No checkpoint reference was supplied.");
  }
  const keys = Object.keys(reference).sort();
  if (JSON.stringify(keys) !== JSON.stringify([...CHECKPOINT_REFERENCE_FIELDS].sort())) {
    return checkpointReferenceError("invalid_checkpoint_reference_fields", "Checkpoint references may contain metadata only.");
  }
  if (reference.schema_version !== CHECKPOINT_REFERENCE_SCHEMA) {
    return checkpointReferenceError("unsupported_checkpoint_reference_schema", "Unsupported checkpoint reference schema.");
  }
  if (
    typeof reference.session_id !== "string"
    || !/^[A-Za-z0-9_-]+$/.test(reference.session_id)
    || !SESSION_LAUNCH_CAMPAIGNS.has(reference.campaign)
    || !Number.isSafeInteger(reference.seed)
    || reference.seed < 0
    || !Number.isSafeInteger(reference.transition_count)
    || reference.transition_count < 0
    || !["archive", "legacy"].includes(reference.storage)
  ) {
    return checkpointReferenceError("invalid_checkpoint_reference_entry", "Checkpoint reference metadata is invalid.");
  }
  return { ok: true, reference };
}

export function serializeCheckpointReference(reference) {
  const validation = validateCheckpointReference(reference);
  if (!validation.ok) return validation;
  const stableReference = {
    schema_version: CHECKPOINT_REFERENCE_SCHEMA,
    session_id: reference.session_id,
    campaign: reference.campaign,
    seed: reference.seed,
    transition_count: reference.transition_count,
    storage: reference.storage,
  };
  return { ok: true, reference: stableReference, text: `${JSON.stringify(stableReference, null, 2)}\n` };
}

export function parseCheckpointReference(text) {
  if (typeof text !== "string" || !text.trim()) {
    return checkpointReferenceError("empty_checkpoint_reference", "The checkpoint reference file is empty.");
  }
  let reference;
  try {
    reference = JSON.parse(text);
  } catch {
    return checkpointReferenceError("invalid_checkpoint_reference_json", "The checkpoint reference is not valid JSON.");
  }
  return validateCheckpointReference(reference);
}

export function downloadCheckpointReference(reference, root = document) {
  const serialized = serializeCheckpointReference(reference);
  if (!serialized.ok) return serialized;
  const documentRef = root?.ownerDocument ?? globalThis.document;
  if (
    typeof Blob !== "function"
    || !documentRef?.createElement
    || typeof globalThis.URL?.createObjectURL !== "function"
  ) {
    return checkpointReferenceError("checkpoint_reference_export_unavailable", "Checkpoint reference export is unavailable in this browser.");
  }
  const blob = new Blob([serialized.text], { type: "application/json" });
  const objectUrl = globalThis.URL.createObjectURL(blob);
  const link = documentRef.createElement("a");
  const filename = `hs-mgt-checkpoint-${reference.session_id}.json`;
  link.href = objectUrl;
  link.download = filename;
  link.setAttribute?.("aria-label", `Download checkpoint reference for ${reference.session_id}`);
  try {
    link.click?.();
  } finally {
    globalThis.URL.revokeObjectURL?.(objectUrl);
  }
  return { ok: true, reference: serialized.reference, text: serialized.text, filename };
}

export async function importCheckpointReference(file, root = document) {
  const status = root.querySelector("#session-checkpoint-status");
  if (!file || typeof file.text !== "function") {
    const result = checkpointReferenceError("checkpoint_reference_file_missing", "Choose a checkpoint reference file first.");
    if (status) status.textContent = result.message;
    return result;
  }
  let text;
  try {
    text = await file.text();
  } catch {
    const result = checkpointReferenceError("checkpoint_reference_file_unreadable", "The checkpoint reference file could not be read.");
    if (status) status.textContent = result.message;
    return result;
  }
  const result = parseCheckpointReference(text);
  if (!result.ok) {
    if (status) status.textContent = `${result.message} Enter an ID manually or choose another reference.`;
    return result;
  }
  const input = root.querySelector("#session-id");
  if (input) input.value = result.reference.session_id;
  input?.focus?.();
  if (status) status.textContent = `Reference for ${result.reference.session_id} is ready to load; the host will validate the current checkpoint.`;
  return result;
}

export function renderCheckpointDiscovery(envelope, root = document, { onDownloadArtifact = null } = {}) {
  const validation = validateCheckpointDiscoveryEnvelope(envelope);
  const list = root.querySelector("#session-checkpoint-list");
  const status = root.querySelector("#session-checkpoint-status");
  if (!validation.ok) {
    if (list) { list.replaceChildren(); emptyState(list, validation.message); }
    if (status) status.textContent = validation.message;
    return validation;
  }
  if (list) {
    list.replaceChildren();
    for (const checkpoint of envelope.checkpoints) {
      const item = document.createElement("li");
      const select = document.createElement("button");
      select.textContent = `${sessionCampaignLabel(checkpoint.campaign)} · ${checkpoint.session_id} · ${checkpoint.transition_count} transitions · ${checkpoint.storage} · Use this session ID`;
      select.addEventListener("click", () => {
        const input = root.querySelector("#session-id");
        if (input) input.value = checkpoint.session_id;
        input?.focus?.();
        if (status) status.textContent = `ID ${checkpoint.session_id} is ready to load.`;
      });
      const exportButton = document.createElement("button");
      exportButton.type = "button";
      exportButton.textContent = "Export reference";
      exportButton.setAttribute?.("aria-label", `Export reference for ${checkpoint.session_id}`);
      exportButton.addEventListener("click", () => {
        const result = downloadCheckpointReference({
          schema_version: CHECKPOINT_REFERENCE_SCHEMA,
          ...checkpoint,
        }, root);
        if (status) status.textContent = result.ok
          ? `Checkpoint reference exported for ${checkpoint.session_id}. It contains metadata only.`
          : result.message;
      });
      item.append(select, exportButton);
      if (typeof onDownloadArtifact === "function") {
        const artifactButton = document.createElement("button");
        artifactButton.type = "button";
        artifactButton.textContent = "Download host save";
        artifactButton.setAttribute?.("aria-label", `Download host save for ${checkpoint.session_id}`);
        artifactButton.addEventListener("click", async () => {
          artifactButton.disabled = true;
          try {
            const result = await onDownloadArtifact(checkpoint);
            if (status) status.textContent = result.ok
              ? `Host save downloaded for ${checkpoint.session_id}. The file remains host-generated.`
              : result.message;
          } finally {
            artifactButton.disabled = false;
          }
        });
        item.append(artifactButton);
      }
      list.append(item);
    }
    if (!envelope.checkpoints.length) emptyState(list, "No valid checkpoints found.");
  }
  if (status) status.textContent = envelope.invalid_entry_count
    ? `${envelope.checkpoints.length} valid checkpoint(s); ${envelope.invalid_entry_count} invalid omitted.`
    : `${envelope.checkpoints.length} valid checkpoint(s).`;
  return { ok: true, envelope };
}

export async function downloadHostCheckpointArtifact({ adapter, checkpoint, root = document } = {}) {
  const sessionId = String(checkpoint?.session_id ?? "").trim();
  const storage = checkpoint?.storage;
  if (
    !adapter || typeof adapter.downloadCheckpointArtifact !== "function"
    || !/^[A-Za-z0-9_-]+$/.test(sessionId)
    || !["archive", "legacy"].includes(storage)
  ) {
    return { ok: false, code: "checkpoint_artifact_unavailable", message: "Host save download is unavailable for this checkpoint." };
  }
  try {
    const result = await adapter.downloadCheckpointArtifact(sessionId, storage);
    if (!result?.blob || typeof Blob !== "function" || typeof globalThis.URL?.createObjectURL !== "function") {
      return { ok: false, code: "checkpoint_artifact_download_unavailable", message: "This browser cannot download the host save artifact." };
    }
    const documentRef = root?.ownerDocument ?? globalThis.document;
    if (!documentRef?.createElement) {
      return { ok: false, code: "checkpoint_artifact_download_unavailable", message: "The checkpoint download surface is unavailable." };
    }
    const objectUrl = globalThis.URL.createObjectURL(result.blob);
    const link = documentRef.createElement("a");
    link.href = objectUrl;
    link.download = result.filename || `hs-mgt-checkpoint-${sessionId}.save`;
    link.setAttribute?.("aria-label", `Download host save for ${sessionId}`);
    try {
      link.click?.();
    } finally {
      globalThis.URL.revokeObjectURL?.(objectUrl);
    }
    return { ok: true, filename: link.download };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return { ok: false, code: error?.code ?? "checkpoint_artifact_download_error", message: `Host save download failed; the current session remains active: ${message}` };
  }
}

function renderObservationLines(observation, root) {
  const list = root.querySelector("#observation-list");
  list.replaceChildren();
  if (!observation) {
    emptyState(list, "No current observation available.");
    return;
  }
  const staffing = (observation.staffing ?? [])
    .map((metric) => `${metric.label ?? "Staffing"} ${metric.value ?? "Unavailable"}`)
    .join(", ");
  const capacity = (observation.capacity ?? [])
    .map((metric) => `${metric.label ?? "Capacity"} ${metric.value ?? "Unavailable"}`)
    .join(", ");
  const operations = observation.operations ?? {};
  for (const line of [
    `Organization: ${observation.organization_name ?? "Unavailable"}`,
    `Reported access index: ${observation.access_index ?? "Unavailable"}`,
    `Reported quality index: ${observation.quality_index ?? "Unavailable"}`,
    `Workforce trust: ${observation.workforce_trust ?? "Unavailable"}`,
    `Community trust: ${observation.community_trust ?? "Unavailable"}`,
    `Staffing: ${staffing || "Unavailable"}`,
    `Physical capacity: ${capacity || "Unavailable"}`,
    `Prior-month operations: treated ${operations.treated_volume ?? "Unavailable"}/${operations.demand ?? "Unavailable"} demand units (${operations.unmet_demand ?? "Unavailable"} unmet); revenue ${operations.revenue ?? "Unavailable"}, cost ${operations.cost ?? "Unavailable"}, margin ${operations.margin ?? "Unavailable"}`,
    `Cash runway: ${observation.cash_runway_signal ?? "Unavailable"}`,
    `In-flight projects: ${observation.in_flight_projects ?? "Unavailable"}`,
  ]) appendText(list, line);
}

function visibleTargetId(detail, institutions) {
  const normalized = String(detail ?? "").toLowerCase();
  return institutions.find((institution) => {
    const name = String(institution.name ?? "").toLowerCase().trim();
    return name && normalized.includes(name);
  })?.id;
}

function readOnlyEnvelopeToFixture(envelope) {
  const observation = envelope.observation ?? {};
  const session = envelope.session ?? {};
  const resources = envelope.resources ?? {};
  const operations = observation.operations ?? {};
  const institutions = (envelope.institutions ?? []).map((institution) => ({
    id: institution.id ?? "institution",
    icon: "▣",
    type: institution.role ?? "Institution",
    name: institution.name ?? "Unavailable institution",
    status: "reported",
    status_label: "Host-reported",
    summary: "Actor-visible institution detail supplied by the host.",
    public_signal: "Actor-visible institution",
    metrics: [
      { label: "Access", value: observation.access_index ?? "Unavailable" },
      { label: "Quality", value: observation.quality_index ?? "Unavailable" },
      { label: "Workforce", value: observation.workforce_trust ?? "Unavailable" },
      { label: "Margin", value: operations.margin ?? "Unavailable" },
    ],
    facilities: (institution.facilities ?? []).map((facility) => ({
      icon: "▥",
      name: facility.name ?? "Observed facility detail",
      kind: facility.kind ?? "Host-reported",
      status: "reported",
      status_label: "Host-reported",
      detail: (facility.metrics ?? [])
        .map((metric) => `${metric.label ?? "Metric"} ${metric.value ?? "Unavailable"}`)
        .join(" · ") || "No visible facility metrics available.",
    })),
  }));
  const briefing = [
    ...(observation.market_bullets ?? []).map((detail) => ({
      kind: "Market signal",
      title: detail,
      detail: "Public actor-visible market information.",
      status: "reported",
      status_label: "Reported",
      source: "ReadOnlyObservation.market_bullets",
      target_id: visibleTargetId(detail, institutions),
    })),
    ...(observation.policy_bullets ?? []).map((detail) => ({
      kind: "Policy signal",
      title: detail,
      detail: "Actor-visible policy information.",
      status: "reported",
      status_label: "Reported",
      source: "ReadOnlyObservation.policy_bullets",
      target_id: visibleTargetId(detail, institutions),
    })),
    ...(observation.information_gaps ?? []).map((detail) => ({
      kind: "Information gap",
      title: detail,
      detail: "Unavailable information remains explicit; no private state is inferred.",
      status: "uncertain",
      status_label: "Unavailable",
      source: "ReadOnlyObservation.information_gaps",
    })),
  ];
  const latest = envelope.latest_transition;
  const transitionEffects = [
    ...(latest?.events ?? []),
    ...(latest?.effects ?? []),
  ];
  return {
    header_metrics: [
      { label: "Month", value: `Year ${session.year ?? "Unavailable"} · ${session.month_name ?? "Unavailable"}` },
      { label: "Turn", value: `${session.turn ?? "Unavailable"} / ${session.max_turns ?? "Unavailable"}` },
      { label: "Cash", value: `${resources.cash ?? "Unavailable"} units` },
      { label: "Action points", value: `${resources.action_points ?? "Unavailable"} AP` },
      { label: "Political capital", value: resources.political_capital ?? "Unavailable" },
      { label: "Workforce trust", value: observation.workforce_trust ?? "Unavailable" },
      { label: "Session", value: session.session_id ?? "Unavailable" },
    ],
    briefing,
    entities: institutions,
    selected_entity_id: institutions[0]?.id,
    actions: [],
    pending: (envelope.pending_effects ?? []).map((effect) => ({
      title: effect.label ?? "Pending process",
      status: "reported",
      status_label: "Host-reported",
      timing: "Timing supplied by the host observation",
      detail: effect.detail ?? "No visible process detail available.",
      source: effect.source ?? "ReadOnlyPresentation.pending_effects",
    })),
    monthly_result: {
      status: "reported",
      status_label: "Host-reported",
      headline: `Committed observation for turn ${session.turn ?? "Unavailable"}`,
      metrics: [
        `Treated volume: ${operations.treated_volume ?? "Unavailable"} / ${operations.demand ?? "Unavailable"} demand units`,
        `Unmet demand: ${operations.unmet_demand ?? "Unavailable"} units`,
        `Revenue: ${operations.revenue ?? "Unavailable"} · cost: ${operations.cost ?? "Unavailable"} · margin: ${operations.margin ?? "Unavailable"}`,
      ],
      effects: transitionEffects.length ? transitionEffects : ["No committed transition is available yet."],
      source: "ReadOnlyPresentation.observation and committed history",
    },
  };
}

function clearReadOnlySurface(root, message) {
  const campaignCoveragePanel = root.querySelector("#campaign-coverage-panel");
  if (campaignCoveragePanel) {
    campaignCoveragePanel.hidden = true;
    campaignCoveragePanel.dataset.workspaceReady = "false";
    campaignCoveragePanel.dataset.workspaceAreas = "brief decide resolve review";
  }
  setCampaignCoverageReviewSurface(root, false);
  renderPresentation({ presentation_fixture: undefined }, root);
  renderObservationLines(null, root);
  renderHistory([], root);
  const meta = root.querySelector("#session-meta");
  if (meta) meta.textContent = "—";
  const debrief = root.querySelector("#debrief-list");
  debrief.replaceChildren();
  emptyState(debrief, "Debrief is unavailable in the read-only session view.");
  const commands = root.querySelector("#legal-command-list");
  commands.replaceChildren();
  emptyState(commands, "Submission is unavailable in this view.");
  setEndSessionControl(root, false);
  setReadOnlyControls(root, true);
  setPresentationState(root, message);
}

export function validateReadOnlyEnvelope(envelope) {
  if (!envelope || typeof envelope !== "object") {
    return { ok: false, message: "No read-only presentation envelope was supplied." };
  }
  if (envelope.schema_version !== READ_ONLY_PRESENTATION_SCHEMA) {
    return { ok: false, message: "Unsupported read-only presentation schema." };
  }
  if (!envelope.session || !envelope.observation) {
    return { ok: false, message: "Read-only presentation is missing session or observation data." };
  }
  return { ok: true, envelope };
}

export function renderReadOnlyEnvelope(envelope, root = document) {
  const validation = validateReadOnlyEnvelope(envelope);
  if (!validation.ok) {
    clearReadOnlySurface(root, validation.message);
    return validation;
  }
  const campaignCoveragePanel = root.querySelector("#campaign-coverage-panel");
  if (campaignCoveragePanel) {
    campaignCoveragePanel.hidden = true;
    campaignCoveragePanel.dataset.workspaceReady = "false";
    campaignCoveragePanel.dataset.workspaceAreas = "brief decide resolve review";
  }
  setCampaignCoverageReviewSurface(root, false);
  const fixture = readOnlyEnvelopeToFixture(envelope);
  renderPresentation({ presentation_fixture: fixture }, root);
  renderObservationLines(envelope.observation, root);
  renderHistory(envelope.history, root);
  const debrief = root.querySelector("#debrief-list");
  debrief.replaceChildren();
  emptyState(debrief, "Debrief is supplied by the host end-session view.");
  const commands = root.querySelector("#legal-command-list");
  commands.replaceChildren();
  emptyState(commands, "Submission is unavailable in this view.");
  setReadOnlyControls(root, true);
  const latestHash = envelope.replay?.latest_state_hash ?? "no committed hash yet";
  const session = envelope.session;
  const meta = root.querySelector("#session-meta");
  if (meta) meta.textContent = `${session.campaign ?? "session"} · turn ${session.turn ?? "—"}/${session.max_turns ?? "—"} · hash ${latestHash}`;
  setPresentationState(root, "Live or recorded read-only presentation loaded");
  return { ok: true, envelope };
}

export function validateEndSessionEnvelope(envelope) {
  if (!envelope || typeof envelope !== "object") {
    return { ok: false, code: "empty_end_session", message: "No final host envelope was supplied." };
  }
  if (envelope.schema_version !== END_SESSION_SCHEMA) {
    return { ok: false, code: "unsupported_end_session_schema", message: "Unsupported final host envelope schema." };
  }
  if (!envelope.session_id || !envelope.campaign || envelope.done !== true) {
    return { ok: false, code: "invalid_end_session", message: "Final host envelope is missing terminal session fields." };
  }
  if (
    !Array.isArray(envelope.history)
    || !Array.isArray(envelope.debrief)
    || !envelope.replay
    || !Number.isInteger(envelope.replay.transition_count)
    || envelope.replay.transition_count < 0
    || envelope.replay.transition_count !== envelope.history.length
  ) {
    return { ok: false, code: "incomplete_end_session", message: "Final host envelope is missing history, replay, or debrief data." };
  }
  const latestHash = envelope.history.at(-1)?.state_hash ?? null;
  if (envelope.replay.latest_state_hash !== latestHash) {
    return { ok: false, code: "misaligned_end_session", message: "Final host replay metadata does not match committed history." };
  }
  return { ok: true, envelope };
}

export function resolutionAudioCueIds(envelope = {}) {
  return Array.isArray(envelope?.audio_cue_ids)
    ? envelope.audio_cue_ids
    : visibleEventCues(envelope);
}

export function resolutionMusicStateId(envelope = {}) {
  const state = envelope?.music_state_id;
  return typeof state === "string" && state.trim() ? state.trim() : null;
}

export function renderEndSessionEnvelope(envelope, root = document) {
  const validation = validateEndSessionEnvelope(envelope);
  if (!validation.ok) return validation;
  const historyList = root.querySelector("#history-list");
  const debriefList = root.querySelector("#debrief-list");
  const meta = root.querySelector("#session-meta");
  if (historyList) renderHistory(envelope.history, root);
  if (debriefList) {
    debriefList.replaceChildren();
    for (const line of envelope.debrief) {
      const item = document.createElement("li");
      item.textContent = String(line);
      debriefList.append(item);
    }
    if (!envelope.debrief.length) emptyState(debriefList, "The host supplied no debrief lines.");
  }
  if (meta) {
    const hash = envelope.replay.latest_state_hash ?? "no committed hash";
    meta.textContent = `${envelope.campaign} · final turn ${envelope.turn}/${envelope.max_turns} · ${envelope.replay.transition_count} transitions · hash ${hash}`;
  }
  const campaignCoveragePanel = root.querySelector("#campaign-coverage-panel");
  if (campaignCoveragePanel && envelope.campaign === "competitive-regional-v1") {
    campaignCoveragePanel.hidden = true;
    campaignCoveragePanel.dataset.workspaceReady = "false";
    campaignCoveragePanel.dataset.workspaceAreas = "brief decide resolve review";
  }
  setCampaignCoverageReviewSurface(root, false);
  setReadOnlyControls(root, true);
  setEndSessionControl(root, false);
  setActionControls(root, false);
  setPresentationState(root, "Host session ended; final history and debrief loaded");
  workspaceEvent(root, "session_ended", { focus: false });
  workspaceController(root)?.sync?.();
  return { ok: true, envelope };
}

async function endHostSession({ adapter, sessionId, root, recorder, audio, firstMonthFlow }) {
  if (!adapter || typeof adapter.endSession !== "function") {
    const message = "No host end-session adapter configured; the current session remains active.";
    setPresentationState(root, message);
    showRecovery(root, "Ending the session is unavailable. Keep the current host session active or load a compatible adapter.");
    recordPlaytestFailure(recorder, "end_session_adapter_missing", message);
    return { ok: false, code: "end_session_adapter_missing" };
  }
  if (!String(sessionId ?? "").trim()) {
    const message = "A live session ID is required before ending a session.";
    setPresentationState(root, message);
    return { ok: false, code: "session_id_missing", message };
  }
  setPresentationState(root, "Ending the host session…");
  setEndSessionControl(root, false);
  try {
    const envelope = await adapter.endSession(sessionId);
    const result = renderEndSessionEnvelope(envelope, root);
    if (!result.ok) {
      setEndSessionControl(root, typeof adapter.endSession === "function");
      recordPlaytestFailure(recorder, result.code, result.message);
      showRecovery(root, "The host returned an unsupported final envelope; the current session remains active.");
      return result;
    }
    clearRecovery(root);
    renderOnboarding(envelope, root, recorder);
    recordVisibleEnvelope(recorder, envelope);
    firstMonthFlow?.update({ sessionLoaded: true, sessionDone: true, refreshed: true, resolutionReviewed: true });
    audio?.setMusicState("debrief");
    audio?.setAmbienceFromVisible({ campaign: envelope.campaign, done: true });
    return result;
  } catch (error) {
    setEndSessionControl(root, typeof adapter.endSession === "function");
    const message = error instanceof Error ? error.message : String(error);
    recordPlaytestFailure(recorder, "end_session_adapter_error", message);
    setPresentationState(root, `End-session failed; the current session remains active: ${message}`);
    showRecovery(root, `The host did not end the session: ${message}`);
    return { ok: false, code: "end_session_adapter_error", message };
  }
}

const SESSION_LAUNCH_CAMPAIGNS = new Set([
  "competitive-regional-v1",
  "stabilization-v1",
  "regional-affiliation-v1",
]);
const SESSION_LAUNCH_DIFFICULTIES = new Set(["easy", "normal", "hard", "expert"]);

function sessionCampaignLabel(campaign) {
  return {
    "competitive-regional-v1": "competitive regional",
    "stabilization-v1": "stabilization",
    "regional-affiliation-v1": "regional affiliation",
  }[campaign] ?? "selected";
}

function sessionLaunchStatus(root, message) {
  const node = root.querySelector("#session-launch-status");
  if (node) node.textContent = message;
}

function readSessionLaunchOptions(root) {
  const campaign = root.querySelector("#session-campaign")?.value;
  const seedText = String(root.querySelector("#session-seed")?.value ?? "").trim();
  const difficulty = String(root.querySelector("#session-difficulty")?.value ?? "").toLowerCase();
  if (!SESSION_LAUNCH_CAMPAIGNS.has(campaign)) {
    return { ok: false, code: "unsupported_campaign", message: "Choose a supported campaign before starting." };
  }
  if (!/^\d+$/.test(seedText)) {
    return { ok: false, code: "invalid_seed", message: "Enter a non-negative integer seed before starting." };
  }
  const seed = Number(seedText);
  if (!Number.isSafeInteger(seed) || seed < 0) {
    return { ok: false, code: "invalid_seed", message: "Enter a safe, non-negative integer seed before starting." };
  }
  if (campaign === "competitive-regional-v1" && !SESSION_LAUNCH_DIFFICULTIES.has(difficulty)) {
    return { ok: false, code: "invalid_difficulty", message: "Choose Easy, Normal, Hard, or Expert before starting." };
  }
  const options = { campaign, seed };
  if (campaign === "competitive-regional-v1") options.difficulty = difficulty;
  return { ok: true, options };
}

export function createSessionLauncher({ adapter, root = document, load, recorder = null, sessionStore = createSessionIdStorage() } = {}) {
  const form = root.querySelector("#session-launch-form");
  const start = root.querySelector("#session-start");
  const existingId = root.querySelector("#session-id");
  const loadButton = root.querySelector("#session-load");
  const discoveryButton = root.querySelector("#session-checkpoints-refresh");
  const referenceFile = root.querySelector("#session-checkpoint-reference-file");
  const referenceImportButton = root.querySelector("#session-checkpoint-reference-import");
  const campaign = root.querySelector("#session-campaign");
  const difficulty = root.querySelector("#session-difficulty");
  let busy = false;

  function updateCampaignControls() {
    const selected = campaign?.value;
    if (start) start.textContent = `Start ${sessionCampaignLabel(selected)} session`;
    if (difficulty) difficulty.disabled = selected !== "competitive-regional-v1";
  }

  const setBusy = (value) => {
    busy = value;
    if (start) start.disabled = value;
    if (loadButton) loadButton.disabled = value;
    if (discoveryButton) discoveryButton.disabled = value;
    if (referenceImportButton) referenceImportButton.disabled = value;
  };

  async function refreshCheckpoints() {
    if (!adapter || typeof adapter.listCheckpoints !== "function") {
      return { ok: false, code: "checkpoint_discovery_adapter_missing", message: "Host adapter unavailable." };
    }
    setBusy(true);
    try {
      return renderCheckpointDiscovery(await adapter.listCheckpoints(), root, {
        onDownloadArtifact: (checkpoint) => downloadHostCheckpointArtifact({ adapter, checkpoint, root }),
      });
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      const status = root.querySelector("#session-checkpoint-status");
      if (status) status.textContent = `Checkpoint discovery failed; enter an ID manually: ${message}`;
      return { ok: false, code: "checkpoint_discovery_error", message };
    } finally {
      setBusy(false);
    }
  }

  async function loadExisting(event) {
    event?.preventDefault?.();
    if (busy) return { ok: false, code: "session_launch_busy" };
    const sessionId = String(existingId?.value ?? "").trim();
    if (!sessionId) {
      sessionLaunchStatus(root, "Enter an existing session ID before loading.");
      return { ok: false, code: "session_id_missing" };
    }
    if (!adapter) {
      sessionLaunchStatus(root, "Loading an existing session requires a host adapter; the demo fixture was not replaced.");
      return { ok: false, code: "session_load_adapter_missing" };
    }
    if (typeof load !== "function") {
      sessionLaunchStatus(root, "Session loading is unavailable in this client.");
      return { ok: false, code: "session_load_unavailable" };
    }
    setBusy(true);
    sessionLaunchStatus(root, "Loading the host session…");
    try {
      const result = await load(sessionId);
      if (!result?.ok) {
        if (isUnknownSessionResult(result)) sessionStore.clear();
        sessionLaunchStatus(root, result?.message ?? "The host session could not be loaded; the current view remains active.");
        return result ?? { ok: false, code: "session_load_failed" };
      }
      sessionStore.set(sessionId);
      sessionLaunchStatus(root, `Host session loaded: ${sessionId}`);
      return result;
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      recorder?.recordFailure({ class: "adapter_error", message, recoverable: true });
      sessionLaunchStatus(root, `Session load failed; the current view remains active: ${message}`);
      return { ok: false, code: "session_load_error", message };
    } finally {
      setBusy(false);
    }
  }

  async function startSession(event) {
    event?.preventDefault?.();
    if (busy) return { ok: false, code: "session_launch_busy" };
    const input = readSessionLaunchOptions(root);
    if (!input.ok) {
      sessionLaunchStatus(root, input.message);
      return input;
    }
    if (!adapter || typeof adapter.startSession !== "function") {
      sessionLaunchStatus(root, "Starting a session requires a host start-session adapter; no local session was created.");
      return { ok: false, code: "start_session_adapter_missing" };
    }
    if (typeof load !== "function") {
      sessionLaunchStatus(root, "Session loading is unavailable in this client.");
      return { ok: false, code: "session_load_unavailable" };
    }
    setBusy(true);
    sessionLaunchStatus(root, "Starting a host session…");
    let response;
    try {
      response = await adapter.startSession(input.options);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      recorder?.recordFailure({ class: "adapter_error", message, recoverable: true });
      sessionLaunchStatus(root, `Host session start failed: ${message}`);
      setBusy(false);
      return { ok: false, code: "start_session_adapter_error", message };
    }
    const sessionId = typeof response?.session_id === "string" ? response.session_id.trim() : "";
    if (!sessionId) {
      sessionLaunchStatus(root, "The host start response did not include a valid session ID; the current view remains active.");
      setBusy(false);
      return { ok: false, code: "session_id_missing" };
    }
    try {
      const result = await load(sessionId);
      if (!result?.ok) {
        if (isUnknownSessionResult(result)) sessionStore.clear();
        sessionLaunchStatus(root, result?.message ?? "The new host session could not be loaded; the current view remains active.");
        return result ?? { ok: false, code: "session_load_failed" };
      }
      if (existingId) existingId.value = sessionId;
      sessionStore.set(sessionId);
      sessionLaunchStatus(root, `${sessionCampaignLabel(response?.campaign ?? input.options.campaign)} session loaded: ${sessionId}`);
      return { ok: true, session_id: sessionId, envelope: result.envelope ?? response };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      recorder?.recordFailure({ class: "adapter_error", message, recoverable: true });
      sessionLaunchStatus(root, `Session started, but its presentation could not be loaded: ${message}`);
      return { ok: false, code: "session_load_error", message };
    } finally {
      setBusy(false);
    }
  }

  form?.addEventListener("submit", startSession);
  loadButton?.addEventListener("click", loadExisting);
  discoveryButton?.addEventListener("click", () => refreshCheckpoints());
  referenceImportButton?.addEventListener("click", async () => {
    if (busy) return;
    setBusy(true);
    try {
      await importCheckpointReference(referenceFile?.files?.[0], root);
    } finally {
      setBusy(false);
    }
  });
  campaign?.addEventListener("change", updateCampaignControls);
  updateCampaignControls();
  const storedSessionId = sessionStore.get();
  if (storedSessionId && existingId && !String(existingId.value ?? "").trim()) {
    existingId.value = storedSessionId;
  }
  if (!adapter?.startSession) {
    sessionLaunchStatus(root, "Configure a host adapter to start or load a session; the demo fixture remains available.");
  }
  return { start: startSession, load: loadExisting, refreshCheckpoints, importReference: () => importCheckpointReference(referenceFile?.files?.[0], root) };
}

export function createReadOnlyClient({ adapter = globalThis.HsMgtGameReadOnlyAdapter, root = document, recorder = null } = {}) {
  let currentEnvelope = null;
  let sessionId = adapter?.sessionId;
  const sessionStore = createSessionIdStorage();
  const firstMonthFlow = createFirstMonthFlow({ root });
  bindWorkspaceFlow(firstMonthFlow, root);
  const audioClient = createAudioClient({ root, recorder });
  const regionalWorldClient = createRegionalWorldClient({ adapter, root });
  const coverageAdapter = globalThis.HsMgtGameCampaignAdapter ?? adapter;
  const campaignCoverageClient = createCampaignCoverageClient({ adapter: coverageAdapter, root, audio: audioClient, recorder });
  const settings = createPresentationSettings({ root, recorder, audio: audioClient });

  function render(envelope) {
    const result = renderReadOnlyEnvelope(envelope, root);
    currentEnvelope = result.ok ? envelope : null;
    if (result.ok) {
      setEndSessionControl(root, typeof adapter?.endSession === "function");
      clearRecovery(root);
      renderOnboarding(envelope, root, recorder);
      recordVisibleEnvelope(recorder, envelope);
      audioClient.setMusicFromVisible(envelope);
      audioClient.setAmbienceFromVisible(envelope);
    }
    return result;
  }

  function renderStaticFixture(fixture = presentationFixture) {
    currentEnvelope = null;
    renderEnvelope({ ...demoEnvelope, legal_commands: [], presentation_fixture: fixture }, root);
    setEndSessionControl(root, false);
    setReadOnlyControls(root, false);
    setPresentationState(root, "Static fixture loaded; no live adapter configured");
    firstMonthFlow.update({
      sessionLoaded: true,
      sessionDone: Boolean(fixture?.session?.done),
      briefingReviewed: false,
      resolutionReviewed: false,
      resolutionVisible: false,
      refreshed: false,
      submitted: false,
    });
    workspaceEvent(root, { type: "session_loaded", done: Boolean(fixture?.session?.done) }, { focus: false });
    audioClient.setMusicState("stable_operations");
    return { ok: true, fixture };
  }

  async function load(nextSessionId = sessionId) {
    const requestedSessionId = String(nextSessionId ?? "").trim();
    const replacingSession = Boolean(sessionId && requestedSessionId && requestedSessionId !== sessionId);
    configureRecovery(root, () => load(requestedSessionId), recorder);
    setReadOnlyControls(root, true);
    setPresentationState(root, "Loading read-only presentation…");
    if (adapter && !requestedSessionId) {
      setPresentationState(root, "A host session ID is required before loading presentation data.");
      showRecovery(root, "Enter or start a host session before loading the presentation.");
      return { ok: false, code: "session_id_missing" };
    }
    if (!adapter || typeof adapter.getPresentation !== "function") {
      if (coverageAdapter && typeof coverageAdapter.getCampaignCoverage === "function") {
        const result = await campaignCoverageClient.load(requestedSessionId);
        if (result.ok) {
          sessionId = requestedSessionId;
          sessionStore.set(requestedSessionId);
        }
        return result;
      }
      recordPlaytestFailure(recorder, "read_only_adapter_missing", "No read-only presentation adapter is configured.");
      showRecovery(root, "No live read adapter is configured. Load a host adapter, then retry the current read.");
      return renderStaticFixture();
    }
    try {
      const envelope = await adapter.getPresentation(requestedSessionId);
      if (!envelope) {
        if (!replacingSession) clearReadOnlySurface(root, "The read-only adapter returned no presentation data.");
        recordPlaytestFailure(recorder, "adapter_error", "The read-only adapter returned no presentation data.");
        showRecovery(root, "The host returned no presentation. Retry the current read.");
        return { ok: false, code: "empty_presentation" };
      }
      const validation = validateReadOnlyEnvelope(envelope);
      if (!validation.ok) {
        recordPlaytestFailure(recorder, validation.code, "The replacement presentation schema is unavailable.");
        showRecovery(root, "The host returned an unsupported presentation. The current session remains active.");
        return validation;
      }
      const result = render(envelope);
      if (result.ok) {
        await regionalWorldClient.load(requestedSessionId);
        sessionId = requestedSessionId;
        sessionStore.set(requestedSessionId);
        setEndSessionControl(root, typeof adapter?.endSession === "function");
      }
      if (!result.ok) {
        recordPlaytestFailure(recorder, result.code, "The read-only presentation schema is unavailable.");
        showRecovery(root, "The host returned an unsupported presentation. Retry the current read or use a compatible adapter.");
      }
      if (result.ok) {
        firstMonthFlow.update({
          sessionLoaded: true,
          sessionDone: Boolean(envelope?.session?.done),
          briefingReviewed: false,
          resolutionReviewed: false,
          resolutionVisible: false,
          refreshed: false,
          submitted: false,
        });
        workspaceEvent(root, { type: "session_loaded", done: Boolean(envelope?.session?.done) }, { focus: false });
        audioClient.playCue("ui.report-received");
      }
      return result;
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      if (!replacingSession) clearReadOnlySurface(root, `Read-only adapter error: ${message}`);
      recordPlaytestFailure(recorder, "read_only_adapter_error", message);
      showRecovery(root, `Read-only adapter error: ${message}`);
      return { ok: false, code: "adapter_error", message };
    }
  }

  async function endSession() {
    const result = await endHostSession({ adapter, sessionId, root, recorder, audio: audioClient, firstMonthFlow });
    if (result.ok) {
      currentEnvelope = result.envelope;
      sessionId = null;
      sessionStore.clear();
      adapter.activateSession?.(null);
    }
    return result;
  }

  root.querySelector("#session-end")?.addEventListener("click", endSession);
  const sessionLauncher = createSessionLauncher({ adapter, root, load, recorder, sessionStore });
  return { load, render, renderStaticFixture, endSession, sessionLauncher, sessionStore, firstMonthFlow, audio: audioClient, settings, regionalWorld: regionalWorldClient, campaignCoverage: campaignCoverageClient, get envelope() { return currentEnvelope; } };
}

function setActionControls(root, enabled) {
  const mode = actionState(root).actionSubmissionMode ?? "read-only";
  const surfaceRoot = root.querySelector("#action-builder");
  if (surfaceRoot) surfaceRoot.hidden = !enabled;
  const plan = root.querySelector("#action-plan");
  if (plan) plan.hidden = mode !== "draft" || !enabled;
  for (const selector of ["#draft-action-list", "#validate-actions", "#submit-month", "#cancel-edit"]) {
    const node = root.querySelector(selector);
    if (node) {
      const editing = selector === "#cancel-edit" && actionState(root).actionEditing === "true";
      node.hidden = !enabled || mode !== "draft" || (selector === "#cancel-edit" && !editing);
      node.disabled = !enabled;
    }
  }
}

function renderDraftActions(drafts, root, onRemove, onRevise) {
  const list = root.querySelector("#draft-action-list");
  if (!list) return;
  list.replaceChildren();
  for (const [index, draft] of drafts.entries()) {
    const item = actionNode(root, "li", null, "draft-action");
    const detail = actionNode(root, "div");
    detail.append(actionNode(root, "strong", draft.label ?? draft.action?.label ?? draft.action_id ?? "Action"));
    const params = actionNode(root, "small");
    const labels = draft.action?.parameters ?? [];
    params.textContent = labels.length
      ? labels.map((parameter) => `${parameter.label}: ${draft.params?.[parameter.name] ?? "—"}`).join(" · ")
      : "No parameters";
    detail.append(params);
    const controls = actionNode(root, "span");
    const revise = actionNode(root, "button", "Revise");
    revise.type = "button";
    revise.addEventListener("click", () => onRevise(index));
    const remove = actionNode(root, "button", "Remove");
    remove.type = "button";
    remove.addEventListener("click", () => onRemove(index));
    controls.append(revise, remove);
    item.append(detail, controls);
    list.append(item);
  }
  if (!drafts.length) emptyState(list, "Your plan is empty. Add an action.");
  const cancel = root.querySelector("#cancel-edit");
  if (cancel) cancel.hidden = actionState(root).actionEditing !== "true";
}

function renderActionCatalog(catalog, root, onAdd, onChange = null) {
  const actions = (catalog?.actions ?? []).map((spec) => normalizeActionViewModel(
    spec,
    "draft",
    spec.source ?? null,
  ));
  actionState(root).actionSubmissionMode = "draft";
  return renderUnifiedActionSurface(actions, root, {
    submissionMode: "draft",
    onSubmit: (action, params, form, command) => onAdd(action, params, form, command),
    onChange,
  });
}

function renderValidation(validation, root, drafts = []) {
  const status = root.querySelector("#validation-status");
  const submit = root.querySelector("#submit-month");
  const previews = root.querySelector("#validation-preview-list");
  if (!validation) {
    if (status) status.textContent = "Add actions to build a plan.";
    if (submit) submit.hidden = true;
    previews?.replaceChildren();
    return;
  }
  if (status) {
    status.textContent = validation.valid
      ? `Plan checked: ${validation.cost?.action_points ?? "?"} AP · ${validation.cost?.cash_cost ?? "?"} cash · ${validation.cost?.political_capital ?? "?"} political capital.`
      : `Plan needs changes: ${(validation.errors ?? []).join(" ")}`;
  }
  if (submit) submit.hidden = !validation.valid;
  if (!previews) return;
  previews.replaceChildren();
  const labels = new Map((drafts ?? []).map((draft) => [
    draft.action_id,
    draft.label ?? draft.action?.label ?? draft.action_id,
  ]));
  for (const preview of validation.previews ?? []) {
    const item = actionNode(root, "li");
    item.append(
      actionNode(root, "strong", labels.get(preview.action_id) ?? preview.action_id ?? "Checked action"),
      actionNode(root, "span", ` · ${preview.cost?.action_points ?? "?"} AP · ${preview.cost?.cash_cost ?? "?"} cash · ${preview.cost?.political_capital ?? "?"} political capital`),
    );
    const details = actionNode(root, "details");
    details.append(actionNode(root, "summary", "Details"), actionNode(root, "code", preview.canonical_command ?? "Not provided by the host.", "command-preview"));
    item.append(details);
    previews.append(item);
  }
}

export function createActionClient({ adapter = globalThis.HsMgtGameActionAdapter, root = document, recorder = null, storage } = {}) {
  let catalog = null;
  let drafts = [];
  let validation = null;
  let editingIndex = null;
  let sessionId = adapter?.sessionId;
  let activeCampaign = adapter?.campaign ?? null;
  const sessionStore = createSessionIdStorage({ storage });
  const firstMonthFlow = createFirstMonthFlow({ root });
  bindWorkspaceFlow(firstMonthFlow, root);
  const audioClient = createAudioClient({ root, recorder });
  const resolutionClient = createResolutionClient({ adapter, root, audio: audioClient });
  const historyClient = createHistoryClient({ adapter, root, recorder });
  const replayClient = createReplayClient({ adapter, root });
  const checkpointClient = createCheckpointClient({ adapter, root, recorder, refresh: load, audio: audioClient });
  const regionalWorldClient = createRegionalWorldClient({ adapter, root });
  const coverageAdapter = globalThis.HsMgtGameCampaignAdapter ?? adapter;
  const campaignCoverageClient = createCampaignCoverageClient({
    adapter: coverageAdapter,
    root,
    audio: audioClient,
    recorder,
    autosave: (sessionId) => checkpointClient.autosave(sessionId),
    onCommitted: (envelope) => {
      firstMonthFlow.update({
        flow: "campaign-coverage",
        sessionLoaded: true,
        sessionDone: Boolean(envelope?.session?.done),
        coverageLoaded: true,
        decisionSubmitted: true,
        refreshed: Boolean(envelope),
        resolutionReviewed: false,
      });
      workspaceEvent(root, envelope?.session?.done ? "session_ended" : "transition_committed", { focus: false });
    },
  });
  const settings = createPresentationSettings({ root, recorder, audio: audioClient });

  async function refreshCompetitiveCoverageCompanion(requestedSessionId) {
    if (activeCampaign !== "competitive-regional-v1" || typeof campaignCoverageClient.loadCompanion !== "function") {
      return { ok: true, skipped: true };
    }
    const result = await campaignCoverageClient.loadCompanion(requestedSessionId);
    if (!result.ok) {
      recordPlaytestFailure(
        recorder,
        result.code ?? "campaign_coverage_companion_error",
        result.message ?? "Competitive campaign context could not be refreshed.",
      );
    }
    return result;
  }

  function draftCommand() {
    return drafts.map((draft) => draft.command).join("; ");
  }

  function invalidateDraft() {
    validation = null;
    firstMonthFlow.update({ draftCount: drafts.length, validated: false });
    renderValidation(null, root, drafts);
    setPresentationState(root, "Draft changed; host validation is required again.");
  }

  function renderDraftState() {
    actionState(root).actionEditing = editingIndex == null ? "false" : "true";
    renderDraftActions(
      drafts,
      root,
      (index) => {
        editingIndex = null;
        root.__hsMgtActionSurface?.resetEditing?.();
        drafts.splice(index, 1);
        audioClient.playCue("ui.action-remove");
        invalidateDraft();
        renderDraftState();
      },
      (index) => {
        const draft = drafts[index];
        editingIndex = index;
        invalidateDraft();
        renderDraftState();
        root.__hsMgtActionSurface?.edit?.(draft.action_id, draft.params);
        setPresentationState(root, `Revising draft action ${index + 1}.`);
      },
    );
  }

  function handleDraftSubmit(action, params, form, command) {
    const draft = {
      action_id: action.id,
      label: action.label,
      action,
      params,
      command,
    };
    const replacing = editingIndex != null
      && form?.dataset?.editing === "true"
      && drafts[editingIndex]?.action_id === action.id;
    const targetIndex = replacing ? editingIndex : null;
    if (targetIndex == null) drafts.push(draft);
    else drafts[targetIndex] = draft;
    if (replacing) {
      editingIndex = null;
      root.__hsMgtActionSurface?.resetEditing?.();
    }
    invalidateDraft();
    audioClient.playCue("ui.action-add");
    renderDraftState();
    setActionControls(root, true);
    const added = root.querySelector(`#draft-action-list li:nth-child(${(targetIndex ?? drafts.length - 1) + 1})`);
    if (added) {
      added.tabIndex = -1;
      added.focus?.({ preventScroll: true });
    }
    setPresentationState(root, replacing ? `${action.label} saved.` : `${action.label} added to your plan.`);
    return { ok: true, action, params, form };
  }

  async function validateDraft() {
    if (!adapter || typeof adapter.validateTurn !== "function") {
      setPresentationState(root, "No host validation adapter configured; no submission was attempted.");
      recordPlaytestFailure(recorder, "validation_adapter_missing", "Host validation adapter is unavailable.");
      showRecovery(root, "Validation is unavailable. Load a host adapter before submitting a decision.");
      return { ok: false, code: "validation_adapter_missing" };
    }
    setPresentationState(root, "Checking plan…");
    try {
      const result = await adapter.validateTurn(sessionId, draftCommand());
      validation = result;
      recorder?.recordValidation({ valid: Boolean(result.valid), code: result.code, message: result.error ?? result.message });
      renderValidation(validation, root, drafts);
      firstMonthFlow.update({ validated: Boolean(validation.valid) });
      audioClient.playCue(validation.valid ? "ui.action-confirm" : "ui.action-reject");
      setPresentationState(root, validation.valid ? "Plan checked; review before committing." : "Plan needs changes; revise and retry.");
      return { ok: Boolean(validation.valid), envelope: validation };
    } catch (error) {
      validation = null;
      renderValidation(null, root, drafts);
      audioClient.playCue("ui.action-reject");
      const message = error instanceof Error ? error.message : String(error);
      recordPlaytestFailure(recorder, "validation_adapter_error", message);
      setPresentationState(root, `Validation adapter error: ${message}`);
      showRecovery(root, `Validation could not be read: ${message}`);
      return { ok: false, code: "validation_adapter_error", message };
    }
  }

  async function submit() {
    if (!validation?.valid || validation.canonical_command_text !== draftCommand()) {
      setPresentationState(root, "Validate the unchanged draft before submitting.");
      return { ok: false, code: "validation_required" };
    }
    if (!adapter || typeof adapter.submitTurn !== "function") {
      setPresentationState(root, "No submit adapter configured; no transition was attempted.");
      recordPlaytestFailure(recorder, "submit_adapter_missing", "Submit adapter is unavailable.");
      showRecovery(root, "Submission is unavailable. Review the validated draft or load a submit-capable host adapter.");
      return { ok: false, code: "submit_adapter_missing" };
    }
    let response;
    try {
      recorder?.record("command_submitted", { campaign: "competitive-regional-v1", command: validation.canonical_command_text, turn: catalog?.turn });
      response = await adapter.submitTurn(validation.canonical_command_text);
      if (response?.error) throw new Error(response.error);
      await checkpointClient.autosave(sessionId);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      recordPlaytestFailure(recorder, "submit_rejected", message);
      setPresentationState(root, `Submission rejected; current session was not replaced: ${message}`);
      showRecovery(root, "The host rejected this command. Review the validation message, revise the draft, and retry.");
      return { ok: false, code: "submit_rejected", message };
    }
    drafts = [];
    validation = null;
    editingIndex = null;
    firstMonthFlow.update({
      draftCount: 0,
      validated: false,
      submitted: true,
      resolutionVisible: false,
      refreshed: false,
      sessionDone: false,
    });
    audioClient.playCue("ui.submit");
    let refreshMessage = "Committed response received from the host adapter.";
    let refreshedPresentationDone = false;
    if (typeof adapter.getResolution === "function") {
      const resolution = await resolutionClient.load(response.latest_transition?.turn, sessionId);
      if (!resolution.ok) refreshMessage += " Resolution presentation was unavailable.";
      else {
        firstMonthFlow.update({ resolutionVisible: true });
        audioClient.playCue("ui.advance-month");
        const musicStateId = resolutionMusicStateId(resolution.envelope);
        if (musicStateId) audioClient.setMusicState(musicStateId, resolution.envelope.after);
        else audioClient.setMusicFromVisible(resolution.envelope.after);
        const cueIds = resolutionAudioCueIds(resolution.envelope);
        for (const cueId of cueIds) audioClient.playCue(cueId);
      }
    }
    if (typeof adapter.getPresentation === "function") {
      try {
        const presentation = await adapter.getPresentation(sessionId);
        refreshedPresentationDone = Boolean(presentation?.session?.done);
        const rendered = renderReadOnlyEnvelope(presentation, root);
        if (!rendered.ok) {
          recordPlaytestFailure(recorder, rendered.code, "The refreshed action presentation schema is unavailable.");
          showRecovery(root, "The committed result loaded, but its refreshed presentation is unavailable. Retry the current read.");
          renderEnvelope(response, root);
          refreshMessage = "Committed response received; read-only refresh was unavailable.";
        } else {
          clearRecovery(root);
          renderOnboarding(presentation, root, recorder);
          recordVisibleEnvelope(recorder, presentation);
          firstMonthFlow.update({ refreshed: true });
          audioClient.setMusicFromVisible(presentation);
          audioClient.setAmbienceFromVisible(presentation);
          audioClient.playCue("ui.report-received");
          if (typeof adapter.getHistory === "function") {
            await historyClient.load(sessionId);
          }
          if (typeof adapter.getReplay === "function") {
            const replay = await replayClient.load(sessionId);
            if (!replay.ok) {
              recordPlaytestFailure(recorder, replay.code, replay.message ?? "Live replay refresh was unavailable.");
            }
          }
          await regionalWorldClient.load(sessionId);
          await refreshCompetitiveCoverageCompanion(sessionId);
        }
      } catch (error) {
        renderEnvelope(response, root);
        const message = error instanceof Error ? error.message : String(error);
        recordPlaytestFailure(recorder, "adapter_error", message);
        showRecovery(root, `Committed response received, but the refreshed read failed: ${message}`);
        refreshMessage = `Committed response received; read-only refresh failed: ${message}`;
      }
    } else {
      renderEnvelope(response, root);
    }
    if (catalog) renderActionCatalog(catalog, root, handleDraftSubmit, () => {
      if (actionState(root).actionEditing === "true") invalidateDraft();
    });
    setReadOnlyControls(root, true);
    setActionControls(root, !refreshedPresentationDone);
    setEndSessionControl(root, typeof adapter.endSession === "function" && !refreshedPresentationDone);
    renderDraftState();
    renderValidation(null, root, drafts);
    firstMonthFlow.update({ sessionDone: refreshedPresentationDone });
    workspaceEvent(root, refreshedPresentationDone ? "session_ended" : "transition_committed", { focus: false });
    setPresentationState(root, refreshMessage);
    return { ok: true, envelope: response };
  }

  async function loadCampaignCoverage(requestedSessionId) {
    const result = await campaignCoverageClient.load(requestedSessionId);
    if (!result.ok) return result;
    catalog = null;
    drafts = [];
    validation = null;
    editingIndex = null;
    sessionId = requestedSessionId;
    sessionStore.set(requestedSessionId);
    adapter.activateSession?.(requestedSessionId, result.envelope?.session?.campaign ?? null);
    actionState(root).actionSubmissionMode = "commit";
    const terminalSession = Boolean(result.envelope?.session?.done);
    setActionControls(root, !terminalSession);
    renderDraftState();
    renderValidation(null, root, drafts);
    const actionMode = root.querySelector("#action-mode");
    if (actionMode) actionMode.textContent = "Choose an action";
    firstMonthFlow.update({
      flow: "campaign-coverage",
      sessionLoaded: true,
      sessionDone: Boolean(result.envelope?.session?.done),
      actionCatalogLoaded: false,
      coverageLoaded: true,
      draftCount: 0,
      validated: false,
      submitted: false,
      resolutionVisible: false,
      refreshed: false,
      briefingReviewed: false,
      resolutionReviewed: false,
    });
    workspaceEvent(root, { type: "session_loaded", done: terminalSession }, { focus: false });
    setEndSessionControl(root, typeof adapter.endSession === "function" && !terminalSession);
    checkpointClient.setEnabled(
      typeof adapter.saveSession === "function" && typeof adapter.loadSession === "function",
    );
    setPresentationState(root, `${result.envelope.session.campaign} actions loaded; choose an action.`);
    return result;
  }

  // Action-client load owns an explicitly requested, one-attempt host-only
  // durable-checkpoint retry for the browser-refresh resume path.
  async function load(nextSessionId = sessionId, { automaticResume = false } = {}) {
    const requestedSessionId = String(nextSessionId ?? "").trim();
    const replacingSession = Boolean(sessionId && requestedSessionId && requestedSessionId !== sessionId);
    configureRecovery(root, () => load(requestedSessionId), recorder);
    const actionMode = root.querySelector("#action-mode");
    setReadOnlyControls(root, true);
    if (!replacingSession && !sessionId) {
      setActionControls(root, false);
      renderActions([], root);
      if (actionMode) actionMode.textContent = "Choose an action";
    }
    setPresentationState(root, "Loading action catalog…");
    if (adapter && !requestedSessionId) {
      setPresentationState(root, "A host session ID is required before loading actions.");
      showRecovery(root, "Enter or start a host session before loading the action catalog.");
      return { ok: false, code: "session_id_missing" };
    }
    let requestedCampaign = adapter?.sessionId === requestedSessionId ? adapter?.campaign : null;
    if (!requestedCampaign && typeof adapter?.getSession === "function") {
      try {
        const session = await adapter.getSession(requestedSessionId);
        requestedCampaign = session?.campaign ?? null;
        if (requestedCampaign) adapter.activateSession?.(requestedSessionId, requestedCampaign);
      } catch {
        // The campaign-specific fallback below preserves the existing error boundary.
      }
    }
    activeCampaign = requestedCampaign;
    if (
      ["stabilization-v1", "regional-affiliation-v1"].includes(requestedCampaign)
      && typeof coverageAdapter?.getCampaignCoverage === "function"
    ) {
      return loadCampaignCoverage(requestedSessionId);
    }
    if (!adapter || typeof adapter.getActionCatalog !== "function" || typeof adapter.validateTurn !== "function") {
      if (coverageAdapter && typeof coverageAdapter.getCampaignCoverage === "function") {
        const result = await campaignCoverageClient.load(requestedSessionId);
        if (result.ok) sessionId = requestedSessionId;
        return result;
      }
      setPresentationState(root, "Action adapter unavailable; read-only mode remains active.");
      recordPlaytestFailure(recorder, "action_adapter_missing", "No action catalog and validation adapter is configured.");
      showRecovery(root, "Action mode is unavailable. Use a read-only or campaign adapter, then retry the current read.");
      return { ok: false, code: "action_adapter_missing" };
    }
    try {
      const presentation = typeof adapter.getPresentation === "function"
        ? await adapter.getPresentation(requestedSessionId)
        : null;
      const nextCatalog = await adapter.getActionCatalog(requestedSessionId);
      if (!nextCatalog || nextCatalog.schema_version !== "competitive-actions-v1") {
        throw new Error("Unsupported action catalog schema.");
      }
      const terminalSession = Boolean(presentation?.session?.done);
      if (typeof adapter.getPresentation === "function") {
        const validation = validateReadOnlyEnvelope(presentation);
        if (!validation.ok) {
          recordPlaytestFailure(recorder, validation.code, "The replacement action presentation schema is unavailable.");
          showRecovery(root, "The host returned an unsupported presentation. The current session remains active.");
          return validation;
        }
        const rendered = renderReadOnlyEnvelope(presentation, root);
        if (!rendered.ok) {
          recordPlaytestFailure(recorder, rendered.code, "The action presentation schema is unavailable.");
          showRecovery(root, "The host returned an unsupported presentation. Retry the current read or use a compatible adapter.");
          return rendered;
        }
        clearRecovery(root);
        renderOnboarding(presentation, root, recorder);
        recordVisibleEnvelope(recorder, presentation);
        audioClient.setMusicFromVisible(presentation);
        if (typeof adapter.getHistory === "function") {
          await historyClient.load(requestedSessionId);
        }
        if (typeof adapter.getReplay === "function") {
          const replay = await replayClient.load(requestedSessionId);
          if (!replay.ok) {
            recordPlaytestFailure(recorder, replay.code, replay.message ?? "Live replay refresh was unavailable.");
          }
        }
        await regionalWorldClient.load(requestedSessionId);
        await refreshCompetitiveCoverageCompanion(requestedSessionId);
      }
      catalog = nextCatalog;
      renderActionCatalog(catalog, root, handleDraftSubmit, () => {
        if (actionState(root).actionEditing === "true") invalidateDraft();
      });
      setActionControls(root, !terminalSession);
      if (actionMode) actionMode.textContent = "Build your plan";
      renderDraftState();
      renderValidation(null, root, drafts);
      firstMonthFlow.update({
        sessionLoaded: true,
        sessionDone: terminalSession,
        actionCatalogLoaded: true,
        draftCount: drafts.length,
        validated: false,
        submitted: false,
        resolutionVisible: false,
        refreshed: false,
        briefingReviewed: false,
        resolutionReviewed: false,
      });
      workspaceEvent(root, { type: "session_loaded", done: terminalSession }, { focus: false });
      setPresentationState(root, "Actions loaded; build your plan.");
      sessionId = requestedSessionId;
      sessionStore.set(requestedSessionId);
      adapter.activateSession?.(requestedSessionId);
      setEndSessionControl(root, typeof adapter.endSession === "function" && !terminalSession);
      checkpointClient.setEnabled(
        typeof adapter.saveSession === "function" && typeof adapter.loadSession === "function",
      );
      if (automaticResume) {
        sessionLaunchStatus(root, `Host session refreshed after browser refresh: ${requestedSessionId}`);
      }
      return { ok: true, catalog };
    } catch (error) {
      if (
        automaticResume
        && isUnknownSessionResult(error)
        && typeof adapter?.loadSession === "function"
      ) {
        try {
          sessionLaunchStatus(root, `Recovering durable host checkpoint ${requestedSessionId}…`);
          await adapter.loadSession(requestedSessionId);
          return load(requestedSessionId);
        } catch (restoreError) {
          error = restoreError;
        }
      }
      const message = error instanceof Error ? error.message : String(error);
      if (typeof coverageAdapter?.getCampaignCoverage === "function") {
        const coverage = await loadCampaignCoverage(requestedSessionId);
        if (coverage.ok) return coverage;
      }
      recordPlaytestFailure(recorder, "action_adapter_error", message);
      if (replacingSession) {
        setPresentationState(root, `Replacement session could not be loaded; the current session remains active: ${message}`);
      } else {
        setActionControls(root, false);
        if (actionMode) actionMode.textContent = "read-only view · action adapter unavailable";
        setPresentationState(root, `Action adapter error: ${message}`);
      }
      showRecovery(root, `Action adapter error: ${message}`);
      return { ok: false, code: "action_adapter_error", message };
    }
  }

  async function endSession() {
    const result = await endHostSession({ adapter, sessionId, root, recorder, audio: audioClient, firstMonthFlow });
    if (result.ok) {
      drafts = [];
      validation = null;
      editingIndex = null;
      sessionId = null;
      activeCampaign = null;
      sessionStore.clear();
      adapter.activateSession?.(null);
      checkpointClient.setEnabled(false);
    }
    return result;
  }

  root.querySelector("#validate-actions")?.addEventListener("click", validateDraft);
  root.querySelector("#submit-month")?.addEventListener("click", submit);
  root.querySelector("#cancel-edit")?.addEventListener("click", () => {
    editingIndex = null;
    root.__hsMgtActionSurface?.cancelEditing?.();
    renderDraftState();
    setPresentationState(root, "Revision cancelled.");
  });
  root.querySelector("#session-end")?.addEventListener("click", endSession);
  const sessionLauncher = createSessionLauncher({ adapter, root, load, recorder, sessionStore });
  return { load, validate: validateDraft, submit, endSession, sessionLauncher, sessionStore, firstMonthFlow, audio: audioClient, settings, history: historyClient, replay: replayClient, checkpoint: checkpointClient, regionalWorld: regionalWorldClient, campaignCoverage: campaignCoverageClient, get drafts() { return drafts; } };
}

function reducedMotion(root) {
  return Boolean(
    root.documentElement?.dataset.reducedMotion === "true"
      || globalThis.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches,
  );
}

function appendResolutionItems(list, items, emptyMessage) {
  list.replaceChildren();
  for (const value of items ?? []) {
    const item = document.createElement("li");
    item.textContent = String(value);
    list.append(item);
  }
  if (!items?.length) emptyState(list, emptyMessage);
}

function snapshotItems(snapshot) {
  const operations = snapshot?.observation?.operations ?? {};
  const resources = snapshot?.resources ?? {};
  return [
    `Cash: ${resources.cash ?? "—"}`,
    `Action points: ${resources.action_points ?? "—"}`,
    `Political capital: ${resources.political_capital ?? "—"}`,
    `Demand: ${operations.demand ?? "—"}`,
    `Treated volume: ${operations.treated_volume ?? "—"}`,
    `Unmet demand: ${operations.unmet_demand ?? "—"}`,
    `Revenue: ${operations.revenue ?? "—"}`,
    `Cost: ${operations.cost ?? "—"}`,
    `Margin: ${operations.margin ?? "—"}`,
  ];
}

export function renderResolution(envelope, root = document) {
  const panel = root.querySelector("#resolution-panel");
  const status = root.querySelector("#resolution-state");
  const steps = root.querySelector("#resolution-step-list");
  const before = root.querySelector("#resolution-before-list");
  const after = root.querySelector("#resolution-after-list");
  const effects = root.querySelector("#resolution-effect-list");
  const progress = root.querySelector("#resolution-progress");
  if (!panel || !status || !steps || !before || !after || !effects) {
    return { ok: false, code: "resolution_surface_missing" };
  }
  panel.hidden = false;
  steps.replaceChildren();
  if (!envelope) {
    currentResolutionLinks = [];
    currentResolutionSessionId = null;
    renderConsequenceLinks(currentRegionalLinks, root);
    status.textContent = "No committed resolution is available.";
    if (progress) progress.textContent = "No written resolution stages are loaded.";
    appendResolutionItems(before, [], "Decision-time snapshot unavailable.");
    appendResolutionItems(after, [], "Post-resolution snapshot unavailable.");
    appendResolutionItems(effects, [], "No direct committed effects available.");
    return { ok: false, code: "empty_resolution" };
  }
  const sequence = planResolutionSequence(envelope);
  for (const step of sequence) {
    const item = document.createElement("li");
    item.className = "resolution-step";
    item.dataset.stepId = step.stage_id ?? "";
    item.dataset.attentionPriority = String(step.attention_priority);
    item.dataset.surfaceSync = step.surface_sync.join(",");
    const heading = document.createElement("div");
    heading.className = "timeline-row";
    const label = document.createElement("strong");
    label.textContent = String(step.label ?? step.stage_id ?? "Resolution step");
    heading.append(label);
    const source = document.createElement("small");
    source.className = "source";
    source.textContent = `Source: ${step.source ?? "host resolution"}`;
    item.append(heading, source);
    for (const value of step.items ?? []) {
      const detail = document.createElement("p");
      detail.textContent = String(value);
      item.append(detail);
    }
    if (!step.items?.length) {
      const detail = document.createElement("p");
      detail.className = "empty";
      detail.textContent = "No additional visible detail.";
      item.append(detail);
    }
    steps.append(item);
  }
  if (!sequence.length) emptyState(steps, "No resolution steps available.");
  if (progress) progress.textContent = `${sequence.length} written stages loaded; local pacing never removes committed text.`;
  appendResolutionItems(before, snapshotItems(envelope.before), "Decision-time snapshot unavailable.");
  appendResolutionItems(after, snapshotItems(envelope.after), "Post-resolution snapshot unavailable.");
  appendResolutionItems(
    effects,
    (envelope.effects ?? []).map((effect) => `${effect.text ?? "Effect"} · Source: ${effect.source ?? "host"}`),
    "No direct committed effects available.",
  );
  currentResolutionLinks = [
    ...resolutionResponseLinks(envelope),
    ...resolutionConsequenceLinks(envelope),
  ];
  currentResolutionSessionId = envelope.session_id ?? null;
  renderConsequenceLinks([...currentRegionalLinks, ...currentResolutionLinks], root);
  status.textContent = `Committed turn ${envelope.turn ?? "—"} · state hash ${envelope.replay?.state_hash ?? "—"}`;
  workspaceController(root)?.sync?.();
  return { ok: true, envelope };
}

export function createResolutionClient({ adapter = globalThis.HsMgtGameActionAdapter, root = document, audio = null } = {}) {
  let envelope = null;
  let activeIndex = 0;
  let paused = true;
  let timer = null;

  function steps() {
    return planResolutionSequence(envelope ?? {});
  }

  function updateControls() {
    const items = root.querySelectorAll("#resolution-step-list .resolution-step");
    items.forEach((item, index) => {
      const active = index === activeIndex;
      item.classList.toggle("resolution-step--active", active);
      if (active) item.setAttribute("aria-current", "step");
      else item.removeAttribute("aria-current");
    });
    const state = root.querySelector("#resolution-state");
    if (state && envelope) {
      const current = steps()[activeIndex];
      state.textContent = paused
        ? `Reviewing committed turn ${envelope.turn ?? "—"} · ${current?.label ?? "resolution"} · state hash ${envelope.replay?.state_hash ?? "—"}`
        : `Playing committed turn ${envelope.turn ?? "—"} · step ${Math.min(activeIndex + 1, steps().length)} of ${steps().length} · ${current?.label ?? "resolution"}`;
    }
  }

  function stopTimer() {
    if (timer != null) globalThis.clearTimeout(timer);
    timer = null;
  }

  function setStep(index) {
    activeIndex = Math.max(0, Math.min(index, Math.max(steps().length - 1, 0)));
    updateControls();
  }

  function announceStep() {
    const entry = steps()[activeIndex];
    if (entry?.audio_cue) audio?.playCue?.(entry.audio_cue);
  }

  function tick() {
    if (paused || activeIndex >= steps().length - 1) {
      paused = true;
      stopTimer();
      updateControls();
      return;
    }
    setStep(activeIndex + 1);
    announceStep();
    timer = globalThis.setTimeout(tick, 700);
  }

  function play() {
    if (!envelope) return { ok: false, code: "resolution_missing" };
    if (reducedMotion(root)) return skip();
    paused = false;
    if (activeIndex >= steps().length - 1) activeIndex = 0;
    updateControls();
    stopTimer();
    timer = globalThis.setTimeout(tick, 700);
    announceStep();
    return { ok: true };
  }

  function pause() {
    paused = true;
    stopTimer();
    updateControls();
    return { ok: true };
  }

  function skip() {
    if (!envelope) return { ok: false, code: "resolution_missing" };
    paused = true;
    stopTimer();
    const skipped = sequenceForSkip(envelope);
    setStep(skipped.active_index);
    return { ok: true, ...skipped };
  }

  function advance() {
    if (!envelope) return { ok: false, code: "resolution_missing" };
    paused = true;
    stopTimer();
    setStep(activeIndex + 1);
    announceStep();
    return { ok: true, active_index: activeIndex, complete: activeIndex >= steps().length - 1 };
  }

  function review() {
    paused = true;
    stopTimer();
    setStep(0);
    const state = root.querySelector("#resolution-state");
    if (state && envelope) state.textContent = "Review mode: all committed resolution text remains available.";
    return { ok: true };
  }

  function render(nextEnvelope) {
    envelope = nextEnvelope;
    activeIndex = 0;
    paused = true;
    stopTimer();
    const result = renderResolution(envelope, root);
    updateControls();
    return result;
  }

  async function load(turn, sessionId = adapter?.sessionId) {
    if (!adapter || typeof adapter.getResolution !== "function") {
      return { ok: false, code: "resolution_adapter_missing" };
    }
    try {
      const nextEnvelope = await adapter.getResolution(sessionId, turn ?? null);
      if (!nextEnvelope || nextEnvelope.schema_version !== "competitive-resolution-v1") {
        throw new Error("Unsupported resolution schema.");
      }
      return render(nextEnvelope);
    } catch (error) {
      envelope = null;
      stopTimer();
      renderResolution(null, root);
      const state = root.querySelector("#resolution-state");
      if (state) state.textContent = `Resolution adapter error: ${error instanceof Error ? error.message : String(error)}`;
      return { ok: false, code: "resolution_adapter_error" };
    }
  }

  root.querySelector("#resolution-play")?.addEventListener("click", play);
  root.querySelector("#resolution-pause")?.addEventListener("click", pause);
  root.querySelector("#resolution-next")?.addEventListener("click", () => {
    advance();
  });
  root.querySelector("#resolution-skip")?.addEventListener("click", skip);
  root.querySelector("#resolution-review")?.addEventListener("click", review);
  root.querySelector("#load-resolution")?.addEventListener("click", () => {
    const input = root.querySelector("#resolution-turn");
    load(input?.value ? Number(input.value) : undefined);
  });
  return { load, render, play, pause, skip, review, advance, get envelope() { return envelope; } };
}

export function createHistoryClient({ adapter = globalThis.HsMgtGameActionAdapter, root = document, recorder = null } = {}) {
  let envelope = null;

  function failure(result, sessionId) {
    const message = result.message ?? "Live history refresh was unavailable.";
    recordPlaytestFailure(recorder, result.code, message);
    if (typeof root?.querySelector === "function") {
      setPresentationState(root, `Live history refresh failed; current view preserved: ${message}`);
      showRecovery(root, "The current history view was preserved. Retry the live history read.");
      configureRecovery(root, () => load(sessionId), recorder);
    }
    return result;
  }

  async function load(sessionId = adapter?.sessionId) {
    if (!adapter || typeof adapter.getHistory !== "function") {
      return failure({ ok: false, code: "history_adapter_missing", message: "No live history adapter configured." }, sessionId);
    }
    try {
      const nextEnvelope = await adapter.getHistory(sessionId);
      const validation = validateHistoryEnvelope(nextEnvelope);
      if (!validation.ok) return failure(validation, sessionId);
      const rendered = renderHistoryEnvelope(nextEnvelope, root);
      if (!rendered.ok) return failure(rendered, sessionId);
      envelope = nextEnvelope;
      if (typeof root?.querySelector === "function") {
        clearRecovery(root);
        setPresentationState(root, "Live history loaded from the host.");
      }
      return { ...rendered, envelope: nextEnvelope };
    } catch (error) {
      return failure({
        ok: false,
        code: "history_adapter_error",
        message: error instanceof Error ? error.message : String(error),
      }, sessionId);
    }
  }

  return { load, get envelope() { return envelope; } };
}

export function createReplayClient({ adapter = globalThis.HsMgtGameActionAdapter, root = document } = {}) {
  let envelope = null;
  let selectedIndex = -1;
  let playing = false;
  let playbackTimer = null;

  function rows() {
    return envelope?.transitions ?? [];
  }

  function renderPlayback() {
    const entries = rows();
    renderHistory(entries, root, selectedIndex);
    renderReplayPlaybackState(entries[selectedIndex], selectedIndex, entries.length, playing, root);
  }

  function stopTimer() {
    if (playbackTimer !== null) {
      clearInterval(playbackTimer);
      playbackTimer = null;
    }
  }

  function haltPlayback({ render = false } = {}) {
    stopTimer();
    playing = false;
    if (render && typeof root?.querySelector === "function" && root.querySelector("#history-list")?.replaceChildren) {
      renderPlayback();
    }
  }

  function pause() {
    haltPlayback();
    renderPlayback();
    return { ok: true, index: selectedIndex };
  }

  function select(index) {
    const entries = rows();
    if (!entries.length) {
      selectedIndex = -1;
      renderPlayback();
      return { ok: false, code: "replay_empty" };
    }
    selectedIndex = Math.max(0, Math.min(index, entries.length - 1));
    renderPlayback();
    return { ok: true, index: selectedIndex, entry: entries[selectedIndex] };
  }

  function previous() {
    return select(selectedIndex <= 0 ? 0 : selectedIndex - 1);
  }

  function next() {
    return select(selectedIndex < 0 ? 0 : selectedIndex + 1);
  }

  function play() {
    const entries = rows();
    if (!entries.length) return { ok: false, code: "replay_empty" };
    if (selectedIndex < 0 || selectedIndex >= entries.length - 1) selectedIndex = 0;
    stopTimer();
    playing = true;
    renderPlayback();
    playbackTimer = setInterval(() => {
      if (selectedIndex >= rows().length - 1) {
        pause();
        return;
      }
      selectedIndex += 1;
      renderPlayback();
    }, 900);
    return { ok: true, index: selectedIndex };
  }

  function bindControls() {
    if (typeof root?.querySelector !== "function") return;
    const controls = [
      ["#replay-previous", previous],
      ["#replay-play", play],
      ["#replay-pause", pause],
      ["#replay-next", next],
    ];
    for (const [selector, handler] of controls) {
      const button = root.querySelector(selector);
      if (typeof button?.addEventListener === "function") button.addEventListener("click", handler);
    }
  }

  bindControls();

  async function load(sessionId = adapter?.sessionId) {
    if (!adapter || typeof adapter.getReplay !== "function") {
      return { ok: false, code: "replay_adapter_missing", message: "No live replay adapter configured." };
    }
    try {
      const nextEnvelope = await adapter.getReplay(sessionId);
      const validation = validateReplayEnvelope(nextEnvelope);
      if (!validation.ok) {
        haltPlayback({ render: true });
        return validation;
      }
      const rendered = renderReplayEnvelope(nextEnvelope, root);
      if (!rendered.ok) return rendered;
      pause();
      envelope = nextEnvelope;
      selectedIndex = nextEnvelope.transitions.length ? 0 : -1;
      renderPlayback();
      return { ...rendered, envelope: nextEnvelope, index: selectedIndex };
    } catch (error) {
      haltPlayback({ render: true });
      return {
        ok: false,
        code: "replay_adapter_error",
        message: error instanceof Error ? error.message : String(error),
      };
    }
  }

  return { load, previous, next, play, pause, get envelope() { return envelope; }, get selectedIndex() { return selectedIndex; } };
}

export function createCheckpointClient({ adapter = globalThis.HsMgtGameActionAdapter, root = document, recorder = null, refresh, audio } = {}) {
  let envelope = null;
  let enabled = false;
  let busy = false;
  let operationCompletion = null;
  let autosaveQueue = Promise.resolve();

  function setEnabled(value) {
    enabled = Boolean(value);
    setCheckpointControls(root, enabled, busy);
  }

  async function save(sessionId = adapter?.sessionId, { automatic = false } = {}) {
    if (!enabled || !adapter || typeof adapter.saveSession !== "function") {
      return {
        ok: false,
        code: automatic ? "autosave_unavailable" : "save_adapter_missing",
        message: "No host checkpoint-save adapter configured.",
      };
    }
    if (busy) {
      if (automatic) {
        const message = "Host autosave was skipped because another checkpoint operation is still running.";
        recordPlaytestFailure(recorder, "checkpoint_autosave_error", message);
        sessionLaunchStatus(root, `${message} The current session remains active.`);
      }
      return { ok: false, code: automatic ? "autosave_busy" : "checkpoint_busy" };
    }
    busy = true;
    let resolveOperation;
    operationCompletion = new Promise((resolve) => {
      resolveOperation = resolve;
    });
    setCheckpointControls(root, enabled, busy);
    try {
      const nextEnvelope = await adapter.saveSession(sessionId);
      const validation = validateSaveEnvelope(nextEnvelope);
      if (!validation.ok) {
        if (automatic) {
          recordPlaytestFailure(recorder, "checkpoint_autosave_error", validation.message ?? validation.code);
          sessionLaunchStatus(root, "Host autosave returned incomplete checkpoint metadata; the current session remains active.");
        }
        return validation;
      }
      envelope = nextEnvelope;
      sessionLaunchStatus(root, automatic
        ? `Host autosave completed at ${nextEnvelope.transition_count} committed transitions.`
        : `Host checkpoint saved at ${nextEnvelope.transition_count} committed transitions.`);
      if (automatic) audio?.playCue?.("ui.save-complete");
      return { ...validation, automatic };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      const code = automatic ? "checkpoint_autosave_error" : "checkpoint_save_error";
      recordPlaytestFailure(recorder, code, message);
      sessionLaunchStatus(root, `${automatic ? "Host autosave" : "Checkpoint save"} failed; the current session remains active: ${message}`);
      return { ok: false, code, message };
    } finally {
      busy = false;
      resolveOperation?.();
      operationCompletion = null;
      setCheckpointControls(root, enabled, busy);
    }
  }

  function autosave(sessionId = adapter?.sessionId) {
    if (!enabled || !adapter || typeof adapter.saveSession !== "function") {
      return Promise.resolve({
        ok: false,
        code: "autosave_unavailable",
        message: "No host checkpoint-save adapter configured.",
      });
    }
    const request = autosaveQueue.then(async () => {
      if (busy && operationCompletion) await operationCompletion;
      return save(sessionId, { automatic: true });
    });
    autosaveQueue = request.then(() => undefined, () => undefined);
    return request;
  }

  async function load(sessionId = adapter?.sessionId) {
    if (!enabled || !adapter || typeof adapter.loadSession !== "function") {
      return { ok: false, code: "load_adapter_missing", message: "No host checkpoint-restore adapter configured." };
    }
    if (busy) return { ok: false, code: "checkpoint_busy" };
    busy = true;
    let resolveOperation;
    operationCompletion = new Promise((resolve) => {
      resolveOperation = resolve;
    });
    setCheckpointControls(root, enabled, busy);
    try {
      const nextEnvelope = await adapter.loadSession(sessionId);
      const validation = validateSaveEnvelope(nextEnvelope);
      if (!validation.ok) return validation;
      const refreshed = typeof refresh === "function" ? await refresh(sessionId) : { ok: true };
      if (!refreshed.ok) {
        recordPlaytestFailure(recorder, "checkpoint_refresh_error", refreshed.message ?? "Restored checkpoint could not be refreshed.");
        showRecovery(root, "The host checkpoint was restored, but the current presentation could not be refreshed. Retry the current read.");
        return { ok: false, code: "checkpoint_refresh_error", message: refreshed.message, envelope: nextEnvelope };
      }
      envelope = nextEnvelope;
      clearRecovery(root);
      sessionLaunchStatus(root, `Host checkpoint restored at ${nextEnvelope.transition_count} committed transitions.`);
      return { ...validation, envelope: nextEnvelope, refreshed: refreshed.envelope ?? refreshed };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      recordPlaytestFailure(recorder, "checkpoint_load_error", message);
      sessionLaunchStatus(root, `Checkpoint restore failed; the current session remains active: ${message}`);
      showRecovery(root, `Checkpoint restore failed: ${message}`);
      return { ok: false, code: error?.code === "checkpoint_missing" ? "checkpoint_missing" : "checkpoint_load_error", message };
    } finally {
      busy = false;
      resolveOperation?.();
      operationCompletion = null;
      setCheckpointControls(root, enabled, busy);
    }
  }

  root.querySelector("#session-save")?.addEventListener("click", () => save());
  root.querySelector("#session-restore")?.addEventListener("click", () => load());
  setCheckpointControls(root, false);
  return {
    save,
    autosave,
    load,
    setEnabled,
    get envelope() { return envelope; },
  };
}

export function renderPresentation(envelope, root = document) {
  const fixture = envelope.presentation_fixture;
  currentRegionalLinks = [];
  briefingFocusEntityId = null;
  const presentationSessionId = envelope.session?.session_id;
  if (!presentationSessionId || (currentResolutionSessionId && presentationSessionId !== currentResolutionSessionId)) {
    currentResolutionLinks = [];
    currentResolutionSessionId = null;
  }
  renderConsequenceLinks(currentResolutionLinks, root);
  if (!fixture) {
    renderMetricList([], root);
    renderBriefing([], root);
    renderMap([], root);
    renderSelectedEntity([], root);
    renderActions([], root);
    renderPending([], root);
    renderMonthlyResult(null, root);
    renderRegionalBoard(null, root);
    return;
  }
  const entityIds = new Set((fixture.entities ?? []).map((entity) => entity.id));
  if (!entityIds.has(selectedEntityId)) {
    selectedEntityId = fixture.selected_entity_id ?? fixture.entities?.[0]?.id;
  }
  selectedBoardId = selectedEntityId;
  renderMetricList(fixture.header_metrics, root);
  renderBriefing(fixture.briefing, root);
  renderMap(fixture.entities, root);
  renderSelectedEntity(fixture.entities, root);
  renderRegionalBoard(presentationFixtureToSceneData(fixture), root);
  renderActions(fixture.actions, root);
  renderPending(fixture.pending, root);
  renderMonthlyResult(fixture.monthly_result, root);
}

export function validateCommand(command, legalCommands) {
  if (!String(command ?? "").trim()) {
    return { ok: false, message: "Enter a command first." };
  }
  if (!Array.isArray(legalCommands) || legalCommands.length === 0) {
    return { ok: false, message: "No legal command surface is available." };
  }
  return {
    ok: true,
    message: "Command ready; the MCP adapter remains authoritative for validation.",
  };
}

export function renderEnvelope(envelope, root = document) {
  const observationList = root.querySelector("#observation-list");
  const commandList = root.querySelector("#legal-command-list");
  const historyList = root.querySelector("#history-list");
  const debriefList = root.querySelector("#debrief-list");
  const meta = root.querySelector("#session-meta");

  observationList.replaceChildren();
  commandList.replaceChildren();
  historyList.replaceChildren();
  debriefList.replaceChildren();

  for (const line of envelope.observation ?? []) appendText(observationList, line);
  if (!envelope.observation?.length) emptyState(observationList, "No observation available.");

  for (const command of envelope.legal_commands ?? []) {
    const item = document.createElement("li");
    item.textContent = String(command);
    commandList.append(item);
  }
  if (!envelope.legal_commands?.length) emptyState(commandList, "No legal commands available.");

  renderHistory(envelope.history, root);

  for (const line of envelope.debrief ?? []) {
    const item = document.createElement("li");
    item.textContent = String(line);
    debriefList.append(item);
  }
  if (!envelope.debrief?.length) emptyState(debriefList, "Debrief becomes available after a committed session.");

  if (meta) meta.textContent = `${envelope.campaign ?? "session"} · turn ${envelope.turn ?? "—"}/${envelope.max_turns ?? "—"}`;
  setReadOnlyControls(root, false);
  renderPresentation(envelope, root);
}

export function createThinClient({ adapter = globalThis.HsMgtGameAdapter, root = document } = {}) {
  let currentEnvelope = null;

  function render(envelope) {
    currentEnvelope = envelope;
    renderEnvelope(envelope, root);
    return envelope;
  }

  async function submit(command) {
    const validation = validateCommand(command, currentEnvelope?.legal_commands);
    const status = root.querySelector("#command-status");
    if (!validation.ok) {
      if (status) status.textContent = validation.message;
      return { ok: false, code: "client_input" };
    }
    if (!adapter || typeof adapter.submitTurn !== "function") {
      const message = "No MCP adapter configured; no transition was attempted.";
      if (status) status.textContent = message;
      return { ok: false, code: "adapter_missing" };
    }
    const nextEnvelope = await adapter.submitTurn(command);
    render(nextEnvelope);
    if (status) status.textContent = "Committed response received from the MCP adapter.";
    return { ok: true, envelope: nextEnvelope };
  }

  return { render, submit, get envelope() { return currentEnvelope; } };
}

if (typeof document !== "undefined") {
  document.__hsMgtWorkspace = createWorkspaceController({ root: document, initialWorkspace: "setup" });
  renderAssetCredits({ root: document });
  const actionAdapter = globalThis.HsMgtGameActionAdapter;
  if (actionAdapter) {
    const client = createActionClient({ root: document });
    const storedSessionId = client.sessionStore.get();
    const initialSessionId = actionAdapter.sessionId || storedSessionId;
    if (initialSessionId) {
      if (!actionAdapter.sessionId) {
        sessionLaunchStatus(document, `Recovering host session ${initialSessionId} after browser refresh…`);
      }
      client.load(initialSessionId, { automaticResume: !actionAdapter.sessionId && Boolean(storedSessionId) }).then((result) => {
        if (!result?.ok && isUnknownSessionResult(result)) {
          client.sessionStore.clear();
          sessionLaunchStatus(document, "The stored host session is no longer available; start or load a current session.");
        }
      });
    } else {
      renderEnvelope(demoEnvelope, document);
      setPresentationState(document, "Demo fixture loaded; start a host session to play");
    }
    globalThis.HsMgtGui = {
      client,
      AUDIO_CATALOG,
      ASSET_CREDITS,
      VISUAL_CATALOG,
      CAMPAIGN_COVERAGE_FLOW_SCHEMA,
      FIRST_MONTH_FLOW_SCHEMA,
      PLAYTEST_CAPTURE_SCHEMA,
      WORKSPACE_IDS,
      DEFAULT_VISIBLE_COUNTS,
      workspaceForEvent,
      createWorkspaceController,
      createPlaytestRecorder,
      createAudioClient,
      createActionClient,
      createSessionIdStorage,
      ACTIVE_SESSION_STORAGE_KEY,
      createCampaignCoverageClient,
      createSessionLauncher,
      createPresentationSettings,
      renderAssetCredits,
      createRegionalWorldClient,
      createResolutionClient,
      createHistoryClient,
      createReplayClient,
      createCheckpointClient,
      CHECKPOINT_REFERENCE_SCHEMA,
      validateCheckpointDiscoveryEnvelope,
      validateCheckpointReference,
      serializeCheckpointReference,
      parseCheckpointReference,
      downloadCheckpointReference,
      importCheckpointReference,
      downloadHostCheckpointArtifact,
      renderCheckpointDiscovery,
      createReadOnlyClient,
      createThinClient,
      campaignMusicStateId,
      campaignAudioCueIds,
      renderEnvelope,
      renderPresentation,
      renderReadOnlyEnvelope,
      renderEndSessionEnvelope,
      renderResolution,
      renderRegionalWorld,
      renderCampaignCoverage,
      validateCommand,
      validateReadOnlyEnvelope,
      validateEndSessionEnvelope,
      validateHistoryEnvelope,
      renderHistoryEnvelope,
      validateReplayEnvelope,
      renderReplayEnvelope,
      validateSaveEnvelope,
    };
  } else {
    const client = createReadOnlyClient({ root: document });
    client.load();
    globalThis.HsMgtGui = {
      client,
      AUDIO_CATALOG,
      ASSET_CREDITS,
      VISUAL_CATALOG,
      CAMPAIGN_COVERAGE_FLOW_SCHEMA,
      FIRST_MONTH_FLOW_SCHEMA,
      PLAYTEST_CAPTURE_SCHEMA,
      WORKSPACE_IDS,
      DEFAULT_VISIBLE_COUNTS,
      workspaceForEvent,
      createWorkspaceController,
      createPlaytestRecorder,
      createAudioClient,
      createActionClient,
      createSessionIdStorage,
      ACTIVE_SESSION_STORAGE_KEY,
      createCampaignCoverageClient,
      createSessionLauncher,
      createPresentationSettings,
      renderAssetCredits,
      createRegionalWorldClient,
      createResolutionClient,
      createHistoryClient,
      createReplayClient,
      createCheckpointClient,
      createReadOnlyClient,
      createThinClient,
      campaignMusicStateId,
      campaignAudioCueIds,
      renderEnvelope,
      renderPresentation,
      renderReadOnlyEnvelope,
      renderEndSessionEnvelope,
      renderResolution,
      renderRegionalWorld,
      renderCampaignCoverage,
      validateCommand,
      validateReadOnlyEnvelope,
      validateEndSessionEnvelope,
      validateHistoryEnvelope,
      renderHistoryEnvelope,
      validateReplayEnvelope,
      renderReplayEnvelope,
      validateSaveEnvelope,
    };
  }
}

export {
  demoEnvelope,
  presentationFixture,
  CAMPAIGN_COVERAGE_SCHEMA,
  END_SESSION_SCHEMA,
  HISTORY_SCHEMA,
  REPLAY_SCHEMA,
  SAVE_SCHEMA,
  PLAYTEST_CAPTURE_SCHEMA,
  READ_ONLY_PRESENTATION_SCHEMA,
  regionalEntitiesToFixture,
};
