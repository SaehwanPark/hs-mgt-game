---
name: hs-policy-domain-qa
description: Review Health Policy Strategy Game artifacts for project-specific simulation, policy, education, scope, and determinism risks.
---

# HS Policy Domain QA

## When to Use

- Use this skill to review project-specific docs, mechanism designs, scenario
  specs, or code changes against the health-policy strategy game principles.
- Use it after a mechanism or implementation artifact is produced and before
  treating the work as ready.
- Do not use it as a replacement for global code review, Rust quality review, or
  release review.

## Required Inputs

- Original user request.
- Produced artifact or changed files.
- Relevant `_workspace/` handoffs.
- Canonical docs and `docs/harness/health-policy-strategy-game/team-spec.md`.
- Verification output when code changed.

## Workflow

1. Compare the artifact to the original request and roadmap phase.
2. Check project-specific risks:
   scope expansion, false precision, normative opacity, strategic opacity,
   educational opacity, premature frameworking, and replay instability.
3. Verify that state, beliefs, observations, actor utility, social welfare, and
   educational evaluation remain distinct where relevant.
4. Check deterministic boundaries: no hidden randomness, wall-clock dependency,
   global mutable state, or unresolved stochastic behavior inside core
   transitions.
5. Return one status:
   `pass` when the artifact is ready, `fix` when targeted revision is enough, or
   `redo` when the direction conflicts with the project.

## Outputs

Write `_workspace/03_domain_qa.md` with these sections:

- `Status`
- `Reviewed Inputs`
- `Findings`
- `Required Fixes`
- `Residual Risks`
- `Verification Evidence`

## Validation

- Findings cite file paths or handoff sections.
- QA does not repeat generic code review that belongs to global skills.
- A `pass` still records residual uncertainty when evidence, calibration, or
  educational validation is incomplete.

## References

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
