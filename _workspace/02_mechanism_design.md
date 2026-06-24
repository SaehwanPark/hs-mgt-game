# Mechanism Design

## Goal and Roadmap Phase

Extend the seeded two-turn playable demo with a third-turn workforce pressure
interaction while preserving the deterministic transition core, replay, debrief,
and CLI strategy paths.

## Slice Boundary

Included:

- One player-controlled nonprofit health system.
- One commercial insurer decision (turn 1).
- One state policy official decision (turn 2).
- One nursing workforce representative decision (turn 3).
- One capacity investment command.
- One access-mandate response command.
- One workforce pressure response command.
- One explicit run seed at the CLI boundary.
- Named random streams for measurement noise, delayed access reporting, labor
  pressure, and policy signal resolution.
- Three hard-coded strategy paths selected through the existing CLI input
  boundary.
- One append-only three-transition history.
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
  response, and workforce pressure response commands through one of three
  compiled strategy paths.
- Commercial insurer: may accept, counter, or reject the requested rate path.
- State policy officials: may grant flexibility, continue the mandate, or
  escalate oversight.
- Nursing workforce representative: may accept a cooperative retention package,
  offer limited support, or signal a work action.
- Exogenous variation enters only through resolved inputs derived from the run
  seed before transition evaluation.
- Educational debrief: may summarize committed observations, effects, actor
  rationales, and final state movement; it does not alter the simulation state.

## State, Beliefs, and Observations

- True state tracks cash, staffed beds, access, quality, workforce trust,
  community trust, commercial rate, and policy pressure.
- Player observation reports delayed/noisy access and current quality.
- Labor decisions use reported access, prior workforce trust, and explicit
  labor sick-call pressure from resolved inputs.
- The transition core receives observations and resolved inputs explicitly; it
  does not generate randomness.

## Commands, Events, and Effects

- Valid commands: `StabilizeAccess`, `RespondToStateAccessMandate`, and
  `RespondToWorkforcePressure`.
- Workforce command fields: `retention_spend` and `schedule_relief_commitment`.
- CLI strategy paths: access stabilization, fiscal caution, and aggressive
  bargaining each include a third compiled workforce posture.
- Validation failures: negative or excessive retention spend and non-positive
  schedule relief commitment.
- Modeled unfavorable labor outcome: work action signal reducing access and
  trust.
- Events summarize actor-visible occurrences.
- Effects attribute metric deltas to sources.

## Strategic Interaction

The nursing workforce representative chooses among cooperative acceptance,
limited support, or work action by comparing retention spend, schedule relief
commitment, workforce trust, reported access, and labor sick-call pressure from
resolved inputs. The decision record includes a rationale for inspection and
debriefing.

## Stochastic Input Boundary

- Default seed: `42`.
- Named streams unchanged from v0.1.6.
- Third turn resolves inputs from seed and post-turn-2 state before transition.

## Assumptions and Parameters

- All prototype values are small integer abstractions.
- `demo-ruleset-0.1.7` is a temporary in-code ruleset name.
- `max_retention_spend` and minimum credible offer thresholds are design
  abstractions, not empirically calibrated values.

## Educational Debrief Hooks

- Debrief includes labor actor rationale and a workforce tradeoff prompt.
- Supports discussion of retention investment versus access and trust effects
  under labor pressure.

## Determinism and Replay Notes

- Resolved inputs are computed outside the transition core and committed into
  history.
- Replay recomputes all three committed transitions from genesis.
- No RNG inside `transition()`.

## Open Questions

- Whether future state fingerprints should use a cryptographic hash.
- Whether the first scenario loader should store seeds and stream definitions
  separately from command presets.
