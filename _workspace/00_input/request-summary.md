# Request Summary - Post-Guidance Validation

## Phase / Gate
Phase 7: AI-agent gameplay evaluation follow-up — post-guidance validation for
the access-commitment guidance hardening.

## Scope
Test whether the v0.10.3 access-commitment guidance can be represented as a
bounded simulated-agent policy change. Compare unchanged free-form Hard
competitive policies against a guidance-aware variant that suppresses repeated
or high-access pledges and redirects to existing legal fallback actions.

Expected artifacts:
- `_workspace/experiments/v0.10.4-post-guidance-validation/run_sessions.py`
- `_workspace/experiments/v0.10.4-post-guidance-validation/results.json`
- `docs/playtest-findings-v0.10.4.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- package version metadata (`0.10.4`)
- `_workspace/final/handoff.md`

## Non-Goals
- No simulation behavior changes.
- No command grammar, MCP DTO, scenario schema, replay artifact, state hash, or
  balance changes.
- No automatic runtime command cooldowns or pledge-effect tuning.
- No default baseline batch replacement in `scripts/run_automated_playtests.py`.
- No LLM runner.
- No human-learning, calibration, classroom-effectiveness, policy-validity, or
  balance-tuning claims.

## Sources
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.10.2.md`
- `CHANGELOG.md`
- `docs/how-to-play.md`
- `LESSONS.md`
- `SPEC.md`

## Validation Target
- `python3 _workspace/experiments/v0.10.4-post-guidance-validation/run_sessions.py`
- `python3 -m json.tool _workspace/experiments/v0.10.4-post-guidance-validation/results.json >/dev/null`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
- Three-pass `code-reviewer` loop on the PR diff.
