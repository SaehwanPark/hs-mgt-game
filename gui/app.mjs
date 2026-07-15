const presentationFixture = {
  header_metrics: [
    { label: "Month", value: "Year 1 · January" },
    { label: "Cash", value: "60 units" },
    { label: "Monthly margin", value: "+12 units" },
    { label: "Action points", value: "3 AP" },
    { label: "Political capital", value: "10" },
    { label: "Workforce trust", value: "Moderate" },
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

let selectedEntityId = null;

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

function createStatus(status, label) {
  const node = document.createElement("span");
  node.className = `status status--${status ?? "uncertain"}`;
  node.textContent = label ?? status ?? "Uncertain";
  return node;
}

function appendSource(parent, source) {
  if (!source) return;
  const node = document.createElement("small");
  node.className = "source";
  node.textContent = `Source: ${source}`;
  parent.append(node);
}

function renderMetricList(metrics, root) {
  const list = root.querySelector("#header-metrics");
  list.replaceChildren();
  for (const metric of metrics ?? []) {
    const item = document.createElement("div");
    item.className = "metric";
    const label = document.createElement("dt");
    label.textContent = String(metric.label ?? "Metric");
    const value = document.createElement("dd");
    value.textContent = String(metric.value ?? "Unavailable");
    item.append(label, value);
    list.append(item);
  }
  if (!metrics?.length) emptyState(list, "No executive metrics available.");
}

function renderBriefing(items, root) {
  const list = root.querySelector("#briefing-list");
  list.replaceChildren();
  for (const entry of items ?? []) {
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
    appendSource(item, entry.source);
    list.append(item);
  }
  if (!items?.length) emptyState(list, "No briefing items available.");
}

function renderMap(entities, root) {
  const list = root.querySelector("#map-list");
  list.replaceChildren();
  for (const entity of entities ?? []) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "entity-card";
    card.dataset.entityId = entity.id;
    card.setAttribute("aria-current", entity.id === selectedEntityId ? "true" : "false");
    const icon = document.createElement("span");
    icon.className = "entity-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.textContent = entity.icon ?? "◆";
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
      renderMap(entities, root);
      renderSelectedEntity(entities, root);
    });
    list.append(card);
  }
  if (!entities?.length) emptyState(list, "No regional institutions available.");
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
  const icon = document.createElement("span");
  icon.className = "entity-icon";
  icon.setAttribute("aria-hidden", "true");
  icon.textContent = entity.icon ?? "◆";
  const title = document.createElement("h3");
  title.textContent = String(entity.name);
  heading.append(icon, title, createStatus(entity.status, entity.status_label));
  const summary = document.createElement("p");
  summary.className = "detail-summary";
  summary.textContent = String(entity.summary ?? "No visible summary available.");
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
    const kind = document.createElement("small");
    kind.className = "source";
    kind.textContent = `${facility.icon ?? "▥"} ${facility.kind ?? "Facility"}`;
    const detailText = document.createElement("p");
    detailText.textContent = String(facility.detail ?? "No visible facility detail.");
    item.append(row, kind, detailText);
    facilities.append(item);
  }
  if (!entity.facilities?.length) emptyState(facilities, "No visible facility detail available.");
  detail.append(heading, summary, metrics, facilitiesHeading, facilities);
}

function renderActions(actions, root) {
  const list = root.querySelector("#action-preview-list");
  list.replaceChildren();
  for (const action of actions ?? []) {
    const item = document.createElement("article");
    item.className = "action-card";
    const heading = document.createElement("div");
    heading.className = "action-heading";
    const title = document.createElement("strong");
    title.textContent = String(action.label ?? "Action preview");
    heading.append(title, createStatus("uncertain", "Preview"));
    const command = document.createElement("p");
    command.className = "command-preview";
    command.textContent = String(action.command ?? "Canonical command unavailable");
    const meta = document.createElement("div");
    meta.className = "action-meta";
    for (const value of [action.cost, action.delay, action.constraint]) {
      const line = document.createElement("span");
      line.textContent = String(value ?? "Unavailable");
      meta.append(line);
    }
    const uncertainty = document.createElement("p");
    uncertainty.textContent = String(action.uncertainty ?? "Realized outcome remains uncertain.");
    item.append(heading, command, meta, uncertainty);
    appendSource(item, action.source);
    list.append(item);
  }
  if (!actions?.length) emptyState(list, "No contextual action previews available.");
}

function renderPending(items, root) {
  const list = root.querySelector("#pending-list");
  list.replaceChildren();
  for (const entry of items ?? []) {
    const item = document.createElement("li");
    item.className = "timeline-item";
    const row = document.createElement("div");
    row.className = "timeline-row";
    const title = document.createElement("strong");
    title.textContent = String(entry.title ?? "Pending process");
    row.append(title, createStatus(entry.status, entry.status_label));
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

export function renderPresentation(envelope, root = document) {
  const fixture = envelope.presentation_fixture;
  if (!fixture) {
    renderMetricList([], root);
    renderBriefing([], root);
    renderMap([], root);
    renderSelectedEntity([], root);
    renderActions([], root);
    renderPending([], root);
    renderMonthlyResult(null, root);
    return;
  }
  selectedEntityId = selectedEntityId ?? fixture.selected_entity_id ?? fixture.entities?.[0]?.id;
  renderMetricList(fixture.header_metrics, root);
  renderBriefing(fixture.briefing, root);
  renderMap(fixture.entities, root);
  renderSelectedEntity(fixture.entities, root);
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

  for (const entry of envelope.history ?? []) {
    const item = document.createElement("li");
    item.className = "history-item";
    const turn = document.createElement("strong");
    turn.textContent = `Turn ${entry.turn ?? "—"}`;
    const command = document.createElement("span");
    command.textContent = String(entry.command ?? "—");
    const hash = document.createElement("span");
    hash.className = "hash";
    hash.textContent = `state hash: ${entry.state_hash ?? "—"}`;
    item.append(turn, command, hash);
    historyList.append(item);
  }
  if (!envelope.history?.length) emptyState(historyList, "No committed transitions yet.");

  for (const line of envelope.debrief ?? []) {
    const item = document.createElement("li");
    item.textContent = String(line);
    debriefList.append(item);
  }
  if (!envelope.debrief?.length) emptyState(debriefList, "Debrief becomes available after a committed session.");

  if (meta) meta.textContent = `${envelope.campaign ?? "session"} · turn ${envelope.turn ?? "—"}/${envelope.max_turns ?? "—"}`;
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
  const client = createThinClient({ root: document });
  client.render(demoEnvelope);
  document.querySelector("#command-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const input = document.querySelector("#command-input");
    await client.submit(input.value);
    input.value = "";
  });
  globalThis.HsMgtGui = { client, createThinClient, renderEnvelope, renderPresentation, validateCommand };
}

export { demoEnvelope, presentationFixture };
