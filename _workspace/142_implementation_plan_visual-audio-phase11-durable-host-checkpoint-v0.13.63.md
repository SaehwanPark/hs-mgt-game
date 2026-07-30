# Implementation Plan — Durable host checkpoint recovery v0.13.63

## Target slice

Close the next narrow Phase 11.1 technical boundary: an explicitly saved
`competitive-regional-v1` checkpoint survives a stopped/restarted loopback GUI
host and can be recovered by the existing browser session handle.

## Risk and scope

- Risk: medium. The slice crosses file I/O, session reconstruction, and browser
  recovery, but it reuses the existing typed competitive save artifact and
  keeps the transition core unchanged.
- In scope: host-owned durable checkpoint wrapper with session identity,
  default GUI save path, competitive-session reconstruction after restart,
  automatic browser retry through the existing `loadSession` route when a
  stored ID is no longer live, focused Rust/Node/Python boundary tests, and
  synchronized evidence/docs/version metadata.
- Out of scope: stabilization/affiliation durable saves, browser
  serialization of state or commands, autosave, service workers, replay
  playback/regeneration, new assets/audio, full-campaign placement/screenshots,
  human accessibility/educational/legal/provenance review, and public release.

## Design contract

1. `CompetitiveSessionSave` remains the canonical serialized true-state
   artifact. A host-only wrapper adds the opaque session ID and a GUI-save
   schema marker; the wrapper is never returned to the browser.
2. The GUI host writes only after an explicit `save_session` request. The
   default path is inside the existing application config directory, and the
   write is replaced as one host-owned file operation.
3. A restarted host may hydrate the saved competitive session only when the
   requested session ID matches the durable wrapper. Hydration restores the
   immutable history, current world, prior aggregated actions, and done flag;
   no new transition is entered and no stochastic input is regenerated.
4. Existing live in-memory checkpoint behavior remains unchanged. A live
   session is preferred; durable hydration is attempted only after the normal
   session read reports an unknown session. Missing or malformed files remain
   written, recoverable errors and never create a replacement session.
5. Browser storage continues to hold only the opaque session ID. Browser
   recovery calls host `loadSession`, then repeats the existing actor-visible
   reads. No true state, resolved input, command, history payload, or hash is
   serialized in JavaScript.

## Implementation steps

1. Add host persistence helpers and a `GameSessionStore` constructor/path
   boundary that can serialize and reconstruct competitive checkpoints.
2. Wire the loopback GUI server to the default host-owned path while leaving
   test routers and MCP default stores in-memory unless explicitly configured.
3. Extend the action client’s unknown-session recovery to try the explicit
   host load route once, then re-enter the current read path.
4. Add focused restart/hash/continuation tests and update existing source
   boundary tests for the durable-vs-browser authority distinction.
5. Update the Phase 11.1 ledger, roadmap, GUI guide/README, SPEC, CHANGELOG,
   LESSONS, request/contract/QA/handoff records, and all release metadata to
   v0.13.63.

## Verification and handoff

- `cargo fmt --check`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
- focused durable-session Rust/GUI tests and Node/Python recovery tests
- full Python suite plus release metadata, docs links, assets/security/
  generation/credits, offline/browser/device, visual/audio contract, and diff
  checks
- exactly one medium-effort read-only code reviewer
- commit, push, draft-to-ready PR, hosted checks, merge to `main`, and delete
  the temporary branch locally and remotely

## Exit evidence

The technical boundary is complete only when a new store process recovers the
same saved session ID, transition count, latest hash, visible presentation,
and deterministic next-month result from the host file, while a missing or
invalid file cannot mutate browser state or create an unknown session.
