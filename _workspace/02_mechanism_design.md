# Mechanism Design - Debrief-Coherence Audit

## Goal and Roadmap Phase

Phase 7 validation: inspect decision-to-debrief trace coherence without
changing the deterministic competitive simulation.

## Slice Boundary

- Included: six existing JSON artifacts, 39 completed runs, source-specific
  coherence checks, project hash continuity, deterministic outputs, and tests.
- Excluded: new sessions, runtime changes, MCP changes, schema generalization,
  new mechanics, and debrief wording changes.

## Actors and Authority

The audit treats source records as prior simulated policies. It introduces no
actors, authority, incentives, or strategic decisions.

## State, Beliefs, and Observations

The audit keeps actor-visible observations, committed transitions, delayed or
partial signals, true-state hashes, and retrospective instructor material as
separate evidence categories. Hidden state is not inferred.

## Commands, Events, and Effects

The audit records submitted commands, expected validation failures, safe retries,
transition effects/events, state hashes, and debrief markers. It does not create
or modify commands, events, or effects.

## Strategic Interaction

Existing rival-pressure, resource-retry, and project-recovery traces are checked
for continuity. No policy is evaluated as optimal, causal, or educationally
effective.

## Assumptions and Parameters

- Review steps: decision context, action response, transition follow-through,
  delayed or partial context, outcome context, and debrief explanation.
- Delayed/partial context is not applicable to source lanes that do not claim
  that evidence dimension.
- Project recovery hashes compare v0.10.54 with v0.10.55 and v0.10.55 with
  v0.10.56 for seeds 42–44.
- Runtime promotion is deferred by this slice.

## Educational Debrief Hooks

The report supports reviewer discussion of what was visible, what response
followed, what transition occurred, what remained delayed or partial, and what
the debrief records. It does not assess human understanding or learning.

## Determinism and Replay Notes

The runner reads immutable artifacts in fixed contract order, uses no randomness
or wall-clock state, sorts generated JSON keys, and must regenerate byte-
identical JSON and Markdown.

## Open Questions

If a future reviewer identifies an actual explanation limitation, create a
separate approved wording or interface slice rather than expanding this audit.
