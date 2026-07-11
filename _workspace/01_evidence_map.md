# Evidence Map - Debrief-Coherence Audit

## Scope

Audit whether existing Phase 7 traces preserve a reconstructable path from
actor-visible decision context through response, committed transition, delayed
or partial information, realized outcome, and retrospective explanation.

## Sources Reviewed

- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, and `SPEC.md`.
- `docs/harness/health-policy-strategy-game/team-spec.md`.
- v0.10.43, v0.10.50, v0.10.51, and v0.10.54–v0.10.56 JSON artifacts.
- v0.10.57 findings, audit, lessons, and project handoff.

## Mechanisms and Institutions

- Rival information, resource validation, project concurrency, delayed effects,
  and competitive debriefing are existing game abstractions.
- The audit evaluates evidence structure only; it adds no institution or
  strategic mechanism.

## Actor Incentives and Information

- Player commands are evaluated against actor-visible observations and legal
  command surfaces.
- Rival information remains partial or lagged where the source declares it.
- Instructor-only retrospective material remains distinct from information
  available during play.

## Assumptions

- Existing artifact contracts are immutable source records.
- Source-specific adapters are required because v0.10.51 records expected
  probe failures against the pre-submit observation rather than an
  `observation_after_failure` field.
- Decision-versus-outcome text is a traceability marker, not a quality score.

## Unresolved Questions

- Whether a learner or instructor would find any supported explanation clear
  remains untested.
- A future wording or interface change requires concrete player-facing,
  instructor-facing, or domain-review evidence of an unexplained limitation.

## Design Implications

- Keep the audit read-only, deterministic, and source-specific.
- Report missing fields and malformed retries explicitly as limited evidence.
- Preserve observation, actor utility, organizational outcome, social welfare,
  and educational evaluation boundaries.

## Risks

- Structural continuity can be mistaken for causal evidence or comprehension.
- Retrospective debrief markers can be mistaken for measured decision quality.
- Project ceilings, rival behavior, and delayed effects remain gameplay
  abstractions rather than empirical health-system constraints.
