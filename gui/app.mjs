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
};

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
  globalThis.HsMgtGui = { client, createThinClient, renderEnvelope, validateCommand };
}

export { demoEnvelope };
