# Request Summary: Feedback-Aligned SDD Future Planning

## Scope

Review the supplied external feedback and translate it into future-facing
spec-driven-development documentation. The work should adjust planning,
validation, evidence, and release bookkeeping without changing runtime behavior.

## Roadmap Phase

Primarily Phase 7 validation and calibration, with Phase 6 and Phase 8 planning
language updated where the feedback affects scenario, debrief, and release
priorities.

## Non-Goals

- No Rust runtime, ruleset, scenario, replay, MCP DTO, or golden-hash changes.
- No new scenario loader, diagnostics implementation, calibration pass, or
  analytics platform.
- No external human recruitment gate or human learning-outcome claim.
- No policy-forecasting claim or research-grade model claim.
- No broad actor, ontology, or framework expansion.

## Sources

- User-supplied external feedback
- `README.md`
- `SPEC.md`
- `ARCHITECTURE.md`
- `CHANGELOG.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/agent-playtest-protocol.md`
- `docs/evidence-registry.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`

## Expected Files

- Updated SDD and release bookkeeping: `SPEC.md`, `ARCHITECTURE.md`,
  `CHANGELOG.md`, `README.md`, `Cargo.toml`, `Cargo.lock`
- Updated planning/evidence docs: `docs/roadmap.md`,
  `docs/agent-playtest-protocol.md`, `docs/evidence-registry.md`, `LESSONS.md`
- Updated handoffs under `_workspace/`

## Validation Target

Future planning should foreground gameplay validity hypotheses,
strategy-space diagnostics, debrief quality, one exemplary scenario,
model-confidence labels, and evidence gates for new abstractions. The docs must
preserve AI-agent evidence limits and avoid implying human educational
measurement, empirical calibration, or policy forecasting validity.
