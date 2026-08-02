# Implementation Plan — Progressive workspace navigation gating v0.14.4

## Narrow restatement and repository understanding

The GUI already maps host/session events to five task workspaces, but every
workspace navigation button is currently enabled from the initial Setup state.
This permits a user to open future empty sections before the host event that
makes those sections meaningful. The Rust host, routes, schemas, transitions,
and browser authority boundary must remain unchanged.

## Assumptions and stop conditions

- The current workspace event names and order remain the contract:
  `session_loaded`/`session_started` → Brief,
  `briefing_reviewed`/`decision_requested` → Decide,
  `transition_committed`/`resolution_loaded` → Resolve,
  `session_ended`/terminal load → Review.
- Previous workspaces remain reviewable and Setup remains available for a new
  start/load operation.
- If a caller requires a new event, a new workspace, or a host field, stop and
  report the conflict rather than adding a parallel state machine.

## Ordered implementation changes

1. Extend `gui/workspace.mjs` with an ordered unlock set. `goForEvent` unlocks
   the workspace selected by the existing event map before navigating; direct
   navigation refuses locked future workspaces and leaves the current workspace
   unchanged.
2. Keep navigation buttons native and accessible: set `disabled` and an
   `aria-label` that names the required visible handoff for locked stages; clear
   both when a stage becomes available. Do not disable primary handoff controls
   unless their existing flow controller already says they are not ready.
3. Add focused controller tests for initial locks, event unlock order, back
   navigation, terminal review unlock, and locked navigation non-mutation.
4. Add a small HTML/source contract assertion for native disabled semantics and
   update current GUI documentation and handoff artifacts.

## Public API and compatibility effects

No host route, DTO, schema, Rust API, persistence, replay, or command contract
changes. `createWorkspaceController` gains only browser-local controller state;
existing exported functions remain compatible.

## Verification and acceptance criteria

- `python3 -m unittest tests.test_gui_workspace tests.test_gui_static_desktop`
  and the relevant GUI source checks pass.
- `node --check gui/workspace.mjs` passes.
- `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`,
  documentation currentness/link checks, asset/security/release checks,
  browser/default-device/offline/loading/audio/raster/visual-audio checks pass.
- All three campaign paths still route only through host-backed events and can
  revisit completed workspaces without exposing future empty surfaces.

## Non-goals and handoff

Do not broaden into a redesign of the task rail, new browser engines, or human
evaluation. Commit, push, open the authorized PR, run one medium-effort review,
merge to `main`, remove the temporary branch locally and remotely, and update
the canonical docs plus `_workspace/final/handoff.md`.

## Risk

Low — browser-local navigation state only; the main risk is accidentally gating a
host event or primary handoff, covered by event-order and campaign-path tests.

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising.
