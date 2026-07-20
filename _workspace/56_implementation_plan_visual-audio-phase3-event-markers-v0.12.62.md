# Implementation Plan — Visual/audio Phase 3.2 event markers v0.12.62

## Acceptance criteria

- `gui/map-event-markers.mjs` exports a deterministic marker set and generic
  fallback with non-color, text, no-severity, and static-motion contracts.
- `gui/map-environment.mjs` exports target viewport, keyboard order, zoom, and
  bounded pan contracts as pure data/functions.
- `gui/map-environment-proof.html` renders the shared symbolic map vocabulary
  and local controls with responsive, keyboard-reachable semantics.
- Focused Python tests cover the contracts and registry hash.
- The Phase 3.2 checklist and SDD records identify the slice as complete,
  preserve evidence limits, and leave live integration as future work.

## Verification plan

1. Run focused Python tests and `node --check` on new/changed modules.
2. Run asset validation and regenerate credits.
3. Run full Python and Rust checks plus documentation-link and metadata checks.
4. Complete presentation QA and one light code-review pass on the branch diff.
