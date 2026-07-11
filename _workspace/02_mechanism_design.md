# Mechanism Design - Consultant Advice Evidence Synthesis

## Goal and Roadmap Phase

Phase 7 competitive teachability and validation synthesis following the generic
consultant advice, traceability, and usage slices.

## Slice Boundary

- Compare existing v0.10.40 traceability and v0.10.41 usage artifacts.
- Preserve the generic four-option, non-binding advice surface.
- Record whether the evidence identifies a concrete limitation requiring a
  future runtime slice.
- Do not add actors, commands, state, effects, scenarios, or new runs.

## State, Beliefs, and Observations

- Existing evidence remains at the MCP wrapper and debrief boundary.
- The synthesis treats actor-visible options, committed history, and debrief
  records as separate evidence surfaces.
- No hidden state, belief, stochastic input, or transition behavior is changed.

## Commands, Events, and Effects

No commands, events, effects, payroll, actor utility, scoring, or balance
semantics are introduced. The synthesis only reports existing artifact results.

## Strategic Interaction

The artifacts do not add a strategic actor. Advice-aware and advice-ignoring
policies are paired evidence controls; their different commands and endpoints
must not be interpreted as a causal treatment effect.

## Assumptions and Parameters

- The v0.10.40 artifact contains 24 complete runs with exact option/history
  continuity and debrief records.
- The v0.10.41 artifact contains 24 paired runs with zero validation failures
  and control hashes matching the prior artifact.
- All advice wording, option categories, and policy wrappers remain gameplay
  abstractions.

## Educational Debrief Hooks

- Explain what options were visible, what the simulated policy selected or
  declined, what fallback occurred, and what the debrief retained.
- Keep the explanation focused on inspectability and decision context rather
  than adherence, quality, or learning scores.

## Determinism and Replay Notes

- Re-run the existing v0.10.41 generator twice and require byte stability.
- Do not alter replay artifacts, state hashes, rulesets, or transition logic.

## Open Questions

- A future artifact must identify a concrete generic-baseline limitation before
  advisor roster mechanics are promoted.
