# Request Summary - Competitive Playtest Policy Coverage

## Phase / Gate
Phase 7: AI-agent gameplay evaluation and strategy-space diagnostics

## Scope
Continue development from the clean `v0.9.5` checkpoint by extending scripted
competitive MCP playtest policies beyond month 3. Preserve current simulation
behavior while improving 24-month command coverage for newer service-line,
public-payer, staffing, monitoring, and commitment commands.

Expected artifacts:
- `scripts/run_automated_playtests.py`
- `docs/playtest-findings-v0.9.6.md`
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
  equilibrium, or policy-validity claims.
- No broad raw transcript archive.
- No new analytics platform or automated optimization framework.

## Sources
- `README.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.9.5.md`
- `SPEC.md`
- `scripts/run_automated_playtests.py`
- `scripts/diagnose_runs.py`

## Validation Target
- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/run_automated_playtests.py --json-output _workspace/experiments/v0.9.6-playtest-policy-coverage/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.6-playtest-policy-coverage/results.json --output _workspace/experiments/v0.9.6-playtest-policy-coverage/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
