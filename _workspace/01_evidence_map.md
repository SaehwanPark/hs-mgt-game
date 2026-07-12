# Evidence Map

## Scope

Audit whether the latest frozen competitive evidence supports descriptive
strategy comparison by profile, seed, and difficulty while preserving the
existing operating-outcome observation, transition, hash, and debrief links.

## Sources Reviewed

- `SPEC.md`, the v0.11.5 baseline, and the ranked teachability queue.
- `docs/roadmap.md`, Phase 7 validation and educational artifact gates.
- `docs/design_principles.md`, especially deterministic replay, observation
  boundaries, inspectable causality, and evidence limits.
- `_workspace/experiments/v0.11.4-operating-outcome-debrief-validation/capture.json`.
- The v0.11.5 operating-outcome audit parser and focused contract tests.

## Evidence-backed facts

- The source matrix has five profiles, three seeds, four difficulty tiers, and
  60 complete runs.
- The source contains 1,440 committed months, 1,380 prior-month observation
  matches, 1,440 exact player-owned debrief matches, 441 response opportunities,
  and 28 terminal signals.
- Existing source-specific parsing already distinguishes terminal signals,
  rival-owned operating results, and player-owned monthly outcomes.

## Design abstraction

Normalized command families and profile summaries are descriptive groupings for
inspection. They are not validated strategy classes, utility functions, or
causal estimators.

## Assumptions and boundaries

- The v0.11.4 capture is authoritative and remains deterministic.
- A prior-month signal is compared with the following submitted command.
- A final-month signal has no later command and is terminal, not missing.
- Rival operating values remain outside player evidence.

## Routing result

The audit must record a concrete structural gap when evidence is incomplete. If
all contracts pass, record no unexplained gap and keep runtime promotion
deferred.

## Unresolved questions

- Whether a person finds the strategy/debrief surface clear remains untested.
- Whether any response distribution reflects good strategy or causal effect
  remains unresolved.
- Human learning, classroom use, calibration, and policy validity require
  separate evidence.
