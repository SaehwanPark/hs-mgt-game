# Request Summary - Live Retry Cash-Pressure Diagnostics

## Scope

Implement the next preferred-workflow development continuation slice for the
Health Policy Strategy Game: make cash-pressure and validation-retry signals
visible for access-heavy live agents under Hard difficulty.

## Phase

Phase 7 simulated-agent evidence diagnostics. This is a diagnostic visibility
slice over existing capture artifacts, not runtime mechanics, balance, or
educational effectiveness validation.

## Sources

- User request to implement the approved continuation plan.
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.10.16.md`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- Existing live-capture diagnostics in `scripts/diagnose_runs.py`

## Expected Files

- `scripts/diagnose_runs.py`
- `tests/fixtures/live_capture_batch.json`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
- `docs/playtest-findings-v0.10.17.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Validation Target

The diagnostic report separates final replay validation failures from live
decision retries and identifies cash-overrun retries from optional
`live_validation_retries` metadata. The `v0.10.15` Hard Live Access Operator
retry signal is visible without changing runtime behavior.

## Non-Goals

- No runtime simulation, balance formula, transition, command validation,
  stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
  change.
- No access-pledge cooldown, command-cost tuning, action-availability change,
  general analytics platform, optimizer, or broad diagnostics framework.
- No human-learning, classroom-effectiveness, empirical calibration,
  policy-validity, or balance-tuning claim.
