# Domain QA - Live-Capture Diagnostics

## Status

pass

## Reviewed Inputs

- `scripts/diagnose_runs.py`
- `tests/fixtures/live_capture_batch.json`
- `_workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md`
- `docs/playtest-findings-v0.10.10.md`
- `docs/playtest-findings-v0.10.9.md`
- `_workspace/00_input/request-summary.md`
- `_workspace/01_evidence_map.md`
- Canonical docs and harness team spec

## Findings

- Scope fit: The slice stays in Phase 7 diagnostics and does not change runtime
  mechanics, command grammar, transition logic, stochastic inputs, scenario
  schemas, MCP DTOs, state hashes, or balance values.
- Evidence labeling: Findings and generated diagnostics consistently label the
  artifact as simulated-agent evidence and avoid human-learning, empirical
  calibration, classroom-effectiveness, and policy-validity claims.
- Observation boundary: The diagnostic reads post-run captured observations,
  commands, transition summaries, and debriefs. It does not expose hidden state
  during active play.
- Determinism: The source artifact remains fixed by campaign, seed, difficulty,
  and deterministic persona policies.

## Required Fixes

None.

## Residual Risks

- The final metric parser depends on the current competitive debrief wording.
- One seed, one campaign, and one difficulty tier cannot support balance
  conclusions.
- Conservative command choice may under-sample risky or high-pressure command
  paths.

## Verification Evidence

- `python3 -m py_compile scripts/diagnose_runs.py`
- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.9-live-mcp-capture/results.json --output _workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md`
- `python3 -m json.tool _workspace/experiments/v0.10.9-live-mcp-capture/results.json >/dev/null`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
