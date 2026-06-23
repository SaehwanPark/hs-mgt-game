# Project Specification

This file is the lightweight spec-driven-development index for the Health
Policy Strategy Game. It tracks what is already true, what is being changed now,
and what is intentionally deferred.

Canonical product and domain direction lives in:

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`

## Past

- Project concept established as a Rust, CLI-first health-policy strategy game
  about leading a fictional nonprofit US health system.
- Canonical proposal, roadmap, and design principles created under `docs/`.
- Repo-local agent harness created for project-specific health-policy simulation
  workflow.
- Rust package scaffold and spec-driven documentation baseline established.

## Present

- Feature: Deterministic vertical-slice spine
  Status: Active
  Started: 2026-06-23
  Branch: feat/deterministic-slice-spine

  Summary:
  Replace the placeholder CLI with a small deterministic architecture proof: a
  scripted health-system turn with explicit resolved inputs, validation,
  actor-specific observation, one commercial-insurer decision rationale,
  attributed effects, append-only history, and replay verification.

  Verification:
  - Identical prior state, command, resolved inputs, and ruleset produce the
    same transition
  - Observed access can differ from true access through explicit resolved inputs
  - Invalid commands fail validation separately from unfavorable modeled outcomes
  - Replay from genesis reproduces the committed final state
  - `cargo fmt`, `cargo test`, and `cargo run` pass

  Out of Scope:
  - Full campaign or multiple-turn scenario design
  - Interactive CLI input
  - Scenario file loading or external data ingestion
  - Empirical calibration or policy forecasting claims
  - CI, release automation, or contributor-process expansion

## Future

- Define glossary, decision-record conventions, and versioning policy from
  roadmap Phase 0.
- Convert Phase 1 research into an evidence registry and research-to-design
  implications memo.
- Define the initial conceptual model: system boundary, actor classes, ontology,
  observation model, and causal framework.
- Design the first narrow vertical slice with at least one strategic negotiation,
  one policy process, deterministic replay, and educational debrief hooks.
- Split the prototype into stable module boundaries when the next slice needs
  more than one command or actor interaction.
- Add scenario data loading only after the conceptual model and first action
  vocabulary settle.
