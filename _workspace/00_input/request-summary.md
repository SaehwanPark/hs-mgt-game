# Request Summary - Access Follow-Through Debrief Note

## Scope

Implement the approved preferred-workflow continuation slice for the Health
Policy Strategy Game: add a concise competitive debrief explanation for
access-heavy runs that separates public access pledges from durable operational
follow-through under low final cash.

## Phase

Phase 7 explanatory debrief wording. This is a Rust debrief and project-state
slice, not runtime mechanics, balance, command-surface, or educational
effectiveness validation.

## Sources

- User request to implement the approved v0.10.23 plan.
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.10.22.md`
- `_workspace/final/handoff.md`

## Expected Files

- `src/debrief/report.rs`
- `src/debrief/report_tests.rs`
- `docs/playtest-findings-v0.10.23.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/00_input/request-summary.md`
- `_workspace/final/handoff.md`

## Validation Target

The competitive debrief adds an explanatory access follow-through note only
when committed history shows at least two human access pledges, final human cash
below `20`, and fewer durable follow-through actions than pledges. Focused tests
cover the trigger and non-trigger cases.

## Non-Goals

- No runtime simulation, balance formula, transition, Rust MCP DTO, Python
  wrapper logic, diagnostic parser logic, command grammar, stochastic input,
  scenario schema, replay artifact, state hash, action-cost, or ruleset change.
- No MCP transport, auth, durable session persistence, multi-client support, or
  broad tool DTO redesign.
- No access-pledge cooldown, command-cost tuning, action-availability change,
  human-learning claim, empirical calibration, policy-validity claim, or
  balance-tuning claim.
- No new live-capture runs.
