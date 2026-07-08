# Live-Capture Structured Retry Metadata v0.10.19

- **Status:** Phase 7 live-capture tooling hardening slice
- **Date:** 2026-07-08
- **Code version:** 0.10.19
- **Campaign:** `competitive-regional-v1`
- **Evidence input:** `docs/playtest-findings-v0.10.18.md`
- **Exemplar artifact:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`

This slice implements the wrapper-side follow-up from `v0.10.18`: preserve
additive MCP structured validation fields in live-capture retry metadata so
tooling can classify cash-overrun retries without parsing prose when structured
fields are available.

It changes Python capture and diagnostic tooling only. It does not change Rust
runtime mechanics, command legality, scenario formats, replay/state hashes,
ruleset values, or balance.

## Tooling Change

`scripts/play_game.py` now normalizes MCP tool-level structured errors into
retry records that preserve:

- `error` for backward compatibility;
- optional `code`;
- optional `resource_limit`;
- optional `hint`.

`scripts/diagnose_runs.py` now prefers `resource_limit.resource == "cash"` or
`code == "insufficient_cash"` when classifying cash-overrun retries, then falls
back to legacy string matching for older artifacts.

## Exemplar Result

The refreshed `v0.10.15` live difficulty-gate exemplar keeps the same retry
counts as before while making classifiable retries explicit in the artifact:

| Profile | Difficulty | Live retries | Cash-overrun retries | Other retries |
| --- | --- | ---: | ---: | ---: |
| Live Access Operator | Normal | 2 | 1 | 1 |
| Live Access Operator | Hard | 7 | 6 | 1 |

The non-cash examples still remain visible:

- wrapper-only retries can stay string-only when no MCP validation payload
  exists;
- non-resource validator failures can carry `code` without a `resource_limit`.

## Interpretation

- Structured retry metadata reduces wrapper-side ambiguity without changing the
  accepted command stream or final replay validation outcomes.
- Legacy artifacts remain usable because diagnostics still fall back to the
  existing `error` string.
- The refreshed exemplar remains simulated-agent command-surface evidence, not
  human-learning, calibration, or balance evidence.

## Follow-Up Routing

- Future live-capture artifacts should preserve structured retry fields when the
  MCP server provides them.
- Keep broader runtime tuning deferred until a later evidence slice identifies a
  concrete mechanic issue beyond retry classification friction.

## Verification

```bash
python3 -m unittest discover -s tests -p 'test_playtest_wrapper*.py'
python3 -m py_compile scripts/play_game.py scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py tests/test_playtest_wrapper.py
python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json
python3 _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
