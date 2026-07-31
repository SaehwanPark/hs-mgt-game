# Implementation Plan — Cross-campaign checkpoint identity v0.13.75

## Status

Implementation, full automated validation, and exactly one medium-effort
review are complete with no actionable findings; PR handoff, merge,
temporary-branch cleanup, and final evidence synchronization remain.

## Task restatement

Close the remaining host-persistence boundary in the visual/audio roadmap:
prove that the single configured durable checkpoint path replaces older
campaign wrappers atomically and restores only the newest matching opaque
session ID across competitive, stabilization, and regional-affiliation hosts.

## Current understanding

- Competitive, stabilization, and regional-affiliation campaigns each have
  full-campaign checkpoint continuation regressions.
- The configured application path intentionally stores one latest checkpoint;
  existing tests cover same-campaign replacement and matching IDs but not a
  sequential cross-campaign replacement chain on fresh hosts.
- The browser remains opaque-ID-only and presentation-only; no multi-save
  archive or browser serialization is authorized.

## Target slice

1. Save one committed competitive checkpoint, replace it with stabilization,
   and prove a fresh host rejects the replaced competitive ID while restoring
   the matching stabilization ID.
2. Replace that checkpoint with regional affiliation, and prove another fresh
   host rejects the replaced stabilization ID while restoring only the matching
   affiliation ID and campaign wrapper.
3. End the recovered latest session and verify only the matching checkpoint is
   removed.
4. Record the bounded cross-campaign identity result in the Phase 11.1 ledger
   and synchronize request/contract/QA/handoff records, roadmap, SPEC, lessons,
   changelog, and version metadata to `0.13.75`.

## Non-goals

- No new route/schema, save format, simulation, stochastic input, asset/audio
  file, browser state artifact, archive, screenshot, human review, or
  public-release claim.

## Acceptance criteria

- Each fresh host observes `checkpoint_missing` for a replaced opaque ID and
  restores only the latest matching campaign wrapper.
- The latest loaded envelope reports the expected campaign and the matching
  checkpoint is removed after end-session cleanup.
- Focused/full validation, exactly one medium-effort review, PR merge, branch
  cleanup, and clean-main verification pass.

## Handoff requirements

After the sole reviewer approves, create and merge the PR into `main`, delete
the temporary branch locally/remotely, verify clean `main`, then design the
next unmet roadmap slice.
