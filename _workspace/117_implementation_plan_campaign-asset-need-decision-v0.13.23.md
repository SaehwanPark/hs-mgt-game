# Implementation Plan — Phase 12 campaign map/facility asset-need decision v0.13.23

## Task restatement

Continue Phase 12 with the next unmet item: identify current campaign-specific
map or facility needs for stabilization and regional affiliation. Record the
bounded “no new asset required by the current abstract/stage contracts” result
and the conditions that would reopen it; do not create or promote assets.

## Current understanding

- The current campaign-coverage inventory records no map/facility need for
  `stabilization-v1` or `regional-affiliation-v1`.
- The reuse matrix records the generic facility descriptor as fallback-only and
  keeps current identity, marker, status, and written-equivalent primitives
  reusable.
- The Phase 12 roadmap still leaves “campaign-specific map or facility needs
  identified” unchecked because the decision has not been represented by one
  dedicated evidence record.

## Target slice

Add `docs/evaluation/phase12-campaign-asset-need-decision.json` and a parity
test that records:

- the exact current campaign IDs and campaign-coverage source;
- current surface evidence for each campaign;
- the current decision, fallback, and written-equivalent boundary;
- future triggers that would require new map/facility work; and
- explicit limits against treating the decision as asset quality, placement,
  screenshot, human, or full-campaign evidence.

## Assumptions

- “Identified” means a documented current need decision with a reopen trigger,
  not a claim that future campaign design cannot require assets.
- Existing facility descriptors remain reusable fallback/catalog evidence only;
  the current Phase 12 contracts do not consume a new map/facility asset.
- No runtime, simulation, asset registry, audio, or authority change is needed.

## Minimal implementation plan

1. Add the map/facility asset-need decision record and parity test.
2. Check only the Phase 12.1 and 12.2 asset-need checklist items and
   synchronize canonical docs, lessons, version metadata, generated credits,
   and additive request/contract/QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add map, facility, portrait, stage-art, raster, audio, or registry
  entries.
- Do not add facility placement, campaign transitions, screenshots, durable
  persistence, quality review, instructor views, or human evaluation.
- Do not close reusable-assets, pressure, tutorial, audio, debrief, or
  educational checklist items with this decision record.

## Stop conditions

Stop if a current campaign surface requires a new asset, placement contract,
quality decision, asset promotion, or human review.

## Risk label

Risk: low

Reason: The slice formalizes an existing no-new-asset decision and future
triggers without changing runtime behavior or asset bytes.
