# Request Summary - Access Commitment Guidance Hardening

## Phase / Gate
Phase 7: AI-agent gameplay evaluation follow-up — player-facing guidance
hardening from the access-loop diagnostic.

## Scope
Convert the completed `v0.10.2` access-loop diagnostic into competitive
player-facing guidance. Clarify that public access pledges can reduce scrutiny
and build legitimacy, but repeated pledges do not substitute for durable
capacity, staffing, monitoring, or payer work.

Expected artifacts:
- `src/cli/guidance.rs`
- `docs/how-to-play.md`
- `SPEC.md`
- `CHANGELOG.md`
- package version metadata (`0.10.3`)
- `_workspace/final/handoff.md`

## Non-Goals
- No simulation behavior changes.
- No command grammar, MCP DTO, scenario schema, replay artifact, state hash, or
  balance changes.
- No automatic runtime command cooldowns or pledge-effect tuning.
- No new playtest evidence batch or LLM runner.
- No default baseline batch replacement in `scripts/run_automated_playtests.py`.
- No human-learning, calibration, classroom-effectiveness, or policy-validity
  claims.

## Sources
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.10.2.md`
- `LESSONS.md`
- `SPEC.md`

## Validation Target
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`
- Three-pass `code-reviewer` loop on the PR diff.
