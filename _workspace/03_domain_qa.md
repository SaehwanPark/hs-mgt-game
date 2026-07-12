# Domain QA - Regional Affiliation Runtime v0.12.0

## Status

Pass.

## Reviewed Inputs

- v0.12.0 request summary, evidence map, and mechanism design.
- `src/model/affiliation.rs`, `src/inputs/resolve_affiliation.rs`,
  `src/affiliation/`, `src/scenario/mod.rs`, and the bundled scenario fixture.
- CLI/MCP routing, replay artifact verification, state hashing, and debrief
  surfaces.
- ADR-0010, `docs/expansion-proposal-review.md`, `docs/roadmap.md`, `SPEC.md`,
  `docs/system-boundary.md`, and `docs/scenario-format-draft.md`.
- Existing deterministic transition, observation, history, replay, and debrief
  boundaries.

## Findings

- The implementation is an opt-in six-stage scenario and does not modify the
  default competitive campaign or its hash/golden path.
- Partner, review, labor, payer, and community roles have distinct authority,
  incentives, and information boundaries.
- True state, Riverside observation, actor utility, organizational outcomes,
  social welfare, community effects, and educational evaluation remain
  separate.
- Regulatory outcomes are explicitly stylized or unresolved rather than legal
  forecasts.
- Stochastic affiliation outcomes are explicit resolved inputs and do not enter
  deterministic transition logic implicitly.
- Independence, deferral, and affiliation remain multiple defensible choices.

## Required Fixes

None.

## Residual Risks

- Numeric thresholds and commitment costs are explicit game abstractions, not
  calibrated policy or legal parameters.
- The partner's hidden condition remains out of the Riverside observation;
  only resolved public/report signals are exposed.
- A rejected or delayed affiliation still advances through the fixed schedule so
  the debrief can distinguish choice quality from actor realization.
- The six-stage slice does not establish legal validity, calibration, gameplay
  value, or educational learning.
- Full acquisition/deal-market breadth, AI-rival affiliation behavior, and
  autosave expansion remain deferred.

## Verification Evidence

- Canonical documentation consistency review completed.
- Runtime boundaries reviewed against existing scenario, replay, history, and
  debrief documents.
- `cargo test --all -- --test-threads=1`, competitive golden tests, Python
  tests, clippy, formatting, and `git diff --check` passed.
- Repository verification commands are recorded in the final handoff.
