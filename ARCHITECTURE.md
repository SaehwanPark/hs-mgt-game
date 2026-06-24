# Architecture

The project is currently in early research and design. This document records the
intended architecture boundaries that future implementation should preserve.

## Current State

- Language: Rust
- Interface: command-line first
- Package: single Rust package, `hs-mgt-game`
- Executable: interactive and preset-play CLI over a four-turn deterministic demo
  with a starting executive dashboard, per-turn executive briefings, strategy
  previews, seeded resolved inputs, replay state-hash checks, and educational
  debrief in `src/main.rs`
- Canonical design docs: `README.md` and `docs/`

Last Reviewed: 2026-06-24
Status: Verified

The current implementation is a compact architecture proof, not a production
simulation. It demonstrates a pure transition function, explicit resolved
inputs derived from a run seed and named streams, actor-specific observation,
local strategic decision rationales for a commercial insurer, state policy
officials, nursing workforce representative, and regional provider coalition
liaison, attributed effects, append-only history, stable per-transition state
hashes, replay verification that detects committed hash drift, a deterministic
end-of-run educational debrief, and CLI play modes for per-turn interactive
command entry or three hard-coded preset strategy paths with a starting
dashboard, commitment previews, and optional seed input. The first Phase 3 design
artifacts now define the actor-card template and first scenario brief that future
runtime additions should satisfy before adding new strategic actors or scenario
content.

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

Current proof location: `src/main.rs`. Each committed transition records a
stable 64-bit FNV-1a state hash over a canonical, labeled state record. This is
a deterministic replay check, not a cryptographic integrity guarantee.

Last Reviewed: 2026-06-23
Status: Verified

### Stochastic Input Resolution

Responsible for:

- seeded exogenous events
- measurement noise
- delayed or missing observations
- bounded-rationality draws where needed

Random draws should become explicit inputs before the deterministic transition
core is evaluated.

Current proof: `ResolvedInputs` are derived outside the transition core from a
run seed, turn index, prior state, and named streams for measurement noise,
delayed access reporting, labor pressure, policy signal values, coalition
leverage, and prior-period access measurement revisions.

Last Reviewed: 2026-06-23
Status: Verified

### Actor Information

The architecture must distinguish:

- true state
- actor-specific beliefs
- observations and public reports
- later corrections or revised estimates

Players and non-player actors should make decisions from available information,
not omniscient state.

Current proof: the player observation uses reported access and quality; later
turns may include prior-period access measurement revisions in the briefing
without rewriting committed history. The commercial insurer, state-policy,
coalition, and workforce decisions use actor-visible values and record
rationales. The educational debrief reports those rationales from committed
history rather than recomputing hidden actor knowledge.

Last Reviewed: 2026-06-23
Status: Verified

### Interface

The initial interface is a CLI. Terminal rendering, input parsing, and display
formatting should remain outside the deterministic simulation core.

Current proof: `cargo run` prints a starting executive dashboard and strategy
commitment previews, prompts for interactive play (default) or one of three
preset strategy paths and an optional run seed, then either collects four
per-turn command entries with executive briefings and turn-resolution summaries
or runs a preset path with the full technical demo dump, replay result, and
educational debrief. The CLI input boundary selects play mode, per-turn command
parameters or compiled strategy paths, and seeds only; there is no general
command parser, scenario loader, save format, or durable replay artifact yet.

Last Reviewed: 2026-06-24
Status: Verified

## Durable Constraints

- Model strategic interaction among institutions, not direct policy levers alone.
- Preserve meaningful tradeoffs; do not collapse the game into one score.
- Keep actor utility, organizational goals, social welfare, and educational
  assessment distinct.
- Prefer narrow vertical slices before general frameworks.
- Make assumptions, causal mechanisms, and debrief explanations inspectable.
- Treat history as immutable after committed transitions.
- Keep prototype formulas visibly labeled as abstractions until evidence and
  calibration work justify stronger claims.

Last Reviewed: 2026-06-23
Status: Verified

### Scenario and Actor Design

Responsible for:

- actor-card fields before strategic actor expansion
- first-scenario scope and learning objectives
- educational debrief hooks
- explicit scenario non-goals and evidence gaps

Current design artifacts: `docs/actor-cards.md` and
`docs/first-scenario-brief.md`. These documents are not runtime schemas and do
not add scenario loading, command parsing, or persistence.

Last Reviewed: 2026-06-24
Status: Verified

## Open Architectural Decisions

- Module or crate boundaries for the deterministic core, CLI, scenario loading,
  and educational debriefing once the prototype needs reusable boundaries beyond
  the compact file.
- Ruleset and scenario versioning format.
- Durable replay artifact format.
- Decision-record convention.
- Data and licensing policy.
