# Request Summary — Visual/audio roadmap execution v0.12.36

## Classification and scope

- Track: presentation; Phase 1.2 SVG rendering proof of concept.
- Slice: pure fixture-driven scene model/renderer, static proof page, keyboard
  selection, text/symbol fallbacks, uncertainty/unknown handling, deterministic
  snapshot, and render-time checks.
- Dependency: selected Variant A from v0.12.35.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` Phase 1.2.
- `docs/design/visual-audio-art-direction-board.md` and ADR-0012.
- `README.md`, `SPEC.md`, `ARCHITECTURE.md`, `docs/design_principles.md`, and
  `docs/harness/health-policy-strategy-game/team-spec.md`.

## Expected files

- `gui/scene.mjs`, `gui/svg-proof.html`, focused scene tests, registry/credits,
  Phase 1.2 history/SDD/QA/handoff records, and roadmap checklist updates.

## Non-goals

- No live GUI integration, host DTO, command, transition, stochastic input,
  browser simulation state, production facility/map kit, audio, animation,
  third-party asset, or human usability/accessibility claim.

## Acceptance and validation

- Scene model and deterministic SVG renderer are implemented.
- Institutions and facilities are keyboard reachable; labels/symbols remain
  available without color, motion, or audio.
- Uncertainty has a pattern/symbol and unknown data has generic fallbacks.
- Static fixture output is snapshot-stable, no hidden-state field is consumed,
  reduced motion is tested, and render time meets the proof target.
