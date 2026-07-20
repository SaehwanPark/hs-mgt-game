const MAP_GRID = Object.freeze({
  schema_version: "regional-map-grid-v1",
  id: "regional-map-grid",
  width: 960,
  height: 600,
  unit: 24,
  columns: 40,
  rows: 25,
  origin: Object.freeze({ x: 0, y: 0 }),
  coordinate_source: "Fixture-only symbolic layout coordinates",
  geography_boundary: "Spatial arrangement organizes relationships and attention; it does not assert real-world distance, geography, travel time, or jurisdiction.",
  accessible_equivalent: "Named grid coordinates and visible layout labels",
});

const MAP_TARGET_VIEWPORTS = Object.freeze([
  Object.freeze({ id: "compact", label: "Compact", width: 320, height: 480, text_scale: "100%" }),
  Object.freeze({ id: "standard", label: "Standard", width: 768, height: 600, text_scale: "100%" }),
  Object.freeze({ id: "wide", label: "Wide", width: 1280, height: 720, text_scale: "100%" }),
]);

const MAP_KEYBOARD_NAVIGATION_ORDER = Object.freeze([
  "board-heading",
  "return-link",
  "map-viewport",
  "zoom-controls",
  "pan-controls",
  "event-marker-policy",
  "event-marker-workforce",
  "event-marker-community",
  "event-marker-project",
  "event-marker-generic",
  "map-target-compact",
  "map-target-standard",
  "map-target-wide",
]);

const MAP_ZOOM_STEPS = Object.freeze([0.75, 1, 1.25, 1.5]);
const MAP_PAN_BOUNDS = Object.freeze({
  x: Object.freeze({ min: -240, max: 240 }),
  y: Object.freeze({ min: -144, max: 144 }),
});

export { MAP_GRID };

export {
  MAP_KEYBOARD_NAVIGATION_ORDER,
  MAP_PAN_BOUNDS,
  MAP_TARGET_VIEWPORTS,
  MAP_ZOOM_STEPS,
};

export function mapGridCell(column, row) {
  if (!Number.isInteger(column) || !Number.isInteger(row) || column < 0 || column >= MAP_GRID.columns || row < 0 || row >= MAP_GRID.rows) {
    throw new RangeError("Map grid coordinate is outside the declared grid.");
  }
  const normalizedColumn = column;
  const normalizedRow = row;
  return Object.freeze({
    column: normalizedColumn,
    row: normalizedRow,
    x: MAP_GRID.origin.x + normalizedColumn * MAP_GRID.unit,
    y: MAP_GRID.origin.y + normalizedRow * MAP_GRID.unit,
  });
}

export function normalizeMapZoom(value) {
  if (!Number.isFinite(value)) return 1;
  return MAP_ZOOM_STEPS.reduce((closest, step) => (
    Math.abs(step - value) < Math.abs(closest - value) ? step : closest
  ), MAP_ZOOM_STEPS[0]);
}

export function clampMapPan(position = {}) {
  const x = Number.isFinite(position.x) ? position.x : 0;
  const y = Number.isFinite(position.y) ? position.y : 0;
  return Object.freeze({
    x: Math.min(MAP_PAN_BOUNDS.x.max, Math.max(MAP_PAN_BOUNDS.x.min, x)),
    y: Math.min(MAP_PAN_BOUNDS.y.max, Math.max(MAP_PAN_BOUNDS.y.min, y)),
  });
}
