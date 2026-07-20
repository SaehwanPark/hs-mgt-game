const SERVICE_AREA_INFORMATION_BOUNDARY = "Service-area overlays organize actor-visible service relationships; they do not establish real-world catchment, distance, travel time, population, access, jurisdiction, or performance.";

const SERVICE_AREA_FALLBACK = Object.freeze({
  schema_version: "regional-service-area-overlay-v1",
  id: "service-area-generic",
  label: "Service area unavailable",
  overlay_type: "unknown",
  contour_pattern: "dotted",
  fill_pattern: "none",
  geometry_claim: "symbolic contour only",
  metric_encoding: "none",
  directionality: "not encoded",
  non_color_pattern: "dotted contour with text label",
  text_equivalent: "Service-area category unavailable",
  visible_source: "Fixture-only symbolic service-area vocabulary",
  information_boundary: SERVICE_AREA_INFORMATION_BOUNDARY,
});

const SERVICE_AREA_SET = Object.freeze([
  Object.freeze({
    schema_version: "regional-service-area-overlay-v1",
    id: "service-area-primary",
    label: "Primary visible service area",
    overlay_type: "primary",
    contour_pattern: "solid",
    fill_pattern: "diagonal hatch",
    geometry_claim: "symbolic contour only",
    metric_encoding: "none",
    directionality: "not encoded",
    non_color_pattern: "solid contour with diagonal hatch",
    text_equivalent: "Primary visible service area; symbolic contour and hatch",
    visible_source: "Fixture-only symbolic service-area vocabulary",
    information_boundary: SERVICE_AREA_INFORMATION_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-service-area-overlay-v1",
    id: "service-area-shared",
    label: "Shared visible service area",
    overlay_type: "shared",
    contour_pattern: "double",
    fill_pattern: "crosshatch",
    geometry_claim: "symbolic contour only",
    metric_encoding: "none",
    directionality: "not encoded",
    non_color_pattern: "paired contour with crosshatch",
    text_equivalent: "Shared visible service area; symbolic paired contour and crosshatch",
    visible_source: "Fixture-only symbolic service-area vocabulary",
    information_boundary: SERVICE_AREA_INFORMATION_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-service-area-overlay-v1",
    id: "service-area-coordinated",
    label: "Coordinated visible service area",
    overlay_type: "coordinated",
    contour_pattern: "dash-dot",
    fill_pattern: "sparse hatch",
    geometry_claim: "symbolic contour only",
    metric_encoding: "none",
    directionality: "not encoded",
    non_color_pattern: "dash-dot contour with sparse hatch",
    text_equivalent: "Coordinated visible service area; symbolic dash-dot contour and hatch",
    visible_source: "Fixture-only symbolic service-area vocabulary",
    information_boundary: SERVICE_AREA_INFORMATION_BOUNDARY,
  }),
]);

export { SERVICE_AREA_SET, SERVICE_AREA_FALLBACK, SERVICE_AREA_INFORMATION_BOUNDARY };

export function serviceAreaFor(id) {
  return SERVICE_AREA_SET.find((overlay) => overlay.id === id) ?? SERVICE_AREA_FALLBACK;
}
