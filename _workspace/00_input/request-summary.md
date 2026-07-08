# Request Summary - Access Debrief Validation

## Scope

Implement the approved preferred-workflow continuation slice for the Health
Policy Strategy Game: validate the `v0.10.23` competitive access
follow-through debrief note through bounded MCP trigger/control runs.

## Phase

Phase 7 debrief-surface validation. This is an evidence, documentation, and
project-state slice, not runtime mechanics, balance, command-surface, scenario,
or educational-effectiveness validation.

## Sources

- User request to implement the approved `v0.10.24` plan.
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.10.23.md`
- `_workspace/final/handoff.md`

## Expected Files

- `_workspace/experiments/v0.10.24-access-debrief-validation/run_sessions.py`
- `_workspace/experiments/v0.10.24-access-debrief-validation/results.json`
- `docs/playtest-findings-v0.10.24.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/00_input/request-summary.md`
- `_workspace/final/handoff.md`

## Validation Target

The MCP end-session debrief includes `Access follow-through note:` for
bounded low-cash runs with repeated access pledges and fewer durable
follow-through actions than pledges, and omits the note from nearby control
runs.

## Non-Goals

- No runtime simulation, balance formula, transition, Rust MCP DTO, Python
  wrapper logic, diagnostic parser logic, command grammar, stochastic input,
  scenario schema, replay artifact, state hash, action-cost, or ruleset change.
- No MCP transport, auth, durable session persistence, multi-client support, or
  broad tool DTO redesign.
- No access-pledge cooldown, command-cost tuning, action-availability change,
  human-learning claim, empirical calibration, policy-validity claim, or
  balance-tuning claim.
- No organic live-capture runs or external human recruitment gate.
