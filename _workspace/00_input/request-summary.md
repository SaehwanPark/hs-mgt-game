# Request Summary - Rival Information Follow-Through Evidence

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation loop.
- Task type: development continuation and bounded evidence capture.
- Selected slice: test whether visible rival monitor intel changes the next
  simulated-policy command without changing runtime mechanics.

## Sources

- Canonical project docs and the harness team specification.
- `docs/playtest-findings-v0.10.37.md` and `docs/playtest-findings-v0.10.42.md`.
- `_workspace/experiments/v0.10.37-rival-info-monitor-evidence/`.
- Existing MCP wrapper and consultant-advice evidence patterns.

## Expected Files

- `_workspace/experiments/v0.10.43-rival-info-follow-through/`
- `tests/test_rival_info_follow_through.py`
- `docs/playtest-findings-v0.10.43.md`, `docs/mcp-playtesting-guide.md`,
  `SPEC.md`, `CHANGELOG.md`, `README.md`, `LESSONS.md`, package metadata,
  and project handoffs

## Validation Target

- Complete 18 runs: three policy arms, seeds 42–44, Hard/Expert, 24 months.
- Record visible signal source months and exact next-turn response commands.
- Verify monitor-ignoring and unmonitored controls retain matching hashes.
- Confirm no Rust runtime, scenario, replay, MCP schema, or state-hash files
  change.

## Non-Goals

- No monitor-cost, AP-budget, difficulty, balance, scoring, public-disclosure,
  rival-AI, or runtime mechanics change.
- No causal monitor-value, human-learning, policy-validity, or calibration
  claim.
