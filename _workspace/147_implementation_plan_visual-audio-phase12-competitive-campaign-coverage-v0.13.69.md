# Implementation Plan — Competitive campaign-coverage envelope v0.13.69

## Task restatement

Expose `competitive-regional-v1` through the existing host-owned
`campaign-coverage-v1` read projection so the shared visual/audio coverage
contract covers all three launchable campaigns, while preserving the existing
competitive action-catalog → validation → submit mutation path.

## Current understanding

- `src/mcp/session.rs` already owns the typed campaign-coverage route for
  stabilization and regional affiliation, but rejects competitive sessions.
- `src/mcp/presentation.rs` and `src/sim/observe_competitive.rs` already define
  the actor-visible competitive observation needed for a coverage projection.
- `src/mcp/action.rs` already defines the canonical competitive action catalog.
- `gui/app.mjs` already renders the generic campaign-coverage envelope and keeps
  competitive mutation on its richer action client.
- `src/mcp/campaign_coverage.rs` already owns the shared schema, audio metadata,
  sanitized coverage history summaries, and terminal debrief fields.

## Target slice

1. Add a `from_competitive` builder that projects only the human player’s
   `PlayerObservation`, player resources, current public campaign signals,
   public process/status summaries, canonical action-catalog decisions,
   sanitized public-action history summaries, a player-safe terminal debrief,
   and existing audio metadata into `campaign-coverage-v1`.
2. Connect the builder to `GameSessionStore::get_campaign_coverage` and allow
   competitive sessions through the loopback GUI campaign-coverage launch
   boundary.
3. Keep `gui/app.mjs`’s competitive action client unchanged: campaign coverage
   is a typed read projection; competitive commands still require the existing
   catalog and host validation before `submitTurn`.
4. Update the Phase 12 and Phase 13.1 evidence ledgers, roadmap, SPEC,
   contracts, guide/README-facing records, lessons, and package version to
   `0.13.69`.

## Assumptions and stop conditions

- The existing `campaign-coverage-v1` schema is sufficient; no new route,
  field, dependency, save format, or browser authority is required.
- `observe_for_human` remains the only source for competitive actor-visible
  observations. Do not read rival private metrics, `effect_queue`, resolved
  inputs, or true state into the envelope.
- The action catalog remains the canonical decision source. If its parameter
  contract cannot be mapped into the existing coverage decision shape without
  changing either schema, stop and report the conflict.
- If making competitive coverage the default GUI action rail would bypass host
  validation or require a second mutation protocol, do not broaden the slice;
  retain the existing competitive action rail and document the read-only
  coverage boundary.

## Minimal implementation plan

1. Add `from_competitive` and small private conversion helpers in
   `src/mcp/campaign_coverage.rs`; derive metrics, briefings, actor/process
   summaries, decisions, replay metadata, and debrief from existing typed
   sources.
2. Add the competitive branch in `src/mcp/session.rs`, update the GUI campaign
   allowlist in `src/gui_server.rs`, and add focused Rust tests for active,
   terminal, actor-visible, and no-mutation behavior.
3. Update the Phase 12/13.1 Python contract tests and ledgers, plus the
   campaign-coverage test fixture/launcher markers needed to prove competitive
   read availability without moving competitive mutations to the shared rail.
4. Synchronize package version, changelog, roadmap, SPEC, lessons, guide and
   `_workspace` request/contract/QA/handoff records.
5. Run focused tests, full Rust/Python/repository checks, then perform exactly
   one medium-effort code review before PR handoff. The sole reviewer approved
   the final implementation after the history and terminal-debrief fixes.

## Likely files and functions

- `src/mcp/campaign_coverage.rs`: `from_competitive`, action-parameter
  conversion, visible competitive actor/process/briefing helpers.
- `src/mcp/session.rs`: competitive `get_campaign_coverage` branch and Rust
  coverage tests.
- `src/gui_server.rs`: include `competitive-regional-v1` in the existing
  campaign-coverage allowlist.
- `tests/test_phase12_live_campaign_coverage.py`,
  `tests/test_phase13_1_competitive_campaign_boundary.py`,
  `tests/test_phase11_campaign_coverage.py`, and
  `tests/test_gui_campaign_coverage.py`: evidence and authority contracts.
- `docs/evaluation/phase12-live-campaign-coverage.json`,
  `docs/evaluation/phase13.1-competitive-campaign-boundary.json`, and
  `docs/evaluation/phase11.1-campaign-coverage-ledger.json`: evidence state.
- `gui/index.html`, `docs/guides/gui-how-to-play.md`, `README.md`,
  `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`, `SPEC.md`,
  `docs/visual_audio_enhancement_roadmap.md`, `LESSONS.md`, and `_workspace/*`:
  synchronized project records only.

## Public/API and compatibility effects

The existing `campaign-coverage-v1` schema, route, and adapter remain stable.
The route gains a supported competitive response; no serialized field or
mutation API changes. Competitive action submissions, validation errors,
history, replay, checkpoint, and debrief behavior must remain unchanged.

## Tests and checks

- Rust: focused campaign-coverage tests, `cargo fmt --check`,
  `cargo test -- --test-threads=1`, and `cargo clippy --all-targets -- -D warnings`.
- Python/Node/repository: focused Phase 11/12/13.1 and GUI tests, then
  `python3 -m unittest discover -s tests -p 'test_*.py'` and the existing
  release/docs/assets/device/offline/browser/audio/raster/loading/visual-audio
  checks.

## Acceptance criteria

- A competitive host session returns `campaign-coverage-v1` with campaign ID,
  24-month stage metadata, visible metrics/briefings, canonical decisions,
  history/replay metadata, and optional terminal debrief/audio.
- The projection contains no true-state or browser-authority markers and does
  not advance history when read; competitive history excludes private rival
  events/effects and retains only public-action summaries, while terminal
  debrief omits instructor-only rival actions, rationales, and deltas.
- The loopback GUI accepts the competitive coverage read while competitive
  decisions still use action-catalog validation and host submit.
- Evidence documents and version metadata state the new bounded capability and
  preserve remaining visual, human, device, provenance, and release gates.

## Non-goals

- Do not replace the competitive action rail with campaign coverage.
- Do not add browser simulation, hidden-state fields, rival private metrics,
  resolved-input disclosure, replay regeneration, persistence, assets, audio
  files, screenshots, human evaluation, or public-release approval.
- Do not refactor unrelated campaign builders or introduce dependencies.

## Handoff requirements

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising. Report files
changed, tests run, deviations, and unresolved risks. After the sole review is
approved, create the PR, merge it into `main`, delete the temporary branch
locally and remotely, verify clean `main`, then design the next unmet slice.

## Risk

Risk: medium — the shared typed read contract gains a third campaign consumer,
so actor-visible mapping and compatibility assertions must remain exact while
competitive mutation authority stays separate.
