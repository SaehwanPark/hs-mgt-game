# Domain QA - Live Retry Cash-Pressure Diagnostics

## Status

pass

## Reviewed Inputs

- `docs/playtest-findings-v0.10.16.md`
- `docs/playtest-findings-v0.10.17.md`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
- `scripts/diagnose_runs.py`
- `tests/fixtures/live_capture_batch.json`
- `_workspace/00_input/request-summary.md`
- Canonical docs and harness team spec

## Findings

- Scope fit: The slice stays in Phase 7 diagnostics and does not change runtime
  mechanics, command grammar, transition logic, stochastic inputs, scenario
  schemas, MCP DTOs, replay formats, state hashes, or balance values.
- Evidence labeling: The findings consistently label retry counts as
  simulated-agent/operator-authored decision-process evidence, not balance
  proof, empirical calibration, human-learning evidence, or policy validity.
- Observation boundary: The diagnostic reads optional wrapper metadata already
  present in the artifact and does not request hidden runtime state or MCP DTO
  expansion.
- Determinism: No accepted command streams, replay artifacts, state hashes, or
  simulation inputs are changed. The regenerated diagnostic is derived from the
  fixed `v0.10.15` artifact.
- Follow-up fit: The live retry table directly addresses the `v0.10.16`
  selected issue by separating accepted-stream validity from cash-overrun live
  retries.

## Required Fixes

None.

## Residual Risks

- The evidence base remains simulated-agent evidence, not human play.
- The retry signal depends on optional wrapper metadata; older artifacts without
  that field report zero live retries.
- Cash-overrun retry classification currently uses validation error text.
- The diagnostic final-metric parser depends on current competitive debrief
  wording.

## Verification Evidence

- `python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
- `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
