# Live Retry Cash-Pressure Diagnostics v0.10.17

- **Status:** Phase 7 diagnostic visibility slice
- **Date:** 2026-07-08
- **Code version:** 0.10.17
- **Campaign:** `competitive-regional-v1`
- **Evidence input:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`

This slice implements the follow-up selected in `v0.10.16`: make cash-pressure
and validation-retry signals visible for access-heavy live agents before any
runtime tuning. It changes diagnostic reporting only. It does not change runtime
mechanics, validation rules, command grammar, scenario schemas, MCP DTOs, replay
formats, state hashes, action costs, or balance values.

## Diagnostic Change

`scripts/diagnose_runs.py` now reads optional `live_validation_retries` metadata
from live-capture artifacts and reports:

- final replay validation failures;
- live retry count;
- cash-overrun retry count;
- other retry count;
- representative retry details.

Artifacts without `live_validation_retries` remain compatible and report zero
live retries.

## Findings

The regenerated `v0.10.15` diagnostic separates accepted command-stream
validity from live decision-process friction:

| Profile | Difficulty | Final validation failures | Live retries | Cash-overrun retries | Other retries |
| --- | --- | ---: | ---: | ---: | ---: |
| Live Fiscal Steward | Normal | 0 | 0 | 0 | 0 |
| Live Fiscal Steward | Hard | 0 | 0 | 0 | 0 |
| Live Competitive Analyst | Normal | 0 | 0 | 0 | 0 |
| Live Competitive Analyst | Hard | 0 | 0 | 0 | 0 |
| Live Access Operator | Normal | 0 | 2 | 1 | 1 |
| Live Access Operator | Hard | 0 | 7 | 6 | 1 |

The strongest signal remains the Hard Live Access Operator: the final accepted
stream replayed cleanly, but the live decision process had repeated rejected
cash-overrun attempts after cash became constrained.

## Interpretation

- Final replay validation failures answer whether the accepted command stream
  is legal and reproducible.
- Live retries answer whether the decision process encountered command-surface
  or resource-pressure friction before the accepted stream.
- Cash-overrun retries are useful guidance and debrief evidence, but they are
  not enough to justify changing runtime balance, command costs, or action
  availability by themselves.

## Follow-Up Routing

- Use this diagnostic surface in future live-decision evidence gates.
- Keep runtime tuning deferred until a later evidence slice identifies a
  concrete mechanic problem, not just live operator friction.
- If access-heavy Hard play remains the focus, compare guidance/debrief changes
  against retry counts and final tradeoff metrics before considering balance
  changes.

## Verification

```bash
python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
