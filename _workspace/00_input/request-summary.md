# Request Summary - Free-Form Hard Seed Variation

## Phase / Gate
Phase 7: AI-agent gameplay evaluation — free-form Hard competitive seed variation

## Scope
Continue from the completed `v0.10.0` checkpoint by extending the bounded
free-form MCP competitive Hard artifact from seed `42` to seeds `42`, `43`, and
`44`. Document whether the existing observation-driven profiles complete the
full 24-month `competitive-regional-v1` campaign across seeds and whether
strategy endpoint claims remain seed-limited.

Expected artifacts:
- `docs/playtest-findings-v0.10.1.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- package version metadata (`0.10.1`)
- `_workspace/final/handoff.md`
- `_workspace/experiments/v0.10.1-free-form-hard-seed-variation/results.json`
  (operator capture)

## Non-Goals
- No simulation behavior changes.
- No command grammar, MCP DTO, scenario schema, replay artifact, state hash, or
  balance changes.
- No new LLM runner committed to the repository.
- No Expert difficulty sweep, stabilization re-run requirement, or
  human-learning claims.
- No default baseline batch replacement in `scripts/run_automated_playtests.py`.
- No profile-policy tuning or validation-failure retries.

## Sources
- `README.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.10.0.md`
- `docs/playtest-findings-v0.9.9.md`
- `docs/playtest-findings-v0.1.54.md`
- `docs/playtest-findings-v0.1.55.md`
- `SPEC.md`
- `scripts/play_game.py`

## Validation Target
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
- `python3 _workspace/experiments/v0.10.1-free-form-hard-seed-variation/run_sessions.py`
- `python3 -m json.tool _workspace/experiments/v0.10.1-free-form-hard-seed-variation/results.json >/dev/null`
