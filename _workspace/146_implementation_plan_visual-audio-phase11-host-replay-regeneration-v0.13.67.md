# Implementation Plan — Host deterministic replay regeneration v0.13.67

## Target slice

Close the next explicit replay gate: deterministic host/core regeneration and
verification of the current competitive history from recorded explicit monthly
action batches, while preserving the existing visible replay route and browser
playback rail.

## Risk and scope

- Risk: medium. The change crosses the deterministic competitive resolution,
  host replay projection, and durable checkpoint-validation boundaries.
- In scope: a reusable deterministic month regeneration path, exact history
  verifier, existing replay-read verification, durable competitive-save reuse,
  tamper regression tests, and synchronized evidence/docs/version metadata.
- Out of scope: fresh AI decision search, new route/schema, browser
  regeneration, true-state/resolved-input exposure, save-format changes,
  autosave, simulation-rule changes, assets/audio, screenshots, human review,
  and public release.

## Design contract

1. The core regenerates each transition from the prior committed state, the
   seeded month-start inputs, and the recorded `AggregatedMonthlyActions`; this
   treats AI/player batches already recorded in immutable history as explicit
   replay inputs.
2. The regenerated transition must equal the recorded prior state, action
   batches, events, attributed effects, next state, consultant options, and
   state hash. Any mismatch fails closed with a written host error.
3. `get_replay` verifies competitive history before building the existing
   `competitive-replay-v1` summary. Durable competitive checkpoint validation
   calls the same verifier; no new persistence format or route is added.
4. The browser remains a read-only projection and local playback cursor. It
   receives no regenerated core fields and does not call transition, submit,
   AI, or random-input APIs.

## Implementation steps

1. Extract the deterministic competitive month-start/transition/institution
   phases into a reusable regeneration function and add a history verifier.
2. Call the verifier from the existing competitive replay read and durable
   save validation; preserve current error boundaries and schemas.
3. Add Rust tests for valid regeneration and tampering of action, prior,
   events/effects, next state, and hash; retain existing GUI replay/transport
   authority tests.
4. Update the Phase 11.1 ledger, roadmap, SPEC, changelog, lessons, guides/
   README if needed, request/contract/QA/handoff records, and version metadata.

## Verification and handoff

- `cargo fmt --check`, `cargo test`, and Clippy with warnings denied
- Focused Rust session/persistence/GUI transport and existing browser replay
  tests, then the full Python suite and all release/documentation/asset/device/
  offline/browser/audio/raster/loading/contract checks
- Exactly one medium-effort read-only code reviewer
- Commit, push, PR checks, merge to `main`, and local/remote branch cleanup

## Exit evidence

The existing replay endpoint must return the same visible rows for a valid
history only after host-side deterministic regeneration succeeds; a tampered
history or durable competitive checkpoint must be rejected without exposing a
partial regenerated trace or changing the browser authority boundary.
