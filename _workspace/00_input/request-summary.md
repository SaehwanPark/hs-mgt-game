# Request Summary - Difficulty-Tier Playtest Synthesis

## Phase / Gate
Phase 7: AI-agent gameplay evaluation and strategy-space diagnostics

## Scope
Continue development from the clean `v0.9.7` checkpoint by adding a targeted
automated MCP playtest mode for competitive difficulty-tier coverage (Easy and
Hard). Preserve current simulation behavior while capturing evidence required
by the agent playtest protocol for difficulty variation.

Expected artifacts:
- `scripts/run_automated_playtests.py`
- `scripts/diagnose_runs.py`
- `docs/playtest-findings-v0.9.8.md`
- `docs/mcp-playtesting-guide.md`
- `LESSONS.md` (if needed)
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
- No folding difficulty sweep into the default baseline batch.
- No Expert difficulty unless Easy/Hard sweep completes cleanly.

## Sources
- `README.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.9.7.md`
- `SPEC.md`
- `scripts/run_automated_playtests.py`
- `scripts/diagnose_runs.py`

## Validation Target
- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/run_automated_playtests.py --target difficulty-sweep --json-output _workspace/experiments/v0.9.8-difficulty-sweep/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.8-difficulty-sweep/results.json --output _workspace/experiments/v0.9.8-difficulty-sweep/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
