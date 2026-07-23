# Phase 11.1 Live Music-State Binding — Implementation Plan v0.12.93

## Task restatement

Advance the bounded Phase 11.1 music-state item by making live competitive
resolution music selection an explicit host-shaped projection from committed
visible transition data and the actor-visible after snapshot.

## Current understanding

- `ResolutionEnvelope` already carries host-owned visible steps, effects, and
  before/after observations; v0.12.92 adds the analogous explicit event-cue
  projection.
- `gui/music-stem-contract.mjs` owns seven stable music IDs and a visible-only
  classifier whose priority is menu/debrief, regulatory, affiliation,
  competitive, pressure, then stable operations.
- The live action client currently calls `setMusicFromVisible` on the browser
  `after` snapshot and later on the refreshed presentation. Older recorded
  envelopes must remain readable.
- The smallest useful slice is an additive `music_state_id` on the live
  resolution envelope. The browser uses it when present and falls back to the
  existing visible classifier when it is absent or malformed.

## Assumptions

- Music IDs are presentation vocabulary and may be emitted by the host without
  entering simulation state, transition evaluation, stochastic input, history
  hashes, or debrief facts.
- The existing seven catalog IDs remain stable and their visible source,
  written equivalent, reduced-audio, and unavailable-audio policies remain
  authoritative.
- The current visible classifier's priority is a sufficient bounded contract
  for a committed resolution: completed transitions map to `debrief`, then
  visible regulatory/affiliation/competitive text, then reported pressure,
  then `stable_operations`.
- Full campaign music-state coverage, audio usefulness/fatigue, loudness,
  browser compatibility, and human evaluation remain separate gates.

## Minimal implementation plan

1. Add deterministic host-side music-state selection to
   `src/mcp/resolution.rs` using only `TransitionSummary`, the actor-visible
   after observation, and the committed terminal boundary; include the ID in
   `ResolutionEnvelope`.
2. Update the live resolution client with a pure helper that prefers a
   non-empty explicit host state and safely falls back to the existing
   visible-only classifier for legacy/malformed envelopes. Keep later
   presentation refreshes and optional audio behavior unchanged.
3. Add Rust and Node/Python tests covering every catalog state that the live
   resolution slice can select, deterministic priority, stable fallback,
   explicit/malformed/unknown state handling, and forbidden authority/network
   markers.
4. Update the roadmap evidence, coverage ledger, README/GUI README, SPEC,
   ARCHITECTURE, CHANGELOG, version projections, lessons, request/contract/QA/
   handoff artifacts, and generated release records.

## Files and functions likely to change

- `src/mcp/resolution.rs`: envelope field, visible music projection, and tests.
- `gui/app.mjs`: explicit host music preference in the resolution submission
  flow and a pure fallback helper.
- `tests/test_phase11_live_music.py`, `tests/test_gui_resolution.py`, and
  existing music/audio tests: focused contract evidence.
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`: bounded live
  music continuity surface and limits.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`, `SPEC.md`,
  `ARCHITECTURE.md`, `LESSONS.md`, and the roadmap: project records.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  and `_workspace/final/handoff.md`: durable handoffs.

## Tests and checks

- `python3 -m unittest tests/test_phase11_live_music.py tests/test_gui_resolution.py tests/test_gui_audio.py tests/test_music_stem_contract.py`
- `cargo fmt --check`
- `cargo test`
- `cargo clippy --all-targets -- -D warnings`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/check_documentation_links.py`
- `python3 scripts/validate_assets.py`
- `python3 scripts/verify_asset_release.py --check`
- `python3 scripts/generate_asset_credits.py --check`
- `python3 scripts/audit_visual_audio_contract.py`
- JavaScript syntax checks for changed modules.

Expected result: current host resolution envelopes carry one deterministic
catalog music ID, older envelopes still classify from visible data, and the
written resolution plus reduced/missing-audio fallbacks remain complete.

## Acceptance criteria

- `ResolutionEnvelope.music_state_id` is deterministic, one of the existing
  catalog IDs, and derived only from visible committed summaries/snapshots and
  the explicit terminal boundary.
- The browser prefers a valid explicit state, ignores malformed/unknown state
  values safely, and uses the existing classifier only when no usable field is
  present.
- Replaying the same resolution envelope yields the same music state; no
  state/hash/history/replay authority changes occur.
- Tests cover regulatory, affiliation, competitive, pressure, stable, and
  debrief states plus legacy/malformed/unknown fallback behavior.
- The roadmap records bounded live music-state evidence and keeps full campaign
  coverage, screenshots, performance, compatibility, and human gates open.

## Non-goals

- Do not add recorded audio, new assets, dependencies, event taxonomy,
  screenshots, save/load, or a new simulation mechanism.
- Do not infer private intent, event severity, causality, probability, or future
  outcomes from music IDs or textual matches.
- Do not mark broad Phase 11.1 music-state or full-campaign coverage complete.

## Stop conditions

- Stop if a state requires true state, hidden rival action, or unresolved event
  taxonomy rather than the visible transition summary/snapshot.
- Stop if the field changes state hashes, history, command validation, or
  deterministic transition evaluation.
- Stop if legacy envelopes lose written output or if the change broadens into
  new audio assets, screenshot, performance, or human-evaluation work.
