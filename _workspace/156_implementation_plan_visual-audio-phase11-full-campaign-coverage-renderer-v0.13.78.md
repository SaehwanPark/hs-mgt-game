# Implementation Plan — Full-campaign coverage renderer continuity v0.13.78

## Task restatement

Continue the visual/audio roadmap with a bounded browser-presentation evidence
slice: prove that the existing campaign-coverage renderer consumes active and
terminal host envelopes for all three launchable campaigns without losing
written history/debrief fallbacks or adding browser authority.

## Current understanding

- The GUI already renders `campaign-coverage-v1` through the shared
  `renderCampaignCoverage` function and receives optional host audio metadata.
- Existing Node fixtures cover representative competitive, stabilization, and
  affiliation behavior, including read-only decision controls and audio state,
  but no fixture matrix walks active and terminal renderer inputs for all three
  campaigns together.
- The host remains authoritative for coverage rows, debrief, audio metadata,
  transition, and replay; the renderer is a presentation-only consumer.

## Target slice

1. Exercise active and terminal `campaign-coverage-v1` fixtures for
   competitive, stabilization, and regional-affiliation campaigns through the
   existing `renderCampaignCoverage` function.
2. Require campaign identity/stage metadata, history rows, terminal debrief
   lines, supplied audio metadata, and read-only decision controls to remain
   visible in the renderer fixture contract.
3. Record the bounded renderer result in the Phase 11.1 ledger and synchronize
   request/contract/QA/handoff records, roadmap, SPEC, lessons, changelog, and
   version metadata to `0.13.78`.

## Non-goals

- No new route/schema, simulation, stochastic input, browser authority,
  checkpoint archive, browser serialization, asset, audio file, screenshot,
  human review, or public-release claim.

## Status

Implementation, full automated validation, and the sole medium-effort review
are complete; the reviewer found no actionable findings. PR handoff, merge,
branch cleanup, and clean-main verification remain.

## Acceptance criteria

- All six active/terminal campaign fixtures render successfully with supplied
  identity, history/debrief, and audio/written fallback data; decisions remain
  disabled unless an existing host submit callback is explicitly supplied.
- Focused/full validation passes at 373 Rust tests and 787 Python tests, with
  Clippy, formatting, release metadata, documentation links, asset/security/
  generation/credits, device/offline/browser/audio/raster/loading/visual-audio/
  asset-budget, CLI smoke, Node syntax, and diff checks green.

## Handoff requirements

After the sole reviewer approves, create and merge the PR into `main`, delete
the temporary branch locally/remotely, verify clean `main`, then design the
next unmet roadmap slice.
