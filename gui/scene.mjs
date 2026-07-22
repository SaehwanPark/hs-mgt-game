import { facilityComponentFor } from "./facility-components.mjs";
import { visualIdentityFor, visualMarkerFor, visualStatusFor } from "./visual.mjs";

const BOARD = Object.freeze({ width: 960, height: 600 });
const POSITIONS = Object.freeze([
  [32, 104],
  [348, 104],
  [664, 104],
]);

const SCENE_FIXTURE = Object.freeze({
  schema_version: "regional-svg-scene-v1",
  title: "Regional operating board",
  source: "Static actor-visible fixture",
  entities: Object.freeze([
    {
      id: "riverside",
      name: "Riverside",
      role: "Player system",
      status: "constrained",
      summary: "Visible owned detail",
      facilities: Object.freeze([
        { id: "riverside-general", label: "General hospital", kind: "facility", marker: "staffing", status: "constrained" },
        { id: "riverside-clinic", label: "Ambulatory clinic", kind: "facility", marker: "capacity", status: "stable" },
      ]),
    },
    {
      id: "northlake",
      name: "Northlake",
      role: "Public rival",
      status: "uncertain",
      summary: "Public signal only; private detail unavailable",
      facilities: Object.freeze([]),
    },
    {
      id: "future-system",
      name: "Unlisted institution",
      role: "Institution unavailable",
      status: "not-provided",
      summary: "Identity and status unavailable",
      facilities: Object.freeze([
        { id: "future-facility", label: "Unlisted facility", kind: "not-provided", marker: "not-provided", status: "not-provided" },
      ]),
    },
  ]),
});

export const SVG_SCENE_FIXTURE = SCENE_FIXTURE;

function text(value, fallback = "Unavailable") {
  const normalized = String(value ?? "").trim();
  return normalized || fallback;
}

function escapeXml(value) {
  return text(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&apos;",
  }[character]));
}

function safeId(value, fallback) {
  const normalized = text(value, fallback).toLowerCase().replace(/[^a-z0-9_-]+/g, "-").replace(/^-+|-+$/g, "");
  return normalized || fallback;
}

function statusFor(value) {
  return visualStatusFor(value) ?? visualStatusFor("uncertain");
}

function normalizeFacility(facility, index) {
  const component = facilityComponentFor(facility?.component_id);
  const marker = visualMarkerFor({
    id: facility?.id,
    kind: facility?.kind,
    marker: facility?.marker,
    label: facility?.label,
  });
  return {
    id: safeId(facility?.id, `facility-${index + 1}`),
    label: text(facility?.label, "Facility unavailable"),
    marker,
    status: statusFor(facility?.status),
    source: text(facility?.source, ""),
    component_id: component.id,
    component_label: component.label,
    component_source: component.source,
    component_equivalent: component.equivalent,
    component_release_path: component.release_path ?? null,
  };
}

function normalizeEntity(entity, index) {
  const identity = visualIdentityFor({ id: entity?.id, name: entity?.name });
  return {
    id: safeId(entity?.id, `institution-${index + 1}`),
    name: text(entity?.name, identity.label),
    role: text(entity?.role, "Institution"),
    identity,
    status: statusFor(entity?.status),
    summary: text(entity?.summary, "No visible summary available."),
    facilities: (Array.isArray(entity?.facilities) ? entity.facilities : [])
      .map(normalizeFacility),
  };
}

function normalizeOverlay(overlay, index) {
  return {
    id: safeId(overlay?.id, `overlay-${index + 1}`),
    label: text(overlay?.label, "Visible overlay"),
    value: text(overlay?.value, "Unavailable"),
    unit: text(overlay?.unit, ""),
    marker: visualMarkerFor(overlay?.marker ?? overlay?.label),
    source: text(overlay?.source, "Visible source unavailable"),
    equivalent: text(overlay?.equivalent, "Visible source-linked overlay."),
  };
}

export function normalizeScene(scene = SVG_SCENE_FIXTURE) {
  const entities = Array.isArray(scene?.entities) ? scene.entities : [];
  const overlays = Array.isArray(scene?.overlays) ? scene.overlays : [];
  return {
    title: text(scene?.title, "Regional operating board"),
    source: text(scene?.source, "Visible source unavailable"),
    entities: entities.map(normalizeEntity),
    overlays: overlays.map(normalizeOverlay),
  };
}

function statusAttributes(status) {
  const pattern = status.id === "uncertain" || status.id === "delayed" ? "stroke-dasharray=\"7 5\"" : "";
  return `class=\"status status-${escapeXml(status.id)}\" data-status=\"${escapeXml(status.id)}\" ${pattern}`;
}

function renderFacility(facility, x, y, selectedId) {
  const selected = facility.id === selectedId;
  const label = `${facility.label}; ${facility.status.label}; ${facility.marker.label}; Component: ${facility.component_label}${facility.source ? `; Source: ${facility.source}` : ""}`;
  const detail = `${facility.status.symbol} ${facility.status.label} · ${facility.marker.label} · ${facility.component_label}${facility.source ? ` · Source: ${facility.source}` : ""}`;
  const componentDescription = `Visual component: ${facility.component_label}; Source: ${facility.component_source}; Equivalent: ${facility.component_equivalent}`;
  return `
    <a href=\"#${escapeXml(facility.id)}\" role=\"button\" tabindex=\"0\" data-facility-id=\"${escapeXml(facility.id)}\" data-component-id=\"${escapeXml(facility.component_id)}\" aria-label=\"Select ${escapeXml(label)}\">
      <title>${escapeXml(componentDescription)}</title>
      <rect x=\"${x}\" y=\"${y}\" width=\"250\" height=\"52\" rx=\"8\" fill=\"#ffffff\" stroke=\"${selected ? "#0b6e69" : "#9ec7c1"}\" stroke-width=\"${selected ? "4" : "2"}\" ${statusAttributes(facility.status)}/>
      <text x=\"${x + 14}\" y=\"${y + 22}\" class=\"label\" font-size=\"16\">${escapeXml(facility.marker.symbol)} ${escapeXml(facility.label)}</text>
      <text x=\"${x + 14}\" y=\"${y + 42}\" class=\"sub-label\" font-size=\"13\">${escapeXml(detail)}</text>
    </a>`;
}

function renderEntity(entity, index, selectedEntityId, selectedId) {
  const [x, y] = POSITIONS[index % POSITIONS.length];
  const selected = entity.id === selectedEntityId;
  const facilities = entity.facilities.length
    ? entity.facilities.map((facility, facilityIndex) => renderFacility(facility, x + 14, y + 142 + facilityIndex * 60, selectedId)).join("")
    : `<text x=\"${x + 14}\" y=\"${y + 166}\" class=\"sub-label\" font-size=\"14\">No visible facility detail.</text>`;
  return `
    <g data-entity-container-id=\"${escapeXml(entity.id)}\">
      <a href=\"#${escapeXml(entity.id)}\" role=\"button\" tabindex=\"0\" data-entity-id=\"${escapeXml(entity.id)}\" aria-label=\"Select ${escapeXml(entity.name)}; ${escapeXml(entity.role)}; ${escapeXml(entity.status.label)}\">
      <rect x=\"${x}\" y=\"${y}\" width=\"280\" height=\"344\" rx=\"14\" fill=\"#ffffff\" stroke=\"${selected ? "#0b6e69" : "#d6e2df"}\" stroke-width=\"${selected ? "5" : "2"}\"/>
      <rect x=\"${x}\" y=\"${y}\" width=\"280\" height=\"78\" rx=\"14\" fill=\"#e1f1ee\"/>
      <text x=\"${x + 18}\" y=\"${y + 32}\" class=\"label\" font-size=\"21\">${escapeXml(entity.identity.symbol)} ${escapeXml(entity.name)}</text>
      <text x=\"${x + 18}\" y=\"${y + 56}\" class=\"sub-label\" font-size=\"14\">${escapeXml(entity.role)} · ${escapeXml(entity.identity.label)}</text>
      <text x=\"${x + 18}\" y=\"${y + 110}\" class=\"label\" font-size=\"16\">${escapeXml(entity.status.symbol)} ${escapeXml(entity.status.label)}</text>
      <text x=\"${x + 18}\" y=\"${y + 132}\" class=\"sub-label\" font-size=\"13\">${escapeXml(entity.summary)}</text>
      </a>
      ${facilities}
    </g>`;
}

function renderOverlays(overlays) {
  if (!overlays.length) return "";
  const visible = overlays.slice(0, 4);
  const cards = visible.map((overlay, index) => {
    const x = 32 + index * 232;
    const value = `${overlay.value} ${overlay.unit}`.trim();
    return `<g data-overlay-id="${escapeXml(overlay.id)}">
      <rect x="${x}" y="474" width="216" height="78" rx="8" fill="#ffffff" stroke="#c5d8d3" stroke-width="2"/>
      <text x="${x + 12}" y="496" class="label" font-size="13">${escapeXml(overlay.marker.symbol)} ${escapeXml(overlay.label)}</text>
      <text x="${x + 12}" y="516" class="sub-label" font-size="12">${escapeXml(value)}</text>
      <text x="${x + 12}" y="536" class="sub-label" font-size="10">${escapeXml(overlay.source)}</text>
    </g>`;
  }).join("");
  const overflow = overlays.length > visible.length
    ? `<text x="42" y="574" class="sub-label" font-size="12">+${overlays.length - visible.length} more visible overlays</text>`
    : "";
  return `${cards}${overflow}`;
}

export function renderRegionalSvg(scene = SVG_SCENE_FIXTURE, { selectedId = "riverside", reducedMotion = false } = {}) {
  const normalized = normalizeScene(scene);
  const selected = normalized.entities.find((entity) => entity.id === selectedId)
    ?? normalized.entities.find((entity) => entity.facilities.some((facility) => facility.id === selectedId))
    ?? normalized.entities[0];
  const entities = normalized.entities.length
    ? normalized.entities.map((entity, index) => renderEntity(entity, index, selected?.id, selectedId)).join("")
    : `<text x=\"42\" y=\"160\" class=\"sub-label\" font-size=\"18\">No visible institutions available.</text>`;
  const overlays = renderOverlays(normalized.overlays);
  return `<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"${BOARD.width}\" height=\"${BOARD.height}\" viewBox=\"0 0 ${BOARD.width} ${BOARD.height}\" role=\"group\" aria-labelledby=\"scene-title scene-desc\" data-motion=\"${reducedMotion ? "reduced" : "standard"}\">
  <title id=\"scene-title\">${escapeXml(normalized.title)}</title>
  <desc id=\"scene-desc\">${escapeXml(normalized.source)}. Labels and symbols remain visible when color, motion, or audio is unavailable.</desc>
  <style>
    .label { fill: #17232d; font-family: system-ui, sans-serif; font-weight: 700; }
    .sub-label { fill: #60707b; font-family: system-ui, sans-serif; }
    a:focus rect { stroke: #075952; stroke-width: 5; }
    .status-uncertain, .status-delayed { stroke-dasharray: 7 5; }
  </style>
  <rect width=\"${BOARD.width}\" height=\"${BOARD.height}\" fill=\"#f4f7f6\"/>
  <rect x=\"28\" y=\"24\" width=\"904\" height=\"54\" rx=\"12\" fill=\"#17232d\"/>
  <text x=\"52\" y=\"59\" fill=\"#ffffff\" font-family=\"system-ui, sans-serif\" font-size=\"22\" font-weight=\"700\">${escapeXml(normalized.title)}</text>
  <text x=\"696\" y=\"58\" fill=\"#b8d8d3\" font-family=\"system-ui, sans-serif\" font-size=\"14\">KEYBOARD-REACHABLE PROOF</text>
  <text x=\"42\" y=\"96\" class=\"sub-label\" font-size=\"14\">${escapeXml(normalized.source)} · Select an institution or facility</text>
  ${entities}${overlays}
</svg>`;
}
