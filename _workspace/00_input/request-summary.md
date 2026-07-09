# Request Summary - Rival Information Monitor Evidence

## Scope

- Roadmap phase: Phase 7 validation and teachability gate.
- Task type: development continuation from `v0.10.36`.
- Selected slice: paired live MCP evidence comparing monitored and unmonitored
  rival-information policies on Hard and Expert difficulty.
- Branch: `feat/rival-info-monitor-evidence-v0.10.37`.

## Sources

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/playtest-findings-v0.10.35.md`
- `docs/playtest-findings-v0.10.36.md`
- `SPEC.md`

## Expected Files

- `_workspace/experiments/v0.10.37-rival-info-monitor-evidence/run_sessions.py`
- `_workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json`
- `_workspace/experiments/v0.10.37-rival-info-monitor-evidence/diagnostics.md`
- `scripts/diagnose_runs.py`
- `docs/playtest-findings-v0.10.37.md`
- `docs/mcp-playtesting-guide.md`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
- `Cargo.lock`
- `_workspace/03_domain_qa.md`
- `_workspace/final/handoff.md`

## Validation Target

- Paired Hard/Expert MCP sessions complete 24 transitions with zero validation
  failures.
- Diagnostics expose monitor-intel, public-rival, and intel-gap signal counts.
- No runtime behavior changes.
- Standard Rust checks pass.
- Domain QA confirms the artifact preserves actor-observation, deterministic
  replay, scope, and evidence-limit boundaries.

## Non-Goals

- No runtime simulation, balance, scenario schema, MCP DTO, replay, state hash,
  command grammar, AP budget, command-cost, scoring, difficulty value, or
  rival-AI behavior change.
- No Expert winnability claim, hidden rival omniscience, broad balance pass,
  GUI, M&A, release automation, human-learning claim, empirical calibration, or
  policy-validity claim.
