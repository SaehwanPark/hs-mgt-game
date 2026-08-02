export const CONSEQUENCE_LINK_SCHEMA = "visible-consequence-links-v1";

const REGIONAL_WORLD_SCHEMA = "competitive-regional-world-v1";
const RESOLUTION_SCHEMA = "competitive-resolution-v1";

function text(value, fallback = "Unavailable") {
  const normalized = String(value ?? "").trim();
  return normalized || fallback;
}

function positiveInteger(value) {
  if (typeof value !== "number" || !Number.isSafeInteger(value) || value <= 0) return null;
  return value;
}

function nonEmptyString(value) {
  return typeof value === "string" && value.trim() ? value.trim() : "";
}

export function consequenceLinkContext(link = {}) {
  const observedMonth = positiveInteger(link.observed_month);
  const turn = positiveInteger(link.turn);
  const timing = observedMonth != null
    ? `Observed month ${observedMonth}`
    : turn != null
      ? `Turn ${turn}`
      : "Timing unavailable";
  const hash = nonEmptyString(link.state_hash);
  return `${timing} · ${hash ? `Replay state hash ${hash}` : "Replay context unavailable"}`;
}

export function consequenceLinkDelta(link = {}) {
  if (link.kind !== "committed-effect") return "";
  const delta = link.delta;
  if (typeof delta !== "number" || !Number.isSafeInteger(delta)) return "Delta unavailable";
  return `Delta ${delta > 0 ? "+" : ""}${delta}`;
}

function stableId(value, fallback) {
  const normalized = text(value, fallback)
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return normalized || fallback;
}

function sortLinks(left, right) {
  const turn = Number(left.turn ?? 0) - Number(right.turn ?? 0);
  const target = String(left.target_id ?? "").localeCompare(String(right.target_id ?? ""), "en", { numeric: true });
  const kind = String(left.kind ?? "").localeCompare(String(right.kind ?? ""));
  const source = String(left.source ?? "").localeCompare(String(right.source ?? ""));
  return turn || target || kind || source || String(left.id).localeCompare(String(right.id), "en", { numeric: true });
}

export function regionalWorldConsequenceLinks(envelope = {}) {
  if (envelope.schema_version !== REGIONAL_WORLD_SCHEMA) return [];
  const links = [];
  for (const entity of envelope.entities ?? []) {
    const targetId = text(entity.id, "institution");
    for (const signal of entity.signals ?? []) {
      links.push({
        id: stableId(`signal-${targetId}-${signal.text}`, "visible-signal"),
        kind: "public-signal",
        target_id: targetId,
        label: `${text(entity.name, "Institution")}: ${text(signal.text, "Public signal unavailable")}`,
        detail: `Observed month ${signal.observed_month ?? "Unavailable"}; private rival detail remains unavailable.`,
        turn: Number(signal.observed_month ?? 0),
        observed_month: signal.observed_month,
        source: text(signal.source, "RegionalWorldSignal.source"),
        information_boundary: "Public signal only; private rival detail remains unavailable and no hidden action is inferred.",
      });
    }
    for (const process of entity.processes ?? []) {
      links.push({
        id: stableId(`process-${targetId}-${process.label}`, "visible-process"),
        kind: "visible-process",
        target_id: targetId,
        label: text(process.label, "Visible process"),
        detail: text(process.detail, "No visible process detail available."),
        turn: Number(envelope.session?.turn ?? 0),
        source: text(process.source, "RegionalWorldProcess.source"),
        information_boundary: "Host-reported visible process; no future outcome is inferred.",
      });
    }
  }
  return links.sort(sortLinks);
}

export function resolutionConsequenceLinks(envelope = {}) {
  if (envelope.schema_version !== RESOLUTION_SCHEMA) return [];
  const effects = [...(envelope.effects ?? [])].sort((left, right) => {
    const metric = String(left.metric ?? "").localeCompare(String(right.metric ?? ""));
    const source = String(left.source ?? "").localeCompare(String(right.source ?? ""));
    return metric || source || String(left.text ?? "").localeCompare(String(right.text ?? ""));
  });
  return effects.map((effect, index) => ({
    id: stableId(`effect-${envelope.turn}-${effect.metric}-${index}`, `visible-effect-${index + 1}`),
    kind: "committed-effect",
    target_id: effect.target_id,
    label: text(effect.metric, "Committed effect"),
    detail: text(effect.text, "Direct committed effect reported by the host."),
    delta: effect.delta,
    turn: envelope.turn,
    state_hash: envelope.replay?.state_hash,
    source: text(effect.source, "ResolutionEffect.source"),
    information_boundary: "Direct host-committed effect; no future outcome is inferred.",
  })).sort(sortLinks);
}

export function resolutionResponseLinks(envelope = {}) {
  if (envelope.schema_version !== RESOLUTION_SCHEMA) return [];
  const responseStep = Array.isArray(envelope.steps)
    ? envelope.steps.find((step) => step?.id === "responses")
    : null;
  if (!responseStep) return [];
  const responseItems = Array.isArray(responseStep.items) ? responseStep.items : [];
  const details = responseItems.length
    ? responseItems.map((item) => nonEmptyString(item) || "No visible institutional responses.")
    : ["No visible institutional responses."];
  const source = nonEmptyString(responseStep.source) || "Host response source unavailable.";
  return details.map((detail, index) => ({
    id: stableId(`response-${envelope.turn}-${index}-${detail}`, `visible-response-${index + 1}`),
    kind: "visible-response",
    label: "Visible institutional response",
    detail,
    turn: envelope.turn,
    state_hash: envelope.replay?.state_hash,
    source,
    information_boundary: "Host-reported visible response; actor intent, private rival action, and future outcome remain unavailable.",
  })).sort(sortLinks);
}

export function composeConsequenceLinks({ regionalWorld, resolution } = {}) {
  return [
    ...regionalWorldConsequenceLinks(regionalWorld),
    ...resolutionResponseLinks(resolution),
    ...resolutionConsequenceLinks(resolution),
  ].sort(sortLinks);
}

export function consequenceLinksForTarget(links = [], targetId) {
  return links.filter((link) => !targetId || link.target_id === targetId);
}

export function replayConsequenceSequence(resolutions = []) {
  return resolutions
    .filter((resolution) => resolution?.schema_version === RESOLUTION_SCHEMA)
    .sort((left, right) => Number(left.replay?.selected_turn ?? left.turn ?? 0) - Number(right.replay?.selected_turn ?? right.turn ?? 0))
    .map((resolution) => Object.freeze({
      turn: resolution.turn,
      state_hash: resolution.replay?.state_hash,
      links: Object.freeze([
        ...resolutionResponseLinks(resolution),
        ...resolutionConsequenceLinks(resolution),
      ]),
    }));
}
