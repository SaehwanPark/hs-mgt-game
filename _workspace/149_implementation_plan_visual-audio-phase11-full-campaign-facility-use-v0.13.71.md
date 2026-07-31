# Implementation Plan — Full-campaign facility placement/use evidence v0.13.71

## Task restatement

Continue the visual/audio roadmap by closing the missing machine-verifiable
technical evidence for competitive facility placement/use across the complete
24-month host campaign. The read must remain actor-visible and presentation-
only; it must not claim full visual quality, screenshot completeness, or human
approval.

## Current understanding

- `src/mcp/regional_world.rs` projects the player-owned facility groups from
  `PlayerObservation` capacity fields and exposes public-rival entities without
  private facility detail.
- The GUI refreshes this host-owned regional-world read during competitive
  start/load and after accepted monthly actions, but the existing Rust
  regression only proves the initial projection and public-signal lag.
- The roadmap’s broad full-campaign facility placement/use item remains open;
  the next bounded improvement is a 24-month host-read continuity contract,
  not a new facility simulation or an asset-quality approval.

## Target slice

1. Add a host/session regression that reads the regional-world projection before
   every month of a deterministic 24-month competitive run and after terminal
   completion.
2. Require the four player-owned facility components, all eleven visible
   capacity metric labels, `PlayerObservation capacity fields` sources, stable
   actor-visible fallbacks, and private-rival facility exclusion at every read.
3. Record the bounded facility placement/use evidence in the Phase 11.1 ledger
   and Phase 13.1 competitive boundary, while keeping the broader human,
   screenshot, accessibility, and visual/audio quality gates open.
4. Synchronize request/contract/QA/handoff records, roadmap, SPEC, lessons,
   changelog, and package metadata to `0.13.71`.

## Assumptions and stop conditions

- Existing `competitive-regional-world-v1`, `get_regional_world`, facility
  catalog, and host session loop are sufficient; no route or schema changes are
  needed.
- Facility “use” means the current host-reported capacity metrics and their
  continuity through committed monthly transitions, not client-inferred
  utilization, hidden rival operations, or a new utilization model.
- The test must fail if a facility projection derives from true state,
  resolved inputs, effect queues, or private rival fields.

## Minimal implementation plan

1. Add the 24-month regression beside the existing regional-world session tests.
2. Extend the campaign-coverage and competitive-boundary evidence contracts to
   require the new test and ledger field.
3. Update roadmap/SPEC wording so “current technical facility placement/use” is
   distinguished from the still-open full-campaign visual and human gates.
4. Bump the project version to `0.13.71`, run focused and full validation, and
   use exactly one medium-effort code reviewer before PR handoff. The sole
   review is approved with no actionable findings; PR handoff is the next gate.

## Likely files

- `src/mcp/session.rs`
- `tests/test_phase11_campaign_coverage.py`
- `tests/test_phase13_1_competitive_campaign_boundary.py`
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`
- `docs/evaluation/phase13.1-competitive-campaign-boundary.json`
- `_workspace/00_input/request-summary.md`, `_workspace/02_presentation_contract.md`,
  `_workspace/03_presentation_qa.md`, `_workspace/final/handoff.md`
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `LESSONS.md`,
  `CHANGELOG.md`, and release metadata

## Acceptance criteria

- The host regression observes all 24 monthly competitive reads and the
  terminal read without changing the session through read calls.
- Every read exposes the same four player facility components and eleven
  source-bound capacity metrics; rival entities expose no private facilities.
- Focused tests, full Rust/Python/repository checks, exactly one medium-effort
  review, PR merge, branch cleanup, and clean-main verification pass.
- Evidence explicitly excludes pixel-level quality, raster screenshots,
  accessibility certification, human comprehension, legal/provenance approval,
  and public release.

## Non-goals

- No new simulation mechanics, facility types, route/schema, asset, audio file,
  browser authority, persistence format, screenshot suite, or human approval.

## Handoff requirements

After the sole reviewer approves, create and merge the PR into `main`, delete
the temporary branch locally and remotely, verify clean `main`, then design the
next unmet roadmap slice.
