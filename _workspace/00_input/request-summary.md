# Request Summary - Live Difficulty Evidence Synthesis

## Scope

Implement the next preferred-workflow development continuation slice for the
Health Policy Strategy Game: synthesize recent Phase 7 live difficulty evidence
from `v0.10.12` through `v0.10.15` and select one bounded follow-up issue before
any runtime tuning.

## Phase

Phase 7 simulated-agent evidence synthesis and strategy-space diagnostics. This
is a documentation and handoff slice over existing capture artifacts, not runtime
mechanics, balance, or educational effectiveness validation.

## Sources

- User request to implement the approved continuation plan.
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/mcp-playtesting-guide.md`
- Latest handoff: `_workspace/final/handoff.md`
- Prior evidence: `docs/playtest-findings-v0.10.12.md`,
  `docs/playtest-findings-v0.10.13.md`,
  `docs/playtest-findings-v0.10.14.md`, and
  `docs/playtest-findings-v0.10.15.md`
- Existing live-capture artifacts under `_workspace/experiments/`

## Expected Files

- `docs/playtest-findings-v0.10.16.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Validation Target

The synthesis cites session counts, seeds, difficulty tiers, profile families,
validation failures/retries, access-heavy behavior, and evidence limits. It
selects cash-pressure and validation-retry visibility for access-heavy Hard live
agents as the next bounded issue while preserving existing runtime and MCP
interfaces.

## Non-Goals

- No runtime simulation, balance formula, transition, command validation,
  stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
  change.
- No access-pledge cooldown, command-cost tuning, action-availability change,
  general LLM runner, analytics platform, optimizer, or broad diagnostics
  framework.
- No human-learning, classroom-effectiveness, empirical calibration,
  policy-validity, or balance-tuning claim.
