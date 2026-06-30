# Request Summary: MCP Playtest Evidence Slice

## Scope

Implement the preferred-workflow continuation plan for the next Phase 7 evidence
slice. Fix the automated MCP playtest harness enough to complete the current
scripted-policy batch, then record versioned findings before changing gameplay.

## Roadmap Phase

Phase 7 validation and calibration prep. This is evidence collection and harness
repair, not gameplay expansion.

## Non-Goals

- No transition, ruleset, scenario schema, replay format, MCP DTO, campaign
  length, or golden-hash change.
- No balance tuning, scoring redesign, diagnostics platform, human learning
  claim, empirical calibration claim, or policy forecast claim.
- No competitive final-metric export in this slice; record it as an evidence gap.

## Sources

- User request to implement the proposed preferred-workflow plan
- `README.md`
- `SPEC.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- Existing scripts under `scripts/`

## Expected Files

- MCP playtest scripts: `scripts/play_game.py`,
  `scripts/run_automated_playtests.py`
- Findings and docs: `docs/playtest-findings-v0.1.49.md`,
  `docs/mcp-playtesting-guide.md`, `README.md`, `SPEC.md`, `CHANGELOG.md`,
  `LESSONS.md`
- Version and handoff files: `Cargo.toml`, `Cargo.lock`, `_workspace/`

## Validation Target

The automated batch should complete three scripted profiles for
`stabilization-v1` and `competitive-regional-v1` at seed `42` without silent
hangs. Findings must preserve AI-agent evidence limits and identify follow-up
work without implying human educational measurement, empirical calibration, or
policy forecasting validity.
