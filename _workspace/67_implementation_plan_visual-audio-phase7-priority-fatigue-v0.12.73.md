# Implementation Plan — Visual/audio Phase 7.4 priority and fatigue manager v0.12.73

## 1. Task restatement

Complete Milestone 7.4 as a bounded local audio manager for the existing
visible cue, music, and ambience layers. Make dense resolution audio legible,
bounded, optional, and preference-aware without changing simulation authority.

## 2. Current understanding

- `gui/audio.mjs` currently plays valid cues immediately and relies on per-cue
  cooldown timestamps; music and ambience run on separate local timers.
- `gui/audio-cue-contract.mjs` already supplies 16 visible cue entries with
  `critical`, `major`, or `routine` classes and written equivalents.
- Phase 7.3 tracks active music voices and releases them with bounded ramps;
  Phase 7.2 tracks ambience recipes but does not coordinate cue ducking.
- `gui/app.mjs` calls cues synchronously around committed visible actions and
  resolution presentations, making a local microtask batch boundary inspectable.

## 3. Target slice and assumptions

- Add `gui/audio-priority-contract.mjs` with fixed priority values, queue caps,
  one-critical-per-batch policy, routine aggregation, duplicate suppression,
  bounded ducking factors, and validation/pure planning helpers.
- Integrate a local queue in `gui/audio.mjs`: requests are recorded with their
  visible cue metadata, planned by priority, dispatched one transient voice at
  a time, and drained through bounded timers/voice cleanup.
- Critical cues duck music and ambience; major cues duck ambience. Background
  music remains layered, and one ambience bed remains independent from the
  transient queue.
- Persist only explicit local audio preferences using a stable storage key;
  defaults and session behavior remain safe when storage is missing or throws.
- Use a bounded queue cap so repeated rapid requests cannot create unbounded
  timers, active voices, or sound stacking.

## 4. Minimal implementation plan

1. Define pure priority policy and batch planner, including stable ordering,
   one-critical selection, exact duplicate suppression, routine aggregation,
   queue overflow metadata, and policy validation.
2. Refactor client-local cue dispatch to use the planner and one transient
   voice slot while preserving existing `visual_only`, `muted`, cooldown, sink,
   recorder, reduced-notification, cues-only, and fallback behavior.
3. Track background voice gains and apply bounded local duck/restore ramps for
   major/critical dispatch without changing music/ambience recipes or state.
4. Add safe local preference read/write, initialize controls from stored values,
   and retain session-local defaults when storage is unavailable.
5. Add a fixture-only priority proof, focused runtime/stress tests, and update
   audio docs, QA, asset metadata only as required, roadmap status, version,
   changelog, architecture/spec/lessons, and generated catalog/hash records.

## 5. Acceptance criteria

- Pure policy validates and deterministically plans batches with at most one
  critical cue, routine aggregation, duplicate suppression, priority ordering,
  queue cap, and explicit simultaneous-voice bounds.
- Rapid synchronous requests and dense month-resolution sequences never create
  more than one transient cue voice or an unbounded queue; all visible text and
  recorder/sink equivalents remain available.
- Major/critical cues produce bounded ambience/music ducking according to the
  contract and restore behavior remains local and interruptible.
- Explicit audio preferences round-trip through local storage, but storage
  failures do not break controls, fallback text, or host presentation.
- Existing music, ambience, cues-only, music-only mute, full mute, focus,
  reduced-notification, and unsupported-audio behavior remains covered.
- Registry, credits, release metadata, docs, full Python/Rust, formatting,
  Clippy, JavaScript syntax, and diff checks pass.

## 6. Non-goals

- Do not change host DTOs, simulation transitions, actor observations, command
  validation, state hashes, replay artifacts, or debrief facts.
- Do not infer priority from true state, private intent, hidden outcome,
  metrics, or client-side severity formulas.
- Do not add recorded/third-party audio, network assets, speech, automatic
  permission requests, or a second simulation/authority layer.
- Do not claim human fatigue, accessibility, screen-reader, learning,
  calibration, musical quality, or policy validity from automated checks.

## 7. Stop conditions

- Stop if the queue needs a host batch identifier or hidden state to behave
  correctly; use the local synchronous batch boundary and document the limit.
- Stop if a new asset or external dependency is required.
- Stop on unrelated failures rather than expanding into Phase 8 or later audio
  generation work.

## 8. Verification target

Focused priority contract/runtime tests; fake Web Audio and fake timer stress;
preference storage round trips and failure; visible/live-region markers;
Node syntax; asset/credits/release/docs checks; full Python tests; `cargo fmt
--check`; Clippy; Rust tests; and `git diff --check`.

## 9. Risk label

Risk: medium. The slice refactors optional browser audio scheduling and adds
local timers/storage, so the main risks are cue reordering, inaccessible
meaning, voice/timer leaks, preference side effects, and accidental authority
drift. The deterministic pure planner and fake-runtime tests bound those risks.
