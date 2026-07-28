# Implementation Plan — Visual/audio Phase 11.1 checkpoint continuity v0.13.14

## Task restatement

Record and verify the current in-memory host checkpoint save/restore view as a
bounded Phase 11.1 save/load visual-continuity item. Existing behavior stores a
host-owned snapshot, returns `competitive-save-v1` metadata, restores the
session without a new transition, and refreshes actor-visible presentation.
This slice adds explicit ledger and parity evidence without claiming durable
file persistence, cross-process recovery, or browser-refresh continuity.

## Current understanding

- `src/mcp/session.rs` stores one cloned `GameSession` checkpoint per active
  session and restores it through host-owned `save_session`/`load_session`.
- `src/mcp/server.rs`, `src/gui_server.rs`, and `gui/host-adapter.mjs` expose
  the loopback/MCP boundary; the browser never serializes true state.
- `gui/app.mjs` validates save metadata, refreshes presentation after a
  successful restore, keeps action controls host-gated, and preserves the
  current view on adapter/refresh failure.
- `tests/test_phase11_live_checkpoint.py` covers schema/operation/hash/count,
  adapter save/load, refresh, missing adapter, controls/routes, syntax, and
  authority exclusions.

## Target slice

Define `checkpoint_view_coverage` for the current in-memory host checkpoint:

- `competitive-save-v1` saved/loaded envelope and loopback/MCP sources;
- host snapshot ownership and restore without a new transition;
- transition-count/latest-hash alignment;
- browser refresh and visible-control continuity after restore; and
- explicit durable-persistence and cross-process/browser-refresh limits.

## Assumptions

- The current in-memory checkpoint is the authoritative bounded save/load view
  for this milestone; a durable save format is a separate roadmap slice.
- `tests/test_phase11_live_checkpoint.py` is sufficient evidence because it
  exercises host markers and browser adapter behavior without starting a client
  state store.
- A successful load refresh is presentation continuity, not replay regeneration
  or a new simulation transition.

If the test does not directly cover a stated contract, add only the smallest
focused assertion required before closing the bounded item.

## Minimal implementation plan

1. Add `checkpoint_view_coverage` to the Phase 11.1 campaign ledger with exact
   schema, host/MCP/route/adapter/browser sources, metadata contracts, refresh
   behavior, and limits.
2. Extend `tests/test_phase11_campaign_coverage.py` to validate the ledger shape,
   link it to `tests/test_phase11_live_checkpoint.py`, and require the authority
   and durable-persistence boundaries.
3. Update roadmap checklist/status and add v0.13.14 evidence; synchronize
   `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LESSONS.md`, version metadata,
   and additive request/contract/QA/handoff records.
4. Run focused/full Python and Rust checks plus release/documentation, asset,
   offline, browser, device, and visual/audio contract checks.
5. Stop before adding durable file persistence, browser serialization, replay
   playback/regeneration, new runtime fields, screenshots, or human evaluation.

## Files and functions likely to change

- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`.
- `tests/test_phase11_campaign_coverage.py` and, only if a gap is found,
  `tests/test_phase11_live_checkpoint.py`.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  `_workspace/108_implementation_plan_visual-audio-phase11-save-load-v0.13.14.md`,
  and `_workspace/final/handoff.md`.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `CHANGELOG.md`, `LESSONS.md`, `README.md`, `Cargo.toml`, `Cargo.lock`, and
  generated package-version projections.

Avoid changing Rust runtime, GUI, adapter, or asset behavior unless focused
inspection proves the existing contract is incomplete.

## Tests and checks

- `python3 -m unittest tests.test_phase11_live_checkpoint`
- `python3 -m unittest tests.test_phase11_campaign_coverage`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt --check`
- `cargo test -- --test-threads=1`
- `cargo clippy --all-targets --all-features -- -D warnings`
- release, documentation, asset, offline, browser-policy, device-policy, and
  visual/audio contract checks.

## Acceptance criteria

- The ledger records current checkpoint schema, host/MCP/route/adapter/browser
  sources, snapshot/restore contract, count/hash alignment, refresh behavior,
  and failure limits.
- Coverage tests link the ledger to the live checkpoint test and require no
  browser-side simulation/state serialization or client authority.
- The roadmap closes only current in-memory checkpoint visual continuity;
  durable save/load, cross-process/browser-refresh recovery, replay continuity,
  screenshots, accessibility, usability, and learning remain open.
- Package version increments to v0.13.14 and generated metadata is consistent.

## Non-goals

- Do not add a durable file format, browser storage, cross-process recovery,
  replay regeneration/playback, new simulation fields, screenshots, assets,
  audio files, browser dependencies, telemetry, or human evaluation.
- Do not call a host checkpoint a complete save/load release feature.

## Stop conditions

Stop if evidence requires client-owned state, durable serialization, a new
transition, replay regeneration, or a claim beyond the tested in-memory host
session boundary.

## Review checklist

- Schema, host/MCP/route/adapter/browser/test sources match exactly.
- Save/load metadata remains aligned to committed transition count/latest hash.
- Restore refreshes visible presentation without entering a new transition.
- Missing adapter, missing checkpoint, malformed metadata, and refresh failure
  remain recoverable and preserve the current view.
- Durable-persistence and cross-process limits are explicit in docs and ledger.
- No unrelated runtime, asset, audio, or simulation behavior changed.

## Risk label

Risk: low

Reason: The slice adds a read-only ledger contract and coverage assertions over
existing host checkpoint behavior; no runtime or asset behavior is intended to
change.
