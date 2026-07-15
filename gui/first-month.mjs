export const FIRST_MONTH_FLOW_SCHEMA = "competitive-first-month-v1";

export const FIRST_MONTH_STAGES = Object.freeze([
  Object.freeze({
    id: "start",
    label: "Start or load",
    detail: "Use the host to start a competitive session or load an existing session.",
  }),
  Object.freeze({
    id: "inspect",
    label: "Inspect the visible market",
    detail: "Review the briefing, Riverside, facilities, workforce, capacity, payer, and public rival signals.",
  }),
  Object.freeze({
    id: "draft",
    label: "Draft contextual actions",
    detail: "Choose host-catalogued actions and revise or remove local drafts before validation.",
  }),
  Object.freeze({
    id: "validate",
    label: "Review and validate",
    detail: "Review at least two draft commands, costs, delays, constraints, and uncertainty through the host.",
  }),
  Object.freeze({
    id: "submit",
    label: "Submit the unchanged batch",
    detail: "Submit only the batch that the host marked valid; no local outcome is promised.",
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
]);

const DEFAULT_STATE = Object.freeze({
  sessionLoaded: false,
  actionCatalogLoaded: false,
  draftCount: 0,
  validated: false,
  submitted: false,
  resolutionVisible: false,
  refreshed: false,
});

function safeDraftCount(value) {
  return Number.isInteger(value) && value > 0 ? value : 0;
}

export function firstMonthStageFor(state = {}) {
  const draftCount = safeDraftCount(state.draftCount);
  if (!state.sessionLoaded) return "start";
  if (!state.actionCatalogLoaded) return "inspect";
  if (state.submitted) {
    if (!state.resolutionVisible || !state.refreshed) return "resolution";
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

export function createFirstMonthFlow({ root = globalThis.document } = {}) {
  let state = { ...DEFAULT_STATE };

  function render() {
    const list = root?.querySelector?.("#first-month-flow-list");
    const currentNode = root?.querySelector?.("#first-month-flow-state");
    const detailNode = root?.querySelector?.("#first-month-flow-detail");
    const stageId = firstMonthStageFor(state);
    const currentIndex = FIRST_MONTH_STAGES.findIndex((stage) => stage.id === stageId);
    const current = FIRST_MONTH_STAGES[currentIndex] ?? FIRST_MONTH_STAGES[0];
    if (currentNode) currentNode.textContent = `${current.label} · ${currentIndex + 1} of ${FIRST_MONTH_STAGES.length}`;
    if (detailNode) detailNode.textContent = `${current.detail} This rail reports presentation handoffs; the host owns commands and outcomes.`;
    if (!list) return { ok: false, code: "first_month_flow_surface_missing", stage: current };

    list.replaceChildren();
    FIRST_MONTH_STAGES.forEach((stage, index) => {
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
    get stage() { return FIRST_MONTH_STAGES.find((stage) => stage.id === firstMonthStageFor(state)) ?? FIRST_MONTH_STAGES[0]; },
  };
}
