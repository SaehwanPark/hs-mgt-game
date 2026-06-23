# Mechanism Design

## Goal and Roadmap Phase

Build a Phase 4 deterministic architecture proof that can serve as the spine of
a later Phase 5 vertical slice.

## Slice Boundary

Included:

- One player-controlled nonprofit health system.
- One commercial insurer decision.
- One capacity investment command.
- One policy pressure signal.
- One actor-specific observation.
- One append-only transition history.

Excluded:

- Full campaign.
- Interactive CLI.
- Persistent save files.
- Scenario data loader.
- Empirical calibration.

## Actors and Authority

- Health system CEO: may choose a valid capacity stabilization command and
  request a commercial rate.
- Commercial insurer: may accept, counter, or reject the requested rate path.
- Policy environment: may add pressure through resolved inputs only.

## State, Beliefs, and Observations

- True state tracks cash, staffed beds, access, quality, workforce trust,
  community trust, commercial rate, and policy pressure.
- Player observation reports delayed/noisy access and current quality.
- The transition core receives observations and resolved inputs explicitly; it
  does not generate randomness.

## Commands, Events, and Effects

- Valid command: `StabilizeAccess`.
- Validation failures: non-positive capacity change or excessive capital spend.
- Modeled unfavorable outcomes: insurer counteroffer or rejection.
- Events summarize actor-visible occurrences.
- Effects attribute metric deltas to sources.

## Strategic Interaction

The commercial insurer chooses among accept, counter, and reject by comparing
requested rate against a target and reported access against a leverage threshold.
The decision record includes a rationale for inspection and debriefing.

## Assumptions and Parameters

- All prototype values are small integer abstractions.
- `demo-ruleset-0.1.2` is a temporary in-code ruleset name.
- State fingerprinting is deterministic string formatting for now.

## Educational Debrief Hooks

- The demo prints the CEO observation, insurer decision rationale, events,
  attributed effects, state fingerprint, and replay result.
- This supports discussion of decision quality under incomplete information,
  payer bargaining, delayed reporting, and unintended workforce/community
  effects.

## Determinism and Replay Notes

- Transition inputs are prior state, validated command, resolved inputs, and
  ruleset.
- Replay recomputes the committed transition from genesis and compares the final
  state.
- No wall-clock time, hidden random number generation, file I/O, network I/O, or
  global mutable state is used in the transition core.

## Open Questions

- Whether future state fingerprints should use a cryptographic hash.
- Whether the first interactive CLI should load scenario data or keep compiled
  demos until the conceptual model settles.
- How many actor classes should appear before the first classroom playtest.
