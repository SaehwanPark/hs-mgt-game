# Request Summary - Access-Loop Diagnostic

## Phase / Gate
Phase 7: AI-agent gameplay evaluation — free-form Hard access-loop diagnostic

## Scope
Continue from the completed `v0.10.1` checkpoint by testing whether repetitive
access commitments in free-form Hard competitive runs are reducible through
bounded operator-policy variants. Compare the unchanged baseline policies
against access-pledge cooldown and reported-access-threshold variants across the
same three profiles and seeds `42`, `43`, and `44`.

Expected artifacts:
- `docs/playtest-findings-v0.10.2.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- package version metadata (`0.10.2`)
- `_workspace/final/handoff.md`
- `_workspace/experiments/v0.10.2-access-loop-diagnostic/results.json`
  (operator capture)

## Non-Goals
- No simulation behavior changes.
- No command grammar, MCP DTO, scenario schema, replay artifact, state hash, or
  balance changes.
- No automatic runtime command cooldowns or pledge-effect tuning.
- No new LLM runner committed to the repository.
- No default baseline batch replacement in `scripts/run_automated_playtests.py`.
- No human-learning, calibration, classroom-effectiveness, or policy-validity
  claims.

## Sources
- `README.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.10.1.md`
- `SPEC.md`
- `_workspace/experiments/v0.10.1-free-form-hard-seed-variation/run_sessions.py`
- `scripts/play_game.py`

## Validation Target
- `python3 _workspace/experiments/v0.10.2-access-loop-diagnostic/run_sessions.py`
- `python3 -m json.tool _workspace/experiments/v0.10.2-access-loop-diagnostic/results.json >/dev/null`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
