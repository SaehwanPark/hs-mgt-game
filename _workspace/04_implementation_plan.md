# Implementation Plan - Live-Capture Diagnostics

## Summary

Add a bounded diagnostics path for live MCP capture artifacts. Keep the change
additive to `scripts/diagnose_runs.py`, preserve existing replay and automated
batch diagnostics, and document the output as simulated-agent evidence only.

## Key Changes

- Detect artifacts with top-level `runs` and `evidence_type`.
- Parse command verbs from submitted command text.
- Parse final player metrics from existing debrief lines.
- Print profile outcome and action-frequency tables with evidence limits.
- Add a compact fixture and generate the v0.10.10 diagnostic report from the
  v0.10.9 live-capture artifact.

## Tests

- `python3 -m py_compile scripts/diagnose_runs.py`
- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.9-live-mcp-capture/results.json --output _workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## Non-Goals

No runtime mechanics, transition, validation, scenario schema, MCP DTO, replay
format, state hash, balance, LLM runner, optimizer, or analytics platform
change.
