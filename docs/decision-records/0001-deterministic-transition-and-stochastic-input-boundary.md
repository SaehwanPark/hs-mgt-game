# ADR-0001: Deterministic Transition and Stochastic Input Boundary

**Status:** Accepted  
**Date:** 2026-06-24  
**Deciders:** Project contributors

## Context

The Health Policy Strategy Game models health-policy outcomes as strategic
interaction among institutions. Contributors and classroom users must be able to
replay runs, inspect causal mechanisms, and trust that identical inputs produce
identical outcomes.

The project proposal and [`docs/design_principles.md`](../design_principles.md)
require:

- a deterministic core transition kernel;
- explicit separation of true state, observations, and stochastic inputs;
- immutable committed history;
- and inspectable actor decisions with rationales.

Before adding scenario loading, new actors, or forecast UI, the team needed a
recorded boundary between pure simulation and everything that may vary by seed or
run configuration.

## Decision

1. **Pure transition core.** `sim/transition.rs` evaluates
   `prior state + validated command + resolved inputs + ruleset -> transition`
   without RNG, wall-clock time, filesystem or network access, terminal I/O, or
   global mutable state.

2. **Stochastic input resolution upstream.** All random draws are resolved in
   `inputs/resolve.rs` into a `ResolvedInputs` record before `transition()` runs.
   The CLI and replay artifact store seed, turn index, and resolved values for
   verification.

3. **Named random streams.** `inputs/streams.rs` assigns stable stream indices
   (measurement, access delay/noise, labor, policy, coalition, revision,
   competitor) so subsystem changes do not unnecessarily perturb unrelated draws.

4. **Replay integrity via state hash.** Each committed transition stores a
   stable 64-bit FNV-1a hash over a canonical state record (`replay/hash.rs`).
   Replay verifies hashes; this is a deterministic regression check, not
   cryptographic integrity.

5. **Replay artifacts for reproducibility.** `replay-artifact-0.1.15` exports
   genesis state, ruleset id, seed, play mode, and committed transitions with
   explicit resolved inputs. Artifacts support external analysis and classroom
   replay; they are not mid-run save files.

## Consequences

### Positive

- Core simulation is unit-testable without terminal I/O.
- Seeds and resolved inputs are inspectable teaching artifacts.
- Golden trajectories (`tests/golden_seed42.rs`) guard accidental drift.
- Actor decisions and debrief explanations can cite committed history only.

### Negative / tradeoffs

- Every new stochastic mechanism requires a named stream and resolved field.
- CLI and artifact parsers must stay aligned when resolved inputs expand.
- FNV-1a hashes are not tamper-evident for untrusted artifact files.

### Follow-ups

- Scenario/ruleset format design (see [`scenario-format-draft.md`](../scenario-format-draft.md)).
- Forecast preview UI must use observation and ruleset bounds only, not future
  resolved inputs.
- Consider ADR for scenario loader when runtime format is approved.

## Alternatives Considered

| Alternative | Why not chosen |
| --- | --- |
| RNG inside `transition()` | Breaks determinism testing and hides stochastic inputs from replay |
| Single global seed draw per turn | Subsystem coupling; harder to isolate measurement noise from labor draws |
| Cryptographic state hash | Unnecessary for educational reproducibility; adds dependency |
| Mid-run save as replay artifact | Conflates analysis export with interactive resume semantics |

## Verification

- `cargo test` includes deterministic repeatability, seed isolation, and replay
  hash mismatch detection.
- `tests/golden_seed42.rs` pins canonical seed-42 trajectory.
- Code review checks that new `transition()` paths do not import RNG or I/O.

## Related Documents

- [`ARCHITECTURE.md`](../../ARCHITECTURE.md)
- [`docs/versioning-policy.md`](../versioning-policy.md)
- [`docs/evidence-registry.md`](../evidence-registry.md)
