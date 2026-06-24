# Mechanism Design

## Goal and Roadmap Phase

Extend the seeded three-turn playable demo with a fourth-turn regional access
coalition interaction while preserving the deterministic transition core, replay,
debrief, and CLI strategy paths.

## Slice Boundary

Included:

- One player-controlled nonprofit health system.
- One commercial insurer decision (turn 1).
- One state policy official decision (turn 2).
- One nursing workforce representative decision (turn 3).
- One regional provider coalition liaison decision (turn 4).
- One capacity investment command.
- One access-mandate response command.
- One workforce pressure response command.
- One coalition access command.
- One explicit run seed at the CLI boundary.
- Named random streams including coalition leverage signal resolution.
- Three hard-coded strategy paths selected through the existing CLI input
  boundary.
- One append-only four-transition history.
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

- Health system CEO: may choose valid capacity stabilization, access-mandate
  response, workforce pressure response, and coalition access commands through
  one of three compiled strategy paths.
- Commercial insurer: may accept, counter, or reject the requested rate path.
- State policy officials: may grant flexibility, continue the mandate, or
  escalate oversight.
- Nursing workforce representative: may accept a cooperative retention package,
  offer limited support, or signal a work action.
- Regional provider coalition liaison: may accept full partnership, offer
  limited participation, or withdraw from the coalition.
- Exogenous variation enters only through resolved inputs derived from the run
  seed before transition evaluation.
- Educational debrief: may summarize committed observations, effects, actor
  rationales, and final state movement; it does not alter the simulation state.

## State, Beliefs, and Observations

- True state tracks cash, staffed beds, access, quality, workforce trust,
  community trust, commercial rate, and policy pressure.
- Player observation reports delayed/noisy access and current quality.
- Coalition decisions use reported access, prior community trust, coalition
  investment, shared access commitment, and coalition leverage from resolved
  inputs.
- The transition core receives observations and resolved inputs explicitly; it
  does not generate randomness.

## Commands, Events, and Effects

- Valid commands: `StabilizeAccess`, `RespondToStateAccessMandate`,
  `RespondToWorkforcePressure`, and `JoinRegionalAccessCoalition`.
- Coalition command fields: `coalition_investment` and
  `shared_access_commitment`.
- CLI strategy paths: access stabilization, fiscal caution, and aggressive
  bargaining each include a fourth compiled coalition posture.
- Validation failures: negative or excessive coalition investment and
  non-positive shared access commitment.
- Modeled unfavorable coalition outcome: coalition withdrawal reducing community
  trust and increasing policy pressure.
- Events summarize actor-visible occurrences.
- Effects attribute metric deltas to sources.

## Strategic Interaction

The regional provider coalition liaison chooses among full partnership, limited
participation, or coalition withdrawal by comparing coalition investment, shared
access commitment, community trust, reported access, and coalition leverage from
resolved inputs. The decision record includes a rationale for inspection and
debriefing.

## Stochastic Input Boundary

- Default seed: `42`.
- New named stream: coalition leverage signal (bounded 1–6).
- Fourth turn resolves inputs from seed and post-turn-3 state before transition.

## Assumptions and Parameters

- All prototype values are small integer abstractions.
- `demo-ruleset-0.1.8` is a temporary in-code ruleset name.
- Coalition thresholds are design abstractions, not empirically calibrated values.

## Educational Debrief Hooks

- Debrief includes coalition liaison rationale and a coalition tradeoff prompt.
- Supports discussion of community investment versus policy buffer and access
  leverage under coalition pressure.

## Determinism and Replay Notes

- Resolved inputs are computed outside the transition core and committed into
  history.
- Replay recomputes all four committed transitions from genesis.
- No RNG inside `transition()`.

## Open Questions

- Whether future state fingerprints should use a cryptographic hash.
- Whether the first scenario loader should store seeds and stream definitions
  separately from command presets.
