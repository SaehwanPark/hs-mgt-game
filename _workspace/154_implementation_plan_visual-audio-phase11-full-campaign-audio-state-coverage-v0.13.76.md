# Implementation Plan — Full-campaign audio-state coverage v0.13.76

## Task restatement

Continue the visual/audio roadmap with a bounded host-source evidence slice:
prove that all three launchable campaigns provide valid audio metadata on every
active and terminal `campaign-coverage-v1` read through their full endpoints.

## Current understanding

- The host already derives optional campaign music and event-cue IDs from
  visible stage, process, actor, and committed history summaries.
- Existing tests cover representative stabilization, affiliation, competitive,
  and registry mappings but do not walk every stage/month through terminal
  coverage for all launchable campaigns.
- The browser renders supplied metadata and existing written equivalents; no
  client classification or new audio asset is authorized.

## Target slice

1. Walk competitive (24 months), stabilization (5 stages), and
   regional-affiliation (6 stages) through their existing host sessions.
2. Read `campaign-coverage-v1` before and after every committed transition,
   require optional audio metadata, allowlisted music/cue IDs, and terminal
   `debrief` music state.
3. Record this bounded full-campaign audio-state result in the Phase 11.1
   ledger and synchronize request/contract/QA/handoff records, roadmap, SPEC,
   lessons, changelog, and version metadata to `0.13.76`.

## Non-goals

- No new route/schema, simulation, stochastic input, browser authority, asset,
  audio file, screenshot, human listening review, or public-release claim.

## Status

Implementation, full automated validation, and the sole medium-effort review
are complete; the reviewer found no actionable findings. PR handoff, merge,
branch cleanup, and clean-main verification remain.

## Acceptance criteria

- Every active and terminal coverage read for all three campaigns has valid
  allowlisted music/cue metadata and written coverage data; terminal reads use
  the debrief music state.
- Focused/full validation passes at 372 Rust tests and 785 Python tests, with
  Clippy, formatting, release metadata, documentation links, asset/security/
  generation/credits, device/offline/browser/audio/raster/loading/visual-audio/
  asset-budget, CLI smoke, Node syntax, and diff checks green.

## Handoff requirements

After the sole reviewer approves, create and merge the PR into `main`, delete
the temporary branch locally/remotely, verify clean `main`, then design the
next unmet roadmap slice.
