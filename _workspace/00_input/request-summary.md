# Request Summary - Live MCP Capture Evidence

## Scope

Implement the next preferred-workflow development continuation slice for the
Health Policy Strategy Game: live observation-by-observation MCP evidence
capture for the competitive Hard campaign.

## Phase

Phase 7 validation and calibration evidence. This is workflow/evidence capture,
not runtime mechanics, balance, or educational effectiveness validation.

## Sources

- User request to implement the preferred-workflow continuation + PR handoff plan.
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- Latest handoff: `_workspace/final/handoff.md`

## Expected Files

- `scripts/play_game.py`
- `_workspace/experiments/v0.10.9-live-mcp-capture/run_sessions.py`
- `_workspace/experiments/v0.10.9-live-mcp-capture/results.json`
- `docs/playtest-findings-v0.10.9.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/01_evidence_map.md`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Validation Target

Three deterministic persona-policy runs complete the Hard competitive campaign
at seed `42` through MCP trace capture with zero validation failures. The
artifact records observations, legal command hints, submitted commands,
transition hashes, final observations, and debriefs.

## Non-Goals

- No runtime access-pledge cooldown, pledge-effect tuning, transition change,
  command validation change, stochastic input change, scenario schema change,
  MCP DTO change, state hash change, or balance change.
- No general LLM runner, networked agent integration, hidden-state exposure, or
  MCP transport change.
- No human-learning, classroom-effectiveness, empirical calibration,
  policy-validity, or balance-tuning claim.
