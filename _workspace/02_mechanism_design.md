# Mechanism Design

## Goal and Roadmap Phase

Extend the deterministic architecture proof toward Phase 5 by adding the first
minimal playable CLI choice over the existing two-turn history and educational
debrief.

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
- One deterministic educational debrief over committed history.
- Three hard-coded strategy paths selected through a small CLI input boundary.

Excluded:

- Full campaign.
- General command parser.
- Persistent save files.
- Scenario data loader.
- Empirical calibration.
- General instructor reporting framework.

## Actors and Authority

- Health system CEO: may choose a valid capacity stabilization command and
  request a commercial rate, then choose a valid access-mandate response through
  one of three compiled strategy paths.
- Commercial insurer: may accept, counter, or reject the requested rate path.
- State policy officials: may grant flexibility, continue the mandate, or
  escalate oversight.
- Policy pressure still enters through resolved inputs only.
- Educational debrief: may summarize committed observations, effects, actor
  rationales, and final state movement; it does not alter the simulation state.

## State, Beliefs, and Observations

- True state tracks cash, staffed beds, access, quality, workforce trust,
  community trust, commercial rate, and policy pressure.
- Player observation reports delayed/noisy access and current quality.
- The transition core receives observations and resolved inputs explicitly; it
  does not generate randomness.
- The debrief reads committed history and reports actor rationales already
  recorded at decision time.

## Commands, Events, and Effects

- Valid commands: `StabilizeAccess` and `RespondToStateAccessMandate`.
- CLI strategy paths: access stabilization, fiscal caution, and aggressive
  bargaining.
- Validation failures: non-positive capacity change or excessive capital spend.
- Additional validation failures: negative or excessive advocacy spend and
  non-positive access commitment.
- CLI failures: invalid numbered strategy choice.
- Modeled unfavorable outcomes: insurer counteroffer or rejection, and state
  oversight escalation.
- Events summarize actor-visible occurrences.
- Effects attribute metric deltas to sources.
- Debrief lines summarize run-level tradeoffs, actor rationales, attributed
  mechanisms, and classroom prompts.

## Strategic Interaction

The commercial insurer chooses among accept, counter, and reject by comparing
requested rate against a target and reported access against a leverage threshold.
The decision record includes a rationale for inspection and debriefing.

State policy officials choose among flexibility, mandate continuation, and
oversight escalation by comparing advocacy spend, access commitment, reported
access, and explicit policy pressure. The decision record is an abstraction of a
policy-process response, not a full policy lifecycle model.

The debrief does not add a new strategic interaction. It exposes the recorded
strategic rationales and attributed effects in a stable end-of-run summary.

The CLI choice does not add a new strategic model. It selects one compiled
two-command plan before the deterministic transition path runs.

## Assumptions and Parameters

- All prototype values are small integer abstractions.
- `demo-ruleset-0.1.5` is a temporary in-code ruleset name.
- State fingerprinting is deterministic string formatting for now.

## Educational Debrief Hooks

- The demo prompts for one of three strategy paths and then prints the CEO
  observation, insurer and state-policy rationales, events, attributed effects,
  state fingerprints, replay result, and educational debrief.
- This supports discussion of decision quality under incomplete information,
  payer bargaining, state policy response, delayed reporting, and unintended
  workforce/community effects.

## Determinism and Replay Notes

- Transition inputs are prior state, validated command, resolved inputs, and
  ruleset.
- Replay recomputes committed transitions from genesis and compares the final
  state.
- Debrief generation reads the committed history after transitions and does not
  use randomness, time, filesystem, network, or global mutable state.
- CLI input is outside the transition core and only selects a hard-coded
  strategy path.
- No wall-clock time, hidden random number generation, file I/O, network I/O, or
  global mutable state is used in the transition core.

## Open Questions

- Whether future state fingerprints should use a cryptographic hash.
- Whether the first interactive CLI should load scenario data or keep compiled
  demos until the conceptual model settles.
- How many actor classes should appear before the first classroom playtest.
