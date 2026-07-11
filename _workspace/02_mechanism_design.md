# Mechanism Design - Rival Information Follow-Through

## Goal and Roadmap Phase

Phase 7 competitive teachability and validation: determine whether a visible
monitor signal can be traced to a later simulated-policy command.

## Slice Boundary

- Campaign: `competitive-regional-v1`, 24 months.
- Matrix: seeds 42–44, Hard/Expert, three policy arms, 18 runs.
- No runtime, command, schema, scenario, replay, or balance changes.

## Actors and Authority

- Human-led system: owns the submitted command stream.
- Rival systems: existing AI actors; their behavior is unchanged.
- Evidence policies: deterministic wrappers, not game actors.

## State, Beliefs, and Observations

- True rival state remains inside the Rust simulation.
- Policies consume only MCP observation text and legal resource hints.
- Monitor intel is recorded with its source month and the observation turn in
  which it becomes visible.

## Commands, Events, and Effects

- Existing v0.10.37 monitor and baseline commands are reused.
- Reactive responses use bounded visible-signal categories and safe resource
  fallback to `hold`.
- No new command or transition semantics are introduced.

## Strategic Interaction

The reactive and ignoring policies submit different commands intentionally. The
artifact therefore evaluates traceability and control hash behavior, not a
causal treatment effect.

## Assumptions and Parameters

- Monitor signals are classified from visible text as payer, capacity,
  workforce, access, or other.
- The response mapping is a deterministic gameplay abstraction.
- Each completed run must contain 24 transitions and no validation failures.

## Educational Debrief Hooks

- Show what signal was visible, when it originated, and what command followed.
- Distinguish a response, an ignored signal, and a safe fallback.
- Preserve the existing debrief as evidence context, not a learning score.

## Determinism and Replay Notes

- Build the local MCP binary before capture.
- Require stable JSON/diagnostic regeneration.
- Verify monitor-ignoring and unmonitored state hashes match.

## Open Questions

- Later human or instructor evidence may determine whether current traceability
  wording is adequate; this slice does not answer that question.
