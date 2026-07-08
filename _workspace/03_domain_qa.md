# Domain QA - Live Difficulty Evidence Synthesis

## Status

pass

## Reviewed Inputs

- `docs/playtest-findings-v0.10.12.md`
- `docs/playtest-findings-v0.10.13.md`
- `docs/playtest-findings-v0.10.14.md`
- `docs/playtest-findings-v0.10.15.md`
- `docs/playtest-findings-v0.10.16.md`
- `_workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
- `_workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- `_workspace/00_input/request-summary.md`
- Canonical docs and harness team spec

## Findings

- Scope fit: The slice stays in Phase 7 evidence/diagnostics and does not
  change runtime mechanics, command grammar, transition logic, stochastic
  inputs, scenario schemas, MCP DTOs, state hashes, or balance values.
- Evidence labeling: The synthesis consistently labels the inputs as
  simulated-agent or operator-authored evidence and avoids human-learning,
  empirical calibration, classroom-effectiveness, policy-validity, and balance
  claims.
- Observation boundary: The synthesis relies on committed artifacts and
  documented live-capture boundaries; it does not expose hidden active-play
  state or request runtime export changes.
- Determinism: No new runs or stochastic inputs are introduced. Existing
  artifacts remain fixed by campaign, seed, difficulty, accepted commands, and
  ruleset version.
- Matrix result: The synthesis correctly separates broad clean replay matrices
  from the `v0.10.15` live retry signal.
- Follow-up fit: Cash-pressure and validation-retry visibility is a bounded
  guidance/debrief/diagnostic issue and does not require balance tuning first.

## Required Fixes

None.

## Residual Risks

- The evidence base remains simulated-agent evidence, not human play.
- The matrices use one campaign and limited seeds/profiles.
- The diagnostic final-metric parser depends on current competitive debrief
  wording.
- The `v0.10.15` retry signal is useful for routing but not sufficient for
  runtime tuning.

## Verification Evidence

- `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null`
- `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null`
- `python3 -m json.tool _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json >/dev/null`
- `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
