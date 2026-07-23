# Phase 11.1 Live Debrief Handoff — Implementation Plan v0.12.91

## Task restatement

Close the next bounded Phase 11.1 continuity gap by making the host's final
competitive-session debrief available to the live browser together with the
immutable committed history and replay metadata that produced it.

## Current understanding

- `GameSessionStore::end_session` already owns terminal debrief generation and
  removes the mutable session from the store, but its DTO contains only the
  debrief lines and cannot support a continuity-preserving browser view.
- The loopback GUI server exposes presentation, action, resolution, and
  regional-world reads, but no terminal end-session route.
- `renderReadOnlyEnvelope` and `renderEnvelope` can show history/debrief lists,
  while the live adapter has no `endSession` method and the terminal view is
  currently represented as unavailable.
- The smallest useful slice is a terminal, text-first presentation envelope
  that carries host-provided history and replay metadata without recreating a
  competitive observation or allowing another command after termination.

## Assumptions

- Adding a versioned, serialized terminal envelope field set is compatible with
  the current MCP/GUI consumers because the existing end-session operation is
  already a typed response and the new fields are additive in purpose.
- `TransitionSummary` is the approved actor-visible history representation;
  the browser may render its command, events, effects, consultant options, and
  state hash but must not reconstruct true state from them.
- Calling end-session is intentionally terminal: the host removes the session,
  the browser disables action controls, and the final view remains available in
  local DOM memory only.
- This slice applies to the live competitive GUI endpoint. The shared host DTO
  retains complete summaries for all existing session campaigns so MCP callers
  do not lose terminal continuity.

## Minimal implementation plan

1. Extend `EndSessionEnvelope` with a stable schema version, terminal turn
   bounds, immutable transition summaries, and replay metadata; populate these
   fields from the session histories before returning the host debrief.
2. Add a loopback-only `POST /api/v1/sessions/{session_id}/end` route and
   `endSession` adapter method that forwards the host response without local
   state changes or retries that could duplicate termination.
3. Add a terminal browser renderer with explicit schema validation, history and
   debrief text, final hash/transition count, disabled action/session controls,
   written equivalents, and debrief music-state selection that remains
   optional and never carries meaning alone.
4. Add focused Rust, GUI transport, Node, and Python tests for the endpoint,
   terminal removal behavior, history/replay/debrief alignment, failure
   preservation, syntax, and forbidden hidden-state/network markers.
5. Update the roadmap evidence, coverage ledger, README/GUI README, SPEC,
   ARCHITECTURE, CHANGELOG, version projections, lessons, request/contract/QA/
   handoff artifacts, and registry hash projections.

## Files and functions likely to change

- `src/mcp/session.rs`: terminal DTO and history/replay population.
- `src/gui_server.rs`: end-session route and transport test.
- `gui/host-adapter.mjs`: `endSession` host call.
- `gui/app.mjs`: terminal envelope validation/rendering and client action.
- `gui/index.html`: explicit terminal debrief control.
- `gui/README.md`: adapter contract and terminal behavior.
- `tests/test_phase11_live_debrief.py`, `tests/test_gui_live_host.py`, and
  `tests/test_gui_live_read_only.py`: focused contract evidence.
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`: bounded
  continuity surface and limits.
- `assets/registry/visual-assets.json`, generated credits, and release
  projections: hashes for changed presentation files.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`, `SPEC.md`,
  `ARCHITECTURE.md`, `LESSONS.md`, and the roadmap: project records.
- `_workspace/00_input/request-summary.md`, `_workspace/02_presentation_contract.md`,
  `_workspace/03_presentation_qa.md`, and `_workspace/final/handoff.md`:
  durable handoffs.

## Tests and checks

- `python3 -m unittest tests/test_phase11_live_debrief.py tests/test_gui_live_host.py tests/test_gui_live_read_only.py`
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

Expected result: the terminal route returns a host-authored final envelope,
the browser displays aligned history/replay/debrief text, no command can be
submitted after termination, and all repository checks pass.

## Acceptance criteria

- Terminal history entries and `replay.transition_count` come from the same
  host history as the debrief; the latest hash is visible in the final view.
- The browser resolves only the declared terminal schema, keeps all meaningful
  content in text, and does not infer outcomes or private state.
- End-session failure leaves the current presentation/session active; a
  successful end-session disables action and repeated end controls.
- The GUI route remains loopback-only and the adapter adds no hidden fields,
  fetches, WebSockets, simulation imports, or client-side mutation.
- The roadmap records only bounded live terminal continuity evidence; full
  campaign screenshots, save/load, replay campaigns, performance,
  compatibility, and human gates remain open.

## Non-goals

- Do not add a save format, load implementation, new assets, audio files,
  screenshot tooling, browser dependencies, or simulation rules.
- Do not reconstruct observations, true state, causal graphs, rival state, or
  debrief facts in JavaScript.
- Do not mark the broad Phase 11.1 history/debrief/save-load/replay checklist
  complete from one live terminal path.
- Do not claim human accessibility, usability, audio, legal, or educational
  approval from automated checks.

## Stop conditions

- Stop if terminal continuity requires a new simulation state or a second
  debrief implementation.
- Stop if the GUI endpoint cannot preserve the host's terminal removal and
  structured error behavior.
- Stop if the change broadens into save/load, screenshot, or full-campaign
  architecture rather than the bounded terminal handoff.

## Review checklist

- The final DTO is host-authoritative and history/replay aligned.
- The browser's terminal view is text-complete, accessible by construction,
  and not color/audio dependent.
- Failed termination preserves the current session and successful termination
  cannot submit another turn.
- No private state, rival detail, local transition, or client authority is
  introduced.
- Documentation and registry hash projections match the final diff.
- One code-reviewer skill performs the required review passes; actionable
  findings are fixed before merge.

## Risk label

Risk: medium

Reason: this extends a terminal host DTO and adds a GUI mutation endpoint, but
the terminal transition already exists and no simulation authority changes.
