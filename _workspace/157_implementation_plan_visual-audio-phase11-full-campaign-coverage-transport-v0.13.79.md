# Implementation Plan — Full-campaign coverage transport continuity v0.13.79

## Task restatement

Continue the visual/audio roadmap with a bounded loopback transport evidence
slice: prove that the existing campaign-coverage route carries active and
terminal host envelopes through full runs of all three launchable campaigns.

## Current understanding

- The loopback GUI route already serves `campaign-coverage-v1` for competitive,
  stabilization, and regional-affiliation sessions.
- Existing transport tests cover genesis and one accepted transition per
  campaign, plus invalid-decision recovery, while host and renderer tests now
  cover full runs and six browser fixtures separately.
- No route, schema, client authority, or browser serialization is authorized;
  the transport must remain a read of the existing host store.

## Target slice

1. Start each launchable campaign through the existing loopback route.
2. Read campaign coverage at genesis and after every valid transition through
   competitive month 24, stabilization stage 5, and affiliation stage 6.
3. Require status/schema/campaign identity, history/replay counts, audio
   metadata, terminal written debrief, and terminal `debrief` music state.
4. Record the bounded transport result in the Phase 11.1 ledger and synchronize
   request/contract/QA/handoff records, roadmap, SPEC, lessons, changelog, and
   version metadata to `0.13.79`.

## Non-goals

- No new route/schema, simulation, stochastic input, browser authority,
  checkpoint archive, browser serialization, asset, audio file, screenshot,
  human review, or public-release claim.

## Status

Implementation and full automated validation are complete; the sole
medium-effort review, PR handoff, merge, branch cleanup, and clean-main
verification remain.

## Acceptance criteria

- The existing loopback route returns valid active and terminal coverage for
  all three full campaign paths with aligned history/replay counts, optional
  audio, written debrief, and no client mutation authority.
- Focused/full validation passes at 374 Rust tests and 788 Python tests, with
  Clippy, formatting, release metadata, documentation links, asset/security/
  generation/credits, device/offline/browser/audio/raster/loading/visual-audio/
  asset-budget, CLI smoke, Node syntax, and diff checks green.

## Handoff requirements

After the sole reviewer approves, create and merge the PR into `main`, delete
the temporary branch locally/remotely, verify clean `main`, then design the
next unmet roadmap slice.
