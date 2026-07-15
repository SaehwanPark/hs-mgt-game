# Domain QA — Visual and Audio Phase 1 Static Desktop v0.12.17

## Status

pass

## Reviewed Inputs

- User request and `_workspace/00_input/request-summary.md`.
- `_workspace/20_implementation_plan_visual_audio_phase1.md`.
- `docs/visual-audio-phase1-static-desktop-v0.12.17.md` and the accepted
  Phase 0 alignment/ADR-0011.
- `SPEC.md`, `ARCHITECTURE.md`, `docs/visual_audio_upgrade_proposal.md`,
  canonical product docs, and the harness team spec.
- `gui/index.html`, `gui/app.mjs`, `gui/README.md`, and
  `tests/test_gui_static_desktop.py`.

## Findings

- The static prototype exposes finance, workforce, capacity, access, and
  public rival information through executive-facing surfaces without raw JSON
  or CLI output.
- The regional schematic, facility cards, selected detail, briefing, action
  preview, pending-effects timeline, and monthly result all use display-only
  fixture data for one competitive month.
- Selection is presentation state only. The prototype does not import or
  duplicate `CompetitiveWorldState`, transition logic, resolved inputs,
  command legality, history, replay hashes, or debrief authority.
- Action cards show canonical command names, costs, delay, uncertainty,
  constraints, and source labels without pretending that the client can
  validate or execute them.
- Statuses have text equivalents, controls are keyboard-operable buttons, the
  layout has responsive breakpoints, reduced motion is respected, and the
  prototype uses no downloaded assets, fonts, or network calls.
- The fixture preserves the actor-observation boundary: public rival
  intelligence is shown while private rival state remains unavailable.

## Required Fixes

None.

## Residual Risks

- Browser rendering and viewport checks could not be exercised in this
  environment because no Chromium/Chrome binary is installed; browser-native
  QA remains a follow-up.
- Static technical checks do not establish human usability, lived
  accessibility, learning, engagement, or domain-expert validity.
- Phase 2 must promote only justified actor-visible DTOs and must not turn the
  fixture into a second simulation state or client-side command authority.

## Verification Evidence

- `python3 -m unittest tests/test_gui_thin_client.py
  tests/test_gui_static_desktop.py tests/test_release_metadata.py`: 16 tests
  passed.
- `node --check gui/app.mjs`: passed.
- `python3 scripts/check_release_metadata.py`: passed at `0.12.17`.
- `git diff --check`: passed.
- `cargo fmt --check`: passed.
- `cargo clippy --all-targets -- -D warnings`: passed.
- `cargo test --all -- --test-threads=1`: passed.
- No Rust, MCP, scenario, ruleset, replay, or asset files were changed for
  Phase 1.
