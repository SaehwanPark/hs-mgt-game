# Implementation Plan — Visual/audio Phase 5.2 metric visualization v0.12.67

## Objective

Complete Milestone 5.2 of `docs/visual_audio_enhancement_roadmap.md` as one
bounded presentation slice. Visuals must stay faithful to explicit
actor-visible metric data and must not create precision, probability,
missing-value estimates, or client-side authority.

## Work units

1. Define `gui/metric-visualizations.mjs` for eight deterministic visual forms,
   with precision, uncertainty, missingness, exact-text, color-independent,
   large-text, and screenshot rules.
2. Add the fixture-only `gui/metric-visualization-proof.html` with responsive,
   print, large-text, and reduced-motion inspection.
3. Add opt-in live rendering to existing header metrics only when a descriptor
   explicitly supplies a visualization; retain written value/source/status text.
4. Add deterministic SVG snapshot and focused tests, then registry/credits
   provenance.
5. Update roadmap, SPEC, ARCHITECTURE, CHANGELOG, README, GUI reference,
   lessons, and SDD handoff artifacts.
6. Run focused and full verification, perform one light code review, and merge
   the feature branch to `main` before selecting the next slice.

## Completion gate

- All nine checklist dimensions are evidenced.
- No absent or hidden field is converted into a visual value.
- Exact values and evidence limits remain in text.
- Registry, credits, metadata, documentation, snapshot, tests, formatting, and
  diff checks pass.
