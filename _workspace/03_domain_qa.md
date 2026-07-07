# Domain QA - Static-vs-Adaptive Live Capture

## Status

pass

## Reviewed Inputs

- `scripts/diagnose_runs.py`
- `scripts/run_automated_playtests.py`
- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py`
- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md`
- `docs/playtest-findings-v0.10.13.md`
- `_workspace/00_input/request-summary.md`
- `_workspace/01_evidence_map.md`
- Canonical docs and harness team spec

## Findings

- Scope fit: The slice stays in Phase 7 evidence/diagnostics and does not
  change runtime mechanics, command grammar, transition logic, stochastic
  inputs, scenario schemas, MCP DTOs, state hashes, or balance values.
- Evidence labeling: Findings and generated diagnostics consistently label the
  artifact as simulated-agent evidence and avoid human-learning, empirical
  calibration, classroom-effectiveness, and policy-validity claims.
- Observation boundary: The diagnostic reads post-run captured observations,
  commands, transition summaries, and debriefs. It does not expose hidden state
  during active play.
- Determinism: The source artifact remains fixed by campaign, seeds,
  difficulties, policy variants, and deterministic policies.
- Matrix result: All 48 sessions completed 24 months with zero validation
  failures.
- Policy-variant signal: Normal static and adaptive runs are identical, while
  Hard adaptive runs increase monitoring and shift endpoint tradeoffs for
  Capacity Growth and Balanced Strategy.

## Required Fixes

None.

## Residual Risks

- The final metric parser depends on the current competitive debrief wording.
- Three seeds, one campaign, and two difficulty labels cannot support balance
  conclusions.
- Static/adaptive differences are policy-mediated by the existing adaptive
  wrapper and should not be interpreted as isolated balance evidence.

## Verification Evidence

- `python3 -m py_compile scripts/play_game.py`
- `python3 -m py_compile scripts/run_automated_playtests.py`
- `python3 -m py_compile _workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py`
- `python3 _workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json --output _workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md`
- `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
