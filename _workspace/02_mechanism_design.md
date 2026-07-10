# Mechanism Design - Consultant Advice Traceability Evidence

## Goal and Roadmap Phase

Phase 7 competitive teachability and validation slice following v0.10.39's
generic consultant-advice repair.

## Slice Boundary

- Reuse existing observations and scripted policies to capture a 3-seed,
  2-difficulty, 4-profile matrix.
- Compare the four rendered `A`–`D` options with the options stored on the same
  committed transition, then count monthly debrief records.
- Report command-family alignment without scoring compliance or treating advice
  as a causal input to the scripted policy.

## State, Beliefs, and Observations

- The runner reads only MCP observation text, accepted commands, committed
  transition summaries, and final debrief text. The transition summary carries
  the already-stored consultant options as an additive audit field.
- It does not inspect hidden rival state or add agent behavior.

## Commands, Events, and Effects

- No commands, events, effects, payroll, or actor utility changes are
  introduced. The runner fails if an expected trace field is missing.

## Determinism and Replay Notes

- The evidence artifact contains no timestamps and is regenerated twice to
  establish byte-for-byte stability. State hashes remain evidence of unchanged
  world transitions, not advice effectiveness.

## Open Questions

- If rendered and stored options diverge, stop and route the mismatch to a
  separate runtime repair slice; do not change the simulation from this PR.

## Educational Debrief Hooks

- Preserve enough evidence for instructors to verify what was shown, what was
  chosen, and what the debrief retained without claiming that aligned choices
  were better choices.

## Conclusion

Keep differentiated advisors, employment state, payroll, AI parity, and all
runtime changes beyond the additive history-audit DTO field outside this slice.
