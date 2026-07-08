# Request Summary - Live-Capture Structured Retry Metadata

## Scope

Implement the next preferred-workflow development continuation slice for the
Health Policy Strategy Game: update the Python live-capture wrapper and
diagnostic path so additive MCP structured validation fields are preserved in
retry metadata and preferred during retry classification.

## Phase

Phase 7 agent-play support hardening. This is a live-capture tooling slice
informed by `v0.10.18`, not runtime mechanics, balance, or educational
effectiveness validation.

## Sources

- User request to implement the approved continuation plan.
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.10.18.md`
- `docs/mcp-playtesting-guide.md`
- Existing Python playtest wrapper and diagnostics in `scripts/`

## Expected Files

- `scripts/play_game.py`
- `scripts/diagnose_runs.py`
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py`
- `tests/fixtures/live_capture_batch.json`
- `tests/test_playtest_wrapper.py`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.10.19.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/00_input/request-summary.md`
- `_workspace/final/handoff.md`

## Validation Target

Wrapper-captured retry records preserve the existing `error` string and add
optional `code`, `resource_limit`, and `hint` fields when the MCP server
provides them. Diagnostics prefer structured cash-retry fields and still accept
legacy string-only artifacts. Invalid commands still do not advance sessions.

## Non-Goals

- No runtime simulation, balance formula, transition, Rust MCP DTO, command
  grammar, stochastic input, scenario schema, replay artifact, state hash,
  action-cost, or ruleset change.
- No MCP transport, auth, durable session persistence, multi-client support, or
  broad tool DTO redesign.
- No broad historical artifact rewrite, analytics platform expansion, or
  diagnostic table redesign.
- No access-pledge cooldown, command-cost tuning, action-availability change,
  human-learning claim, empirical calibration, or balance-tuning claim.
