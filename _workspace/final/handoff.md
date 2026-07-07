# Final Handoff - Live MCP Capture Evidence

## Summary

Implemented the `v0.10.9` Phase 7 live MCP capture slice. The Python MCP wrapper
can now optionally return per-month trace entries containing actor-visible
observations, legal command hints, submitted command text, validation failures,
transition summaries, and done state. Three deterministic Hard competitive
persona-policy runs at seed `42` completed 24 months with zero validation
failures.

This is evidence/workflow-only. It does not change transition logic, validation,
command grammar, scenario schemas, MCP DTOs, replay hashes, state hashes, or
balance values.

## Changed Files

- `scripts/play_game.py`: optional trace capture return field.
- `docs/playtest-findings-v0.10.9.md`: findings and evidence limits.
- `_workspace/experiments/v0.10.9-live-mcp-capture/`: capture script and JSON
  artifact.
- `_workspace/00_input/request-summary.md`, `_workspace/01_evidence_map.md`,
  `_workspace/03_domain_qa.md`: harness handoff artifacts.
- `SPEC.md`, `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`: `v0.10.9` record and
  package metadata.
- `docs/mcp-playtesting-guide.md`: live-capture command and evidence boundary.

## Verification

- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
- `python3 _workspace/experiments/v0.10.9-live-mcp-capture/run_sessions.py`
- `python3 -m json.tool _workspace/experiments/v0.10.9-live-mcp-capture/results.json >/dev/null`
- `python3 scripts/run_automated_playtests.py --target project-coverage --json-output /tmp/hs-mgt-game-project-coverage.json`

## PR Handoff

- Branch: `feat/live-mcp-capture-evidence`
- Base: `main`
- PR: pending

## Review Summary

Pending PR review loop.

## Known Limits

- The runs are simulated-agent evidence, not human play, classroom learning, or
  empirical calibration.
- Policies are deterministic local heuristics, not autonomous live LLM play.
- One seed and one difficulty cannot support balance conclusions.
