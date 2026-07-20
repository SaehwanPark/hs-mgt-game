# Visual/audio Phase 3.1 — Emergency-department component

Status: Implemented as a bounded fixture-only facility slice in v0.12.45.

## Outcome

Added a distinct fictional emergency-department source/release SVG pair and
extended the shared facility component catalog/proof selector with the same
base, identity, capacity, project, pressure, selection, and uncertainty layers
as the general-hospital base and patient tower. Visible sources, written
equivalents, non-color patterns, and generic fallback remain shared.

## Roadmap bookkeeping

All 13 per-component emergency-department checklist items are complete.
Ambulatory center and other facility types remain separate bounded slices.

## Verification and limits

- Focused emergency-department/patient-tower/general-hospital component,
  layer, fallback, registry, and syntax tests pass.
- Full Python, Rust, Clippy, formatting, metadata, documentation-link,
  registry/credits, and diff checks pass before handoff.
- Static evidence does not establish human art direction, contrast,
  screen-reader behavior, lived accessibility, learning, or policy validity.
