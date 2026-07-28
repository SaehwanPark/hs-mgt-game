# Implementation Plan — Phase 12 campaign-specific presentation inventory v0.13.21

## Task restatement

Continue Phase 12 with a bounded inventory of the current
`campaign-coverage-v1` presentation surface for the stabilization and regional-
affiliation campaigns. Record the campaign-specific visual/audio needs already
supported by the shared surface and the explicit “no new map/facility asset”
boundary; do not claim full campaign art/audio implementation.

## Current understanding

- `src/mcp/campaign_coverage.rs` defines typed campaign-specific briefing,
  metrics, actors, processes, decisions, immutable history, replay metadata,
  and debrief projections for `stabilization-v1` and
  `regional-affiliation-v1`.
- `gui/app.mjs`, `gui/index.html`, and `gui/README.md` render those fields
  through shared campaign coverage panels and the host-shaped submit path.
- Existing campaign, audio, accessibility, playtest, Rust, and debrief tests
  cover current source and authority boundaries, but the Phase 12 checklist
  does not have one inventory record that distinguishes shared surfaces from
  future campaign-specific map/facility, tutorial, stage-art, and audio work.

## Target slice

Add `docs/evaluation/phase12-campaign-presentation-coverage.json` and parity
tests that record:

- exact current campaign IDs and `campaign-coverage-v1` source/route/adapter;
- shared visible surface fields for briefing, metrics, actors, processes,
  decisions, history/replay, debrief, and optional audio;
- stabilization's current abstract executive surface and explicit absence of a
  new campaign-specific map/facility asset requirement;
- regional affiliation's current stage/partner/commitment/debrief surface;
- existing accessibility/fallback/provenance evidence; and
- open limits for new pressure states, tutorial presentation, stage-specific
  visuals/audio, full-campaign placement, and human educational review.

## Assumptions

- “Inventory” means the current typed presentation contract and design
  boundary, not completion of the Phase 12 campaign-specific checklist.
- Shared assets and surfaces may be reused when the actor-visible semantics
  remain explicit; no new map/facility or portrait asset is required by the
  current abstract stabilization/affiliation DTO.
- Host/core remains authoritative for campaign facts, commands, history,
  replay metadata, and debrief; the browser only renders the projection.

## Minimal implementation plan

1. Add the campaign-presentation coverage ledger with exact IDs, sources,
   shared surface fields, current no-new-asset decisions, and limits.
2. Add a focused parity test for source markers, campaign IDs, surface fields,
   and authority exclusions.
3. Update the Phase 12 roadmap evidence and synchronize canonical docs, lessons,
   version metadata, generated credits, and additive request/contract/QA/
   handoff records.
4. Run full Python/Rust/lint/release/documentation/generation/asset/offline/
   browser/device/visual-audio checks.
5. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the remaining campaign gates.

## Non-goals

- Do not add new map/facility/portrait assets, stage art, audio files, tutorial
  copy, runtime transitions, instructor views, or human educational review.
- Do not call current campaign-coverage projection a full Phase 12 delivery.

## Stop conditions

Stop if evidence requires new campaign content, a visual/audio quality decision,
human educational review, a new runtime authority path, or asset promotion.

## Risk label

Risk: low

Reason: The slice records existing typed sources and boundaries with a
read-only ledger/parity test; it does not change campaign behavior or assets.
