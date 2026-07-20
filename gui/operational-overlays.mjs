const OPERATIONAL_OVERLAY_INFORMATION_BOUNDARY = "Operational overlays summarize explicit actor-visible fields; they do not infer hidden severity, intent, causality, probability, or future outcome.";

const OVERLAY_DEFAULTS = Object.freeze({
  schema_version: "operational-overlay-v1",
  semantic_role: "operational-overlay",
  glyph: "•",
  marker_shape: "outlined circle",
  non_color_pattern: "outlined circle with text label",
  reduced_motion: "static overlay and text; no motion required",
  text_equivalent: "Visible operational overlay category unavailable",
  collision_behavior: "Stack visible cards in declared order and summarize overflow by count.",
  display_priority: 0,
  priority_rule: "Higher display priority first; stable ID breaks ties; order is display-only, not severity.",
  severity_encoding: "none",
  motion: "none",
  visible_source: "Fixture-only actor-visible operational overlay vocabulary",
  information_boundary: OPERATIONAL_OVERLAY_INFORMATION_BOUNDARY,
});

function overlay(fields) {
  return Object.freeze({ ...OVERLAY_DEFAULTS, ...fields });
}

const OPERATIONAL_OVERLAY_FALLBACK = overlay({
  id: "operational-overlay-generic",
  label: "Operational overlay unavailable",
  triggering_visible_field: "Unknown visible overlay ID",
  text_equivalent: "Operational overlay unavailable; visible category is unknown",
});

const OPERATIONAL_OVERLAY_SET = Object.freeze([
  overlay({
    id: "operational-staffing-constraint",
    label: "Staffing constraint",
    glyph: "♙",
    marker_shape: "vertical-hatch badge",
    non_color_pattern: "vertical hatch with ♙ glyph and text label",
    triggering_visible_field: "ReadOnlyObservation.staffing / PlayerObservation.nurses, physicians, and admins",
    text_equivalent: "Staffing constraint; visible staffing fields require attention",
    display_priority: 120,
  }),
  overlay({
    id: "operational-capacity-constraint",
    label: "Capacity constraint",
    glyph: "▤",
    marker_shape: "double-line badge",
    non_color_pattern: "double border with ▤ glyph and text label",
    triggering_visible_field: "ReadOnlyObservation.capacity / visible facility capacity metrics",
    text_equivalent: "Capacity constraint; visible capacity metric is constrained",
    display_priority: 110,
  }),
  overlay({
    id: "operational-demand-pressure",
    label: "Demand pressure",
    glyph: "⌁",
    marker_shape: "wave-line badge",
    non_color_pattern: "wave line with ⌁ glyph and text label",
    triggering_visible_field: "ReadOnlyObservation.operations.unmet_demand / PlayerObservation.monthly_unmet_demand",
    text_equivalent: "Demand pressure; visible unmet-demand value is reported",
    display_priority: 100,
  }),
  overlay({
    id: "operational-active-capital-project",
    label: "Active capital project",
    glyph: "◌",
    marker_shape: "solid-ring badge",
    non_color_pattern: "solid ring with ◌ glyph and text label",
    triggering_visible_field: "ReadOnlyObservation.in_flight_projects",
    text_equivalent: "Active capital project; host-reported project timing is visible",
    display_priority: 90,
  }),
  overlay({
    id: "operational-delayed-project",
    label: "Delayed project",
    glyph: "…",
    marker_shape: "dashed-ring badge",
    non_color_pattern: "dashed ring with … glyph and text label",
    triggering_visible_field: "Host-provided visible project timing/status within ReadOnlyObservation.in_flight_projects",
    text_equivalent: "Delayed project; visible timing/status is reported without a hidden cause",
    display_priority: 85,
  }),
  overlay({
    id: "operational-project-completion",
    label: "Project completion",
    glyph: "✓",
    marker_shape: "double-ring badge",
    non_color_pattern: "double ring with ✓ glyph and text label",
    triggering_visible_field: "ReadOnlyPresentation.latest_transition committed visible effects",
    text_equivalent: "Project completion; committed visible effect is reported",
    display_priority: 80,
  }),
  overlay({
    id: "operational-payer-network-change",
    label: "Payer/network change",
    glyph: "⚖",
    marker_shape: "dash-dot badge",
    non_color_pattern: "dash-dot border with ⚖ glyph and text label",
    triggering_visible_field: "ReadOnlyObservation.market_bullets / visible payer or market bullet",
    text_equivalent: "Payer or network change; visible market signal is reported",
    display_priority: 70,
  }),
  overlay({
    id: "operational-regulatory-review",
    label: "Regulatory review",
    glyph: "§",
    marker_shape: "dotted-frame badge",
    non_color_pattern: "dotted frame with § glyph and text label",
    triggering_visible_field: "ReadOnlyObservation.annual_policy_review / policy_bullets",
    text_equivalent: "Regulatory review; visible review text is reported",
    display_priority: 65,
  }),
  overlay({
    id: "operational-community-trust-concern",
    label: "Community-trust concern",
    glyph: "♡",
    marker_shape: "crosshatched badge",
    non_color_pattern: "crosshatch with ♡ glyph and text label",
    triggering_visible_field: "ReadOnlyObservation.community_trust",
    text_equivalent: "Community-trust concern; visible trust status is reported",
    display_priority: 60,
  }),
  overlay({
    id: "operational-financial-distress",
    label: "Financial distress",
    glyph: "$",
    marker_shape: "diagonal-hatch badge",
    non_color_pattern: "diagonal hatch with $ glyph and text label",
    triggering_visible_field: "ReadOnlyResources.cash + ReadOnlyObservation.cash_runway_signal",
    text_equivalent: "Financial distress; visible cash/runway signal is reported",
    display_priority: 55,
  }),
  overlay({
    id: "operational-recovery",
    label: "Operational recovery",
    glyph: "↗",
    marker_shape: "ascending-mark badge",
    non_color_pattern: "ascending marks with ↗ glyph and text label",
    triggering_visible_field: "ReadOnlyObservation.operations.margin / visible monthly operating result",
    text_equivalent: "Operational recovery; visible monthly result is reported",
    display_priority: 50,
  }),
  overlay({
    id: "operational-uncertain-stale-intelligence",
    label: "Uncertain or stale intelligence",
    glyph: "?",
    marker_shape: "dot-dash badge",
    non_color_pattern: "dot-dash border with ? glyph and text label",
    triggering_visible_field: "ReadOnlyObservation.information_gaps / prior_access_revision",
    text_equivalent: "Uncertain or stale intelligence; missingness or revision remains explicit",
    display_priority: 45,
  }),
]);

export {
  OPERATIONAL_OVERLAY_FALLBACK,
  OPERATIONAL_OVERLAY_INFORMATION_BOUNDARY,
  OPERATIONAL_OVERLAY_SET,
};

export function operationalOverlayFor(id) {
  return OPERATIONAL_OVERLAY_SET.find((entry) => entry.id === id) ?? OPERATIONAL_OVERLAY_FALLBACK;
}

function overlayFromEntry(entry) {
  return operationalOverlayFor(typeof entry === "string" ? entry : entry?.id);
}

export function orderedOperationalOverlays(entries = []) {
  return Object.freeze(entries.map(overlayFromEntry).sort((left, right) => (
    right.display_priority - left.display_priority
    || (left.id < right.id ? -1 : left.id > right.id ? 1 : 0)
  )));
}

export function layoutOperationalOverlays(entries = [], maxVisible = 4) {
  const limit = Number.isInteger(maxVisible) && maxVisible > 0 ? maxVisible : 4;
  const ordered = orderedOperationalOverlays(entries);
  const visible = ordered.slice(0, limit).map((entry, index) => Object.freeze({
    ...entry,
    slot: index,
    collision_state: index === 0 ? "stack-root" : "stacked-visible",
  }));
  const overflowCount = Math.max(0, ordered.length - visible.length);
  return Object.freeze({
    visible: Object.freeze(visible),
    overflow_count: overflowCount,
    overflow_text: overflowCount === 0
      ? "No visible overlays hidden by collision layout"
      : `${overflowCount} additional visible overlays`,
    collision_behavior: "Bounded stack with deterministic priority and stable-ID tie-breaking; overflow remains a count.",
  });
}
