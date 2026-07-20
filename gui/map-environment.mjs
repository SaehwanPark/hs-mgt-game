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

export { MAP_GRID };

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
