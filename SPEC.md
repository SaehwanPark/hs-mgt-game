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
- Rust package scaffold exists with a placeholder CLI entry point.

## Present

- Feature: Spec-driven documentation baseline
  Status: Active
  Started: 2026-06-23
  Branch: feat/spec-doc-baseline

  Summary:
  Initiate root-level SDD documents so future implementation work has a stable
  place to track specification state, architecture boundaries, release history,
  and development lessons.

  Verification:
  - `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, and `LESSONS.md` exist at the
    repository root
  - Documents align with the canonical proposal, roadmap, design principles, and
    harness team spec
  - Package version is bumped for this PR-equivalent documentation change
  - `cargo fmt` and `cargo test` still pass

  Out of Scope:
  - Adding new gameplay mechanics
  - Defining detailed scenario data formats
  - Adding CI, release automation, or contributor process beyond the initiated
    documentation baseline

## Future

- Replace the placeholder CLI with the first deterministic engine proof of
  concept.
- Define glossary, decision-record conventions, and versioning policy from
  roadmap Phase 0.
- Convert Phase 1 research into an evidence registry and research-to-design
  implications memo.
- Define the initial conceptual model: system boundary, actor classes, ontology,
  observation model, and causal framework.
- Design the first narrow vertical slice with at least one strategic negotiation,
  one policy process, deterministic replay, and educational debrief hooks.
- Add focused tests around deterministic transitions once core mechanics exist.
