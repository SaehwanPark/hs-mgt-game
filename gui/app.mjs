import { AUDIO_CATALOG, createAudioClient, visibleEventCues } from "./audio.mjs";

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

const READ_ONLY_PRESENTATION_SCHEMA = "competitive-read-only-v1";
const REGIONAL_WORLD_SCHEMA = "competitive-regional-world-v1";
const CAMPAIGN_COVERAGE_SCHEMA = "campaign-coverage-v1";
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

function setPresentationState(root, message) {
  setStatus(root, message);
  const node = root.querySelector("#presentation-state");
  if (node) node.textContent = message;
}

function setReadOnlyControls(root, readOnly) {
  const form = root.querySelector("#command-form");
  if (form) form.hidden = readOnly;
  const commands = root.querySelector("#legal-command-list");
  if (readOnly && commands) {
    commands.replaceChildren();
    emptyState(commands, "Action submission is deferred to Phase 3.");
  }
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
  if (entity.processes || entity.missing) {
    const processHeading = document.createElement("h3");
    processHeading.textContent = "Visible processes";
    const processes = document.createElement("ul");
    processes.className = "facility-list";
    for (const process of entity.processes ?? []) {
      const item = document.createElement("li");
      item.className = "facility-card";
      const title = document.createElement("strong");
      title.textContent = String(process.label ?? "Visible process");
      const processDetail = document.createElement("p");
      processDetail.textContent = String(process.detail ?? "No visible process detail.");
      item.append(title, processDetail);
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
    facilities: (entity.facilities ?? []).map((facility) => ({
      icon: "▥",
      name: facility.name,
      kind: facility.kind,
      status: entity.status,
      status_label: entity.status_label,
      detail: (facility.metrics ?? []).map((metric) => `${metric.label}: ${metric.value}`).join(" · ") || "No visible facility metric.",
    })),
    processes: (entity.processes ?? []).map((process) => ({
      label: process.label,
      detail: process.detail,
      source: process.source,
    })),
    missing: missingByEntity.get(entity.id) ?? [],
  }));
}

function renderRegionalOverlays(overlays, root) {
  const list = root.querySelector("#regional-overlay-list");
  if (!list) return;
  list.replaceChildren();
  for (const overlay of overlays ?? []) {
    const item = document.createElement("li");
    const heading = document.createElement("strong");
    heading.textContent = String(overlay.label ?? "Visible overlay");
    const value = document.createElement("span");
    value.textContent = `${overlay.value ?? "Unavailable"} ${overlay.unit ?? ""}`.trim();
    const equivalent = document.createElement("p");
    equivalent.textContent = String(overlay.equivalent ?? "Visible source-linked overlay.");
    item.append(heading, value, equivalent);
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

function campaignAudioInput(envelope) {
  return {
    done: envelope?.session?.done,
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
  list.replaceChildren();
  for (const entry of items ?? []) {
    const item = document.createElement("li");
    const title = document.createElement("strong");
    title.textContent = String(entry.title ?? entry.kind ?? "Briefing");
    const detail = document.createElement("p");
    detail.textContent = String(entry.detail ?? "No visible campaign detail.");
    item.append(title, detail);
    appendSource(item, entry.source);
    list.append(item);
  }
  if (!items?.length) emptyState(list, "No campaign briefing is available.");
}

function renderCampaignCoverageMetrics(metrics, root) {
  const list = root.querySelector("#campaign-metric-list");
  if (!list) return;
  list.replaceChildren();
  for (const metric of metrics ?? []) {
    const item = document.createElement("div");
    const label = document.createElement("dt");
    label.textContent = String(metric.label ?? "Metric");
    const value = document.createElement("dd");
    value.textContent = `${metric.value ?? "Unavailable"} ${metric.unit ?? ""}`.trim();
    item.append(label, value);
    appendSource(item, `${metric.source ?? "Visible campaign source"} · ${metric.equivalent ?? "Written equivalent"}`);
    list.append(item);
  }
  if (!metrics?.length) emptyState(list, "No visible campaign metrics are available.");
}

function renderCampaignCoverageActors(actors, root) {
  const list = root.querySelector("#campaign-actor-list");
  if (!list) return;
  list.replaceChildren();
  for (const actor of actors ?? []) {
    const item = document.createElement("li");
    item.className = "campaign-actor-card";
    const heading = document.createElement("div");
    heading.className = "timeline-row";
    const title = document.createElement("strong");
    title.textContent = String(actor.label ?? "Actor");
    heading.append(title, createStatus("reported", actor.status));
    const role = document.createElement("small");
    role.className = "source";
    role.textContent = String(actor.role ?? "Actor");
    const detail = document.createElement("p");
    detail.textContent = String(actor.detail ?? "No visible actor detail.");
    item.append(heading, role, detail);
    appendSource(item, actor.source);
    list.append(item);
  }
  if (!actors?.length) emptyState(list, "No campaign actor signals are available.");
}

function renderCampaignCoverageProcesses(processes, root) {
  const list = root.querySelector("#campaign-process-list");
  if (!list) return;
  list.replaceChildren();
  for (const process of processes ?? []) {
    const item = document.createElement("li");
    const heading = document.createElement("div");
    heading.className = "timeline-row";
    const title = document.createElement("strong");
    title.textContent = String(process.label ?? "Process");
    heading.append(title, createStatus(process.status, process.status));
    const detail = document.createElement("p");
    detail.textContent = String(process.detail ?? "No visible process detail.");
    item.append(heading, detail);
    appendSource(item, process.source);
    list.append(item);
  }
  if (!processes?.length) emptyState(list, "No campaign process is available.");
}

function renderCampaignCoverageHistory(entries, root) {
  const list = root.querySelector("#campaign-history-list");
  if (!list) return;
  list.replaceChildren();
  for (const entry of entries ?? []) {
    const item = document.createElement("li");
    const turn = document.createElement("strong");
    turn.textContent = `Turn ${entry.turn ?? "—"}`;
    const command = document.createElement("span");
    command.textContent = ` · ${entry.command ?? "—"}`;
    const hash = document.createElement("small");
    hash.className = "hash";
    hash.textContent = ` · state hash: ${entry.state_hash ?? "—"}`;
    item.append(turn, command, hash);
    list.append(item);
  }
  if (!entries?.length) emptyState(list, "No committed campaign transitions yet.");
}

function coverageCommand(decision, form) {
  let command = String(decision.command_template ?? "");
  for (const parameter of decision.parameters ?? []) {
    const input = form.elements.namedItem(parameter.name);
    const value = input?.value ?? "";
    if (!value) return { ok: false, message: `Enter ${parameter.label ?? parameter.name}.` };
    command = command.replaceAll(`{{${parameter.name}}}`, value);
  }
  return { ok: true, command };
}

function renderCampaignCoverageDecisions(decisions, root, onSubmit) {
  const list = root.querySelector("#campaign-decision-list");
  if (!list) return;
  list.replaceChildren();
  for (const decision of decisions ?? []) {
    const item = document.createElement("article");
    item.className = "campaign-decision-card";
    const heading = document.createElement("h4");
    heading.textContent = String(decision.label ?? "Campaign decision");
    const uncertainty = document.createElement("p");
    uncertainty.textContent = String(decision.uncertainty ?? "Future response remains uncertain.");
    const form = document.createElement("form");
    form.className = "campaign-decision-form";
    for (const parameter of decision.parameters ?? []) {
      const label = document.createElement("label");
      label.textContent = String(parameter.label ?? parameter.name);
      let input;
      if (parameter.input_type === "select") {
        input = document.createElement("select");
        for (const option of parameter.options ?? []) {
          const optionNode = document.createElement("option");
          optionNode.value = String(option.value);
          optionNode.textContent = String(option.label ?? option.value);
          input.append(optionNode);
        }
      } else {
        input = document.createElement("input");
        input.type = parameter.input_type ?? "text";
        if (parameter.min != null) input.min = String(parameter.min);
        if (parameter.max != null) input.max = String(parameter.max);
        input.inputMode = parameter.input_type === "number" ? "numeric" : "text";
      }
      input.name = parameter.name;
      input.required = true;
      label.append(input);
      form.append(label);
    }
    const button = document.createElement("button");
    button.type = "submit";
    button.textContent = decision.parameters?.length ? "Submit host-shaped decision" : "Commit decision";
    form.append(button);
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const result = coverageCommand(decision, form);
      if (!result.ok) {
        setPresentationState(root, result.message);
        return;
      }
      onSubmit(result.command);
    });
    item.append(heading, uncertainty, form);
    appendSource(item, decision.source);
    list.append(item);
  }
  if (!decisions?.length) emptyState(list, "No campaign decision is available.");
}

export function renderCampaignCoverage(envelope, root = document, onSubmit = () => {}) {
  const panel = root.querySelector("#campaign-coverage-panel");
  if (!envelope || envelope.schema_version !== CAMPAIGN_COVERAGE_SCHEMA) {
    if (panel) panel.hidden = true;
    return { ok: false, code: envelope ? "unsupported_campaign_coverage_schema" : "empty_campaign_coverage" };
  }
  if (panel) panel.hidden = false;
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
  renderCampaignCoverageDecisions(envelope.decisions, root, onSubmit);
  renderCampaignCoverageHistory(envelope.history, root);
  const debrief = root.querySelector("#campaign-debrief-list");
  if (debrief) {
    debrief.replaceChildren();
    for (const line of envelope.debrief ?? []) {
      const item = document.createElement("li");
      item.textContent = String(line);
      debrief.append(item);
    }
    if (!envelope.debrief?.length) emptyState(debrief, "Campaign debrief becomes available after completion.");
  }
  return { ok: true, envelope };
}

export function createCampaignCoverageClient({
  adapter = globalThis.HsMgtGameCampaignAdapter ?? globalThis.HsMgtGameActionAdapter ?? globalThis.HsMgtGameReadOnlyAdapter,
  root = document,
  audio,
} = {}) {
  let currentEnvelope = null;
  const audioClient = audio ?? createAudioClient({ root });

  async function load(sessionId = adapter?.sessionId) {
    if (!adapter || typeof adapter.getCampaignCoverage !== "function") {
      return { ok: false, code: "campaign_coverage_adapter_missing" };
    }
    try {
      const envelope = await adapter.getCampaignCoverage(sessionId);
      const result = renderCampaignCoverage(envelope, root, submit);
      if (!result.ok) {
        currentEnvelope = null;
        setPresentationState(root, "Campaign coverage is unavailable; existing presentation remains active.");
        return result;
      }
      currentEnvelope = envelope;
      audioClient.setMusicFromVisible(campaignAudioInput(envelope));
      return result;
    } catch (error) {
      currentEnvelope = null;
      const message = error instanceof Error ? error.message : String(error);
      setPresentationState(root, `Campaign coverage adapter error: ${message}`);
      return { ok: false, code: "campaign_coverage_adapter_error", message };
    }
  }

  async function submit(command) {
    if (!adapter || typeof adapter.submitTurn !== "function") {
      setPresentationState(root, "No campaign submit adapter configured; no transition was attempted.");
      audioClient.playCue("ui.action-reject");
      return { ok: false, code: "campaign_submit_adapter_missing" };
    }
    try {
      setPresentationState(root, "Submitting the canonical campaign decision…");
      const response = await adapter.submitTurn(command);
      if (response?.error) throw new Error(response.error);
      audioClient.playCue("ui.submit");
      const result = await load(adapter.sessionId);
      if (!result.ok) return result;
      audioClient.playCue("ui.report-received");
      audioClient.playCue("ui.advance-month");
      if (result.envelope.session?.campaign === "regional-affiliation-v1") {
        audioClient.playCue("event.affiliation-milestone");
      }
      setPresentationState(root, "Campaign decision committed; current stage refreshed from the host.");
      return { ok: true, envelope: result.envelope };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      audioClient.playCue("ui.action-reject");
      setPresentationState(root, `Campaign decision rejected; current stage remains active: ${message}`);
      return { ok: false, code: "campaign_submit_rejected", message };
    }
  }

  return { load, submit, audio: audioClient, get envelope() { return currentEnvelope; } };
}

export function renderRegionalWorld(envelope, root = document) {
  if (!envelope || envelope.schema_version !== REGIONAL_WORLD_SCHEMA) {
    renderRegionalOverlays([], root);
    renderRegionalNavigation([], root);
    return { ok: false, code: envelope ? "unsupported_regional_world_schema" : "empty_regional_world" };
  }
  const entities = regionalEntitiesToFixture(envelope);
  if (!entities.some((entity) => entity.id === selectedEntityId)) selectedEntityId = entities[0]?.id;
  renderMap(entities, root);
  renderSelectedEntity(entities, root);
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

function renderHistory(entries, root) {
  const list = root.querySelector("#history-list");
  list.replaceChildren();
  for (const entry of entries ?? []) {
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
    list.append(item);
  }
  if (!entries?.length) emptyState(list, "No committed transitions yet.");
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
    })),
    ...(observation.policy_bullets ?? []).map((detail) => ({
      kind: "Policy signal",
      title: detail,
      detail: "Actor-visible policy information.",
      status: "reported",
      status_label: "Reported",
      source: "ReadOnlyObservation.policy_bullets",
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
  emptyState(commands, "Action submission is deferred to Phase 3.");
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
  const fixture = readOnlyEnvelopeToFixture(envelope);
  renderPresentation({ presentation_fixture: fixture }, root);
  renderObservationLines(envelope.observation, root);
  renderHistory(envelope.history, root);
  const debrief = root.querySelector("#debrief-list");
  debrief.replaceChildren();
  emptyState(debrief, "Debrief is supplied by the host end-session view.");
  const commands = root.querySelector("#legal-command-list");
  commands.replaceChildren();
  emptyState(commands, "Action submission is deferred to Phase 3.");
  setReadOnlyControls(root, true);
  const latestHash = envelope.replay?.latest_state_hash ?? "no committed hash yet";
  const session = envelope.session;
  const meta = root.querySelector("#session-meta");
  if (meta) meta.textContent = `${session.campaign ?? "session"} · turn ${session.turn ?? "—"}/${session.max_turns ?? "—"} · hash ${latestHash}`;
  setPresentationState(root, "Live or recorded read-only presentation loaded");
  return { ok: true, envelope };
}

export function createReadOnlyClient({ adapter = globalThis.HsMgtGameReadOnlyAdapter, root = document } = {}) {
  let currentEnvelope = null;
  const audioClient = createAudioClient({ root });
  const regionalWorldClient = createRegionalWorldClient({ adapter, root });
  const coverageAdapter = globalThis.HsMgtGameCampaignAdapter ?? adapter;
  const campaignCoverageClient = createCampaignCoverageClient({ adapter: coverageAdapter, root, audio: audioClient });

  function render(envelope) {
    const result = renderReadOnlyEnvelope(envelope, root);
    currentEnvelope = result.ok ? envelope : null;
    if (result.ok) audioClient.setMusicFromVisible(envelope);
    return result;
  }

  function renderStaticFixture(fixture = presentationFixture) {
    currentEnvelope = null;
    renderEnvelope({ ...demoEnvelope, legal_commands: [], presentation_fixture: fixture }, root);
    setReadOnlyControls(root, true);
    setPresentationState(root, "Static fixture loaded; no live adapter configured");
    audioClient.setMusicState("stable_operations");
    return { ok: true, fixture };
  }

  async function load(sessionId = adapter?.sessionId) {
    setReadOnlyControls(root, true);
    setPresentationState(root, "Loading read-only presentation…");
    if (!adapter || typeof adapter.getPresentation !== "function") {
      if (coverageAdapter && typeof coverageAdapter.getCampaignCoverage === "function") {
        return campaignCoverageClient.load(sessionId);
      }
      return renderStaticFixture();
    }
    try {
      const envelope = await adapter.getPresentation(sessionId);
      if (!envelope) {
        clearReadOnlySurface(root, "The read-only adapter returned no presentation data.");
        return { ok: false, code: "empty_presentation" };
      }
      const result = render(envelope);
      if (result.ok) {
        await regionalWorldClient.load(sessionId);
        await campaignCoverageClient.load(sessionId);
      }
      if (result.ok) audioClient.playCue("ui.report-received");
      return result;
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      clearReadOnlySurface(root, `Read-only adapter error: ${message}`);
      return { ok: false, code: "adapter_error", message };
    }
  }

  return { load, render, renderStaticFixture, audio: audioClient, regionalWorld: regionalWorldClient, campaignCoverage: campaignCoverageClient, get envelope() { return currentEnvelope; } };
}

function setActionControls(root, enabled) {
  for (const selector of ["#action-builder", "#draft-action-list", "#validate-actions", "#submit-month"]) {
    const node = root.querySelector(selector);
    if (node) node.hidden = !enabled;
  }
}

function actionCommand(spec, params) {
  return spec.command_template.replace(/\{\{(.*?)\}\}/g, (_, name) => String(params[name] ?? ""));
}

function renderDraftActions(drafts, root, onRemove, onRevise) {
  const list = root.querySelector("#draft-action-list");
  list.replaceChildren();
  for (const [index, draft] of drafts.entries()) {
    const item = document.createElement("li");
    item.className = "draft-action";
    const command = document.createElement("code");
    command.textContent = draft.command;
    const controls = document.createElement("span");
    const revise = document.createElement("button");
    revise.type = "button";
    revise.textContent = "Revise";
    revise.addEventListener("click", () => onRevise(index));
    const remove = document.createElement("button");
    remove.type = "button";
    remove.textContent = "Remove";
    remove.addEventListener("click", () => onRemove(index));
    controls.append(revise, remove);
    item.append(command, controls);
    list.append(item);
  }
  if (!drafts.length) emptyState(list, "No draft actions. Add Hold or another host-catalogued action.");
}

function renderActionCatalog(catalog, root, onAdd) {
  const list = root.querySelector("#action-preview-list");
  list.replaceChildren();
  const builder = root.querySelector("#action-builder");
  builder.replaceChildren();
  for (const spec of catalog.actions ?? []) {
    const item = document.createElement("article");
    item.className = "action-card action-catalog-card";
    const heading = document.createElement("div");
    heading.className = "action-heading";
    const title = document.createElement("strong");
    title.textContent = spec.label ?? spec.id ?? "Action";
    heading.append(title, createStatus("reported", "Host catalog"));
    const command = document.createElement("p");
    command.className = "command-preview";
    command.textContent = spec.command_template ?? "Canonical template unavailable";
    const meta = document.createElement("div");
    meta.className = "action-meta";
    for (const value of [spec.delay_label, spec.constraint_label, spec.uncertainty_label]) {
      const line = document.createElement("span");
      line.textContent = String(value ?? "Host metadata unavailable");
      meta.append(line);
    }
    item.append(heading, command, meta);
    appendSource(item, `ActionCatalog.${spec.id ?? "unknown"}`);
    list.append(item);

    const form = document.createElement("form");
    form.className = "action-builder-form";
    form.dataset.actionId = spec.id ?? "";
    const formHeading = document.createElement("h3");
    formHeading.textContent = `Add ${spec.label ?? spec.id ?? "action"}`;
    form.append(formHeading);
    for (const parameter of spec.parameters ?? []) {
      const label = document.createElement("label");
      label.textContent = parameter.label ?? parameter.name;
      let input;
      if (parameter.input_type === "select") {
        input = document.createElement("select");
        for (const option of parameter.options ?? []) {
          const optionNode = document.createElement("option");
          optionNode.value = option;
          optionNode.textContent = option;
          input.append(optionNode);
        }
      } else {
        input = document.createElement("input");
        input.type = parameter.input_type ?? "text";
        if (parameter.min != null) input.min = String(parameter.min);
        if (parameter.max != null) input.max = String(parameter.max);
      }
      input.name = parameter.name;
      input.required = true;
      label.append(input);
      form.append(label);
    }
    const add = document.createElement("button");
    add.type = "submit";
    add.textContent = "Add to draft";
    form.append(add);
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const params = {};
      for (const parameter of spec.parameters ?? []) {
        const input = form.elements.namedItem(parameter.name);
        params[parameter.name] = input?.value ?? "";
      }
      if ((spec.parameters ?? []).some((parameter) => !params[parameter.name])) {
        setPresentationState(root, "Complete each required action field before adding it.");
        return;
      }
      onAdd(spec, params, form);
    });
    builder.append(form);
  }
  if (!catalog.actions?.length) emptyState(list, "No host action catalog is available.");
}

function renderValidation(validation, root) {
  const status = root.querySelector("#validation-status");
  const submit = root.querySelector("#submit-month");
  if (!validation) {
    if (status) status.textContent = "Draft actions need host validation before submission.";
    if (submit) submit.hidden = true;
    return;
  }
  if (status) {
    status.textContent = validation.valid
      ? `Host validation passed: ${validation.cost?.action_points ?? "?"} AP · ${validation.cost?.cash_cost ?? "?"} cash · ${validation.cost?.political_capital ?? "?"} political capital.`
      : `Host validation rejected the draft: ${(validation.errors ?? []).join(" ")}`;
  }
  if (submit) submit.hidden = !validation.valid;
  renderActions(
    (validation.previews ?? []).map((preview) => ({
      label: preview.action_id ?? "Validated action",
      command: preview.canonical_command,
      cost: `${preview.cost?.action_points ?? "?"} AP · ${preview.cost?.cash_cost ?? "?"} cash · ${preview.cost?.political_capital ?? "?"} political capital`,
      delay: preview.delay_label,
      uncertainty: preview.uncertainty_label,
      constraint: preview.constraint_label,
      source: "ValidateTurn.host",
    })),
    root,
  );
}

export function createActionClient({ adapter = globalThis.HsMgtGameActionAdapter, root = document } = {}) {
  let catalog = null;
  let drafts = [];
  let validation = null;
  let editingIndex = null;
  let sessionId = adapter?.sessionId;
  const resolutionClient = createResolutionClient({ adapter, root });
  const audioClient = createAudioClient({ root });
  const regionalWorldClient = createRegionalWorldClient({ adapter, root });
  const coverageAdapter = globalThis.HsMgtGameCampaignAdapter ?? adapter;
  const campaignCoverageClient = createCampaignCoverageClient({ adapter: coverageAdapter, root, audio: audioClient });

  function draftCommand() {
    return drafts.map((draft) => draft.command).join("; ");
  }

  function invalidateDraft() {
    validation = null;
    renderValidation(null, root);
    setPresentationState(root, "Draft changed; host validation is required again.");
  }

  function renderDraftState() {
    renderDraftActions(
      drafts,
      root,
      (index) => {
        drafts.splice(index, 1);
        audioClient.playCue("ui.action-remove");
        invalidateDraft();
        renderDraftState();
      },
      (index) => {
        const draft = drafts[index];
        const form = root.querySelector(`form[data-action-id="${draft.action_id}"]`);
        if (!form) return;
        for (const [name, value] of Object.entries(draft.params)) {
          const input = form.elements.namedItem(name);
          if (input) input.value = value;
        }
        editingIndex = index;
        const button = form.querySelector("button[type=submit]");
        if (button) button.textContent = "Replace draft";
        setPresentationState(root, `Revising draft action ${index + 1}.`);
      },
    );
  }

  async function validateDraft() {
    if (!adapter || typeof adapter.validateTurn !== "function") {
      setPresentationState(root, "No host validation adapter configured; no submission was attempted.");
      return { ok: false, code: "validation_adapter_missing" };
    }
    setPresentationState(root, "Validating draft with the host…");
    try {
      const result = await adapter.validateTurn(sessionId, draftCommand());
      validation = result;
      renderValidation(validation, root);
      audioClient.playCue(validation.valid ? "ui.action-confirm" : "ui.action-reject");
      setPresentationState(root, validation.valid ? "Host validation passed; review before submitting." : "Host validation rejected the draft; revise and retry.");
      return { ok: Boolean(validation.valid), envelope: validation };
    } catch (error) {
      validation = null;
      renderValidation(null, root);
      audioClient.playCue("ui.action-reject");
      const message = error instanceof Error ? error.message : String(error);
      setPresentationState(root, `Validation adapter error: ${message}`);
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
      return { ok: false, code: "submit_adapter_missing" };
    }
    let response;
    try {
      response = await adapter.submitTurn(validation.canonical_command_text);
      if (response?.error) throw new Error(response.error);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      setPresentationState(root, `Submission rejected; current session was not replaced: ${message}`);
      return { ok: false, code: "submit_rejected", message };
    }
    drafts = [];
    validation = null;
    editingIndex = null;
    audioClient.playCue("ui.submit");
    let refreshMessage = "Committed response received from the host adapter.";
    if (typeof adapter.getResolution === "function") {
      const resolution = await resolutionClient.load(response.latest_transition?.turn, sessionId);
      if (!resolution.ok) refreshMessage += " Resolution presentation was unavailable.";
      else {
        audioClient.playCue("ui.advance-month");
        audioClient.setMusicFromVisible(resolution.envelope.after);
        for (const cueId of visibleEventCues(resolution.envelope)) audioClient.playCue(cueId);
      }
    }
    if (typeof adapter.getPresentation === "function") {
      try {
        const presentation = await adapter.getPresentation(sessionId);
        if (!renderReadOnlyEnvelope(presentation, root).ok) {
          renderEnvelope(response, root);
          refreshMessage = "Committed response received; read-only refresh was unavailable.";
        } else {
          audioClient.setMusicFromVisible(presentation);
          audioClient.playCue("ui.report-received");
          await regionalWorldClient.load(sessionId);
          await campaignCoverageClient.load(sessionId);
        }
      } catch (error) {
        renderEnvelope(response, root);
        const message = error instanceof Error ? error.message : String(error);
        refreshMessage = `Committed response received; read-only refresh failed: ${message}`;
      }
    } else {
      renderEnvelope(response, root);
      await campaignCoverageClient.load(sessionId);
    }
    setActionControls(root, true);
    renderDraftState();
    renderValidation(null, root);
    setPresentationState(root, refreshMessage);
    return { ok: true, envelope: response };
  }

  async function load(nextSessionId = adapter?.sessionId) {
    sessionId = nextSessionId;
    setActionControls(root, false);
    renderActions([], root);
    const actionMode = root.querySelector("#action-mode");
    if (actionMode) actionMode.textContent = "read-only view · actions deferred to Phase 3";
    setPresentationState(root, "Loading action catalog…");
    if (!adapter || typeof adapter.getActionCatalog !== "function" || typeof adapter.validateTurn !== "function") {
      if (coverageAdapter && typeof coverageAdapter.getCampaignCoverage === "function") {
        return campaignCoverageClient.load(sessionId);
      }
      setPresentationState(root, "Action adapter unavailable; read-only mode remains active.");
      return { ok: false, code: "action_adapter_missing" };
    }
    try {
      if (typeof adapter.getPresentation === "function") {
        const presentation = await adapter.getPresentation(sessionId);
        const rendered = renderReadOnlyEnvelope(presentation, root);
        if (!rendered.ok) return rendered;
        audioClient.setMusicFromVisible(presentation);
        await regionalWorldClient.load(sessionId);
        await campaignCoverageClient.load(sessionId);
      }
      catalog = await adapter.getActionCatalog(sessionId);
      if (!catalog || catalog.schema_version !== "competitive-actions-v1") {
        throw new Error("Unsupported action catalog schema.");
      }
      renderActionCatalog(catalog, root, (spec, params, form) => {
        const draft = { action_id: spec.id, params, command: actionCommand(spec, params) };
        if (editingIndex == null) drafts.push(draft);
        else drafts[editingIndex] = draft;
        editingIndex = null;
        const button = form.querySelector("button[type=submit]");
        if (button) button.textContent = "Add to draft";
        invalidateDraft();
        audioClient.playCue("ui.action-add");
        renderDraftState();
        setActionControls(root, true);
      });
      setActionControls(root, true);
      if (actionMode) actionMode.textContent = "host-catalogued draft builder";
      renderDraftState();
      renderValidation(null, root);
      setPresentationState(root, "Action catalog loaded; build a draft for host validation.");
      return { ok: true, catalog };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      setActionControls(root, false);
      if (actionMode) actionMode.textContent = "read-only view · action adapter unavailable";
      setPresentationState(root, `Action adapter error: ${message}`);
      return { ok: false, code: "action_adapter_error", message };
    }
  }

  root.querySelector("#validate-actions")?.addEventListener("click", validateDraft);
  root.querySelector("#submit-month")?.addEventListener("click", submit);
  return { load, validate: validateDraft, submit, audio: audioClient, regionalWorld: regionalWorldClient, campaignCoverage: campaignCoverageClient, get drafts() { return drafts; } };
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
  if (!panel || !status || !steps || !before || !after || !effects) {
    return { ok: false, code: "resolution_surface_missing" };
  }
  panel.hidden = false;
  steps.replaceChildren();
  if (!envelope) {
    status.textContent = "No committed resolution is available.";
    appendResolutionItems(before, [], "Decision-time snapshot unavailable.");
    appendResolutionItems(after, [], "Post-resolution snapshot unavailable.");
    appendResolutionItems(effects, [], "No direct committed effects available.");
    return { ok: false, code: "empty_resolution" };
  }
  for (const step of envelope.steps ?? []) {
    const item = document.createElement("li");
    item.className = "resolution-step";
    item.dataset.stepId = step.id ?? "";
    const heading = document.createElement("div");
    heading.className = "timeline-row";
    const label = document.createElement("strong");
    label.textContent = String(step.label ?? step.id ?? "Resolution step");
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
  if (!envelope.steps?.length) emptyState(steps, "No resolution steps available.");
  appendResolutionItems(before, snapshotItems(envelope.before), "Decision-time snapshot unavailable.");
  appendResolutionItems(after, snapshotItems(envelope.after), "Post-resolution snapshot unavailable.");
  appendResolutionItems(
    effects,
    (envelope.effects ?? []).map((effect) => `${effect.text ?? "Effect"} · Source: ${effect.source ?? "host"}`),
    "No direct committed effects available.",
  );
  status.textContent = `Committed turn ${envelope.turn ?? "—"} · state hash ${envelope.replay?.state_hash ?? "—"}`;
  return { ok: true, envelope };
}

export function createResolutionClient({ adapter = globalThis.HsMgtGameActionAdapter, root = document } = {}) {
  let envelope = null;
  let activeIndex = 0;
  let paused = true;
  let timer = null;

  function steps() {
    return envelope?.steps ?? [];
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
      state.textContent = paused
        ? `Reviewing committed turn ${envelope.turn ?? "—"} · state hash ${envelope.replay?.state_hash ?? "—"}`
        : `Playing committed turn ${envelope.turn ?? "—"} · step ${Math.min(activeIndex + 1, steps().length)} of ${steps().length}`;
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

  function tick() {
    if (paused || activeIndex >= steps().length - 1) {
      paused = true;
      stopTimer();
      updateControls();
      return;
    }
    setStep(activeIndex + 1);
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
    return { ok: true };
  }

  function pause() {
    paused = true;
    stopTimer();
    updateControls();
    return { ok: true };
  }

  function skip() {
    paused = true;
    stopTimer();
    setStep(Math.max(steps().length - 1, 0));
    return { ok: true };
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
  root.querySelector("#resolution-skip")?.addEventListener("click", skip);
  root.querySelector("#resolution-review")?.addEventListener("click", review);
  root.querySelector("#load-resolution")?.addEventListener("click", () => {
    const input = root.querySelector("#resolution-turn");
    load(input?.value ? Number(input.value) : undefined);
  });
  return { load, render, play, pause, skip, review, get envelope() { return envelope; } };
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
  const entityIds = new Set((fixture.entities ?? []).map((entity) => entity.id));
  if (!entityIds.has(selectedEntityId)) {
    selectedEntityId = fixture.selected_entity_id ?? fixture.entities?.[0]?.id;
  }
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
  const actionAdapter = globalThis.HsMgtGameActionAdapter;
  if (actionAdapter) {
    const client = createActionClient({ root: document });
    client.load();
    globalThis.HsMgtGui = {
      client,
      AUDIO_CATALOG,
      createAudioClient,
      createActionClient,
      createCampaignCoverageClient,
      createRegionalWorldClient,
      createResolutionClient,
      createReadOnlyClient,
      createThinClient,
      renderEnvelope,
      renderPresentation,
      renderReadOnlyEnvelope,
      renderResolution,
      renderRegionalWorld,
      renderCampaignCoverage,
      validateCommand,
      validateReadOnlyEnvelope,
    };
  } else {
    const client = createReadOnlyClient({ root: document });
    client.load();
    globalThis.HsMgtGui = {
      client,
      AUDIO_CATALOG,
      createAudioClient,
      createActionClient,
      createCampaignCoverageClient,
      createRegionalWorldClient,
      createResolutionClient,
      createReadOnlyClient,
      createThinClient,
      renderEnvelope,
      renderPresentation,
      renderReadOnlyEnvelope,
      renderResolution,
      renderRegionalWorld,
      renderCampaignCoverage,
      validateCommand,
      validateReadOnlyEnvelope,
    };
  }
}

export {
  demoEnvelope,
  presentationFixture,
  CAMPAIGN_COVERAGE_SCHEMA,
  READ_ONLY_PRESENTATION_SCHEMA,
};
