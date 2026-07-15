# Request Summary — Visual and Audio SDD Alignment v0.12.15

## Scope

- Translate `docs/visual_audio_upgrade_proposal.md` into complete, durable SDD
  requirements without claiming that the proposed interface already exists.
- Replace budget-dependent human testplay work with reproducible AI-agent
  testplay protocols wherever the visual/audio plan calls for validation.
- Record presentation-layer architecture boundaries, phased promotion gates,
  verification targets, explicit non-goals, and version `0.12.15` metadata.
- Commit the proposal adaptation, SDD specification, and final metadata/handoff
  as coherent chunks.

## Sources

- `docs/visual_audio_upgrade_proposal.md` at checkpoint `43e14a6`.
- Current Rust, MCP, GUI proof, scenario, replay, and debrief surfaces.
- Canonical proposal, roadmap, design principles, harness team spec, SPEC,
  architecture, changelog, lessons, and versioning policy.

## Expected files

- AI-testplay-adjusted visual/audio proposal.
- `SPEC.md`, `ARCHITECTURE.md`, and `CHANGELOG.md`.
- Release metadata, lessons, request framing, and durable handoff.

## Validation target

- Full proposal-to-SPEC coverage review.
- Human-testplay wording review for planned visual/audio validation.
- Release metadata consistency check.
- Documentation diff and whitespace checks.

## Explicit non-goals

No simulation, balance, scenario, interface implementation, asset acquisition,
packaging, publication, deployment, or calibration changes. No claim that AI
testplays establish human usability, engagement, accessibility lived
experience, learning, classroom effectiveness, domain-expert validity, or
policy validity.

## Global workflow

Use the repo orchestrator for Phase 8/9 audience-access planning and the global
spec-driven documentation workflow. No Rust implementation workflow is
required unless the audit uncovers a code defect.
