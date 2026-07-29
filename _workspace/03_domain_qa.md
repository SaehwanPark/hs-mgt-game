# Domain QA — Live competitive GUI repair v0.12.31

## Status

Pass.

## Reviewed inputs

- User request and approved implementation plan.
- Canonical project docs and harness team spec.
- `src/gui_server.rs`, `gui/host-adapter.mjs`, `gui/app.mjs`, tests, ADR,
  player docs, project records, and verification output.

## Findings

- Scope: the change is limited to competitive browser transport and player
  instructions; it does not expand actors, mechanisms, balance, or campaigns.
- Determinism: HTTP and browser code are I/O adapters around the existing
  `GameSessionStore`. No core transition reads network state, time, or hidden
  randomness.
- Observation boundary: responses reuse actor-visible presentation, catalog,
  regional-world, resolution, and session envelopes. No true/private state DTO
  was added.
- History and causality: submission remains host-owned and resolution remains a
  read of committed history; browser audio and progress state do not enter
  hashes or replay.
- Scope/security correction: code review found that the initial HTTP DTO exposed
  MCP `scenario_path` and unsupported campaigns. The final DTO rejects unknown
  fields, forces `scenario_path: None`, and permits only the competitive GUI
  campaign.

## Required fixes

None remaining.

## Residual risks

- Sessions are intentionally in memory and disappear on process exit.
- No live viewport, screen-reader, or hardware-audio claim is made because the
  in-app browser controller was unavailable during this implementation.
- Loopback transport is a local prototype boundary, not authenticated or
  production hosting.

## Verification evidence

- Full Python suite: 316 passed.
- GUI-focused suite: 81 passed.
- Rust: 328 library tests plus all integration, golden, scenario, and doctest
  targets passed.
- Node syntax, release metadata, formatting, Clippy with denied warnings, real
  process/curl launch, and diff checks passed.
- One severity-ranked code-review pass completed; its one blocking finding was
  fixed and reverified. Final review: no actionable issues found.

# Domain QA — Phase 13.1 bounded content boundary v0.13.51

## Status

`pass` for the bounded repository-owned source/content QA. This is not
clinical or policy expert approval.

## Reviewed Inputs

- `README.md`, `docs/guides/gui-how-to-play.md`, and the canonical design,
  proposal, roadmap, and team-spec boundaries.
- Current `gui/*.mjs`, `gui/index.html`, metric visualization proof, and
  semantic-container source/status catalog.
- `docs/evaluation/phase13.1-content-boundary-qa.json` and its focused test.
- Existing hidden-state and limitations ledgers/tests.

## Findings

- Scope remains a fictional educational simulation and research prototype;
  player-facing text rejects calibrated forecasting and operational, clinical,
  financial, regulatory, and legal decision use.
- The reviewed GUI surfaces contain no claims of diagnosis, prescribing,
  treatment plans, patient-specific advice, clinical recommendations, or
  clinical decisions.
- Numeric visualization rules retain exact values, source, status, uncertainty,
  and missingness in written text and prohibit forecast, probability, and
  hidden-state inference.
- Actor-visible source/status language and the existing browser hidden-state
  scan keep current presentation evidence separate from true state, resolved
  inputs, and effects.

## Required Fixes

None for this bounded source/content pass.

## Residual Risks

- A source scan cannot establish clinical validity, policy validity, calibration,
  human comprehension, accessibility quality, or educational effectiveness.
- Portrait resemblance, institutional resemblance, asset/audio provenance,
  legal review, and public-release review remain open.
- The bounded source/content wording gate is recorded for this current reviewed
  checkout; the broader clinical-implication item remains an explicit human
  content/policy release gate.

## Verification Evidence

- `python3 -m unittest tests.test_phase13_1_content_boundary_qa` — pass.
- Existing hidden-state and limitations boundary tests — pass.

# Domain QA — Phase 13.1 technical attribution boundary v0.13.52

## Status

`pass` for the current repository-owned attribution and generated-credits
boundary. This is not legal, ownership, training-data, resemblance, or
public-release approval.

## Reviewed Inputs

- Canonical visual/audio registries, generated static credits/notices, runtime
  credits projection, release manifest, and portrait preview/review queue.
- `docs/evaluation/phase13.1-attribution-boundary.json` and its focused test.
- Existing asset validation, security, generation metadata, release, and
  in-game credits checks.

## Findings

- Current registry entries retain source/generation attribution, legal-basis
  reference, accessible equivalent, approval status, and original hash; release
  entries also carry release hashes and manifest path parity.
- Static credits, third-party notices, runtime credits, and release-manifest
  projections are current relative to canonical registries.
- Unverified portrait previews and review-queue entries remain pending,
  unreleased, unregistered, and absent from runtime attribution surfaces; the
  on-disk preview directory is enumerated against both metadata lists.
- The slice does not fabricate model, seed, human review, ownership, or legal
  approval for previews whose generation tool did not expose those fields.

## Required Fixes

None for this bounded technical attribution pass.

## Residual Risks

- Human legal, ownership, training-data, resemblance, artifact, accessibility,
  educational, and public-release review remain open.
- Portrait AI-generation metadata remains incomplete by design until an
  approved metadata-bearing generation route is used.

## Verification Evidence

- `python3 -m unittest tests.test_phase13_1_attribution_boundary` — pass.
- Existing asset registry, credits, generation, security, and release checks —
  pass.
