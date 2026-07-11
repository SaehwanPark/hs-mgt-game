# Evidence Map - Instructor Debrief-Use Audit

## Scope

Audit existing Phase 7 evidence for the fields required by the v0.10.44
information-to-action comparison surface. This is a traceability check, not a
new simulation mechanism or educational-effect evaluation.

## Sources Reviewed

- `docs/playtest-findings-v0.10.44.md` and canonical project documents.
- v0.10.37 rival-information monitor artifact.
- v0.10.40 consultant-advice traceability artifact.
- v0.10.41 consultant-advice usage artifact.
- v0.10.43 rival-information follow-through artifact.

## Mechanisms and Institutions

- The human-led system acts from actor-visible observations and legal resource
  hints.
- Consultant options and rival-monitor signals remain non-binding observation
  surfaces; response records belong to simulated policies.
- The audit checks five evidence dimensions: visibility, response,
  follow-through, outcome, and explanation.

## Actor Incentives and Information

- Existing artifacts retain the submitted command or policy response alongside
  the relevant observation or signal.
- Retrospective history and debrief fields may contain information unavailable at
  decision time and must not be used as contemporaneous knowledge.
- Different policy streams are descriptive comparisons, not randomized
  treatments.

## Assumptions

- Existing JSON structures are stable enough for shallow field-presence checks.
- `supported` means every complete run in an artifact exposes the relevant
  trace family, not that the trace is pedagogically clear.
- All interpretation labels remain game abstractions.

## Unresolved Questions

- Whether instructors or human players find the fields clear remains untested.
- Whether a future runtime information or debrief change is needed remains
  unresolved because no concrete gap was found by this audit.

## Design Implications

- Prefer a small read-only audit over a generalized cross-artifact schema.
- Keep evidence availability separate from advice quality, monitor value,
  decision quality, outcome quality, and learning.
- Keep runtime promotion gated on reviewer or instructor evidence of a concrete
  gap that current artifacts cannot explain.

## Risks

- Field presence can be mistaken for usability or educational sufficiency.
- Heterogeneous artifact shapes can invite accidental schema expansion.
- Different command streams can still be misread as causal evidence.
