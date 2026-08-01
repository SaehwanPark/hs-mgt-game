export const WORKSPACE_IDS = Object.freeze([
  "setup",
  "brief",
  "decide",
  "resolve",
  "review",
]);

export const DEFAULT_VISIBLE_COUNTS = Object.freeze({
  signals: 3,
  actors: 3,
  processes: 3,
  actions: 6,
  history: 5,
});

const EVENT_WORKSPACES = Object.freeze({
  session_missing: "setup",
  setup: "setup",
  session_started: "brief",
  session_loaded: "brief",
  briefing_ready: "brief",
  briefing_reviewed: "decide",
  decision_requested: "decide",
  transition_committed: "resolve",
  resolution_loaded: "resolve",
  resolution_continued: "brief",
  session_ended: "review",
  terminal_review: "review",
});

function normalizeWorkspace(value, fallback = "brief") {
  return WORKSPACE_IDS.includes(value) ? value : fallback;
}

export function workspaceForEvent(event = {}, fallback = "brief") {
  const type = typeof event === "string" ? event : event?.type ?? event?.event;
  if (type === "session_loaded" && (event?.done === true || event?.session?.done === true)) {
    return "review";
  }
  return EVENT_WORKSPACES[type] ?? normalizeWorkspace(fallback, "brief");
}

function queryAll(root, selector) {
  return root?.querySelectorAll?.(selector) ?? [];
}

function focusTarget(node) {
  const target = node?.querySelector?.("[data-workspace-heading], h1, h2, h3, [tabindex='-1']") ?? node;
  target?.focus?.({ preventScroll: true });
}

function setDialogOpen(dialog, open) {
  if (!dialog) return;
  if (open) {
    if (typeof dialog.showModal === "function" && !dialog.open) dialog.showModal();
    else dialog.open = true;
    dialog.hidden = false;
  } else {
    if (typeof dialog.close === "function" && dialog.open) dialog.close();
    else dialog.open = false;
    dialog.hidden = false;
  }
}

export function createWorkspaceController({
  root = globalThis.document,
  initialWorkspace = "setup",
} = {}) {
  let activeWorkspace = normalizeWorkspace(initialWorkspace, "setup");
  let lastFocus = null;
  const subscribers = new Set();

  function sync() {
    for (const node of queryAll(root, "[data-workspace]")) {
      const visible = node.dataset.workspace === activeWorkspace;
      node.hidden = !visible;
      node.setAttribute?.("aria-hidden", String(!visible));
    }
    for (const node of queryAll(root, "[data-workspace-area]")) {
      const areas = String(node.dataset.workspaceArea ?? "").split(/\s+/).filter(Boolean);
      const visible = areas.includes(activeWorkspace);
      node.hidden = !visible;
      node.setAttribute?.("aria-hidden", String(!visible));
    }
    for (const node of queryAll(root, "[data-workspace-areas]")) {
      const ready = node.dataset.workspaceReady !== "false";
      const areas = String(node.dataset.workspaceAreas ?? "").split(/\s+/).filter(Boolean);
      if (ready && areas.length) node.hidden = !areas.includes(activeWorkspace);
    }
    for (const node of queryAll(root, "[data-workspace-nav]")) {
      const current = node.dataset.workspaceTarget === activeWorkspace;
      if (current) node.setAttribute?.("aria-current", "page");
      else node.removeAttribute?.("aria-current");
    }
  }

  function notify(detail) {
    for (const subscriber of subscribers) subscriber(detail);
  }

  function setWorkspace(nextWorkspace, { focus = true, reason = "navigation" } = {}) {
    const next = normalizeWorkspace(nextWorkspace, activeWorkspace);
    const previous = activeWorkspace;
    if (focus) lastFocus = root?.activeElement ?? lastFocus;
    activeWorkspace = next;
    sync();
    if (focus) {
      const target = root?.querySelector?.(`[data-workspace="${next}"]`);
      focusTarget(target);
    }
    notify({ workspace: next, previous, reason });
    return { ok: true, workspace: next, previous, changed: previous !== next };
  }

  function goForEvent(event, options = {}) {
    return setWorkspace(workspaceForEvent(event, activeWorkspace), options);
  }

  function subscribe(listener) {
    if (typeof listener !== "function") return () => {};
    subscribers.add(listener);
    return () => subscribers.delete(listener);
  }

  function closeDialog(dialog) {
    setDialogOpen(dialog, false);
    lastFocus?.focus?.({ preventScroll: true });
    lastFocus = null;
  }

  function openDialog(dialog, opener = null) {
    lastFocus = opener ?? root?.activeElement ?? lastFocus;
    setDialogOpen(dialog, true);
    focusTarget(dialog);
    return Boolean(dialog);
  }

  for (const button of queryAll(root, "[data-workspace-target]")) {
    button.addEventListener?.("click", (event) => {
      event.preventDefault?.();
      const reason = button.dataset.workspaceReason ?? "navigation";
      setWorkspace(button.dataset.workspaceTarget, { reason });
    });
  }

  for (const button of queryAll(root, "[data-dialog-target]")) {
    button.addEventListener?.("click", () => {
      const dialog = root?.querySelector?.(`#${button.dataset.dialogTarget}`);
      openDialog(dialog, button);
    });
  }
  for (const button of queryAll(root, "[data-dialog-close]")) {
    button.addEventListener?.("click", () => {
      closeDialog(button.closest?.("dialog"));
    });
  }
  for (const dialog of queryAll(root, "dialog")) {
    dialog.addEventListener?.("cancel", (event) => {
      event.preventDefault?.();
      closeDialog(dialog);
    });
    dialog.addEventListener?.("click", (event) => {
      if (event.target === dialog && dialog.dataset.closeOnBackdrop === "true") closeDialog(dialog);
    });
  }

  sync();
  return {
    get activeWorkspace() { return activeWorkspace; },
    get lastFocus() { return lastFocus; },
    setWorkspace,
    goTo: setWorkspace,
    goForEvent,
    subscribe,
    sync,
    openDialog,
    closeDialog,
    visibleWorkspaces: () => WORKSPACE_IDS.filter((id) => id === activeWorkspace),
  };
}
