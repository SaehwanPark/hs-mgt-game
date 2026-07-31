# Implementation Plan — Full stabilization checkpoint continuity v0.13.73

## Status

Implementation, full validation, and exactly one medium-effort review are
complete; PR handoff, merge, temporary-branch cleanup, and final evidence
synchronization remain.

## Task restatement

Continue the visual/audio roadmap with a bounded host-persistence evidence
slice for `stabilization-v1`: restore a stage-2 checkpoint in a fresh host and
prove deterministic continuation through the existing five-stage endpoint.

## Current understanding

- The host already writes/verifies the stabilization save wrapper and exposes
  `competitive-replay-v1`-shaped history/replay metadata plus the typed
  `campaign-coverage-v1` read.
- Existing stabilization durable recovery tests save after stage 1 and compare
  only the next transition hash; cross-stage terminal parity remains open.
- The browser remains opaque-ID-only and presentation-only; no new browser
  persistence or route is needed.

## Target slice

1. Save `stabilization-v1` after stage 2, load it into a fresh host store, and
   continue both original/restored sessions through stage 5.
2. Require equal terminal replay/history metadata and campaign-coverage
   envelopes, plus matching checkpoint cleanup after the recovered session
   ends.
3. Record this bounded stabilization continuity in the Phase 11.1 ledger and
   keep browser serialization, affiliation continuity, screenshots, human
   review, and release gates open.
4. Synchronize request/contract/QA/handoff records, roadmap, SPEC, lessons,
   changelog, and version metadata to `0.13.73`.

## Non-goals

- No new route/schema, save format, simulation, asset/audio file, browser state
  artifact, screenshot, human review, or public-release claim.

## Acceptance criteria

- Stage-2 save/load restores the same envelope metadata and both sessions reach
  equal five-stage terminal replay/history and campaign-coverage data.
- The matching recovered checkpoint is removed after end-session cleanup.
- Focused/full validation, exactly one medium-effort review, PR merge, branch
  cleanup, and clean-main verification pass.

## Handoff requirements

After the sole reviewer approves, create and merge the PR into `main`, delete
the temporary branch locally/remotely, verify clean `main`, then design the
next unmet roadmap slice.
