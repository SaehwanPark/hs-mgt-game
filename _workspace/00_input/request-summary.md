# Request Summary — Visual/audio Phase 5.2 metric visualization v0.12.67

## Authorized outcome

Complete the Phase 5.2 metric and trend visualization checklist while
preserving actor-visible evidence and host authority.

## Slice boundary

- Define eight small deterministic forms: sparkline, month-over-month delta,
  capacity bar, staffing composition, project progress, payer-mix summary,
  trust/legitimacy trend, and visible uncertainty interval.
- Document source precision, uncertainty, missingness, exact-text,
  color-independent, large-text, print, reduced-motion, and screenshot rules.
- Add a fixture-only proof and deterministic SVG snapshot test.
- Add opt-in live rendering only for metric descriptors that explicitly supply
  actor-visible visualization data; retain written value/source/status text.
- Do not change Rust DTOs, simulation state, commands, transitions, stochastic
  inputs, history, hashes, replay authority, audio, or debrief behavior.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 5.2.
- `gui/metric-visualizations.mjs` — deterministic catalog and SVG adapter.
- `gui/metric-visualization-proof.html` — fixture proof.
- `gui/app.mjs` and `gui/index.html` — existing metric surface and opt-in path.
- `docs/design_principles.md` — actor-visible boundaries and accessibility.

## Validation target

Focused metric-visualization, GUI, registry, credits, metadata,
documentation-link, full Python, full Rust, formatting, presentation-contract,
snapshot, and diff checks.

## Evidence limits

Static deterministic models and SVG checks establish technical fidelity and
authority boundaries only. They do not establish human usability, lived
accessibility, contrast, learning, calibration, browser behavior, or policy
validity.
