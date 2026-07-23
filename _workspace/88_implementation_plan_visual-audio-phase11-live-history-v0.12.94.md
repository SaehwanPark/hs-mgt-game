# Phase 11.1 Live History Handoff — Implementation Plan v0.12.94

## Task restatement

Advance the bounded Phase 11.1 history-view item by exposing a dedicated
host-owned live history envelope through the loopback GUI and rendering it
through the existing history surface. Preserve replay/hash authority in Rust
and keep save/load, replay regeneration, and full-campaign continuity open.

## Current understanding

- `GameSessionStore::get_history` already returns immutable transition
  summaries for every current campaign, but `src/gui_server.rs` does not expose
  it and `gui/host-adapter.mjs` has no `getHistory` method.
- `competitive-read-only-v1` and `competitive-end-session-v1` already contain
  history, while `gui/app.mjs` renders history through one existing
  `renderHistory` function without a dedicated history-envelope validator.
- The smallest useful slice is an additive `competitive-history-v1` schema,
  loopback `GET /api/v1/sessions/{session_id}/history`, adapter method, and
  browser validator/client that refreshes the existing history list after a
  successful live presentation refresh when the capability is available.
- The history read is non-mutating and must not create a second replay or
  simulation path; failed history reads must preserve the already-rendered
  presentation history.

## Assumptions

- `HistoryEnvelope.transitions` is the host's immutable committed summary list;
  each summary retains its existing state hash and visible source boundaries.
- A dedicated schema version is additive and does not alter transition hashes,
  replay verification, debrief generation, commands, or session state.
- The existing `renderHistory` text-first view is the approved visual surface;
  this slice adds transport/validation provenance rather than a new UI.
- Full campaign history continuity, replay playback/regeneration, save/load,
  screenshots, performance, browser compatibility, and human quality remain
  separate gates.

## Minimal implementation plan

1. Add `HISTORY_SCHEMA_VERSION` and `schema_version` to the host
   `HistoryEnvelope`; add the loopback history route and handler using the
   existing non-mutating `GameSessionStore::get_history` read.
2. Add `getHistory` to the local adapter and a pure browser
   `validateHistoryEnvelope`/`renderHistoryEnvelope`/`createHistoryClient`
   boundary. After a successful live presentation refresh, use the capability
   when present to refresh the existing history list; preserve the existing
   history when the endpoint is missing or fails.
3. Add Rust session/transport tests plus Node/Python tests for schema,
   transition-count/hash/text rendering, unknown-session errors, no mutation,
   missing-capability fallback, and forbidden authority/network markers.
4. Update the roadmap evidence, coverage ledger, README/GUI README, SPEC,
   ARCHITECTURE, CHANGELOG, version projections, lessons, request/contract/QA/
   handoff artifacts, and generated release records.

## Files and functions likely to change

- `src/mcp/session.rs`: history schema version and envelope field.
- `src/gui_server.rs`: loopback history route, handler, and transport test.
- `gui/host-adapter.mjs`: `getHistory` capability.
- `gui/app.mjs`: history schema, validator, client, render handoff, and public
  exports.
- `tests/test_phase11_live_history.py`, `tests/test_gui_resolution.py`, and
  existing GUI/session tests: focused contract evidence.
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`: bounded history
  continuity surface and limits.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`, `SPEC.md`,
  `ARCHITECTURE.md`, `LESSONS.md`, and the roadmap: project records.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  and `_workspace/final/handoff.md`: durable handoffs.

## Tests and checks

- `python3 -m unittest tests/test_phase11_live_history.py tests/test_gui_resolution.py tests/test_gui_live_read_only.py`
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

Expected result: a current live adapter can obtain host-committed history
through one non-mutating route and the browser can validate/render it without
losing its existing history when the capability is unavailable or fails.

## Acceptance criteria

- `HistoryEnvelope.schema_version` is `competitive-history-v1`, transition
  count equals the host transition list length, and each visible summary/hash
  is rendered text-first.
- The GUI route performs only `GameSessionStore::get_history`; unknown sessions
  return the existing structured 404 error and history reads do not advance a
  session.
- The browser uses the dedicated history capability when present, retains the
  presentation-provided history on missing/failing reads, and does not create
  a replay or simulation client path.
- Tests cover one committed live turn, count/hash alignment, route transport,
  unknown session, fallback capability, syntax, and authority boundaries.
- The roadmap records bounded live history handoff evidence and keeps full
  campaign history/debrief/save-load/replay, screenshots, performance,
  compatibility, and human gates open.

## Non-goals

- Do not add replay regeneration/playback, save/load, new state hashes,
  debrief synthesis, transition logic, new assets, screenshots, or a second
  simulation path.
- Do not expose hidden rival state or true state through history.
- Do not mark the broad Phase 11.1 history, debrief, save/load, replay, or
  full-campaign continuity checklist complete.

## Stop conditions

- Stop if history requires hidden state, mutable client reconstruction, or a
  new replay authority rather than existing committed summaries.
- Stop if the route mutates session state, changes hashes, or creates a second
  command/transition path.
- Stop if endpoint failure replaces or clears already-visible host history, or
  if the change broadens into save/load, replay, screenshot, or performance
  work.
