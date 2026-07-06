# Request Summary - Free-Form Hard Competitive Playtest Synthesis

## Phase / Gate
Phase 7: AI-agent gameplay evaluation — free-form agent profiles at Hard difficulty

## Scope
Continue from the clean `v0.9.9` checkpoint by collecting bounded free-form MCP
competitive sessions at Hard difficulty on the full 24-month
`competitive-regional-v1` campaign. Document observation-driven play evidence and
compare outcomes against v0.9.9 difficulty-adaptive scripted Hard baselines.

Expected artifacts:
- `docs/playtest-findings-v0.10.0.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- package version metadata (`0.10.0`)
- `_workspace/final/handoff.md`
- `_workspace/experiments/v0.10.0-free-form-hard/results.json` (operator capture)

## Non-Goals
- No simulation behavior changes.
- No command grammar, MCP DTO, scenario schema, replay artifact, state hash, or
  balance changes.
- No new LLM runner committed to the repository.
- No Expert difficulty sweep, stabilization re-run requirement, or human-learning
  claims.
- No default baseline batch replacement in `scripts/run_automated_playtests.py`.

## Sources
- `README.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.9.9.md`
- `docs/playtest-findings-v0.1.54.md`
- `docs/playtest-findings-v0.1.55.md`
- `SPEC.md`
- `scripts/play_game.py`

## Validation Target
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
