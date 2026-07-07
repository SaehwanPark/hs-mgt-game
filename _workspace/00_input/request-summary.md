# Request Summary - LLM Access-Pledge Evidence

## Scope

Continue development after PR #88 with a PR-sized Phase 7 evidence slice. Test
whether repeated access pledges appear in bounded sub-agent generated command
plans outside deterministic operator heuristics.

## Non-Goals

- No runtime access-pledge cooldown or pledge-effect tuning.
- No command grammar, scenario schema, MCP DTO, transition, replay, state hash,
  or balance change.
- No general LLM runner or live LLM integration.
- No human-learning, classroom-effectiveness, empirical calibration,
  policy-validity, or balance claim.

## Sources

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.10.5.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`

## Expected Files

- `docs/playtest-findings-v0.10.7.md`
- `_workspace/experiments/v0.10.7-llm-access-pledge-evidence/run_sessions.py`
- `_workspace/experiments/v0.10.7-llm-access-pledge-evidence/results.json`
- `SPEC.md`, `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`
- `_workspace/01_evidence_map.md`, `_workspace/03_domain_qa.md`,
  `_workspace/final/handoff.md`

## Validation Target

Replay at least two 24-month Hard competitive sessions through MCP with zero
validation failures, record command and debrief evidence, and keep conclusions
limited to simulated-agent evidence.
