# Request Summary - Post-Change All-Tier Difficulty Validation v0.11.11

## Scope

- Capture current-code `competitive-regional-v1` sessions after the v0.11.7
  AI risk-posture and v0.11.8 rival-resource changes.
- Run the existing five deterministic policy profiles across seeds `42`, `43`,
  and `44` at Easy, Normal, Hard, and Expert difficulty.
- Preserve actor-visible observations, legal commands, submitted commands,
  validation failures, committed histories, state hashes, final observations,
  and debriefs.
- Audit clearability proxies, strategy trajectories, operating accounting,
  endpoint tradeoffs, bottlenecks, and debrief traceability.
- Bump the package to `0.11.11` and complete the branch, PR, and review
  handoff.

## Non-goals

- No runtime mechanics, difficulty values, AI scoring, commands, scenarios,
  rulesets, replay formats, MCP schemas, or state-hash implementation changes.
- No generalized evidence schema or normalization of historical artifacts.
- No causal strategy, dominance, balance, general winnability, human-learning,
  empirical-calibration, or policy-validity claim.
- No runtime promotion in this evidence slice, even if a follow-up gap is
  identified.

## Sources

- `SPEC.md` ranked Phase 7 queue and v0.11.7-v0.11.10 history.
- `docs/roadmap.md`, Phase 7 validation and AI-agent evidence limits.
- `docs/agent-playtest-protocol.md` matrix and trace requirements.
- `_workspace/experiments/v0.11.1-operating-loop-ai-validation/` existing
  five-profile all-tier runner and audit contracts.
- `_workspace/experiments/v0.11.9-expert-difficulty-validation/` current
  post-change capture and failure-preserving runner pattern.
- `docs/playtest-findings-v0.11.9.md` and `docs/playtest-findings-v0.11.10.md`.

## Expected Files

- `_workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/`.
- `tests/test_phase7_post_change_all_tier_validation.py`.
- `docs/playtest-findings-v0.11.11.md`, `SPEC.md`, `CHANGELOG.md`, `README.md`,
  `docs/roadmap.md`, `docs/mcp-playtesting-guide.md`, and `LESSONS.md`.
- `Cargo.toml`, `Cargo.lock`, `_workspace/03_domain_qa.md`, and
  `_workspace/final/handoff.md`.

## Validation Target

- Exactly 60 unique profile/seed/difficulty coordinates and 1,440 committed
  months are captured.
- Every run completes with zero validation failures before PR handoff.
- The Normal seed-42 hold-control hash remains `61357596d8800592`.
- Focused artifact tests, the full Python/Rust suites, formatting, clippy,
  automated playtests, JSON validation, and diff checks pass.
