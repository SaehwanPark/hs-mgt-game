const SYMBOLIC_ROAD_BOUNDARY = "Road tokens organize symbolic relationships; they do not establish real-world road geometry, travel time, jurisdiction, or geography.";

const ROAD_TILE_FALLBACK = Object.freeze({
  schema_version: "regional-road-tile-v1",
  id: "road-generic",
  label: "Road segment unavailable",
  orientation: "unknown",
  view_box: "0 0 96 96",
  grid: "24px",
  paths: Object.freeze([]),
  text_equivalent: "Road segment unavailable",
  geography_boundary: SYMBOLIC_ROAD_BOUNDARY,
});

const ROAD_TILE_SET = Object.freeze([
  Object.freeze({
    schema_version: "regional-road-tile-v1",
    id: "road-straight-horizontal",
    label: "Road segment, horizontal",
    orientation: "horizontal",
    view_box: "0 0 96 96",
    grid: "24px",
    paths: Object.freeze([
      Object.freeze({ id: "road-bed", d: "M0 30h96v36H0z", role: "road surface" }),
      Object.freeze({ id: "road-centerline", d: "M0 48h96", role: "centerline" }),
    ]),
    text_equivalent: "Horizontal road segment",
    visible_source: "Fixture-only symbolic road-segment vocabulary",
    geography_boundary: SYMBOLIC_ROAD_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-road-tile-v1",
    id: "road-straight-vertical",
    label: "Road segment, vertical",
    orientation: "vertical",
    view_box: "0 0 96 96",
    grid: "24px",
    paths: Object.freeze([
      Object.freeze({ id: "road-bed", d: "M30 0h36v96H30z", role: "road surface" }),
      Object.freeze({ id: "road-centerline", d: "M48 0v96", role: "centerline" }),
    ]),
    text_equivalent: "Vertical road segment",
    visible_source: "Fixture-only symbolic road-segment vocabulary",
    geography_boundary: SYMBOLIC_ROAD_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-road-tile-v1",
    id: "road-curve-quarter",
    label: "Road segment, quarter curve",
    orientation: "quarter-curve",
    view_box: "0 0 96 96",
    grid: "24px",
    paths: Object.freeze([
      Object.freeze({ id: "road-bed", d: "M30 0v42c0 13 11 24 24 24h42v30H54C24 96 0 72 0 42V0z", role: "road surface" }),
      Object.freeze({ id: "road-centerline", d: "M48 0v42c0 3 3 6 6 6h42", role: "centerline" }),
    ]),
    text_equivalent: "Quarter-curve road segment",
    visible_source: "Fixture-only symbolic road-segment vocabulary",
    geography_boundary: SYMBOLIC_ROAD_BOUNDARY,
  }),
]);

export { ROAD_TILE_SET, ROAD_TILE_FALLBACK, SYMBOLIC_ROAD_BOUNDARY };

export function roadTileFor(id) {
  return ROAD_TILE_SET.find((tile) => tile.id === id) ?? ROAD_TILE_FALLBACK;
}
