# Request Summary - Independent Reviewer-Agent Live Capture

## Scope

Implement the next preferred-workflow development continuation slice for the
Health Policy Strategy Game: run independent observation-conditioned reviewer
policies through the existing observation-by-observation live MCP capture path.

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
- Prior policy comparison: `docs/playtest-findings-v0.10.13.md`
- Existing MCP wrapper and diagnostics: `scripts/play_game.py`,
  `scripts/diagnose_runs.py`

## Expected Files

- `_workspace/experiments/v0.10.14-independent-reviewer-agent-capture/run_sessions.py`
- `_workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json`
- `_workspace/experiments/v0.10.14-independent-reviewer-agent-capture/diagnostics.md`
- `docs/playtest-findings-v0.10.14.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/01_evidence_map.md`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Validation Target

The independent reviewer-agent live capture completes 18 competitive sessions
across three observation-conditioned policies, seeds `42`, `43`, and `44`, and
Normal/Hard difficulty tiers. Diagnostics report profile outcomes, action
frequencies, validation failures, access pledge counts, final hashes, and
explicit evidence limits while preserving existing runtime and MCP interfaces.

## Non-Goals

- No runtime simulation, balance formula, transition, command validation,
  stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
  change.
- No LLM runner, analytics platform, optimizer, or broad diagnostics framework.
- No human-learning, classroom-effectiveness, empirical calibration,
  policy-validity, or balance-tuning claim.
