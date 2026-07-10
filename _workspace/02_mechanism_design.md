# Mechanism Design - Consultant Advice Usage Evidence

## Goal and Roadmap Phase

Phase 7 competitive teachability and validation slice following v0.10.40's
consultant-advice traceability repair.

## Slice Boundary

- Reuse existing observations and scripted policies to capture paired
  advice-aware and advice-ignoring runs for two profiles across three seeds and
  two difficulties.
- Compare the four rendered `A`–`D` options with the options stored on the same
  committed transition, then count monthly debrief records.
- Have the advice-aware wrapper select an option from visible cues, execute a
  resource-safe command when possible, and record fallback or safe-hold behavior.
- Report command-family alignment without scoring compliance or treating advice
  as a causal input to a human player.

## State, Beliefs, and Observations

- The runner reads only MCP observation text, legal resource hints, accepted
  commands, committed transition summaries, and final debrief text.
- The advice-aware policy uses no hidden rival state and the control policy does
  not inspect consultant options.
- It does not inspect hidden rival state or add agent behavior.

## Commands, Events, and Effects

- No commands, events, effects, payroll, or actor utility changes are
  introduced. The runner fails if an expected trace field is missing or if an
  inherited command is not safe under visible resources.

## Determinism and Replay Notes

- The evidence artifact contains no timestamps and is regenerated twice to
  establish byte-for-byte stability. State hashes remain evidence of unchanged
  world transitions, not advice effectiveness.

## Open Questions

- If rendered and stored options diverge, or control hashes differ from
  v0.10.40, stop and route the mismatch to a separate runtime repair slice; do
  not change the simulation from this PR.

## Educational Debrief Hooks

- Preserve enough evidence for instructors to verify what was shown, what was
  chosen, and what the debrief retained without claiming that aligned choices
  were better choices.

## Conclusion

Keep differentiated advisors, employment state, payroll, AI parity, and all
runtime changes beyond the additive history-audit DTO field outside this slice.
