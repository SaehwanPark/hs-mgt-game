# Request Summary — Visual/audio Phase 11 first-session launch/load v0.12.27

## User request

Continue implementing the planned items in `SPEC.md` and
`docs/visual_audio_upgrade_proposal.md` through the repository workflow:
design the next bounded slice, implement it, perform exactly one general code
review, hand it off through a PR, merge `main`, and re-audit the remaining
SPEC queue.

## Current context

- Phase 10 accessibility and visual-language hardening is merged on `main` at
  `bcef897` as version `0.12.26`.
- The GUI already renders host-provided competitive presentation, regional
  world, action, resolution, campaign, audio, settings, and accessibility
  surfaces.
- The planned first competitive vertical slice still begins with “Start or
  load a campaign,” but the GUI assumes an adapter already owns `sessionId`.
- The existing MCP host already exposes `start_session`, which creates a
  session without advancing a turn and returns a session envelope.

## Selected bounded slice

Add a visible GUI session-launch boundary for
`competitive-regional-v1`: choose a seed and difficulty to call an optional
host adapter `startSession`, or enter an existing session ID to load through
the current read/action presentation path. The host remains authoritative for
session creation, scenario validation, observations, commands, transitions,
history, hashes, replay, and debriefs.

## User/use context

The primary user is a first-time executive player who opens the GUI without a
preconfigured session ID and needs a truthful path from campaign choice to the
first actor-visible briefing. Contributors and AI-agent testplay harnesses
need the same adapter boundary to remain explicit and inspectable.

## Scope

- Add semantic launch/load controls and status/recovery copy.
- Add the smallest browser adapter contract that maps to existing
  `start_session` inputs and the existing `getPresentation`/action reads.
- Replace the active adapter session ID after a successful start/load.
- Record only the existing visible session-loaded event after a successful
  presentation read.
- Add focused tests for start/load calls, malformed responses, failed starts,
  no-transition behavior, and session replacement.
- Bump version to `0.12.27` and update SPEC/design/architecture/handoff docs.

## Non-goals

- No Rust simulation or MCP schema change.
- No new campaign, scenario authoring, save persistence, auth, transport,
  network, browser automation, asset, audio-source, command, transition,
  stochastic, history/hash/replay, or debrief behavior.
- No local browser-owned session state or automatic first-month action.
- No claim that a launch flow establishes human usability or learning.

## Branch and workflow constraint

- Branch: `feat/visual-audio-phase11-session-launch-v0.12.27`.
- Exactly one general code-review pass is permitted for this item; fix its
  actionable findings and do not invoke a second pass.

## Validation target

Focused GUI/session-launch tests, full Python tests, Rust tests, formatting,
Clippy, Node syntax, release metadata, and diff checks must pass before PR
handoff. CI must pass before squash-merging `main`.
