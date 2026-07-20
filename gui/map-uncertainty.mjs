const UNCERTAINTY_INFORMATION_BOUNDARY = "Uncertainty overlays identify explicit stale, missing, or revised visible information; they do not quantify hidden risk, severity, probability, truth, or future outcome.";

const UNCERTAINTY_FALLBACK = Object.freeze({
  schema_version: "regional-uncertainty-overlay-v1",
  id: "uncertainty-generic",
  label: "Information status unavailable",
  overlay_type: "unknown",
  boundary_pattern: "dotted",
  fill_pattern: "none",
  severity_encoding: "none",
  motion: "none",
  non_color_pattern: "dotted boundary with text label",
  text_equivalent: "Information status unavailable",
  visible_source: "Fixture-only symbolic uncertainty vocabulary",
  information_boundary: UNCERTAINTY_INFORMATION_BOUNDARY,
});

const UNCERTAINTY_SET = Object.freeze([
  Object.freeze({
    schema_version: "regional-uncertainty-overlay-v1",
    id: "uncertainty-stale",
    label: "Stale visible information",
    overlay_type: "stale",
    boundary_pattern: "dash-dot",
    fill_pattern: "diagonal hatch",
    severity_encoding: "none",
    motion: "none",
    non_color_pattern: "dash-dot boundary with diagonal hatch",
    text_equivalent: "Stale visible information; no severity implied",
    visible_source: "Fixture-only symbolic uncertainty vocabulary",
    information_boundary: UNCERTAINTY_INFORMATION_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-uncertainty-overlay-v1",
    id: "uncertainty-missing",
    label: "Missing visible information",
    overlay_type: "missing",
    boundary_pattern: "dashed",
    fill_pattern: "crosshatch",
    severity_encoding: "none",
    motion: "none",
    non_color_pattern: "dashed boundary with crosshatch",
    text_equivalent: "Missing visible information; no severity implied",
    visible_source: "Fixture-only symbolic uncertainty vocabulary",
    information_boundary: UNCERTAINTY_INFORMATION_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-uncertainty-overlay-v1",
    id: "uncertainty-revised",
    label: "Revised visible information",
    overlay_type: "revised",
    boundary_pattern: "solid",
    fill_pattern: "sparse hatch",
    severity_encoding: "none",
    motion: "none",
    non_color_pattern: "solid boundary with sparse hatch",
    text_equivalent: "Revised visible information; no truth or outcome implied",
    visible_source: "Fixture-only symbolic uncertainty vocabulary",
    information_boundary: UNCERTAINTY_INFORMATION_BOUNDARY,
  }),
]);

export { UNCERTAINTY_SET, UNCERTAINTY_FALLBACK, UNCERTAINTY_INFORMATION_BOUNDARY };

export function uncertaintyFor(id) {
  return UNCERTAINTY_SET.find((overlay) => overlay.id === id) ?? UNCERTAINTY_FALLBACK;
}
