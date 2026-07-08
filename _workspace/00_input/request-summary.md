# Request Summary - MCP Structured Validation Errors

## Scope

Implement the next preferred-workflow development continuation slice for the
Health Policy Strategy Game: add additive structured MCP error fields for
competitive validation failures so agent playtest wrappers can classify
resource-limit retries without parsing prose.

## Phase

Phase 7 MCP interface hardening. This is an agent-play support slice informed
by live retry diagnostics, not runtime mechanics, balance, or educational
effectiveness validation.

## Sources

- User request to implement the approved continuation plan.
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.10.17.md`
- `docs/mcp-agent-interface.md`
- Existing MCP session implementation in `src/mcp/session.rs`

## Expected Files

- `src/mcp/session.rs`
- `docs/mcp-agent-interface.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.10.18.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/00_input/request-summary.md`
- `_workspace/final/handoff.md`

## Validation Target

Competitive MCP validation errors preserve the existing `error` string and add
optional `code`, `resource_limit`, and `hint` fields for machine-readable retry
classification. Invalid commands still do not advance sessions.

## Non-Goals

- No runtime simulation, balance formula, transition, command grammar,
  stochastic input, scenario schema, replay artifact, state hash, action-cost,
  or ruleset change.
- No MCP transport, auth, durable session persistence, multi-client support, or
  broad tool DTO redesign.
- No access-pledge cooldown, command-cost tuning, action-availability change,
  human-learning claim, empirical calibration, or balance-tuning claim.
