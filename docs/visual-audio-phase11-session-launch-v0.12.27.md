# Visual/audio Phase 11 — First-session launch and load boundary

**Status:** Implemented, verified, reviewed once, and merged in PR #178
**Scope:** Host-authoritative competitive session start/load handoff
**Version:** 0.12.27

## Purpose

The first competitive vertical slice begins with starting or loading a campaign,
but the current GUI assumes a preconfigured adapter `sessionId`. This phase adds
the smallest visible handoff from a first-time executive's setup choice to the
existing actor-visible presentation.

## User contract

- Choose the fixed `competitive-regional-v1` campaign.
- Choose a finite seed, defaulting to 42.
- Choose host-supported difficulty: Easy, Normal, Hard, or Expert.
- Start through an optional adapter method that maps to the existing host
  `start_session` operation.
- Or enter an existing session ID and load it through the current presentation
  or action client.
- Continue into the existing briefing, regional market, player/facility detail,
  action, resolution, audio, history, and debrief surfaces.

## Adapter boundary

The optional browser adapter method is:

```js
async startSession({
  campaign: "competitive-regional-v1",
  seed: 42,
  difficulty: "normal",
}) {
  // Map to the existing MCP start_session request and return its envelope.
}
```

The response must expose a non-empty `session_id`. The GUI then calls its
existing `getPresentation(sessionId)` or action-client equivalent. The method
does not replace or extend the MCP `StartSessionRequest` or `SessionEnvelope`.

## Authority and failure behavior

The host owns campaign parsing, difficulty/scenario validation, session
allocation, initial state, observations, commands, transitions, stochastic
inputs, history, replay hashes, and debriefs. The browser owns only form,
pending, recovery, and currently selected session-ID presentation state.

Invalid setup is rejected before the adapter call. Missing start capability,
adapter failure, malformed response, empty session ID, and failed replacement
presentation load are visible and recoverable. A failed replacement load keeps
the current rendered session and never calls `submitTurn`.

## Verification and limits

Focused tests cover setup normalization, start/load calls, session replacement,
malformed and failed responses, adapter capability gaps, no-transition
boundaries, and compatibility with the existing static fixture: 17 focused
tests pass. The full Python suite has 294 passing tests; Rust, formatting,
Clippy, Node syntax, release metadata, and diff checks pass. These are
technical interface proxies only; they do not establish browser transport
correctness, human usability, accessibility, learning, or policy validity.

## Deferred work

- No scenario picker, saved-session browser, authentication, web transport,
  persistence, campaign expansion, auto-action, asset, or audio change.
- No first-month strategy recommendation or claim that launch improves learning
  or onboarding for human players.
