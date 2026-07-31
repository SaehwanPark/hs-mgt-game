# Implementation Plan — Full regional-affiliation checkpoint continuity v0.13.74

## Status

Implementation, full automated validation, and exactly one medium-effort
review are complete with no actionable findings; PR handoff, merge,
temporary-branch cleanup, and final evidence synchronization remain.

## Task restatement

Continue the visual/audio roadmap with a bounded host-persistence evidence
slice for `regional-affiliation-v1`: restore a stage-3 checkpoint in a fresh
host and prove deterministic continuation through the existing six-stage
endpoint.

## Current understanding

- The host already writes and verifies the `gui-affiliation-save-v1` wrapper
  around the existing `AffiliationReplayArtifact`.
- Existing regional-affiliation durable recovery saves after stage 1 and
  compares only the next transition hash; terminal continuity remains open.
- The browser remains opaque-ID-only and presentation-only; no new browser
  persistence or route is needed.

## Target slice

1. Commit `assess`, `posture choice=independent`, and `hold`, save after stage
   3, and load the checkpoint into a fresh host store.
2. Continue original and restored sessions with the existing `hold` path
   through stage 6 and require equal history, replay, and terminal
   `campaign-coverage-v1` envelopes.
3. Verify that ending the recovered session removes the matching checkpoint.
4. Record this bounded affiliation continuity in the Phase 11.1 ledger and
   synchronize request/contract/QA/handoff records, roadmap, SPEC, lessons,
   changelog, and version metadata to `0.13.74`.

## Non-goals

- No new route/schema, save format, simulation, stochastic input, asset/audio
  file, browser state artifact, screenshot, human review, or public-release
  claim.

## Acceptance criteria

- Stage-3 save/load restores the same envelope metadata and both sessions reach
  equal six-stage terminal history/replay and campaign-coverage data.
- The matching recovered checkpoint is removed after end-session cleanup.
- Focused/full validation, exactly one medium-effort review, PR merge, branch
  cleanup, and clean-main verification pass.

## Handoff requirements

After the sole reviewer approves, create and merge the PR into `main`, delete
the temporary branch locally/remotely, verify clean `main`, then design the
next unmet roadmap slice.
