# Visual/audio Phase 3.1 — General-hospital base component

Status: Implemented as a bounded fixture-only facility slice in v0.12.43.

## Outcome

Added a reusable fictional general-hospital base source/release SVG pair and a
fixture component catalog for base, identity, capacity, project, pressure,
selection, and uncertainty layers. The proof keeps visible sources and written
equivalents alongside non-color layer patterns and generic fallback.

## Roadmap bookkeeping

All 13 per-component general-hospital-base checklist items are complete.
Patient tower and other facility types remain separate bounded slices.

## Verification and limits

- Focused facility component, layer, fallback, registry, and syntax tests pass.
- Full Python, Rust, Clippy, formatting, metadata, documentation-link,
  registry/credits, and diff checks pass before handoff.
- Static evidence does not establish human art direction, contrast,
  screen-reader behavior, lived accessibility, learning, or policy validity.
