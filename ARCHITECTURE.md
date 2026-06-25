# Architecture

The project is currently in early research and design. This document records the
intended architecture boundaries that future implementation should preserve.

## Current State

- Language: Rust
- Interface: command-line first
- Package: single Rust package, `hs-mgt-game`, with `src/lib.rs` module tree
- Executable: thin `src/main.rs` entry calling `cli::run()`
- Library modules:
  - `model/` — typed world state, commands, competitive commands, resources, history, session types, campaign types
  - `competitive/` — competitive campaign mock fixtures and validation demos
  - `inputs/` — seeded stochastic input resolution
  - `sim/` — deterministic transition core
  - `actors/` — non-player actor decisions
  - `replay/` — replay verification and state hashing
  - `artifact/` — replay artifact serialize/deserialize/verify
  - `debrief/` — educational debrief generation
  - `cli/` — terminal I/O, parsers, session loop, display
- Canonical design docs: `README.md` and `docs/`

Last Reviewed: 2026-06-24
Status: Verified

The current implementation is a compact architecture proof, not a production
simulation. It demonstrates a pure transition function in `sim/transition.rs`,
explicit resolved inputs from `inputs/resolve.rs`, actor-specific observation and
decisions, attributed effects, append-only history, stable per-transition state
hashes in `replay/hash.rs`, replay verification, deterministic educational
debrief in `debrief/report.rs`, optional replay artifact export in
`artifact/`, and CLI play modes in `cli/session.rs`.

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

Current proof location: `sim/transition.rs` and `sim/validate.rs`. Each committed
transition records a stable 64-bit FNV-1a state hash over a canonical, labeled
state record in `replay/hash.rs`. This is a deterministic replay check, not a
cryptographic integrity guarantee.

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

Current proof: `ResolvedInputs` are derived in `inputs/resolve.rs` from a run
seed, turn index, prior state, and named streams for measurement noise, delayed
access reporting, labor pressure, policy signal values, coalition leverage,
prior-period access measurement revisions, and competitor market signal.

Last Reviewed: 2026-06-24
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
coalition, workforce, and competitor decisions use actor-visible values and
record rationales. The educational debrief reports those rationales from
committed history rather than recomputing hidden actor knowledge.

Last Reviewed: 2026-06-24
Status: Verified

### Interface

The initial interface is a CLI. Terminal rendering, input parsing, and display
formatting should remain outside the deterministic simulation core.

Current proof: `cargo run` invokes `cli::run()` for a starting executive
dashboard and strategy commitment previews, play-mode and seed selection,
per-turn interactive command entry or preset strategy paths, executive
briefings, turn-resolution summaries, replay, debrief, and optional replay
artifact export.

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

Current design artifacts: `docs/actor-cards.md`,
`docs/first-scenario-brief.md`, `docs/competitive-scenario-brief.md`,
`docs/core-loop-spec.md`, and `docs/gameplay-competitive-sketch.md`. These
documents are not runtime schemas and do not add scenario loading for the
competitive campaign until approved slices land.

Last Reviewed: 2026-06-24
Status: Verified

## Competitive Campaign (partial runtime)

Implemented modules for `competitive-regional-v1`:

| Module | Responsibility | Status |
| --- | --- | --- |
| `CampaignRouter` | Select stabilization vs competitive entry in CLI | Verified |
| `PolicyCalendar` | Month index, year boundary labels for reports | Verified |
| Executive report renderer | Six-section monthly briefing from `PlayerObservation` | Verified |
| `CompetitiveCommand` + validation | AP/cash/PC batch validation per action catalog | Verified |
| `MultiSystemState` | K+1 health systems in shared market (`model/players.rs`) | Needs Review |
| `SimultaneousActionResolver` | Aggregate monthly player batches before transition | Needs Review |
| `EffectScheduler` | Delayed/project effect queue and annual tick | Needs Review |
| `CommandRepl` | Stata-like parse/display layer (I/O only, ADR-0006) | Needs Review |

Stub fixtures and validation demos live in `src/competitive/`; full simulation deferred to I4–I8.

Last Reviewed: 2026-06-24
Status: Verified (router, report, validation); Needs Review (remaining modules)

## Open Architectural Decisions

- Durable replay artifact format: `replay-artifact-0.1.15` stores ruleset id,
  seed, play mode, genesis state, and committed transitions with explicit
  resolved inputs for external verification. This is analysis/reproducibility,
  not cryptographic integrity or mid-run save/load.
- Mid-run interactive save: **addressed** by `session-save-0.1.27` and
  [ADR-0002](docs/decision-records/0002-mid-run-session-save.md). Autosave on
  voluntary quit; resume on startup; separate from replay artifacts.
- Module boundaries for the deterministic core, CLI, scenario loading, and
  educational debriefing are now established in `src/lib.rs`. Characterization
  tests are colocated with owning modules under `#[cfg(test)]`; a crate-root
  golden integration test lives in `tests/golden_seed42.rs`.
- Ruleset and scenario versioning format: design draft at
  `docs/scenario-format-draft.md`; no runtime loader yet.
- Decision-record convention: **addressed** by
  `docs/decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md`.
- Competitive campaign boundaries: **addressed** by ADRs
  [0003](docs/decision-records/0003-simultaneous-monthly-player-actions.md)–[0006](docs/decision-records/0006-stata-like-cli-layer.md);
  runtime modules deferred to slices I1–I8.
- Data and licensing policy.
