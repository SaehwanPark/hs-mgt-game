# Implementation Plan — Visual/audio Phase 6.2 first-month resolution sequence v0.12.69

## 1. Task restatement

Implement a deterministic presentation contract for the existing committed
competitive monthly resolution so the browser can sequence visible results,
retain all text on skip, synchronize board/report/metric surfaces, and optionally
emit stage-aligned audio cues without changing host authority.

## 2. Current understanding

- `src/mcp/resolution.rs` already exposes eight host-owned ordered steps.
- `gui/app.mjs` already renders all step text and has local play/pause/skip/review
  controls, but the ordering/synchronization/cue contract is implicit.
- `gui/first-month.mjs` already tracks the surrounding start-to-continue handoff.
- `gui/motion-catalog.mjs` supplies reduced-motion policy; no new dependency is
  needed.

## 3. Assumptions

- The existing `competitive-resolution-v1` envelope remains the only input.
- Step IDs are stable enough to map to the eight existing stages; unknown IDs
  use an explicit fallback stage and do not fail the whole presentation.
- Any assumption mismatch stops implementation rather than changing the Rust
  schema or inventing hidden data.

## 4. Minimal implementation plan

1. Add `gui/resolution-sequence.mjs` with a pure storyboard, normalization,
   critical display priority, stage-to-surface/cue mapping, skip/replay helpers,
   and deterministic sequence fingerprint.
2. Update `gui/app.mjs` to render storyboard metadata and use the planner for
   local progression; inject the existing optional audio client only for visible
   cue timing and keep every step rendered before playback.
3. Add a small keyboard/proof surface marker to `gui/index.html` and focused
   Python/Node tests for normal, reduced-motion, skip, replay, malformed, and
   host-boundary paths.
4. Update roadmap, SPEC, ARCHITECTURE, README/GUI guidance, CHANGELOG, and
   LESSONS with the bounded evidence and limitations.

## 5. Files and functions likely to change

- `gui/resolution-sequence.mjs`: new pure sequence contract.
- `gui/app.mjs`: `renderResolution`, `createResolutionClient`, and action-client
  construction/commit wiring.
- `gui/index.html`: visible sequence-status/progress semantics.
- `tests/test_resolution_sequence.py`: new focused contract tests.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `README.md`, `gui/README.md`, `CHANGELOG.md`, `LESSONS.md`: evidence and
  current-state updates.
- `Cargo.toml`, `Cargo.lock`: patch version `0.12.69`.

## 6. Tests and checks

- `python3 -m unittest tests/test_resolution_sequence.py tests/test_gui_first_month.py tests/test_gui_resolution.py`
- `node --check gui/resolution-sequence.mjs`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/check_documentation_links.py`
- `cargo fmt --check`
- `cargo test`
- `git diff --check`

## 7. Acceptance criteria

- The planner returns all eight known stages in deterministic order and keeps
  unknown stages visible with a safe fallback.
- Critical display priority is explicitly non-semantic and stable.
- Map/report/metric synchronization and optional audio cue IDs are stage data,
  not inferred client outcomes.
- Play, pause, advance, skip, review, reduced motion, and historical load keep
  all written resolution content available; skip does not drop reports.
- Keyboard-oriented tests reach every native resolution control and the existing
  host boundary remains free of transition/randomness/network calls.

## 8. Non-goals

- Do not change Rust DTOs, transition formulas, commands, stochastic inputs,
  history, state hashes, replay verification, or debrief generation.
- Do not add cinematic timers, a causal graph, real-time synchronization, or
  human-comprehension claims.
- Do not add a dependency or refactor unrelated GUI surfaces.

## 9. Stop conditions

- Stop if the host schema needs a new field or if more than the named GUI files
  require unrelated changes.
- Stop if stage priority would require private or true-state data.
- Stop if an existing test failure is unrelated to this slice; report it rather
  than broadening scope.

## 10. Review checklist

- Diff matches this slice and roadmap 6.2 only.
- Every visible/audio signal traces to the contract’s authorized source.
- Skip/reduced-motion/replay preserve written information.
- Tests cover malformed input and keyboard-visible controls.
- No broader abstraction or dependency was introduced.

## 11. Risk label

Risk: medium

Reason: The slice changes a multi-control browser presentation path and its
optional audio timing, but leaves host APIs and simulation authority unchanged.
