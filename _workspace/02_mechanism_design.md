# Mechanism Design

## Goal and Roadmap Phase

Complete Phase 4.3 by moving hard-coded per-path `ResolvedInputs` behind a seeded
stochastic input boundary while preserving the existing deterministic transition
core, replay, debrief, and playable CLI strategy paths.

## Slice Boundary

Included:

- One player-controlled nonprofit health system.
- One commercial insurer decision.
- One state policy official decision.
- One capacity investment command.
- One access-mandate response command.
- One explicit run seed at the CLI boundary.
- Named random streams for measurement noise, delayed access reporting, labor
  pressure, and policy signal resolution.
- Deterministic derivation of `ResolvedInputs` from `(seed, turn, prior state)`.
- Three hard-coded strategy paths selected through the existing CLI input
  boundary.
- One append-only two-transition history.
- One deterministic educational debrief over committed history.

Excluded:

- Full campaign.
- General command parser.
- Persistent save files.
- Scenario data loader.
- Empirical calibration.
- General instructor reporting framework.
- New Cargo dependencies.

## Actors and Authority

- Health system CEO: may choose a valid capacity stabilization command and
  request a commercial rate, then choose a valid access-mandate response through
  one of three compiled strategy paths.
- Commercial insurer: may accept, counter, or reject the requested rate path.
- State policy officials: may grant flexibility, continue the mandate, or
  escalate oversight.
- Exogenous variation enters only through resolved inputs derived from the run
  seed before transition evaluation.
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
- CLI seed input: optional unsigned integer with default `42`.
- Validation failures: non-positive capacity change or excessive capital spend.
- Additional validation failures: negative or excessive advocacy spend and
  non-positive access commitment.
- CLI failures: invalid numbered strategy choice or invalid seed string.
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

The seed boundary does not add a new strategic model. It deterministically
resolves exogenous inputs before the existing actor decision procedures run.

## Stochastic Input Boundary

- Default seed: `42`.
- Named streams:
  - `measurement`: bounded measurement noise.
  - `access_delay` and `access_noise`: delayed access report derived from prior
    true access.
  - `labor`: bounded workforce sick-call delta.
  - `policy`: bounded policy pressure signal.
- Stream seeds combine run seed, turn index, and stream id through splitmix64.
- Identical seed, turn, and prior state always produce identical resolved inputs.
- Different seeds may change resolved inputs while commands stay fixed.

## Assumptions and Parameters

- All prototype values are small integer abstractions.
- `demo-ruleset-0.1.6` is a temporary in-code ruleset name.
- State fingerprinting is deterministic string formatting for now.
- Canonical demo trajectory is pinned to seed `42`; prior per-path hard-coded
  input tables are intentionally removed.

## Educational Debrief Hooks

- The demo prompts for one of three strategy paths and an optional seed, then
  prints resolved inputs, CEO observation, insurer and state-policy rationales,
  events, attributed effects, state fingerprints, replay result, and
  educational debrief.
- This supports discussion of decision quality under incomplete information,
  payer bargaining, state policy response, delayed reporting, seeded exogenous
  variation, and unintended workforce/community effects.

## Determinism and Replay Notes

- Transition inputs are prior state, validated command, resolved inputs, and
  ruleset.
- Resolved inputs are computed outside the transition core from seed and prior
  state, then committed into history.
- Replay recomputes committed transitions from genesis and compares the final
  state.
- Debrief generation reads the committed history after transitions and does not
  use randomness, time, filesystem, network, or global mutable state.
- CLI input is outside the transition core and only selects a hard-coded
  strategy path and run seed.
- No wall-clock time, hidden random number generation inside `transition()`,
  file I/O, network I/O, or global mutable state is used in the transition core.

## Open Questions

- Whether future state fingerprints should use a cryptographic hash.
- Whether the first scenario loader should store seeds and stream definitions
  separately from command presets.
- How many actor classes should appear before the first classroom playtest.
