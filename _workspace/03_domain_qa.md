# Domain QA - Live-Capture Matrix Evidence

## Status

pass

## Reviewed Inputs

- `scripts/diagnose_runs.py`
- `_workspace/experiments/v0.10.11-live-capture-matrix/run_sessions.py`
- `_workspace/experiments/v0.10.11-live-capture-matrix/results.json`
- `_workspace/experiments/v0.10.11-live-capture-matrix/diagnostics.md`
- `docs/playtest-findings-v0.10.11.md`
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
  difficulties, and deterministic persona policies.
- Matrix result: All 18 sessions completed 24 months with zero validation
  failures.

## Required Fixes

None.

## Residual Risks

- The final metric parser depends on the current competitive debrief wording.
- Three seeds, one campaign, and two difficulty labels cannot support balance
  conclusions.
- Conservative command choice under-samples risky or high-pressure command paths
  and may not distinguish difficulty tiers.

## Verification Evidence

- `python3 -m py_compile scripts/play_game.py`
- `python3 -m py_compile _workspace/experiments/v0.10.11-live-capture-matrix/run_sessions.py`
- `python3 _workspace/experiments/v0.10.11-live-capture-matrix/run_sessions.py`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.11-live-capture-matrix/results.json --output _workspace/experiments/v0.10.11-live-capture-matrix/diagnostics.md`
- `python3 -m json.tool _workspace/experiments/v0.10.11-live-capture-matrix/results.json >/dev/null`
- `python3 -m py_compile scripts/diagnose_runs.py`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
