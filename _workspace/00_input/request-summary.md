# Request Summary - Gameplay Testing and Review

## Scope

Design a plan to test and review the gameplay of the Health Policy Strategy Game using 3 automated test-player subagents playing via the implemented Model Context Protocol (MCP) server. Collect their logs, analyze the feedback, and produce a comprehensive report assessing:
1. Winnability/Clearability (winnable but not trivial).
2. Entertainment value (non-deterministic transitions, meaningful strategic trade-offs, and lack of a single dominant strategy).

## Phase

Phase 4: Validation / Playtest (aligned with Phase 7 prep protocol of the roadmap).

## Non-Goals

- Do not modify the Rust simulation engine, command parser, or database/ruleset logic.
- Do not add or change any CLI features.
- Do not implement new MCP endpoints or protocols.
- Do not modify existing scenario parameters.

## Sources

- `README.md`
- `docs/external-playtest-protocol.md`
- `docs/how-to-play.md`
- `docs/mcp-agent-interface.md`
- `src/mcp/session.rs`

## Expected Files

- `_workspace/00_input/request-summary.md` (this file)
- `_workspace/03_domain_qa.md` (Domain QA review notes)
- `_workspace/final/handoff.md` (Summary of playtest run and results)
- `docs/playtest-findings-v0.1.42.md` (Comprehensive playtest report)

## Validation Target

- Run at least 3 distinct subagents playing both `stabilization-v1` and `competitive-regional-v1` campaign sessions.
- Produce explicit feedback from each test-player on comprehension, tradeoffs, pacing, winnability, and entertainment.
- Compile observations into a formal report.
