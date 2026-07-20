# Visual/audio Phase 3.1 — Ambulatory-center component

Status: Implemented as a bounded fixture-only facility slice in v0.12.46.

## Outcome

Added a distinct fictional ambulatory-center source/release SVG pair and
extended the shared facility component catalog/proof selector with the same
base, identity, capacity, project, pressure, selection, and uncertainty layers
as the existing facility components. Visible sources, written equivalents,
non-color patterns, and generic fallback remain shared.

## Roadmap bookkeeping

All 13 per-component ambulatory-center checklist items are complete. Specialty
center and other facility types remain separate bounded slices.

## Verification and limits

- Focused ambulatory-center/emergency-department/patient-tower/general-hospital
  component, layer, fallback, registry, and syntax tests pass.
- Full Python, Rust, Clippy, formatting, metadata, documentation-link,
  registry/credits, and diff checks pass before handoff.
- Static evidence does not establish human art direction, contrast,
  screen-reader behavior, lived accessibility, learning, or policy validity.
