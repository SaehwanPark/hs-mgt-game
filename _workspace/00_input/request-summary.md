# Request Summary - Static-vs-Adaptive Live Capture

## Scope

Implement the next preferred-workflow development continuation slice for the
Health Policy Strategy Game: compare static deterministic profile policies
against the existing difficulty-adaptive wrapper in one observation-by-
observation live MCP capture artifact.

## Phase

Phase 7 simulated-agent evidence and strategy-space diagnostics. This is a new
evidence artifact over existing capture tooling and policies, not runtime
mechanics, balance, or educational effectiveness validation.

## Sources

- User request to implement the preferred-workflow continuation + PR handoff
  plan.
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- Latest handoff: `_workspace/final/handoff.md`
- Prior pressure slice: `docs/playtest-findings-v0.10.12.md`
- Existing automated policies: `scripts/run_automated_playtests.py`

## Expected Files

- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py`
- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md`
- `docs/playtest-findings-v0.10.13.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/01_evidence_map.md`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Validation Target

The static-vs-adaptive live capture completes 48 competitive sessions across
four deterministic policies, seeds `42`, `43`, and `44`, Normal/Hard difficulty
tiers, and static/adaptive policy variants. Diagnostics report profile outcomes,
action frequencies, validation failures, access pledge counts, final hashes, and
explicit evidence limits while preserving existing runtime and MCP interfaces.

## Non-Goals

- No runtime simulation, balance formula, transition, command validation,
  stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
  change.
- No LLM runner, analytics platform, optimizer, or broad diagnostics framework.
- No human-learning, classroom-effectiveness, empirical calibration,
  policy-validity, or balance-tuning claim.
