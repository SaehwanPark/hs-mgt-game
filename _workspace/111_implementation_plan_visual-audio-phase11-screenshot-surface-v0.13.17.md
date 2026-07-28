# Implementation Plan — Visual/audio Phase 11.1 current screenshot-surface contract v0.13.17

## Task restatement

Continue the roadmap's screenshot gate with the smallest verifiable slice:
record the current supported actor-visible GUI screenshot surface and prove
that its deterministic structural/snapshot checks and local browser smoke path
remain aligned. Do not call this a full-campaign raster suite or human visual
quality approval.

## Current understanding

- The local GUI server renders a real actor-visible executive desktop at the
  loopback route, including executive metrics, briefing, campaign controls,
  accessibility settings, the first-month rail, action, resolution, history,
  and debrief surfaces.
- `tests/test_regional_board.py` already protects the deterministic regional
  SVG scene with a SHA-256 snapshot. Existing GUI coverage tests protect the
  static desktop, campaign surface, resolution sequence, live host handoffs,
  and visual/audio contracts.
- The browser smoke path can start the current competitive session and capture
  a local viewport for inspection, but the repository has no committed raster
  artifact or deterministic cross-browser screenshot runner.

## Target slice

Define `screenshot_coverage` in the Phase 11.1 ledger for the current supported
surface:

- enumerate the current actor-visible page/surface sources;
- identify the deterministic SVG snapshot and structural GUI checks;
- record the local browser smoke capture as inspection evidence only;
- bind the contract to the focused tests and source markers; and
- state the limits for full campaign placement/use, committed raster goldens,
  cross-browser/device capture, human visual review, accessibility, and quality.

## Assumptions

- “Current screenshot surface” means the supported GUI composition and its
  deterministic presentation contracts, not every future campaign state.
- A browser screenshot inspected during this slice is evidence that the live
  route can render; it is not a stable golden artifact and must not be hashed
  or represented as a completed raster suite.
- Existing deterministic SVG and source/DOM tests remain authoritative for
  repeatable regression. No browser dependency or screenshot asset is needed
  to close this bounded technical item.

If a current surface cannot be linked to a source and test, add only the
smallest focused ledger/parity assertion required to expose that gap.

## Minimal implementation plan

1. Add `screenshot_coverage` to the Phase 11.1 campaign ledger with exact
   surface sources, deterministic snapshot/structural test sources, browser
   smoke evidence, and explicit limits.
2. Extend `tests/test_phase11_campaign_coverage.py` with source-marker and
   surface-contract assertions; keep the client read-only and authority
   boundaries unchanged.
3. Update the roadmap checklist/status and add v0.13.17 evidence; synchronize
   `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LESSONS.md`, `README.md`,
   version metadata, and additive presentation request/contract/QA/handoff
   records.
4. Run focused/full Python and Rust checks plus release, documentation,
   offline, browser-policy, device-policy, and visual/audio contract checks.
5. Review the diff with one reviewer in three independent passes, hand off a
   PR, merge it into `main`, remove the temporary branch locally/remotely, and
   reassess the next roadmap item.

## Files and functions likely to change

- `docs/evaluation/phase11.1-campaign-coverage-ledger.json`.
- `tests/test_phase11_campaign_coverage.py`.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`,
  this plan, and `_workspace/final/handoff.md`.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `CHANGELOG.md`, `LESSONS.md`, `README.md`, `Cargo.toml`, `Cargo.lock`, and
  generated package-version projections.

Avoid changing GUI behavior, server routes, assets, audio, Rust runtime, or
browser dependencies unless focused inspection proves the current surface
cannot be represented accurately.

## Acceptance criteria

- The ledger identifies the current supported GUI screenshot surfaces and
  their live source paths.
- The parity test requires the deterministic regional SVG snapshot, current
  structural GUI coverage, and local browser smoke evidence markers.
- The roadmap closes only current supported screenshot-surface evidence;
  full-campaign raster coverage, cross-browser/device capture, human review,
  accessibility quality, and visual/audio quality remain separately gated.
- Package version increments to v0.13.17 and all version projections agree.

## Non-goals

- Do not add PNG/JPEG goldens, browser automation dependencies, telemetry,
  screenshot upload, new campaign content, runtime transitions, or human
  evaluation claims.
- Do not mark the full campaign screenshot suite complete merely because the
  current supported surface renders in one local browser.

## Stop conditions

Stop if evidence requires a new campaign state, committed raster artifact,
cross-browser/device matrix, screenshot tooling, quality judgment, or a claim
beyond current source/structural/smoke closure.

## Risk label

Risk: low

Reason: This slice adds a bounded evidence contract over existing GUI sources,
deterministic SVG regression, structural tests, and a local browser smoke path;
it does not change runtime behavior or asset/audio bytes.
