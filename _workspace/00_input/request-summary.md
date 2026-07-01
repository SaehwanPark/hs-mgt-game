# Request Summary: Competitive Final Debrief Metrics Slice

## Scope

Implement the preferred-workflow continuation plan for the next Phase 7 evidence
surface. Add bounded final player tradeoff metrics to the competitive MCP
`end_session` debrief so automated playtest findings can compare competitive
outcomes beyond command patterns and final hashes.

## Roadmap Phase

Phase 7 validation and calibration prep. This is a debrief/evidence-surface
extension, not gameplay expansion or balance tuning.

## Non-Goals

- No transition, ruleset, scenario schema, replay format, MCP DTO, campaign
  length, active observation, or golden-hash change.
- No balance tuning, scoring redesign, diagnostics platform, human learning
  claim, empirical calibration claim, or policy forecast claim.
- No rival private-state reporting during active play or final debrief.

## Sources

- User request to implement the proposed preferred-workflow plan
- `README.md`
- `SPEC.md`
- `docs/playtest-findings-v0.1.49.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- Existing MCP session code under `src/mcp/`

## Expected Files

- MCP session code and tests: `src/mcp/session.rs`
- Playtest automation: `scripts/run_automated_playtests.py`
- Documentation: `README.md`, `SPEC.md`, `CHANGELOG.md`,
  `docs/mcp-agent-interface.md`, `docs/mcp-playtesting-guide.md`, `LESSONS.md`
- Version and handoff files: `Cargo.toml`, `Cargo.lock`, `_workspace/`

## Validation Target

Competitive `end_session` debriefs should report final human-system tradeoff and
resource metrics from committed history, and the automated playtest summary
should parse those metrics while leaving MCP schemas, active observations,
deterministic transitions, and golden hashes unchanged.
