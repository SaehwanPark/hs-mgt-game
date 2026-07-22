import { facilityComponentFor } from "./facility-components.mjs";

export const REGIONAL_BOARD_SCHEMA = "regional-board-scene-v1";
const REGIONAL_WORLD_SCHEMA = "competitive-regional-world-v1";

function text(value, fallback = "Unavailable") {
  const normalized = String(value ?? "").trim();
  return normalized || fallback;
}

function safeId(value, fallback) {
  const normalized = text(value, fallback)
    .toLowerCase()
    .replace(/[^a-z0-9_-]+/g, "-")
    .replace(/^-+|-+$/g, "");
  return normalized || fallback;
}

function stableOrder(left, right) {
  const slot = String(left.layout_slot ?? "").localeCompare(String(right.layout_slot ?? ""), "en", { numeric: true });
  return slot || String(left.id ?? "").localeCompare(String(right.id ?? ""), "en", { numeric: true });
}

function missingFor(entityId, missing) {
  const prefix = `${entityId}-`;
  return (missing ?? []).filter((entry) => {
    const id = String(entry?.id ?? "");
    return id === entityId || id.startsWith(prefix);
  });
}

function entitySummary(entity, missing) {
  const visibility = entity.visibility === "owned" ? "Owned detail" : "Public identity only";
  const authority = text(entity.source, "Visible regional-world source unavailable");
  const unavailable = missing.length
    ? ` Missing detail: ${missing.map((entry) => text(entry.label, "Unavailable detail")).join("; ")}.`
    : "";
  return `${visibility} · ${authority}.${unavailable}`;
}

function normalizeFacilityComponent(facility) {
  const component = facilityComponentFor(facility?.component_id);
  return {
    component_id: component.id,
    component_label: component.label,
    component_source: component.source,
    component_equivalent: component.equivalent,
    component_release_path: component.release_path ?? null,
  };
}

function normalizeFacility(facility, entityId, index) {
  const label = text(facility?.name, "Facility unavailable");
  return {
    id: safeId(`${entityId}-${label}`, `facility-${index + 1}`),
    label,
    kind: text(facility?.kind, "facility"),
    marker: text(facility?.kind, "facility"),
    status: "reported",
    source: facility?.source,
    ...normalizeFacilityComponent(facility),
  };
}

function normalizeEntity(entity, missing, index) {
  const id = safeId(entity?.id, `institution-${index + 1}`);
  const entityMissing = missingFor(String(entity?.id ?? id), missing);
  return {
    id,
    source_id: entity?.id,
    name: text(entity?.name, "Institution unavailable"),
    role: text(entity?.role, "Institution"),
    status: text(entity?.status, "uncertain"),
    summary: entitySummary(entity ?? {}, entityMissing),
    layout_slot: text(entity?.layout_slot, `institution-${index + 1}`),
    facilities: (Array.isArray(entity?.facilities) ? entity.facilities : [])
      .map((facility, facilityIndex) => normalizeFacility(facility, id, facilityIndex)),
  };
}

function normalizeOverlay(overlay, index) {
  return {
    id: safeId(overlay?.id, `overlay-${index + 1}`),
    label: text(overlay?.label, "Visible overlay"),
    value: text(overlay?.value, "Unavailable"),
    unit: text(overlay?.unit, ""),
    marker: text(overlay?.label, "overlay"),
    source: text(overlay?.source, "Visible regional-world source unavailable"),
    equivalent: text(overlay?.equivalent, "Visible source-linked overlay."),
  };
}

export function regionalWorldToSceneData(envelope = {}) {
  const missing = Array.isArray(envelope.missing) ? envelope.missing : [];
  const entities = (Array.isArray(envelope.entities) ? envelope.entities : [])
    .map((entity, index) => normalizeEntity(entity, missing, index))
    .sort(stableOrder);
  return {
    schema_version: REGIONAL_BOARD_SCHEMA,
    title: "Regional operating board",
    source: "RegionalWorldEnvelope actor-visible fields",
    entities,
    overlays: (Array.isArray(envelope.overlays) ? envelope.overlays : []).map(normalizeOverlay),
  };
}

export function presentationFixtureToSceneData(fixture = {}) {
  const entities = (Array.isArray(fixture.entities) ? fixture.entities : []).map((entity, index) => ({
    id: safeId(entity?.id, `institution-${index + 1}`),
    source_id: entity?.id,
    name: text(entity?.name, "Institution unavailable"),
    role: text(entity?.type, "Institution"),
    status: text(entity?.status, "uncertain"),
    summary: text(entity?.summary, "No visible summary available."),
    layout_slot: `institution-${index + 1}`,
    facilities: (Array.isArray(entity?.facilities) ? entity.facilities : []).map((facility, facilityIndex) => ({
      id: safeId(`${entity?.id ?? "institution"}-${facility?.name}`, `facility-${facilityIndex + 1}`),
      label: text(facility?.name, "Facility unavailable"),
      kind: text(facility?.kind, "facility"),
      marker: text(facility?.kind, "facility"),
      status: text(facility?.status, "uncertain"),
      source: facility?.source,
      ...normalizeFacilityComponent(facility),
    })),
  }));
  return {
    schema_version: REGIONAL_BOARD_SCHEMA,
    title: "Regional operating board",
    source: "Static actor-visible presentation fixture",
    entities,
    overlays: [],
  };
}

export function sceneDataFromRegionalWorld(envelope = {}) {
  return envelope?.schema_version === REGIONAL_WORLD_SCHEMA
    ? regionalWorldToSceneData(envelope)
    : null;
}
