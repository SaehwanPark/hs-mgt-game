# Request Summary — Visual/audio Phase 4.1 static regional board v0.12.64

## Authorized outcome

Complete the Phase 4.1 static regional-board integration checklist using the
existing actor-visible regional-world DTO and deterministic SVG scene contract.

## Slice boundary

- Map `competitive-regional-world-v1` entities, facilities, overlays, source
  labels, statuses, layout slots, and missingness into scene data.
- Mount the scene in the existing GUI and preserve semantic map/detail panels.
- Keep institutional and facility focus local and synchronized with the
  existing selected-detail state; link visible report targets to the board.
- Provide generic identity/facility fallbacks, keyboard-reachable SVG controls,
  screen-reader order evidence, a static proof page, and a deterministic SVG
  snapshot fixture.
- Do not change host DTOs, simulation state, commands, transitions, stochastic
  inputs, history, hashes, replay, audio, or debrief behavior.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Phase 4.1.
- `src/mcp/regional_world.rs` — typed actor-visible regional-world envelope.
- `gui/scene.mjs` — deterministic SVG scene and visual vocabulary.
- `gui/app.mjs` and `gui/index.html` — existing semantic map/detail surface.
- `docs/design_principles.md` — information-boundary and accessibility rules.

## Validation target

Focused adapter, SVG snapshot, GUI integration, registry, credits, metadata,
documentation-link, full Python, full Rust, formatting, presentation-contract,
and diff checks.

## Evidence limits

Static fixture, DOM-order, and deterministic snapshot checks establish the
technical contract only. They do not establish human design quality, lived
accessibility, contrast, learning, calibration, first-live-month usability, or
policy validity.
