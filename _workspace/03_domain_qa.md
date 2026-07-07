# Domain QA - Live Difficulty-Pressure Capture

## Status

pass

## Reviewed Inputs

- `scripts/diagnose_runs.py`
- `scripts/run_automated_playtests.py`
- `_workspace/experiments/v0.10.12-live-difficulty-pressure/run_sessions.py`
- `_workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
- `_workspace/experiments/v0.10.12-live-difficulty-pressure/diagnostics.md`
- `docs/playtest-findings-v0.10.12.md`
- `_workspace/00_input/request-summary.md`
- `_workspace/01_evidence_map.md`
- Canonical docs and harness team spec

## Findings

- Scope fit: The slice stays in Phase 7 evidence/diagnostics and does not change runtime
  mechanics, command grammar, transition logic, stochastic inputs, scenario
  schemas, MCP DTOs, state hashes, or balance values.
- Evidence labeling: Findings and generated diagnostics consistently label the
  artifact as simulated-agent evidence and avoid human-learning, empirical
  calibration, classroom-effectiveness, and policy-validity claims.
- Observation boundary: The diagnostic reads post-run captured observations,
  commands, transition summaries, and debriefs. It does not expose hidden state
  during active play.
- Determinism: The source artifact remains fixed by campaign, seeds,
  difficulties, and deterministic policies.
- Matrix result: All 24 sessions completed 24 months with zero validation
  failures.
- Pressure signal: Capacity Growth and Balanced Strategy show Normal/Hard
  endpoint differences, while Fiscal Caution and Naive First-Time remain stable
  enough to show that not every profile exercises difficulty pressure.

## Required Fixes

None.

## Residual Risks

- The final metric parser depends on the current competitive debrief wording.
- Three seeds, one campaign, and two difficulty labels cannot support balance
  conclusions.
- The Hard/Normal difference is partially policy-mediated by the existing
  adaptive wrapper and should not be interpreted as isolated balance evidence.

## Verification Evidence

- `python3 -m py_compile scripts/play_game.py`
- `python3 -m py_compile scripts/run_automated_playtests.py`
- `python3 -m py_compile _workspace/experiments/v0.10.12-live-difficulty-pressure/run_sessions.py`
- `python3 _workspace/experiments/v0.10.12-live-difficulty-pressure/run_sessions.py`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json --output _workspace/experiments/v0.10.12-live-difficulty-pressure/diagnostics.md`
- `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null`
- `python3 -m py_compile scripts/diagnose_runs.py`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
