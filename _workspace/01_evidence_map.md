# Evidence Map

## Scope

Audit the existing v0.11.4 competitive capture for operating-outcome
visibility, temporal observation alignment, next-command trace continuity, and
player-owned debrief linkage.

## Sources Reviewed

- `docs/roadmap.md`, Phase 7 validation and educational artifact gates.
- `SPEC.md`, the v0.11.4 baseline and ranked teachability queue.
- `docs/design_principles.md`, especially deterministic replay, observation
  boundaries, inspectable causality, and evidence limits.
- `_workspace/experiments/v0.11.4-operating-outcome-debrief-validation/capture.json`.
- The v0.11.4 audit parser and focused contract tests.

## Mechanisms and Institutions

The audit does not add or tune a health-policy mechanism. Its signal categories
reuse the existing operating-loop diagnostic labels: capacity/demand,
operating loss, and workforce capacity.

## Actor Incentives and Information

The player command is linked only to the player-visible prior-month observation.
Rival-owned operating values remain a regression signal and are never counted
as player evidence.

## Assumptions

- The v0.11.4 capture is authoritative and remains deterministic.
- A month-two observation describes the committed month-one result; it must not
  be compared with the current month transition.
- A final-month signal has no later command and is therefore a terminal signal,
  not a missing response.

## Unresolved Questions

- Whether a person finds the operating-result surface clear remains untested.
- Whether any response distribution reflects good strategy or causal effect
  remains unresolved.
- Human learning, classroom use, calibration, and policy validity require
  separate evidence.

## Design Implications

- Keep the audit read-only and source-specific.
- Preserve exact observation, command, transition, hash, and debrief fields.
- Route runtime promotion only from a concrete unexplained product or domain
  gap.

## Risks

- Deterministic scripted policies are not human players.
- Signal-to-command counts can be overinterpreted as causal response evidence.
- Visible integer game units must not be presented as calibrated financial or
  clinical quantities.
