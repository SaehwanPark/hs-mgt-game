# Visual/audio Phase 4.2 visible consequence linkage — v0.12.65

## Decision

Link existing actor-visible reports, regional processes/signals, and committed
resolution effects through one deterministic local presentation projection.

## Scope

`gui/consequence-links.mjs` retains public signal observed months, process/effect
sources, committed turns, state hashes, explicit target IDs, and missing/targetless
boundaries. `gui/app.mjs` and `gui/index.html` expose report-to-entity,
entity-to-report, and consequence-to-board focus controls while keeping the
semantic panels and history visible.

## Authority boundary

No client-side target, location, causality, severity, outcome, or private rival
detail is inferred. Effects without host-provided targets remain visible but
cannot focus an invented entity. Replay helpers return immutable historical
turn/hash entries and do not overwrite current presentation state.

## Verification

Focused consequence-link, existing GUI resolution/first-month/regional, asset,
credits, metadata, documentation-link, full Python/Rust, formatting,
presentation-contract, and diff checks passed for the merged v0.12.65 slice.
Evidence remains technical and does not establish human usability, lived
accessibility, learning, calibration, contrast, browser replay behavior, or
policy validity.
