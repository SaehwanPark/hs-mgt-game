export const FIRST_MONTH_FLOW_SCHEMA = "competitive-first-month-v1";
export const CAMPAIGN_COVERAGE_FLOW_SCHEMA = "campaign-coverage-first-session-v1";

const TERMINAL_STAGE = Object.freeze({
  id: "terminal",
  label: "Review the final debrief",
  detail: "The host session ended; review committed history and debrief text before starting another session.",
});

export const FIRST_MONTH_STAGES = Object.freeze([
  Object.freeze({
    id: "start",
    label: "Start or load",
    detail: "Use the host to start a competitive session or load an existing session.",
  }),
  Object.freeze({
    id: "inspect",
    label: "Inspect the visible market",
    detail: "Review the visible briefing and market signals.",
  }),
  Object.freeze({
    id: "draft",
    label: "Build your plan",
    detail: "Choose actions and adjust your plan before checking it.",
  }),
  Object.freeze({
    id: "validate",
    label: "Check your plan",
    detail: "Ask the host to check the current plan.",
  }),
  Object.freeze({
    id: "submit",
    label: "Commit month",
    detail: "Commit the plan the host marked valid.",
  }),
  Object.freeze({
    id: "resolution",
    label: "Review monthly resolution",
    detail: "Read or skip the committed resolution, direct effects, pending processes, and refreshed observation.",
  }),
  Object.freeze({
    id: "continue",
    label: "Continue to the next observation",
    detail: "The next actor-visible observation is ready; the host remains authoritative for what changed.",
  }),
  TERMINAL_STAGE,
]);

export const CAMPAIGN_COVERAGE_STAGES = Object.freeze([
  Object.freeze({
    id: "start",
    label: "Start or load",
    detail: "Use the host to start a stabilization or regional-affiliation session, or load an existing session.",
  }),
  Object.freeze({
    id: "inspect",
    label: "Inspect campaign coverage",
    detail: "Review the visible briefing, stage, and signals.",
  }),
  Object.freeze({
    id: "choose",
    label: "Choose an action",
    detail: "Select one visible campaign action.",
  }),
  Object.freeze({
    id: "review",
    label: "Review the committed stage",
    detail: "Read the refreshed host envelope, visible consequences, history, and any campaign debrief text.",
  }),
  Object.freeze({
    id: "continue",
    label: "Continue to the next stage",
    detail: "The next actor-visible campaign observation is ready; the host remains authoritative for what changed.",
  }),
  TERMINAL_STAGE,
]);

const DEFAULT_STATE = Object.freeze({
  flow: "competitive",
  sessionLoaded: false,
  actionCatalogLoaded: false,
  coverageLoaded: false,
  draftCount: 0,
  validated: false,
  submitted: false,
  resolutionVisible: false,
  refreshed: false,
  briefingReviewed: false,
  resolutionReviewed: false,
  sessionDone: false,
});

function safeDraftCount(value) {
  return Number.isInteger(value) && value > 0 ? value : 0;
}

export function firstMonthStageFor(state = {}) {
  if (state.sessionDone) return "terminal";
  if (state.flow === "campaign-coverage") {
    if (!state.sessionLoaded) return "start";
    if (!state.coverageLoaded || !state.briefingReviewed) return "inspect";
    if (!state.decisionSubmitted) return "choose";
    if (!state.refreshed || !state.resolutionReviewed) return "review";
    return "continue";
  }
  const draftCount = safeDraftCount(state.draftCount);
  if (!state.sessionLoaded) return "start";
  if (!state.actionCatalogLoaded || !state.briefingReviewed) return "inspect";
  if (state.submitted) {
    if (!state.resolutionVisible || !state.refreshed || !state.resolutionReviewed) return "resolution";
    return "continue";
  }
  if (draftCount < 2) return "draft";
  if (!state.validated) return "validate";
  return "submit";
}

function createElement(root, tagName) {
  return (root?.ownerDocument ?? root ?? globalThis.document)?.createElement?.(tagName) ?? null;
}

function stageState(index, currentIndex) {
  if (index < currentIndex) return "completed";
  if (index === currentIndex) return "current";
  return "upcoming";
}

function stageMarker(state) {
  if (state === "completed") return "Done";
  if (state === "current") return "Current";
  return "Next";
}

function stagesFor(state) {
  return state.flow === "campaign-coverage" ? CAMPAIGN_COVERAGE_STAGES : FIRST_MONTH_STAGES;
}

export function createFirstMonthFlow({ root = globalThis.document } = {}) {
  let state = { ...DEFAULT_STATE };

  function render() {
    const list = root?.querySelector?.("#first-month-flow-list");
    const currentNode = root?.querySelector?.("#first-month-flow-state");
    const detailNode = root?.querySelector?.("#first-month-flow-detail");
    const continueButton = root?.querySelector?.("#briefing-continue");
    const stageId = firstMonthStageFor(state);
    const stages = stagesFor(state);
    const currentIndex = stages.findIndex((stage) => stage.id === stageId);
    const current = stages[currentIndex] ?? stages[0];
    if (currentNode) currentNode.textContent = `${current.label} · ${currentIndex + 1} of ${stages.length}`;
    if (detailNode) detailNode.textContent = current.detail;
    if (continueButton) {
      const ready = Boolean(state.sessionLoaded) && stageId === "inspect";
      continueButton.hidden = !ready;
      continueButton.disabled = !ready;
      continueButton.textContent = state.flow === "campaign-coverage" ? "Choose an action" : "Build your plan";
    }
    if (!list) return { ok: false, code: "first_month_flow_surface_missing", stage: current };

    list.replaceChildren();
    stages.forEach((stage, index) => {
      const item = createElement(root, "li");
      const marker = createElement(root, "span");
      const label = createElement(root, "strong");
      const detail = createElement(root, "p");
      if (!item || !marker || !label || !detail) return;
      const status = stageState(index, currentIndex);
      item.className = `first-month-flow-item first-month-flow-item--${status}`;
      item.dataset.stepId = stage.id;
      item.dataset.state = status;
      if (status === "current") item.setAttribute("aria-current", "step");
      marker.className = "first-month-flow-marker";
      marker.textContent = stageMarker(status);
      marker.setAttribute("aria-hidden", "true");
      label.textContent = stage.label;
      detail.textContent = stage.detail;
      item.append(marker, label, detail);
      list.append(item);
    });
    return { ok: true, stage: current, state: { ...state } };
  }

  function update(patch = {}) {
    state = { ...state, ...patch, draftCount: safeDraftCount(patch.draftCount ?? state.draftCount) };
    return render();
  }

  render();
  return {
    update,
    render,
    get state() { return Object.freeze({ ...state }); },
    get stage() { return stagesFor(state).find((stage) => stage.id === firstMonthStageFor(state)) ?? stagesFor(state)[0]; },
  };
}
