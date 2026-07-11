# Mechanism Design - ASC Project Observation Coverage

## Goal and Roadmap Phase

Phase 7 validation: correct one actor-visible observation omission while
preserving the deterministic competitive transition boundary.

## Slice Boundary

- Included: existing `AscCapacity` pending effects, human observations,
  project-limit rejection/retry capture, and debrief continuity.
- Excluded: new commands, actors, rules, scenario fields, or resource hints.

## Actors and Authority

- Riverside Community Health remains the human-controlled system.
- Rival systems, payers, regulators, workforce, and existing AI behavior are
  unchanged.

## State, Beliefs, and Observations

- True state stores the pending effect queue and active-project counters.
- The actor-visible observation renders each pending project as
  `Name (months left, monthly draw)`.
- The ASC project must appear alongside existing ClinicNetwork and other
  project labels before and after a rejected third-project command.

## Commands, Events, and Effects

- The existing month-4 clinic project, month-6 ASC project, month-7 rejected
  neurology project, and `hold` retry are reused.
- No command validation, event, effect, or state transition changes.

## Strategic Interaction

No strategic interaction is added. Existing rival and payer responses remain
the same, and the capture does not infer player decision quality.

## Assumptions and Parameters

- ASC resolves in six months and uses its existing monthly draw.
- Hard difficulty and seeds 42, 43, and 44 remain the bounded evidence matrix.

## Educational Debrief Hooks

The capture preserves the observation, rejected-turn state, transition history,
and existing two-project debrief explanation for later review.

## Determinism and Replay Notes

Only observation formatting changes. Every v0.10.55 state-hash sequence must
match the v0.10.54 source artifact.

## Open Questions

Structured validation hints and broader project guidance remain deferred until
separate evidence identifies unexplained friction.
