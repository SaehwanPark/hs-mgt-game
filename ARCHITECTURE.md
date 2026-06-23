# Architecture

The project is currently in early research and design. This document records the
intended architecture boundaries that future implementation should preserve.

## Current State

- Language: Rust
- Interface: command-line first
- Package: single Rust package, `hs-mgt-game`
- Executable: placeholder `src/main.rs`
- Canonical design docs: `README.md` and `docs/`

No production simulation architecture has been implemented yet.

## Intended System Shape

The simulation should grow around a deterministic core transition model:

```text
previous state + actions + resolved external inputs + versioned ruleset
  -> events + attributed effects + next state
```

The core should not read randomness, wall-clock time, filesystem state, network
state, terminal input, or global mutable state during transition evaluation.

## Boundaries

### Core Simulation

Responsible for:

- typed world state
- actor actions
- ruleset evaluation
- deterministic state transitions
- emitted events and attributed effects
- immutable snapshots and append-only history records

The core should be testable without terminal I/O.

### Stochastic Input Resolution

Responsible for:

- seeded exogenous events
- measurement noise
- delayed or missing observations
- bounded-rationality draws where needed

Random draws should become explicit inputs before the deterministic transition
core is evaluated.

### Actor Information

The architecture must distinguish:

- true state
- actor-specific beliefs
- observations and public reports
- later corrections or revised estimates

Players and non-player actors should make decisions from available information,
not omniscient state.

### Interface

The initial interface is a CLI. Terminal rendering, input parsing, and display
formatting should remain outside the deterministic simulation core.

## Durable Constraints

- Model strategic interaction among institutions, not direct policy levers alone.
- Preserve meaningful tradeoffs; do not collapse the game into one score.
- Keep actor utility, organizational goals, social welfare, and educational
  assessment distinct.
- Prefer narrow vertical slices before general frameworks.
- Make assumptions, causal mechanisms, and debrief explanations inspectable.
- Treat history as immutable after committed transitions.

## Open Architectural Decisions

- Module or crate boundaries for the deterministic core, CLI, scenario loading,
  and educational debriefing.
- Ruleset and scenario versioning format.
- State hashing and replay artifact format.
- Decision-record convention.
- Data and licensing policy.
