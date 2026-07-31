# Implementation Plan — Full-campaign screenshot evidence v0.13.80

## Task restatement

Record and validate one active and one terminal local-browser inspection for
each launchable campaign at the documented 1024×768 baseline, while
preserving the host-owned campaign-coverage route, browser read-only boundary,
and existing written/audio fallbacks.

## Current understanding

- `campaign-coverage-v1` already carries active and terminal coverage for
  competitive, stabilization, and regional affiliation.
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json` records the
  supported screenshot surface but intentionally does not claim a full-campaign
  raster suite.
- The in-app browser can inspect the loopback GUI at the documented baseline;
  the repository has no committed browser screenshot harness or raster golden
  set.

## Assumptions

- The existing loopback route and shared campaign panel remain the only source
  for captured content.
- A local browser inspection is evidence of route/render reachability only; it
  is not human visual, accessibility, educational, legal, or public-release
  approval.
- Capture artifacts may remain ephemeral in this slice. The evidence record
  must say so explicitly rather than inventing file paths or hashes.

If any assumption is false, stop and report the mismatch before editing.

## Target slice

1. Inspect the existing GUI at 1024×768 for active and terminal competitive,
   stabilization, and regional-affiliation coverage.
2. Add a six-entry evidence manifest with exact campaign/state/viewport/source
   fields, observed host handoff text, ephemeral-artifact status, and limits.
3. Add a focused validator test that fails closed for missing campaigns, states,
   viewport, source markers, terminal debrief evidence, or authority limits.
4. Update the roadmap, project specification, changelog, version, lessons, and
   handoff records.
5. Run focused and full validation, then perform one medium-effort review.

## Likely files

- `docs/evaluation/phase11.1-full-campaign-screenshot-evidence.json`: six
  capture records and explicit evidence boundary.
- `tests/test_phase11_full_campaign_screenshot_evidence.py`: manifest/source/
  boundary regression test.
- `docs/visual_audio_enhancement_roadmap.md`: current screenshot inspection
  evidence and remaining raster-golden/human limits.
- `SPEC.md`, `README.md`, `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`,
  `LESSONS.md`: synchronized project state and version `0.13.80`.
- `tests/test_phase11_campaign_coverage.py` and
  `tests/test_release_metadata.py`: existing expected-state assertions updated
  for the new ledger entry and package version.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`,
  `_workspace/03_presentation_qa.md`, and `_workspace/final/handoff.md`:
  additive operational handoffs.

Avoid editing files outside this list unless the plan is incomplete; if that
happens, stop and explain why.

## Tests and checks

- `python3 -m unittest tests/test_phase11_full_campaign_screenshot_evidence.py`
- `python3 tests/test_phase11_full_campaign_screenshot_evidence.py`
- Full repository validation used by the contributor documentation, including
  Rust tests, Clippy, formatting, release metadata, documentation links, asset
  gates, GUI/Python tests, Node syntax, and offline/browser contracts.

Expected result: the manifest has exactly six active/terminal records, every
record is 1024×768 and source-bound, and the test continues to state that
ephemeral inspection is not a raster golden or human review.

## Acceptance criteria

- The six exact campaign/state pairs are present and source-bound to the
  existing `campaign-coverage-v1` route and shared GUI surface.
- Each terminal record names host-authored debrief evidence; all records name
  written equivalents and optional audio behavior.
- The validator rejects unknown campaign/state values, wrong viewport, missing
  source markers, missing debrief evidence, and claims of persisted approval.
- No route, schema, simulation rule, stochastic input, browser authority,
  asset, audio file, or hidden-state field is added.

## Non-goals

- Do not add a browser automation dependency or production screenshot runner.
- Do not commit invented PNG/JPEG files, hashes, quality ratings, or human
  approval.
- Do not change simulation, persistence, replay, campaign controls, or asset
  registries.

## Stop conditions

- Stop if capturing requires a new route, schema, simulation field, or browser
  authority path.
- Stop if the six-state matrix cannot be inspected without fabricating an
  artifact or human result.
- Stop if more than the listed evidence/test/documentation files need changes.

## Handoff instruction

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising.

## Risk

Risk: low

Reason: this is an additive evidence contract and validator over existing
host/browser behavior with no runtime or public API change.
