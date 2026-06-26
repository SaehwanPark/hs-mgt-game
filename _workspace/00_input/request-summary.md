# Request Summary

## Scope

Implement local MCP support so AI agents can autonomously play the current
bounded `stabilization-v1` and `competitive-regional-v1` campaigns.

## Phase

Technical prototype / interface slice over existing Phase 5-6 playable runtime.

## Non-Goals

- No Streamable HTTP, auth, remote deployment, or multi-client service.
- No durable MCP session persistence.
- No new health-policy mechanisms or actor behavior.
- No full 24-month competitive campaign.
- No competitive scenario loading or scenario migration tooling.

## Sources

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- MCP specification `2025-11-25`
- Official Rust SDK `rmcp`

## Expected Files

- `src/mcp/`
- `src/bin/hs-mgt-game-mcp.rs`
- `docs/mcp-agent-interface.md`
- `docs/decision-records/0008-mcp-agent-interface.md`
- `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `CHANGELOG.md`

## Validation Target

MCP agent play must reuse existing deterministic transitions and observations.
Invalid commands must not advance a session. Existing golden hashes must remain
unchanged.
