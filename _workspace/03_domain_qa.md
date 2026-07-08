# Domain QA - Live LLM Difficulty Gate

## Status

pass

## Reviewed Inputs

- `scripts/play_game.py`
- `scripts/diagnose_runs.py`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
- `docs/playtest-findings-v0.10.15.md`
- `_workspace/00_input/request-summary.md`
- Canonical docs and harness team spec

## Findings

- Scope fit: The slice stays in Phase 7 evidence/diagnostics and does not
  change runtime mechanics, command grammar, transition logic, stochastic
  inputs, scenario schemas, MCP DTOs, state hashes, or balance values.
- Evidence labeling: Findings consistently label the artifact as
  simulated-agent live-decision evidence and avoid human-learning, empirical
  calibration, classroom-effectiveness, policy-validity, and balance claims.
- Observation boundary: Live decisions used actor-visible MCP observations and
  legal command hints. The replay artifact records observations, commands,
  transition summaries, final observations, and debriefs without exposing hidden
  active-play state.
- Determinism: The committed artifact is fixed by campaign, seed, difficulty,
  accepted commands, and ruleset version.
- Matrix result: All six replayed sessions completed 24 months with zero final
  validation failures.
- Retry signal: Access Operator runs preserve live retry metadata, including
  cash-overrun failures that are relevant to difficulty and guidance review.

## Required Fixes

None.

## Residual Risks

- One seed, one campaign, and three profiles cannot support balance
  conclusions.
- The accepted command streams are simulated-agent evidence, not human play.
- The diagnostic final-metric parser depends on current competitive debrief
  wording.
- One delegated Competitive Analyst Normal run did not complete; the artifact
  records a replacement local live decision stream from the same MCP observation
  and legal-command surface.

## Verification Evidence

- `python3 -m py_compile scripts/play_game.py`
- `python3 -m py_compile scripts/diagnose_runs.py`
- `python3 -m py_compile _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py`
- `python3 _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
- `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
