# Request Summary - Rival Information Pressure Design

## Scope

- Roadmap phase: Phase 7 validation and teachability gate.
- Task type: development continuation from `v0.10.35`.
- Selected slice: documentation-first design note for rival information and
  monitoring pressure visibility by difficulty tier.
- Branch: `feat/rival-info-pressure-design-v0.10.36`.

## Sources

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.10.35.md`
- `docs/expansion-proposal-review.md`

## Expected Files

- `docs/playtest-findings-v0.10.36.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Validation Target

- Referenced JSON artifacts parse.
- No runtime behavior changes.
- Standard Rust checks still pass.
- Domain QA confirms the artifact preserves actor-observation, deterministic
  replay, scope, and evidence-limit boundaries.

## Non-Goals

- No runtime simulation, balance, scenario schema, MCP DTO, replay, state hash,
  command grammar, AP budget, command-cost, scoring, or difficulty value change.
- No Expert winnability claim, hidden rival omniscience, broad balance pass,
  GUI, M&A, release automation, human-learning claim, empirical calibration, or
  policy-validity claim.
