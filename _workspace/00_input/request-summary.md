# Request Summary - Difficulty-Adaptive Playtest Policies

## Phase / Gate
Phase 7: AI-agent gameplay evaluation and strategy-space diagnostics

## Scope
Continue development from the clean `v0.9.8` checkpoint by adding difficulty-adaptive
scripted MCP playtest policies for competitive Easy and Hard runs. Preserve current
simulation behavior while testing whether rival-aware policy adjustments produce
differentiated player tradeoff metrics across difficulty tiers.

Expected artifacts:
- `scripts/run_automated_playtests.py`
- `scripts/diagnose_runs.py`
- `docs/playtest-findings-v0.9.9.md`
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
  equilibrium, policy-validity, or balance-tuning claim.
- No folding difficulty-adaptive into the default baseline batch.
- No Expert difficulty unless Easy/Hard adaptive sweep completes cleanly.

## Sources
- `README.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.9.8.md`
- `SPEC.md`
- `scripts/run_automated_playtests.py`
- `scripts/diagnose_runs.py`

## Validation Target
- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/run_automated_playtests.py --target difficulty-adaptive --json-output _workspace/experiments/v0.9.9-difficulty-adaptive/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.9-difficulty-adaptive/results.json --output _workspace/experiments/v0.9.9-difficulty-adaptive/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
