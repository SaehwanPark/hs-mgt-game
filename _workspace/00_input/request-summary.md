# Request Summary - Strategy-Space Diagnostics Artifact

## Phase / Gate
Phase 7: AI-agent gameplay evaluation and strategy-space diagnostics

## Scope
Continue development from the clean `v0.9.4` checkpoint by adding a lightweight
diagnostics artifact path for scripted MCP playtest batches. Preserve current
simulation behavior while making automated playtest evidence easier to inspect
for action frequencies, outcome ranges, validation failures, and follow-up
routing.

Expected artifacts:
- `scripts/run_automated_playtests.py`
- `scripts/diagnose_runs.py`
- `docs/playtest-findings-v0.9.5.md`
- `docs/mcp-playtesting-guide.md`
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

## Sources
- `README.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.9.4.md`
- `SPEC.md`
- `scripts/run_automated_playtests.py`
- `scripts/diagnose_runs.py`

## Validation Target
- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/run_automated_playtests.py --json-output _workspace/experiments/v0.9.5-playtest-batch/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.5-playtest-batch/results.json --output _workspace/experiments/v0.9.5-playtest-batch/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
