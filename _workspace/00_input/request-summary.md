# Request Summary - Project-Command Playtest Diagnostics

## Phase / Gate
Phase 7: AI-agent gameplay evaluation and strategy-space diagnostics

## Scope
Continue development from the clean `v0.9.6` checkpoint by adding a targeted
automated MCP playtest mode for competitive capital-project command coverage.
Preserve current simulation behavior while improving diagnostics for project
commands, project kinds, final active projects, and monthly project draws.

Expected artifacts:
- `scripts/run_automated_playtests.py`
- `scripts/diagnose_runs.py`
- `docs/playtest-findings-v0.9.7.md`
- `docs/mcp-playtesting-guide.md`
- `LESSONS.md`
- `SPEC.md`
- `CHANGELOG.md`
- package version metadata
- `_workspace/final/handoff.md`

## Non-Goals
- No simulation behavior changes.
- No command grammar, MCP DTO, scenario schema, replay artifact, state hash, or
  balance changes.
- No human-learning, empirical calibration, classroom-effectiveness,
  equilibrium, policy-validity, or balance-tuning claim.
- No broad raw transcript archive.
- No new analytics platform, automated optimization framework, or default
  baseline-policy replacement.

## Sources
- `README.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.9.6.md`
- `SPEC.md`
- `scripts/run_automated_playtests.py`
- `scripts/diagnose_runs.py`

## Validation Target
- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/run_automated_playtests.py --json-output _workspace/experiments/v0.9.7-baseline-regression/results.json`
- `python3 scripts/run_automated_playtests.py --target project-coverage --json-output _workspace/experiments/v0.9.7-project-command-coverage/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.7-project-command-coverage/results.json --output _workspace/experiments/v0.9.7-project-command-coverage/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
