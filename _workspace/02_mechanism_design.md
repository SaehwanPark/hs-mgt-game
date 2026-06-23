# Mechanism Design

## Goal and Roadmap Phase

Extend the Phase 4 deterministic architecture proof with the first policy
process interaction so it can serve as the spine of a later Phase 5 vertical
slice.

## Slice Boundary

Included:

- One player-controlled nonprofit health system.
- One commercial insurer decision.
- One state policy official decision.
- One capacity investment command.
- One access-mandate response command.
- One policy pressure signal.
- One actor-specific observation.
- One append-only two-transition history.

Excluded:

- Full campaign.
- Interactive CLI.
- Persistent save files.
- Scenario data loader.
- Empirical calibration.

## Actors and Authority

- Health system CEO: may choose a valid capacity stabilization command and
  request a commercial rate, then choose a valid access-mandate response.
- Commercial insurer: may accept, counter, or reject the requested rate path.
- State policy officials: may grant flexibility, continue the mandate, or
  escalate oversight.
- Policy pressure still enters through resolved inputs only.

## State, Beliefs, and Observations

- True state tracks cash, staffed beds, access, quality, workforce trust,
  community trust, commercial rate, and policy pressure.
- Player observation reports delayed/noisy access and current quality.
- The transition core receives observations and resolved inputs explicitly; it
  does not generate randomness.

## Commands, Events, and Effects

- Valid commands: `StabilizeAccess` and `RespondToStateAccessMandate`.
- Validation failures: non-positive capacity change or excessive capital spend.
- Additional validation failures: negative or excessive advocacy spend and
  non-positive access commitment.
- Modeled unfavorable outcomes: insurer counteroffer or rejection, and state
  oversight escalation.
- Events summarize actor-visible occurrences.
- Effects attribute metric deltas to sources.

## Strategic Interaction

The commercial insurer chooses among accept, counter, and reject by comparing
requested rate against a target and reported access against a leverage threshold.
The decision record includes a rationale for inspection and debriefing.

State policy officials choose among flexibility, mandate continuation, and
oversight escalation by comparing advocacy spend, access commitment, reported
access, and explicit policy pressure. The decision record is an abstraction of a
policy-process response, not a full policy lifecycle model.

## Assumptions and Parameters

- All prototype values are small integer abstractions.
- `demo-ruleset-0.1.3` is a temporary in-code ruleset name.
- State fingerprinting is deterministic string formatting for now.

## Educational Debrief Hooks

- The demo prints the CEO observation, insurer and state-policy rationales,
  events, attributed effects, state fingerprints, and replay result.
- This supports discussion of decision quality under incomplete information,
  payer bargaining, state policy response, delayed reporting, and unintended
  workforce/community effects.

## Determinism and Replay Notes

- Transition inputs are prior state, validated command, resolved inputs, and
  ruleset.
- Replay recomputes committed transitions from genesis and compares the final
  state.
- No wall-clock time, hidden random number generation, file I/O, network I/O, or
  global mutable state is used in the transition core.

## Open Questions

- Whether future state fingerprints should use a cryptographic hash.
- Whether the first interactive CLI should load scenario data or keep compiled
  demos until the conceptual model settles.
- How many actor classes should appear before the first classroom playtest.
