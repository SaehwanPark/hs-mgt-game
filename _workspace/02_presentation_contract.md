# Presentation Contract — Phase 5.2 metric and trend visualization v0.12.67

## Goal and authorization

Make supplied actor-visible trends and constraints easier to scan through
small deterministic visuals without inferring precision, uncertainty,
missingness, causality, or hidden state.

## Visualization source ledger

| Form | Explicit source fields | Allowed presentation |
| --- | --- | --- |
| Sparkline | Visible ordered numeric periods | Compact line with gaps for missing periods |
| Month-over-month delta | Two visible comparable values | Written increase/decrease/unchanged label |
| Capacity bar | Visible used and total units | Patterned relative bar plus exact units |
| Staffing composition | Visible category units | Patterned composition plus category legend |
| Project progress | Visible completed and total units | Track plus completed/total text; no promise |
| Payer-mix summary | Visible payer categories and values | Patterned mix plus exact category text |
| Trust/legitimacy trend | Visible categorical period labels | Labeled sequence; never numeric scoring |
| Uncertainty interval | Visible lower/estimate/upper fields | Whisker and exact bounds; not probability |

## Visual and interaction contract

- `gui/metric-visualizations.mjs` is the single catalog. Each form documents
  source precision, uncertainty rendering, missingness rendering, exact text,
  color-independent interpretation, large-text behavior, and a screenshot
  fixture.
- `renderMetricVisualizationSvg` emits deterministic SVG with written title,
  description, exact text, source, and status. Geometry is supplementary and
  never normalizes absent fields.
- `gui/app.mjs` renders a visual only when a metric descriptor explicitly
  supplies `visualization_kind` and its values. Existing written metric values
  remain the primary fallback.
- `gui/metric-visualization-proof.html` exposes all eight forms with large-text,
  print, and reduced-motion controls and no host or network path.

## Accessibility and fallback requirements

- Exact values, source/status, uncertainty, and missingness remain in ordinary
  DOM text. SVG title/description text is supplementary, not the only label.
- Color-independent patterns, line styles, point shapes, legends, and explicit
  written labels carry meaning when color or audio is unavailable.
- Large text stacks or reflows labels; print retains visual headings and exact
  text; reduced motion is static because animation is not used.

## Authority, history, and replay boundaries

The catalog accepts only explicit metric descriptor fields. It does not call a
host, submit a command, mutate simulation state, resolve stochastic inputs,
rewrite history, change a state hash, or create debrief facts. It does not
convert missing values into estimates or categorical trust labels into scores.

## Asset provenance and verification

`visual.runtime-metric-visualizations` is a project-generated registry-approved
semantic asset with source hash, visible-source description, accessible
equivalent, and no release image. Focused tests include deterministic SVG
snapshot hashing; full Python/Rust, formatting, registry/credits/metadata,
documentation, presentation-contract, and diff checks are required before
merge.

## Non-goals and next gate

This slice does not add host fields, metric history storage, client-side
forecasting, probability calibration, animation, audio, or a browser screenshot
engine. Later roadmap phases own motion, audio, broader capture, and QA.
