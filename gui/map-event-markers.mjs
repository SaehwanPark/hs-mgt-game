const EVENT_MARKER_INFORMATION_BOUNDARY = "Event markers identify explicit visible categories; they do not encode severity, urgency, causality, intent, resolution, or future outcome.";

const EVENT_MARKER_FALLBACK = Object.freeze({
  schema_version: "regional-event-marker-v1",
  id: "event-marker-generic",
  label: "Event marker unavailable",
  event_category: "unknown",
  glyph: "?",
  marker_shape: "outlined circle",
  priority_encoding: "none",
  severity_encoding: "none",
  motion: "none",
  non_color_pattern: "outlined circle with question mark and text label",
  text_equivalent: "Event marker unavailable; visible category is unknown",
  visible_source: "Fixture-only symbolic event-marker vocabulary",
  information_boundary: EVENT_MARKER_INFORMATION_BOUNDARY,
});

const EVENT_MARKER_SET = Object.freeze([
  Object.freeze({
    schema_version: "regional-event-marker-v1",
    id: "event-marker-policy",
    label: "Policy event marker",
    event_category: "policy",
    glyph: "P",
    marker_shape: "notched square",
    priority_encoding: "none",
    severity_encoding: "none",
    motion: "none",
    non_color_pattern: "notched square with P glyph and text label",
    text_equivalent: "Policy event marker; visible category only",
    visible_source: "Fixture-only symbolic event-marker vocabulary",
    information_boundary: EVENT_MARKER_INFORMATION_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-event-marker-v1",
    id: "event-marker-workforce",
    label: "Workforce event marker",
    event_category: "workforce",
    glyph: "W",
    marker_shape: "striped circle",
    priority_encoding: "none",
    severity_encoding: "none",
    motion: "none",
    non_color_pattern: "striped circle with W glyph and text label",
    text_equivalent: "Workforce event marker; visible category only",
    visible_source: "Fixture-only symbolic event-marker vocabulary",
    information_boundary: EVENT_MARKER_INFORMATION_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-event-marker-v1",
    id: "event-marker-community",
    label: "Community event marker",
    event_category: "community",
    glyph: "C",
    marker_shape: "double-ring circle",
    priority_encoding: "none",
    severity_encoding: "none",
    motion: "none",
    non_color_pattern: "double-ring circle with C glyph and text label",
    text_equivalent: "Community event marker; visible category only",
    visible_source: "Fixture-only symbolic event-marker vocabulary",
    information_boundary: EVENT_MARKER_INFORMATION_BOUNDARY,
  }),
  Object.freeze({
    schema_version: "regional-event-marker-v1",
    id: "event-marker-project",
    label: "Project event marker",
    event_category: "project",
    glyph: "R",
    marker_shape: "outlined diamond",
    priority_encoding: "none",
    severity_encoding: "none",
    motion: "none",
    non_color_pattern: "outlined diamond with R glyph and text label",
    text_equivalent: "Project event marker; visible category only",
    visible_source: "Fixture-only symbolic event-marker vocabulary",
    information_boundary: EVENT_MARKER_INFORMATION_BOUNDARY,
  }),
]);

export {
  EVENT_MARKER_FALLBACK,
  EVENT_MARKER_INFORMATION_BOUNDARY,
  EVENT_MARKER_SET,
};

export function eventMarkerFor(id) {
  return EVENT_MARKER_SET.find((marker) => marker.id === id) ?? EVENT_MARKER_FALLBACK;
}
