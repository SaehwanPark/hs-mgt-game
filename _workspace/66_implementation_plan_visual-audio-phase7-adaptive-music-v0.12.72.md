# Implementation Plan — Visual/audio Phase 7.3 adaptive music stems v0.12.72

## 1. Task restatement

Complete the adaptive music stem milestone as a bounded generated-audio slice:
catalog seven music states, map them only from actor-visible fields, play
deterministic layered recipes with bounded crossfades, preserve text/visual
equivalents, and prove mute/replay/authority boundaries.

## 2. Current understanding

- `gui/audio.mjs` currently has four single-recipe music states and a visible
  classifier for menu, stable operations, pressure, and debrief.
- Phase 7.1 supplies cue standards and cues-only mode; Phase 7.2 supplies the
  separate optional ambience catalog and explicit-context gate.
- The roadmap’s seven music states are menu/planning, stable operations,
  pressure, regulatory scrutiny, competitive escalation, affiliation or
  negotiation, and debrief.

## 3. Target slice and assumptions

- Add the seven-state stem contract while preserving existing IDs for menu,
  stable operations, pressure, and debrief.
- Each state has base pulse, institutional motif, visible pressure layer,
  policy layer, transition cadence, visible trigger, text equivalent, bounded
  crossfade, and optional/mute fallback metadata.
- Classification accepts only explicit actor-visible stage, observation,
  report, or process text. Unknown or unsupported contexts use stable
  operations with an explicit generic equivalent; no hidden state is inferred.
- Generated Web Audio recipes are the release artifact. No recorded or
  third-party audio is added.

## 4. Minimal implementation plan

1. Add `gui/music-stem-contract.mjs` with seven pure state entries, five stem
   recipes per state, visible-state classification, deterministic replay
   sequence planning, validation, and text/fallback metadata.
2. Update `gui/audio.mjs` to build its music catalog from the contract, play
   bounded stems for the selected visible state, keep state transitions local,
   and expose music-only mute alongside existing full mute/cues-only behavior.
3. Update `gui/index.html`, `gui/audio-catalog.json`, the fixture proof, tests,
   asset registry, credits, and source hashes.
4. Update roadmap, SPEC, architecture, README, GUI guidance, CHANGELOG,
   LESSONS, request/contract/QA handoffs, and release metadata.

## 5. Acceptance criteria

- Seven music states and their five stem roles validate with visible sources,
  bounded durations/crossfades, text equivalents, and optional fallbacks.
- The classifier and replay planner are deterministic for the same visible
  inputs and never read true state, private rival data, resolved inputs, or
  client formulas.
- Runtime stem playback remains optional; music-only mute and full mute retain
  written content, while cues-only continues to suppress music.
- Registry, credits, tests, metadata, docs, and full Rust/Python checks pass.

## 6. Non-goals

- Do not implement Phase 7.4 priority/fatigue queue, ducking, aggregation,
  simultaneous-voice stress management, or preference persistence.
- Do not add host DTO fields, simulation transitions, randomness, history,
  hashes, replay artifacts, debrief facts, network assets, or recorded audio.
- Do not claim measured loudness, musical quality, human comprehension,
  fatigue, accessibility, learning, calibration, or policy validity.

## 7. Stop conditions

- Stop if state classification requires hidden or true state.
- Stop if an external asset, license, or dependency is required.
- Stop on unrelated test failures rather than expanding into Phase 7.4.

## 8. Verification target

Focused music-contract/audio tests; Node syntax; asset/credits/release/docs
checks; full Python tests; `cargo fmt --check`; Clippy; Rust tests; and
`git diff --check`.

## 9. Risk label

Risk: medium-low. The slice touches the optional browser audio catalog and
client-local playback only; the main risk is accidentally encoding hidden
state or allowing an unbounded layered playback path.
