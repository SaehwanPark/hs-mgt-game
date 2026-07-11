# Mechanism Design - Information-to-Action Comparison

## Goal and Roadmap Phase

Phase 7 competitive teachability and validation: make the existing path from
visible information to later simulated-policy action inspectable across runs.

## Slice Boundary

- Campaign: `competitive-regional-v1`, existing 24-month artifacts.
- Inputs: v0.10.37, v0.10.40, v0.10.41, v0.10.42, and v0.10.43 evidence.
- Output: one instructor-facing comparison document and routing checkpoint.
- Excluded: new capture runs, runtime changes, new actors, and new schemas.

## Actors and Authority

- Human-led health system: submits the command stream being reviewed.
- Existing rival systems and consultant baseline: unchanged simulation actors or
  observation sources.
- Advice-aware, monitor-reactive, and control policies: deterministic evidence
  wrappers, not new game actors.

## State, Beliefs, and Observations

- True rival state remains inside the Rust simulation.
- Review starts from actor-visible observations and legal resource hints.
- Later history and debrief information are labeled as retrospective context.

## Commands, Events, and Effects

- Existing commands, events, effects, validation, and hashes are reused.
- The comparison records visibility, response or fallback, durable follow-through,
  realized tradeoffs, and explanation continuity without creating transitions.

## Strategic Interaction

The evidence compares information surfaces and policy responses, but does not
estimate a causal treatment effect. Controls and reactive policies intentionally
submit different commands.

## Assumptions and Parameters

- Source-month, observation-turn, option, command, resource, and debrief fields
  are read from existing artifacts.
- All interpretation labels are gameplay or educational abstractions.

## Educational Debrief Hooks

- What was visible at decision time?
- What response was affordable and actually submitted?
- Did the response become durable operational follow-through?
- Which outcome was intended, tolerated, or an unfavorable realization?
- Can the debrief explain the difference without scoring the learner?

## Determinism and Replay Notes

No randomness, transition, replay, state hash, or persistence path changes. The
comparison consumes stable deterministic artifacts and preserves the distinction
between actor observations and retrospective debrief information.

## Open Questions

- Human or instructor review is still needed to assess whether the sequence is
  sufficiently clear.
- No runtime promotion is justified unless current surfaces fail to explain a
  concrete future finding.
