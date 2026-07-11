# Evidence Map - Debrief-Use Audit

## Scope

Audit whether existing Phase 7 artifacts preserve an inspectable chain from
actor-visible information through submitted response, accepted transition and
hash, and event-specific retrospective explanation.

## Sources Reviewed

- `README.md`, `docs/roadmap.md`, `docs/design_principles.md`, and `SPEC.md`.
- `docs/harness/health-policy-strategy-game/team-spec.md`.
- v0.10.43, v0.10.50, v0.10.51, v0.10.54, v0.10.55, and v0.10.56 JSON artifacts.
- Existing findings, playtesting guidance, and prior evidence audits.

## Mechanisms and Institutions

- Rival information, project concurrency, resource validation, and strategic
  tradeoffs are existing game abstractions, not calibrated forecasts.
- The audit evaluates evidence structure; it does not add or reinterpret a
  health-policy mechanism.

## Actor Incentives and Information

- Source traces retain the actor-visible observation and submitted policy.
- Rejected commands and retries are treated as validation-surface records, not
  modeled outcomes or evidence of human confusion.
- Instructor-only retrospective material remains distinct from information
  available during play.

## Assumptions

- Existing artifact contracts are the source of truth and remain immutable.
- Heterogeneous source shapes require source-specific adapters, not a shared
  analytics schema.
- Event-specific debrief markers establish trace coverage only.

## Unresolved Questions

- Whether an actual instructor or learner would find any supported explanation
  clear remains untested.
- A future wording or interface change requires concrete player-facing,
  instructor-facing, or domain-review evidence of an unexplained gap.

## Design Implications

- Keep the audit read-only and deterministic.
- Report missing fields explicitly as limited evidence.
- Preserve source identity, seed identity, hash continuity, and evidence limits.

## Risks

- Simulated-policy trace continuity can be mistaken for comprehension or
  educational effectiveness.
- The project ceiling and rival behavior remain gameplay abstractions.
