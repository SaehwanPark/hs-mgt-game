# Mechanism Design - Debrief-Use Audit

## Goal and Roadmap Phase

Phase 7 validation: inspect debrief-use trace continuity without changing the
deterministic competitive simulation.

## Slice Boundary

- Included: six existing JSON artifacts, source-specific evidence checks,
  project-recovery hash continuity, deterministic JSON/Markdown output, and
  focused tests.
- Excluded: new sessions, runtime changes, MCP changes, schema generalization,
  new mechanics, and debrief wording changes.

## Actors and Authority

The audit treats source records as observations of prior simulated policies. It
does not introduce actors, authority, incentives, or strategic decisions.

## State, Beliefs, and Observations

The audit distinguishes actor-visible observations from accepted transitions,
state hashes, and retrospective debrief material. Hidden state is not inferred.

## Commands, Events, and Effects

The audit records submitted commands, validation failures, safe retries, latest
transitions, and debrief markers as evidence fields only. It does not create
commands, events, or effects.

## Strategic Interaction

Existing rival-pressure and project-recovery traces are reviewed for continuity;
no strategic behavior is evaluated as optimal or causally effective.

## Assumptions and Parameters

- Review steps: visibility, response, follow-through, outcome, explanation.
- Project-recovery continuity compares v0.10.54 with v0.10.55 and v0.10.55 with
  v0.10.56 for seeds 42–44.
- Runtime promotion is always deferred by this slice.

## Educational Debrief Hooks

The generated report supports instructor/reviewer discussion of what was visible,
what response followed, what transition occurred, and what the debrief records.
It does not assess whether a person learned or understood the game.

## Determinism and Replay Notes

The runner reads immutable artifacts in a fixed order, sorts JSON keys, uses no
randomness or wall-clock state, and must produce byte-identical output on repeat.

## Open Questions

If a future reviewer identifies an actual explanation gap, create a separate
approved slice for wording or interface changes rather than expanding this audit.
