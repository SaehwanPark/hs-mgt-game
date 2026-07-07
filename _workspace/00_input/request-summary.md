# Request Summary - Live-Capture Diagnostics

## Scope

Implement the next preferred-workflow development continuation slice for the
Health Policy Strategy Game: diagnostic report support for the existing
observation-by-observation live MCP capture artifact.

## Phase

Phase 7 strategy-space diagnostics. This is reporting/tooling over existing
evidence, not runtime mechanics, balance, or educational effectiveness
validation.

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
- Source artifact:
  `_workspace/experiments/v0.10.9-live-mcp-capture/results.json`

## Expected Files

- `scripts/diagnose_runs.py`
- `tests/fixtures/live_capture_batch.json`
- `_workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md`
- `docs/playtest-findings-v0.10.10.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/01_evidence_map.md`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Validation Target

The diagnostics script accepts live-capture artifacts and reports profile
outcomes, action frequencies, validation failures, access pledge counts, final
hashes, and explicit evidence limits while preserving existing replay and
automated-batch diagnostics.

## Non-Goals

- No runtime simulation, balance formula, transition, command validation,
  stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
  change.
- No LLM runner, analytics platform, optimizer, or broad diagnostics framework.
- No human-learning, classroom-effectiveness, empirical calibration,
  policy-validity, or balance-tuning claim.
