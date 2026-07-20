# Presentation QA — Phase 4.1 static regional board v0.12.64

## Status

Pass for the bounded static regional-board adapter, integrated SVG mount, and
static proof.

## Reviewed inputs and authorization

- Request: `_workspace/00_input/request-summary.md`.
- Contract: `_workspace/02_presentation_contract.md`.
- Roadmap: `docs/visual_audio_enhancement_roadmap.md`, Phase 4.1.
- Produced files: `gui/regional-board.mjs`, `gui/regional-board-proof.html`,
  `gui/scene.mjs`, `gui/app.mjs`, `gui/index.html`, and
  `tests/test_regional_board.py`.
- Authorization is limited to mapping existing actor-visible DTO fields into a
  local presentation scene. Host and simulation authority remain unchanged.

## Information and causality findings

- Pass: entity/facility/overlay values are mapped from the existing typed DTO;
  layout-slot ordering is local deterministic presentation state.
- Pass: status, source, and missingness remain explicit in the scene summary,
  overlay cards, semantic detail, and fallback proof text.
- Pass: unknown identity and facility IDs use generic visual vocabulary without
  inventing private rival detail, severity, geography, causality, or outcomes.
- Pass: report focus uses the existing visible `target_id` as local navigation;
  it does not enter a command or transition path.

## Accessibility and fallback findings

- Pass: SVG entity/facility controls are keyboard reachable and the semantic
  map/detail list remains in the DOM as a fallback.
- Pass: screen-reader order is declared and tested through the board mount
  followed by entity, overlay, and detail regions.
- Pass: status/source/missingness text, symbols, and focus treatment remain
  available without color, motion, or audio.
- Evidence limit: static DOM and SVG checks do not establish lived
  accessibility, contrast, browser compatibility, or human comprehension.

## Provenance and rights findings

- Pass: the regional-board adapter and updated scene renderer have registry
  provenance, source hashes, accessible equivalents, and approved status.
- Pass: no external assets, fonts, URLs, or third-party files were introduced.

## Authority and replay findings

- Pass: the adapter is pure and local; app selection only re-renders existing
  presentation state.
- Pass: no host, command, simulation, stochastic, history, hash, replay, audio,
  or debrief path was added.

## Required fixes

None for this bounded slice.

The single light code-review pass identified two Medium findings in the
initial implementation: the SVG image role could hide keyboard descendants,
and sanitized scene IDs were not mapped back to raw DTO IDs. Both were fixed in
`c031bbe` and covered by focused tests; no second reviewer was spawned under the
task-level one-reviewer constraint.

## Verification evidence

- `python3 -m unittest tests.test_regional_board tests.test_svg_scene -v` — passed.
- `python3 scripts/validate_assets.py` — passed.
- `python3 scripts/generate_asset_credits.py --check` — passed.
- `node --check gui/regional-board.mjs gui/scene.mjs gui/app.mjs` — passed.
- `python3 -m unittest discover -s tests -p 'test_*.py'` — 438 tests passed.
- `cargo fmt -- --check` and `cargo test` — passed, including 328 Rust unit
  tests and all integration/golden/scenario targets.
- Release metadata, documentation links, asset registry/credits, presentation
  contract, and `git diff --check` — passed.
