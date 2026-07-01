# Request Summary: Naive-Profile Playtest Evidence Slice

## Scope

Implement the preferred-workflow continuation plan for the next Phase 7
validation slice. Add one deterministic `Naive First-Time` profile to the
existing MCP automated playtest batch, run it across both current campaigns and
seeds `42`, `43`, and `44`, then record versioned findings.

## Roadmap Phase

Phase 7 validation and calibration prep. This is scripted-player evidence
collection and synthesis, not gameplay expansion, free-form agent orchestration,
or balance tuning.

## Non-Goals

- No transition, ruleset, scenario schema, replay format, MCP DTO, campaign
  length, active observation, or golden-hash change.
- No LLM/free-form agent runner in this slice.
- No balance tuning, scoring redesign, diagnostics platform, human learning
  claim, empirical calibration claim, or policy forecast claim.

## Sources

- User request to implement the proposed preferred-workflow plan
- `README.md`
- `SPEC.md`
- `_workspace/final/handoff.md` from v0.1.51
- `docs/playtest-findings-v0.1.51.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- Existing MCP playtest scripts under `scripts/`

## Expected Files

- Playtest automation: `scripts/run_automated_playtests.py`
- Findings: `docs/playtest-findings-v0.1.52.md`
- Documentation: `README.md`, `SPEC.md`, `CHANGELOG.md`,
  `docs/mcp-playtesting-guide.md`
- Version and handoff files: `Cargo.toml`, `Cargo.lock`, `_workspace/`

## Validation Target

The automated MCP script should complete 24 sessions across both current
campaigns, four scripted profiles, and seeds `42`, `43`, and `44`, then print
per-seed metric rows and compact metric ranges. Findings must label the output
as scripted-agent evidence and avoid human learning, calibration, balance, or
policy-validation claims.
