---
name: hs-mgt-game-orchestrator
description: Route Health Policy Strategy Game work through repo-specific research, design, implementation, and domain-QA handoffs without duplicating global skills.
---

# HS Management Game Orchestrator

## When to Use

- Use this skill for substantial work in this repository that touches research,
  conceptual design, scenario design, simulation mechanics, educational
  debriefing, or deterministic replay boundaries.
- Use it when a request should follow the roadmap phases or preserve `_workspace/`
  handoff artifacts.
- Do not use it for generic Rust formatting, generic code review, release
  preparation, or branch management. Use global skills for those.

## Required Inputs

- User request.
- Current repository state.
- Canonical docs: `README.md`, `docs/proposal.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`.
- Team spec: `docs/harness/health-policy-strategy-game/team-spec.md`.

## Workflow

1. Read the canonical docs before shaping project-specific work.
2. Classify the request by roadmap phase and output type:
   research, conceptual model, game design, technical prototype, vertical slice,
   validation, release, or post-release expansion.
3. Write `_workspace/00_input/request-summary.md` for substantial tasks. Include
   scope, non-goals, sources, expected files, validation target, and whether
   generic global skills are needed.
4. Invoke repo-local skills only for project-specific work:
   `hs-policy-evidence-mapper`, `hs-policy-mechanism-designer`, and
   `hs-policy-domain-qa`.
5. For generic implementation quality, use global skills rather than creating
   local duplicates.
6. Preserve handoff files named in the team spec when the task spans more than
   one phase.
7. Finish with a concise handoff that lists changed files, verification, known
   limits, and next phase dependencies.

## Outputs

- `_workspace/00_input/request-summary.md` for substantial scoped work.
- `_workspace/final/handoff.md` when a durable handoff is useful.
- Updated repository files requested by the user.

## Validation

- Local skill names must not duplicate global skill names.
- The task must not silently skip canonical docs when project-specific judgment
  is required.
- Any broad feature request must be narrowed to the current roadmap phase unless
  the user explicitly asks for future-facing design.
- Code-producing tasks must run focused verification such as `cargo fmt` and
  `cargo test` when Rust files are changed.

## References

- `docs/harness/health-policy-strategy-game/team-spec.md`
- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
