# Implementation Plan — Competitive coverage companion surface v0.13.70

## Task restatement

Make the existing host-owned `campaign-coverage-v1` competitive read useful in
the normal GUI session by rendering it as a companion panel beside the
competitive action rail, while keeping the action-catalog → host validation →
`submitTurn` path as the only competitive mutation authority.

## Current understanding

- `src/mcp/campaign_coverage.rs` and the loopback route now expose a typed,
  actor-visible competitive coverage envelope for all three launchable
  campaigns.
- The normal competitive GUI path currently loads the separate presentation,
  action catalog, history, replay, regional-world, and checkpoint surfaces; it
  does not load the competitive coverage panel during ordinary start/load or
  after an accepted monthly submit.
- `campaignCoverageClient.load` is intentionally a campaign rail loader: it
  resets action drafts and disables controls. Reusing it for normal competitive
  sessions would incorrectly replace the authoritative competitive action rail.
- The shared renderer already supports a null submit callback, so competitive
  coverage can remain visibly read-only while the normal action rail remains
  enabled.

## Target slice

1. Add a companion-only coverage read method that fetches and renders the
   existing envelope without resetting competitive drafts, validation, session
   state, or action controls.
2. Invoke that companion read after a normal competitive session’s initial
   presentation load and after each accepted host refresh; failures remain
   recoverable and do not block the competitive action rail.
3. Keep stabilization and regional-affiliation campaign-coverage rails
   unchanged, and keep competitive coverage decisions disabled with the
   existing “Use the competitive action rail” explanation.
4. Update source contracts, GUI guidance, evidence ledgers, roadmap, SPEC,
   lessons, and package metadata to `0.13.70`.

## Assumptions and stop conditions

- The existing route, envelope schema, host adapter, renderer, audio metadata,
  and panel markup are sufficient; no new route, schema, asset, or dependency
  is needed.
- A companion read must not call `submitTurn`, alter drafts, change the
  `firstMonthFlow` action stage, or disable the action controls.
- Coverage refresh is best-effort. If the host read fails or returns an
  unsupported envelope, retain the normal competitive presentation and expose a
  written recoverable coverage status without treating the committed session as
  failed.
- Do not make competitive coverage the action rail or duplicate competitive
  validation in the shared renderer.

## Minimal implementation plan

1. Add `loadCompanion` to `createCampaignCoverageClient`; share the existing
   envelope rendering/audio path while avoiding campaign-rail state changes.
2. Call the companion method from the normal competitive action client after
   initial host reads and accepted-turn refreshes, recording but not promoting
   optional companion failures.
3. Add Node/static contract coverage proving competitive companion refresh,
   read-only decision controls, preserved action state, and failure fallback;
   retain existing campaign-coverage and authority tests.
4. Synchronize the Phase 12/13.1 ledgers, guide/README, request/contract/QA/
   handoff records, roadmap, lessons, changelog, and package metadata.
5. Run focused tests and full Rust/Python/repository checks, then use exactly
   one medium-effort code reviewer before PR handoff. Implementation, all
   automated validation, and the sole review are complete with no actionable
   findings; PR handoff remains the next gate.

## Likely files and functions

- `gui/app.mjs`: `createCampaignCoverageClient`, `createActionClient.load`,
  accepted-turn refresh, companion error/status handling.
- `gui/index.html`, `docs/guides/gui-how-to-play.md`, `gui/README.md`: explain
  the competitive coverage companion and separate authoritative action rail.
- `tests/test_gui_campaign_coverage.py` and
  `tests/test_phase12_live_campaign_coverage.py`: source and Node behavior
  contracts.
- `docs/evaluation/phase12-live-campaign-coverage.json`,
  `docs/evaluation/phase12-campaign-presentation-coverage.json`, and
  `docs/evaluation/phase13.1-competitive-campaign-boundary.json`: evidence.
- `CHANGELOG.md`, `README.md`, `Cargo.toml`, `Cargo.lock`, generated credits,
  `SPEC.md`, `docs/visual_audio_enhancement_roadmap.md`, `LESSONS.md`, and
  `_workspace/*`: synchronized project records.

## Acceptance criteria

- A normal competitive GUI start/load renders the host competitive coverage
  panel alongside the existing action catalog and regional surfaces.
- An accepted competitive month refreshes both the normal presentation and the
  companion coverage without resetting drafts, validation, or action controls.
- A companion read failure is written and recoverable; the action rail remains
  usable and no client transition is fabricated.
- Coverage decisions remain disabled/read-only, and the existing competitive
  catalog/validation/submit sequence remains the only mutation path.
- Focused and full validation passes, documentation records the visible-only
  source and fallback boundary, and version metadata is `0.13.70`.

## Non-goals

- No new simulation, transition, stochastic input, history/replay format,
  persistence, route/schema, action protocol, asset, audio file, screenshot,
  human evaluation, device certification, provenance/legal approval, or public
  release claim.
- No replacement of the competitive action rail with campaign coverage and no
  browser-side calculation of outcomes, costs, legality, or rival state.

## Handoff requirements

Implement exactly this plan. After the sole reviewer approves, create and merge
the PR into `main`, delete the temporary branch locally and remotely, verify
clean `main`, then design the next unmet roadmap slice.

## Risk

Risk: medium — the same shared panel will become visible in a mutation-capable
competitive session, so lifecycle ordering must preserve the action client’s
draft/validation state and keep optional coverage failure isolated.
