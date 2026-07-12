# Architecture

The project is currently a playable CLI prototype with bounded stabilization,
competitive, and opt-in regional-affiliation campaign modes. This document
records the intended architecture boundaries that future implementation should
preserve.

## Current State

- Language: Rust
- Interface: command-line first
- Package: single Rust package, `hs-mgt-game`, with `src/lib.rs` module tree
- Executable: thin `src/main.rs` entry calling `cli::run()`
- MCP executable: `src/bin/hs-mgt-game-mcp.rs` serving a local stdio MCP server
  for bounded autonomous-agent play
- Library modules:
  - `model/` — typed world state, commands, competitive and affiliation state,
    resources, history, session types, campaign types
  - `affiliation/` — six-stage partner interaction genesis, observation,
    validation, deterministic transition, and replay
  - `competitive/` — competitive campaign mock fixtures and validation demos
  - `inputs/` — seeded stochastic input resolution
  - `sim/` — deterministic transition core
  - `actors/` — non-player actor decisions
  - `replay/` — replay verification and state hashing
  - `artifact/` — replay artifact serialize/deserialize/verify
  - `debrief/` — educational debrief generation
  - `cli/` — terminal I/O, parsers, session loop, display
  - `mcp/` — MCP session store, tool DTOs, and stdio server adapter
- Canonical design docs: `README.md` and `docs/`

Last Reviewed: 2026-07-12
Status: Verified

The current implementation includes a competitive campaign path with genesis
multi-system state, action-economy validation, simultaneous monthly batch
resolution (`sim/resolve.rs`), `transition_competitive()`, bounded AI player batches
(`actors/ai_player.rs`, `sim/observe_ai.rs`), and observation-only rival intel with
1-month lag (`sim/observe_competitive.rs`), monthly event/delay ticks, annual
policy inputs, Stata-like competitive command parsing, and a 24-month
competitive CLI loop with help-command catalog output, colored command prompt
tokens, and Tab autocomplete for verbs, argument keys, and enum values.
It also includes a local stdio MCP server (`hs-mgt-game-mcp`) with in-memory
sessions for `stabilization-v1`, `competitive-regional-v1`, and
`regional-affiliation-v1`.

The current implementation is a playable prototype and compact architecture
proof, not a production simulation or calibrated policy model. It demonstrates a
pure transition function in `sim/transition.rs`, explicit resolved inputs from
`inputs/resolve.rs`, actor-specific observation and decisions, attributed
effects, append-only history, stable per-transition state hashes in
`replay/hash.rs`, replay verification, deterministic educational debrief in
`debrief/report.rs`, optional replay artifact export in `artifact/`, and CLI
play modes in `cli/session.rs`.

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

The initial player interface is a CLI. Terminal rendering, input parsing,
display formatting, MCP protocol handling, and any future GUI rendering should
remain outside the deterministic simulation core.

Current proof: `cargo run` invokes `cli::run()` for a starting executive
dashboard and strategy commitment previews, play-mode and seed selection,
per-turn interactive command entry or preset strategy paths, executive
briefings, turn-resolution summaries, replay, debrief, and optional replay
artifact export.

`cargo run --bin hs-mgt-game-mcp` invokes a local stdio MCP server that exposes
tools for starting a bounded session, reading actor-visible observations,
submitting one turn/month of commands, inspecting committed transition
summaries, and ending a session. The MCP layer reuses existing parsers,
observation helpers, validation, and transition functions; it does not read
randomness or mutate the core directly.

Last Reviewed: 2026-07-07
Status: Verified

Future GUI work should be a thin client over the same scenario, observation,
command-validation, history, replay, and debrief surfaces used by CLI and MCP.
It must not introduce a second simulation state model, hidden randomness,
network-dependent core behavior, or GUI-only transition semantics. Asset loading
and license attribution belong at the interface/distribution boundary, not in
the core engine.

Last Reviewed: 2026-07-09
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
- Freeze major new abstractions unless playtest, scenario-authoring, debrief, or
  domain-review evidence identifies a concrete need that current structures
  cannot satisfy.
- Treat simultaneous resolution as a semantic contract. System-local actions
  may be applied in canonical order only while permutation tests prove order
  independence. Before adding contested hiring, shared capacity, negotiation
  conflicts, or demand diversion, split resolution into prior-snapshot intent
  evaluation, central conflict resolution, and effect application.

Last Reviewed: 2026-06-23
Status: Verified

### Future Architecture Posture

The current architecture is sufficiently expressive for validation of the
bounded stabilization and competitive campaign slices. Future work should avoid
adding generalized actor frameworks, analytics platforms, calibration
structures, GUI platform layers, or broader scenario-authoring infrastructure
until a documented finding shows that gameplay, authoring, debriefing, audience
reach, or validation is blocked by the current narrower shape.

When a new abstraction is justified, the implementing slice should name the
evidence source, keep deterministic replay and actor-observation boundaries
intact, and leave unrelated platform goals deferred.

A future advisor-market slice is deferred as a narrow decision-support
candidate. If later justified, it would require shared market and roster state, advisor-generated
recommendations derived from each owning system's observation, explicit resolved
inputs for outside arrivals and contested hires, and append-only records of
payroll, advice, and employment changes. It must not expose hidden state,
create a generic worker framework, or claim that advisor quality predicts
outcomes. See `docs/expansion-proposal-review.md`.

Last Reviewed: 2026-07-09
Status: Verified; future advisor-market boundary documented

A `regional-affiliation-v1` slice is implemented outside the current
competitive runtime. It reuses the transition, observation, history, and
debrief boundaries through a localized six-stage partner interaction, stores
affiliation-specific resolved inputs before transition evaluation, preserves
actor-specific observations, and leaves the default competitive campaign
unchanged. See ADR-0010.

Last Reviewed: 2026-07-12
Status: Verified; regional-affiliation runtime boundary documented

The v0.12.1 Phase 7 capture compared the typed affiliation observation to the
MCP rendering boundary and found that alternatives, assumptions, and
commitments were omitted. v0.12.2 renders those existing typed fields through
the MCP observation without changing transition semantics, rulesets, or
replay/hash contracts. The projection remains outside the deterministic core.

The v0.12.3 Phase 7 review audits the v0.12.2 affiliation post-fix artifact
against the approved v0.11.12 competitive teachability capture. It compares
decision-context, action/response, transition/hash, outcome, debrief, and
source-specific context coverage without merging campaign semantics or
changing runtime behavior. Runtime promotion remains deferred.

### Scenario and Actor Design

Responsible for:

- actor-card fields before strategic actor expansion
- first-scenario scope and learning objectives
- educational debrief hooks
- explicit scenario non-goals and evidence gaps

Current design artifacts include `docs/actor-cards.md`,
`docs/first-scenario-brief.md`, `docs/competitive-scenario-brief.md`,
`docs/core-loop-spec.md`, and `docs/gameplay-competitive-sketch.md`. Runtime
scenario loading is implemented for both `stabilization-v1` and
`competitive-regional-v1`; scenario migration tooling and broader authoring
workflows remain deferred until a bounded slice is approved.

Last Reviewed: 2026-07-07
Status: Verified

## Competitive Campaign

Implemented modules for `competitive-regional-v1`:

| Module | Responsibility | Status |
| --- | --- | --- |
| `CampaignRouter` | Select stabilization vs competitive entry in CLI | Verified |
| `PolicyCalendar` | Month index, year boundary labels for reports | Verified |
| Executive report renderer | Six-section monthly briefing from `PlayerObservation` | Verified |
| `CompetitiveCommand` + validation | AP/cash/PC batch validation per action catalog | Verified |
| `CompetitiveWorldState` + genesis | K+1 health systems, player slots, difficulty fixtures | Verified (I4) |
| `SimultaneousActionResolver` | Aggregate monthly player batches before transition | Verified (`sim/resolve.rs`, v0.1.32) |
| `transition_competitive()` | Competitive monthly state transition | Verified (`sim/transition_competitive.rs`, v0.1.32) |
| `EffectScheduler` | Delayed/project effect queue and annual tick | Verified (v0.1.34) |
| `CommandRepl` | Stata-like parse/display layer (I/O only, ADR-0006), with help catalog rendering and command autocomplete | Verified |
| `CompetitiveCampaignLoop` | 24-month CLI loop over evolving competitive world state | Verified (v0.5.0) |

Genesis world, observation derivation, and validation demos live in
`src/competitive/`; the competitive campaign loop lives in
`src/cli/campaign.rs` and reuses `resolve_competitive_month()` for each month.
The 24-month campaign loop features autosave/resume, scenario loading, and replay export.

Last Reviewed: 2026-07-07
Status: Verified (router, report, validation, genesis, resolver, AI, events, CLI, campaign loop, autosave, scenario loader)

## Open Architectural Decisions

- Durable replay artifact format: `replay-artifact-0.1.15` stores ruleset id,
  seed, play mode, genesis state, and committed transitions with explicit
  resolved inputs for external verification. This is analysis/reproducibility,
  not cryptographic integrity or mid-run save/load.
- Mid-run interactive save: **addressed** by `session-save-0.1.27` and
  [ADR-0002](docs/decision-records/0002-mid-run-session-save.md). Autosave on
  voluntary quit and resume on startup now cover current interactive campaign
  modes; save state remains separate from replay artifacts.
- Module boundaries for the deterministic core, CLI, scenario loading, and
  educational debriefing are now established in `src/lib.rs`. Characterization
  tests are colocated with owning modules under `#[cfg(test)]`; a crate-root
  golden integration test lives in `tests/golden_seed42.rs`.
- Ruleset and scenario versioning format: design draft at
  `docs/scenario-format-draft.md`; the accepted runtime loader parses and validates
  both stabilization and competitive scenario files.
- Decision-record convention: **addressed** by
  `docs/decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md`.
- Competitive campaign boundaries: **addressed** by ADRs
  [0003](docs/decision-records/0003-simultaneous-monthly-player-actions.md)–[0006](docs/decision-records/0006-stata-like-cli-layer.md);
  I1–I8 and the competitive campaign loop landed.
- Data and licensing policy.
- MCP interface boundary: **addressed** by
  [ADR-0008](docs/decision-records/0008-mcp-agent-interface.md). Local stdio
  tools are accepted for bounded agent play; HTTP transport, auth, persistence,
  and long-running multi-client sessions remain deferred.
