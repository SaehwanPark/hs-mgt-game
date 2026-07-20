const SYMBOLIC_DISTRICT_BOUNDARY = "District tokens organize symbolic relationships and attention; they do not establish real-world land use, population, ownership, zoning, travel time, or jurisdiction.";

const DISTRICT_TILE_FALLBACK = Object.freeze({
  schema_version: "regional-district-tile-v1",
  id: "district-generic",
  label: "District unavailable",
  district_type: "unknown",
  view_box: "0 0 192 144",
  grid: "24px",
  footprint: "8x6 cells",
  paths: Object.freeze([]),
  non_color_pattern: "solid boundary with text label",
  text_equivalent: "District type unavailable",
  visible_source: "Fixture-only symbolic district vocabulary",
  geography_boundary: SYMBOLIC_DISTRICT_BOUNDARY,
});

const DISTRICT_TILE_SET = Object.freeze([
  Object.freeze({
    schema_version: "regional-district-tile-v1",
    id: "district-commercial",
    label: "Commercial district",
    district_type: "commercial",
    view_box: "0 0 192 144",
    grid: "24px",
    footprint: "8x6 cells",
    paths: Object.freeze([
      Object.freeze({ id: "district-surface", d: "M0 12h192v120H0z", role: "district surface" }),
      Object.freeze({ id: "district-blocks", d: "M24 36h48v48H24zM96 36h48v48H96zM48 96h48v24H48z", role: "symbolic activity blocks" }),
      Object.freeze({ id: "district-frontage", d: "M24 30h48M96 30h48M48 90h48", role: "non-color frontage marks" }),
    ]),
    non_color_pattern: "short frontage marks across repeated activity blocks",
    text_equivalent: "Commercial district; symbolic activity-block pattern",
    visible_source: "Fixture-only symbolic district vocabulary",
    geography_boundary: SYMBOLIC_DISTRICT_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-district-tile-v1",
    id: "district-residential",
    label: "Residential district",
    district_type: "residential",
    view_box: "0 0 192 144",
    grid: "24px",
    footprint: "8x6 cells",
    paths: Object.freeze([
      Object.freeze({ id: "district-surface", d: "M0 12h192v120H0z", role: "district surface" }),
      Object.freeze({ id: "district-blocks", d: "M24 36h24v24H24zM72 36h24v24H72zM120 36h24v24H120zM48 84h24v24H48zM96 84h24v24H96zM144 84h24v24H144z", role: "symbolic neighborhood blocks" }),
      Object.freeze({ id: "district-streets", d: "M12 72h168M84 24v96", role: "non-color neighborhood marks" }),
    ]),
    non_color_pattern: "separated small blocks with cross-street marks",
    text_equivalent: "Residential district; symbolic neighborhood-block pattern",
    visible_source: "Fixture-only symbolic district vocabulary",
    geography_boundary: SYMBOLIC_DISTRICT_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-district-tile-v1",
    id: "district-employer-center",
    label: "Employer center",
    district_type: "employer-center",
    view_box: "0 0 192 144",
    grid: "24px",
    footprint: "8x6 cells",
    paths: Object.freeze([
      Object.freeze({ id: "district-surface", d: "M0 12h192v120H0z", role: "district surface" }),
      Object.freeze({ id: "district-campus", d: "M24 30h144v72H24z", role: "symbolic employer campus" }),
      Object.freeze({ id: "district-anchor", d: "M84 48h24v36H84zM72 60h48", role: "non-color employer anchor mark" }),
    ]),
    non_color_pattern: "single framed campus with central anchor mark",
    text_equivalent: "Employer center; symbolic campus-and-anchor pattern",
    visible_source: "Fixture-only symbolic district vocabulary",
    geography_boundary: SYMBOLIC_DISTRICT_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-district-tile-v1",
    id: "district-government",
    label: "Government district",
    district_type: "government",
    view_box: "0 0 192 144",
    grid: "24px",
    footprint: "8x6 cells",
    paths: Object.freeze([
      Object.freeze({ id: "district-surface", d: "M0 12h192v120H0z", role: "district surface" }),
      Object.freeze({ id: "district-civic-block", d: "M48 42h96v54H48z", role: "symbolic civic block" }),
      Object.freeze({ id: "district-steps", d: "M36 108h120M48 102h96M60 96h72", role: "non-color civic steps" }),
    ]),
    non_color_pattern: "framed civic block with stepped lower edge",
    text_equivalent: "Government district; symbolic civic-block pattern",
    visible_source: "Fixture-only symbolic district vocabulary",
    geography_boundary: SYMBOLIC_DISTRICT_BOUNDARY,
  }),
]);

export { DISTRICT_TILE_SET, DISTRICT_TILE_FALLBACK, SYMBOLIC_DISTRICT_BOUNDARY };

export function districtTileFor(id) {
  return DISTRICT_TILE_SET.find((tile) => tile.id === id) ?? DISTRICT_TILE_FALLBACK;
}
