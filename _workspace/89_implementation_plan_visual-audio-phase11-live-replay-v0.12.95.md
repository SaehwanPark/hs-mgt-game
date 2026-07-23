# Implementation Plan — Visual/audio Phase 11.1 live replay continuity v0.12.95

## Target slice

Add a dedicated, host-shaped replay continuity handoff for the live
`competitive-regional-v1` GUI. The slice is limited to replay metadata and the
same immutable actor-visible transition summaries already used by history; it
does not regenerate outcomes or add persistence.

## Evidence and constraints

- `GameSessionStore::get_history` is already a non-mutating source of visible
  transition summaries and hashes.
- `get_resolution(session_id, turn?)` already provides historical committed
  resolution views, but the live adapter has no explicit replay envelope.
- The browser history surface already presents turn, command, and state-hash
  text and must remain the meaning-bearing replay surface.
- Replay metadata must remain outside simulation state, transition hashes,
  stochastic inputs, hidden rival state, and client authority.
- Full save/load persistence, replay regeneration, playback simulation,
  screenshot suites, performance, compatibility, and human evaluation are
  separate roadmap gates.

## Host/core changes

1. Add `REPLAY_SCHEMA_VERSION = "competitive-replay-v1"` and a serializable
   `ReplayEnvelope` containing session/campaign identity, seed, transition
   count, latest visible state hash, and immutable `TransitionSummary` values.
2. Add `GetReplayRequest` and `GameSessionStore::get_replay`, implemented as a
   read-only projection over the existing history source.
3. Expose the read through the MCP server and loopback
   `GET /api/v1/sessions/{session_id}/replay` route.

## Browser changes

1. Add `getReplay` to the local host adapter.
2. Add strict replay-envelope validation for schema, identity, count, and
   latest-hash alignment; reject malformed envelopes without clearing the
   current history.
3. Add a small `createReplayClient` and render helper that use the existing
   text-first committed-history list and metadata, without local replay
   calculation or transition calls.
4. Refresh the replay projection after successful live presentation reads and
   expose the client for host-integrated tests and future playback controls.

## Tests and records

- Rust session, MCP/transport, and hash/count alignment assertions.
- Node/Python validation, render, failure-preservation, syntax, and authority
  boundary tests in `tests/test_phase11_live_replay.py`.
- Update the roadmap, coverage ledger, SPEC, architecture, README, GUI
  adapter contract, lessons, QA, handoff, changelog, version projections, and
  generated credits.

## Explicit non-goals

- No save/load files, replay regeneration, client-side simulation, random
  inputs, hidden-state projection, browser-authored hashes, new assets/audio,
  or full-campaign continuity claim.

## Verification gate

Run `cargo fmt`, `cargo test`, Python discovery, Clippy with warnings denied,
release/documentation/asset/security/generation checks, and the visual/audio
contract audit before one code-reviewer handoff. Merge the temporary branch to
`main`, delete it locally and remotely, then re-audit the next roadmap gap.
