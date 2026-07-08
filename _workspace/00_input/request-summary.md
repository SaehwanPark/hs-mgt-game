# Request Summary - Live LLM Difficulty Gate

## Scope

Implement the next preferred-workflow development continuation slice for the
Health Policy Strategy Game: capture live month-by-month sub-agent decisions
through the existing observation-by-observation MCP wrapper and compare Normal
and Hard competitive difficulty for the same seed and profiles.

## Phase

Phase 7 simulated-agent evidence and strategy-space diagnostics. This is a new
evidence artifact over existing capture tooling, not runtime mechanics, balance,
or educational effectiveness validation.

## Sources

- User request to implement the approved continuation plan.
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- Latest handoff: `_workspace/final/handoff.md`
- Prior live reviewer evidence: `docs/playtest-findings-v0.10.14.md`
- Existing MCP wrapper and diagnostics: `scripts/play_game.py`,
  `scripts/diagnose_runs.py`

## Expected Files

- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
- `docs/playtest-findings-v0.10.15.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Validation Target

The live LLM/sub-agent difficulty gate completes six competitive sessions across
three profiles, seed `42`, and Normal/Hard difficulty tiers. Diagnostics report
profile outcomes, action frequencies, validation failures, access pledge counts,
final hashes, and explicit evidence limits while preserving existing runtime and
MCP interfaces.

## Non-Goals

- No runtime simulation, balance formula, transition, command validation,
  stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
  change.
- No general LLM runner, analytics platform, optimizer, or broad diagnostics
  framework.
- No human-learning, classroom-effectiveness, empirical calibration,
  policy-validity, or balance-tuning claim.
