# Implementation Plan — Full-campaign history/replay continuity v0.13.77

## Task restatement

Continue the visual/audio roadmap with a bounded host-source evidence slice:
prove that immutable history and replay projections stay count- and hash-aligned
through the full endpoint of each launchable campaign.

## Current understanding

- The host already owns immutable transition histories and exposes typed
  `competitive-history-v1` and `competitive-replay-v1` envelopes for all three
  launchable campaign sessions.
- Competitive replay regenerates the recorded history at the host boundary;
  stabilization and regional-affiliation replay reads reuse their canonical
  immutable histories without adding a browser-side trace.
- Existing checkpoint regressions compare replay/history at bounded restore
  points and terminal coverage, but no regression walks every full-campaign
  history/replay read for all three campaign endpoints.

## Target slice

1. Walk competitive (24 months), stabilization (5 stages), and
   regional-affiliation (6 stages) through existing host sessions.
2. Read history and replay at genesis and after every committed transition;
   require matching schema, transition count, ordered rows, state hashes, and
   latest replay hash, including terminal reads.
3. Record this bounded continuity result in the Phase 11.1 ledger and
   synchronize request/contract/QA/handoff records, roadmap, SPEC, lessons,
   changelog, and version metadata to `0.13.77`.

## Non-goals

- No new route/schema, simulation, stochastic input, browser authority,
  checkpoint archive, browser serialization, asset, audio file, screenshot,
  human review, or public-release claim.

## Status

Implementation, full automated validation, and the sole medium-effort review
are complete; the reviewer found no actionable findings. PR handoff, merge,
branch cleanup, and clean-main verification remain.

## Acceptance criteria

- Every active and terminal history/replay read for all three campaigns has
  aligned counts, ordered transition summaries, and state hashes; terminal
  replay metadata identifies the final committed hash.
- Focused/full validation passes at 373 Rust tests and 786 Python tests, with
  Clippy, formatting, release metadata, documentation links, asset/security/
  generation/credits, device/offline/browser/audio/raster/loading/visual-audio/
  asset-budget, CLI smoke, Node syntax, and diff checks green.

## Handoff requirements

After the sole reviewer approves, create and merge the PR into `main`, delete
the temporary branch locally/remotely, verify clean `main`, then design the
next unmet roadmap slice.
