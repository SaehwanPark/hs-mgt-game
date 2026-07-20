const SYMBOLIC_PARCEL_BOUNDARY = "Parcel tokens organize symbolic placement; they do not establish real-world ownership, availability, development potential, land value, zoning, geography, or future use.";

const PARCEL_FALLBACK = Object.freeze({
  schema_version: "regional-parcel-v1",
  id: "parcel-generic",
  label: "Parcel unavailable",
  parcel_type: "unknown",
  view_box: "0 0 144 120",
  grid: "24px",
  footprint: "6x5 cells",
  paths: Object.freeze([]),
  non_color_pattern: "boundary with text label",
  text_equivalent: "Parcel type unavailable",
  visible_source: "Fixture-only symbolic parcel vocabulary",
  geography_boundary: SYMBOLIC_PARCEL_BOUNDARY,
});

const PARCEL_SET = Object.freeze([
  Object.freeze({
    schema_version: "regional-parcel-v1",
    id: "parcel-facility",
    label: "Facility parcel",
    parcel_type: "facility",
    view_box: "0 0 144 120",
    grid: "24px",
    footprint: "6x5 cells",
    paths: Object.freeze([
      Object.freeze({ id: "parcel-boundary", d: "M12 12h120v96H12z", role: "parcel boundary" }),
      Object.freeze({ id: "parcel-footprint", d: "M36 30h72v60H36z", role: "symbolic facility footprint" }),
      Object.freeze({ id: "parcel-slot", d: "M54 48h36v24H54z", role: "non-color placement slot" }),
    ]),
    non_color_pattern: "solid boundary with framed central placement slot",
    text_equivalent: "Facility parcel; symbolic placement slot",
    visible_source: "Fixture-only symbolic parcel vocabulary",
    geography_boundary: SYMBOLIC_PARCEL_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-parcel-v1",
    id: "parcel-undeveloped",
    label: "Undeveloped land parcel",
    parcel_type: "undeveloped",
    view_box: "0 0 144 120",
    grid: "24px",
    footprint: "6x5 cells",
    paths: Object.freeze([
      Object.freeze({ id: "parcel-boundary", d: "M12 12h120v96H12z", role: "parcel boundary" }),
      Object.freeze({ id: "parcel-dashed-edge", d: "M24 24h96M24 96h96M24 24v72M120 24v72", role: "non-color dashed boundary" }),
      Object.freeze({ id: "parcel-open-area", d: "M48 48h48v24H48z", role: "symbolic open-area mark" }),
    ]),
    non_color_pattern: "dashed boundary with open-area mark",
    text_equivalent: "Undeveloped land parcel; type-only open-area pattern",
    visible_source: "Fixture-only symbolic parcel vocabulary",
    geography_boundary: SYMBOLIC_PARCEL_BOUNDARY,
  }),
]);

export { PARCEL_SET, PARCEL_FALLBACK, SYMBOLIC_PARCEL_BOUNDARY };

export function parcelFor(id) {
  return PARCEL_SET.find((parcel) => parcel.id === id) ?? PARCEL_FALLBACK;
}
