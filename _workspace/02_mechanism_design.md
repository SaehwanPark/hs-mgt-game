# Mechanism Design - Instructor Debrief-Use Audit

## Goal and Roadmap Phase

Phase 7 competitive teachability and validation: establish whether existing
information-to-action evidence contains the trace fields needed for review
before any runtime promotion.

## Slice Boundary

- Inputs: v0.10.37, v0.10.40, v0.10.41, and v0.10.43 JSON artifacts.
- Output: deterministic JSON and Markdown audit artifacts plus findings.
- Included: shallow field-presence checks for visibility, response,
  follow-through, outcome, and explanation.
- Excluded: new sessions, runtime changes, new actors, new schemas, and human
  or classroom evaluation.

## Actors and Authority

- Existing human-led system and simulated policy wrappers remain unchanged.
- The audit is an offline reviewer tool, not a game actor or transition.

## State, Beliefs, and Observations

- Visibility checks use observation, rendered-option, monitor-signal, and source
  timing fields already captured in the artifacts.
- Outcome and explanation checks use retrospective hashes, histories, and
  debrief fields only as retrospective evidence.

## Commands, Events, and Effects

- The audit reads commands, response records, and debrief traces without
  creating or resolving commands, events, or effects.
- Missing fields are classified rather than synthesized.

## Strategic Interaction

The audit does not compare policy quality or estimate treatment effects. It only
checks whether a reviewer can locate the trace categories used by the existing
comparison surface.

## Assumptions and Parameters

- Complete runs are the eligible denominator for coverage.
- `supported`, `limited`, and `unsupported` describe artifact coverage only.
- The report uses fixed source ordering and stable JSON serialization.

## Educational Debrief Hooks

- Can the reviewer identify what was visible before the command?
- Can the response or fallback be located?
- Can later operational follow-through be distinguished from public intent?
- Can outcomes and retrospective explanation be inspected without judging from
  hidden state?

## Determinism and Replay Notes

No randomness, transition, replay, state hash, persistence, or MCP path changes.
The audit is read-only with respect to source artifacts and deterministic in its
generated outputs.

## Open Questions

- Human or instructor review is still required to assess clarity.
- Runtime work remains deferred unless future review identifies a concrete gap
  that current observations, history, diagnostics, and debriefs cannot explain.
