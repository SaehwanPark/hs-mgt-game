# Implementation Plan — Visual/audio Phase 11.1 replay visual continuity v0.13.15

## Task restatement

Record and verify the existing live competitive replay metadata/history view as
a bounded Phase 11.1 replay visual-continuity item. The host already exposes
immutable visible transition summaries through `competitive-replay-v1`; the
browser validates and renders the text-first history/replay surface and keeps
the last valid view when a read fails. This slice adds explicit ledger and
parity evidence without claiming replay playback, regeneration, persistence,
or a new simulation path.

## Current understanding

- `src/mcp/session.rs` builds `ReplayEnvelope` from the host's immutable
  history through `get_replay`; it returns seed, transition count, latest hash,
  and visible transition rows without advancing the session.
- `src/mcp/server.rs` and `src/gui_server.rs` expose the read-only MCP and
  loopback replay routes; `gui/host-adapter.mjs` forwards `getReplay`.
- `gui/app.mjs` validates aligned replay metadata and renders the existing
  text-first history list, preserving the cached presentation on adapter
  failure and reporting a recoverable error.
- `tests/test_phase11_live_replay.py` covers host/route markers, empty and
  committed envelopes, hash/count alignment, missing/throwing adapters,
  rendering preservation, syntax, and authority exclusions.

## Target slice

Define `replay_view_coverage` for the current live host replay view:

- `competitive-replay-v1` metadata and immutable visible-row contract;
- MCP/loopback/adapter/browser source closure;
- seed, transition-count, latest-state-hash, and row alignment;
- text-first rendering and last-valid-view failure preservation; and
- explicit non-goals for playback, regeneration, persistence, screenshots,
  and human-learning claims.

## Assumptions

- The current replay view is a host-sourced metadata/history projection, not a
  playback engine or a regenerated simulation trace.
- The existing live replay test is sufficient evidence because it exercises
  both valid browser rendering and failed-read recovery without adding client
  authority.
- The immutable history source and existing Rust/MCP/transport tests remain the
  authority for row and hash alignment.

If the existing test does not directly cover a ledger field or boundary, add
only the smallest focused assertion required before closing the bounded item.

## Minimal implementation plan

1. Add `replay_view_coverage` to the Phase 11.1 campaign ledger with exact
   schema, host/MCP/route/adapter/browser sources, row/metadata contracts,
   visible behavior, and limits.
2. Extend `tests/test_phase11_campaign_coverage.py` to validate the ledger shape,
   link it to `tests/test_phase11_live_replay.py`, and require the playback,
   regeneration, persistence, and client-authority boundaries.
3. Update the roadmap checklist/status and add v0.13.15 evidence; synchronize
   `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LESSONS.md`, version metadata,
   and additive request/contract/QA/handoff records.
4. Run focused/full Python and Rust checks plus release/documentation, asset,
   offline, browser, device, and visual/audio contract checks.
5. Stop before adding playback controls, replay regeneration, durable storage,
   screenshot tooling, new runtime fields, or human evaluation.

## Files and functions likely to change

- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`.
- `tests/test_phase11_campaign_coverage.py` and, only if a gap is found,
  `tests/test_phase11_live_replay.py`.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  this plan, and `_workspace/final/handoff.md`.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `CHANGELOG.md`, `LESSONS.md`, `README.md`, `Cargo.toml`, `Cargo.lock`, and
  generated package-version projections.

Avoid changing Rust runtime, GUI, adapter, or asset behavior unless focused
inspection proves the existing contract is incomplete.

## Tests and checks

- `python3 -m unittest tests.test_phase11_live_replay`
- `python3 -m unittest tests.test_phase11_campaign_coverage`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt --check`
- `cargo test -- --test-threads=1`
- `cargo clippy --all-targets --all-features -- -D warnings`
- release, documentation, asset, offline, browser-policy, device-policy, and
  visual/audio contract checks.

## Acceptance criteria

- The ledger records current replay schema, host/MCP/route/adapter/browser
  sources, immutable row contract, count/hash alignment, visible rendering,
  and failure-preservation behavior.
- Coverage tests link the ledger to the live replay test and require no client
  playback/regeneration, hidden-state access, or simulation authority.
- The roadmap closes only current live replay visual continuity; playback,
  regeneration, persistence, screenshots, accessibility, usability, and
  learning remain open.
- Package version increments to v0.13.15 and generated metadata is consistent.

## Non-goals

- Do not add playback controls, replay regeneration, durable storage, browser
  serialization, new simulation fields, screenshots, assets, audio files,
  browser dependencies, telemetry, or human evaluation.
- Do not call aligned replay metadata/history a complete replay engine.

## Stop conditions

Stop if evidence requires a new transition, client-owned state, playback,
regeneration, durable serialization, or a claim beyond the tested host
projection boundary.

## Review checklist

- Schema, host/MCP/route/adapter/browser/test sources match exactly.
- Transition rows, count, and latest hash remain aligned to immutable host
  history.
- Valid replay renders through the existing text-first surface.
- Missing adapter, failed read, malformed metadata, and unsupported schema fail
  closed while preserving the last valid view.
- Playback, regeneration, persistence, screenshot, and human-quality limits are
  explicit in docs and ledger.
- No unrelated runtime, asset, audio, or simulation behavior changed.

## Risk label

Risk: low

Reason: The slice adds a read-only ledger contract and coverage assertions over
existing host replay behavior; no runtime or asset behavior is intended to
change.
