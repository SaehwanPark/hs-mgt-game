# Request Summary: AI-Agent Playtest Documentation Pivot

## Scope

Update repository documentation and planning artifacts so AI-agent and
sub-agent playtests replace planned external human playtest recruitment as the
active Phase 7 validation path.

## Roadmap Phase

Phase 7 validation and calibration, with documentation updates touching Phase 6
handoff language and Phase 8 release limitations.

## Non-Goals

- No Rust runtime, ruleset, scenario, replay, MCP DTO, or golden-hash changes.
- No new automation dependencies or code.
- No empirical calibration, policy-forecasting claim, or human learning-outcome
  claim from agent runs.
- No deletion of historical records solely because they mention external
  playtests.

## Sources

- `README.md`
- `SPEC.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/external-playtest-protocol.md`
- `docs/mcp-agent-interface.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.1.42.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`

## Expected Files

- New `docs/agent-playtest-protocol.md`
- New `docs/decision-records/0009-ai-agent-playtest-validation-path.md`
- Updated active planning, protocol, evidence, glossary, version, changelog, and
  lesson documents.

## Validation Target

Docs identify AI-agent playtests as the active validation path, keep agent
evidence limits visible, and preserve deterministic/reproducible MCP evidence
requirements. Verification should run MCP playtest automation, Rust checks, and
stale-language scans.
