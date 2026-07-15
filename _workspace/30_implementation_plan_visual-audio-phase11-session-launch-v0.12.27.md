# Operational Plan — Visual/audio Phase 11 first-session launch/load v0.12.27

**Status:** Implemented and verified; one code-review pass complete; PR/CI/merge pending

## Task restatement

Add a host-authoritative GUI boundary that lets a user start a new
`competitive-regional-v1` session with seed/difficulty controls or load an
existing session ID, then reuse the current presentation/action client paths.
Do not add a browser simulation or change host/MCP schemas.

## Current understanding

- `gui/index.html` has onboarding/settings/readiness controls but no session
  launch form.
- `createReadOnlyClient` and `createActionClient` each have a `load(sessionId)`
  path and currently default to `adapter.sessionId`.
- `src/mcp/session.rs` already implements `start_session` with campaign, seed,
  difficulty, and scenario-path validation and returns a `SessionEnvelope`.
- Existing `renderReadOnlyEnvelope`, regional-world, campaign-coverage,
  resolution, audio, and capture paths can be reused after a session ID is
  established.

## Assumptions

- A browser adapter may optionally expose `startSession(options)` as a thin
  mapping to existing `start_session`; the GUI must work without it by showing
  a capability message.
- Start responses expose a non-empty `session_id`; the presentation read is
  still required before the GUI treats the session as loaded.
- The client can keep the current view until the new session's presentation
  has loaded successfully.
- If these assumptions fail or require Rust/MCP schema changes, stop and report
  the mismatch.

## Minimal implementation plan

1. Add a semantic session-launch panel with campaign (fixed competitive target),
   seed, difficulty, Start, existing-session ID, and Load controls plus status.
2. Add one small shared launcher helper in `gui/app.mjs` that validates setup,
   calls optional `adapter.startSession`, and invokes a client-owned load
   callback only after a valid `session_id` is returned.
3. Wire both read-only and action clients through the helper so replacement
   session IDs refresh all existing presentation/action/regional/campaign
   surfaces without duplicating host logic.
4. Preserve current adapter-missing, schema-error, and recovery behavior; never
   call `submitTurn` during launch/load.
5. Add focused tests for valid start/load, invalid seed/difficulty, missing
   start capability, malformed response, failed refresh preserving the current
   view, and no-transition boundary strings.
6. Update SPEC, the Phase 11 protocol/design docs, architecture, README/GUI
   guide, changelog, lessons, metadata, QA, and handoff.

## Files and functions likely to change

- `gui/index.html`: session-launch semantic panel and controls.
- `gui/app.mjs`: shared launch helper, `createReadOnlyClient`,
  `createActionClient`, and client exports if needed.
- `tests/test_gui_session_launch.py`: focused static and Node contract tests.
- `docs/visual-audio-phase11-session-launch-v0.12.27.md` and aligned project
  docs/metadata.
- Do not change `src/`, `gui/audio.mjs`, `gui/playtest.mjs`, or MCP DTOs unless
  discovery proves the adapter contract cannot map to existing host behavior.

## Tests and checks

- `python3 -m unittest tests.test_gui_session_launch`.
- Existing GUI tests and release metadata tests.
- `python3 -m unittest discover -s tests -p 'test_*.py'`.
- `node --check gui/app.mjs gui/audio.mjs gui/playtest.mjs`.
- `cargo fmt -- --check`, `cargo test --all -- --test-threads=1`, and
  `cargo clippy --all-targets -- -D warnings`.
- `python3 scripts/check_release_metadata.py` and `git diff --check`.

## Acceptance criteria

- A user can choose the fixed competitive campaign, finite seed, and allowlisted
  difficulty, then invoke an optional host `startSession` adapter exactly once.
- The GUI accepts a returned host `session_id`, loads the existing typed
  presentation, and refreshes current read/action/regional/campaign surfaces.
- A user can load a non-empty existing session ID through the current read path.
- Invalid setup, missing capability, malformed response, start failure, and
  presentation failure are visible and recoverable; the previous view remains
  intact when replacement loading fails.
- No launcher or load path calls `submitTurn`, creates a local transition,
  changes history/hash/replay/debrief, or exposes hidden state.
- Existing no-adapter demo fixture and all Phase 10 accessibility behavior
  remain available.

## Non-goals

- No new Rust/MCP schema, web transport, authentication, persistence, scenario
  picker, campaign expansion, first-month auto-action, asset, audio, or
  simulation change.
- No automatic optimization, difficulty recommendation, seed ranking, or
  educational/human-usability claim.
- No opportunistic refactor of client loading or adapter error handling beyond
  the named shared helper.
- Do not run a second general code-review pass; exactly one is required.

## Stop conditions

- Stop if the host start operation cannot be represented by the existing MCP
  `StartSessionRequest`/`SessionEnvelope` boundary.
- Stop if session replacement requires a new public DTO, persistence layer,
  browser transport, or simulation state.
- Stop if read-only and action clients require incompatible launch semantics
  that cannot be handled by one small helper/callback.
- Stop if unrelated existing GUI tests fail without a direct relation to the
  launch/load behavior.

## Review checklist

- Only the fixed competitive campaign is startable; no unsupported campaign or
  scenario semantics are invented.
- Start/load uses host session IDs and typed presentation reads, not fixtures or
  locally reconstructed state.
- Failed replacement loads preserve the current view and do not mutate host
  state.
- `submitTurn`, transition, stochastic, history, hash, replay, and debrief
  paths remain untouched.
- Tests cover malformed/missing/failed adapter responses and capability gaps,
  not only the happy path.
- The change remains compatible with no-adapter demo mode and Phase 10
  keyboard/status/settings behavior.

## Risk label

Risk: medium

Reason: The change coordinates multiple existing GUI clients and introduces a
new optional adapter capability, but it reuses the existing host session
operation and does not alter simulation or public MCP DTOs.
