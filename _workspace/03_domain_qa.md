# Domain QA - Regional Affiliation Playtest Validation v0.12.1

## Status

Pass.

## Reviewed Inputs

- v0.12.1 request summary, evidence map, mechanism design, and implementation
  plan.
- `_workspace/experiments/v0.12.1-affiliation-playtest-validation/results.json`
  and `diagnostics.md`.
- `docs/playtest-findings-v0.12.1.md`, `SPEC.md`, `docs/roadmap.md`, and the
  v0.12.0 affiliation runtime boundary.
- `src/model/affiliation.rs`, `src/affiliation/`, `src/mcp/session.rs`, and
  `src/debrief/report.rs`.
- Focused artifact tests and repository verification output.

## Findings

- The artifact stays within Phase 7 validation and does not add a new actor,
  transition, ruleset, scenario, or platform layer.
- The 3-profile × 3-seed matrix is exact, complete, deterministic, and uses
  only actor-visible observations and legal command hints.
- Observation-before-command, append-only transition summaries, state hashes,
  and debrief stage lines remain aligned for all 54 stages.
- Riverside outcomes are reported separately from partner, review, labor,
  payer, and community responses.
- The typed-vs-rendered observation mismatch is grounded in the current code and
  is recorded as one interface-context gap rather than a balance or learning
  claim.
- The artifact preserves the competitive golden boundary and the affiliation
  replay/hash boundary.

## Required Fixes

None.

## Residual Risks

- The matrix is a small scripted simulated-policy sample and cannot establish
  human comprehension, winnability, balance, calibration, legal validity, or
  educational effectiveness.
- Debrief-response parsing is intentionally tied to the current rendered stage
  line contract and should be updated if that contract changes.
- A future MCP observation-context fix must not expose hidden partner condition,
  actor utility, or realized outcomes before they occur.

## Verification Evidence

- Focused artifact tests passed: 6 tests.
- Capture and audit passed: 9 runs, 54 stages, 0 validation failures.
- Full Rust suite passed: 306 tests.
- Full Python suite passed: 169 tests.
- Formatting, clippy, competitive golden, and diff checks passed.
