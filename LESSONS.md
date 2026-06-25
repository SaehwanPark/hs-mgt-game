# Lessons Learned

Use this file to record practical lessons that would save future contributors or
agents meaningful time. Keep entries factual, concise, and tied to prevention.

## Canonical Docs Define Scope Before Structure

- Context: Initiating the spec-driven-development baseline for an early research
  and design repository.
- Symptom: It would be easy to invent implementation, CI, scenario, or release
  conventions before the roadmap calls for them.
- Cause: The repository already has canonical proposal, roadmap, design
  principles, and harness documents that define durable boundaries and phase
  order.
- Resolution: Root SDD documents were initiated as lightweight indexes and
  boundary records, not as detailed process or architecture commitments.
- Prevention: Before major changes, read `README.md`, `docs/proposal.md`,
  `docs/roadmap.md`, `docs/design_principles.md`, and
  `docs/harness/health-policy-strategy-game/team-spec.md`; document deferred
  conventions instead of filling them in prematurely.

## First Engine Proof Should Stay Scripted

- Context: Replacing the placeholder CLI with the first deterministic
  architecture proof.
- Symptom: It is tempting to add scenario loading, interactive menus, richer
  actor frameworks, or hash libraries immediately.
- Cause: The roadmap asks for vertical slices before broad frameworks, and the
  codebase had no existing architecture to constrain abstractions.
- Resolution: The first proof uses one scripted command, explicit resolved
  inputs, simple integer metrics, deterministic replay, and no dependencies.
- Prevention: Add loaders, modules, dependencies, and broader actor frameworks
  only when a later slice has at least two concrete examples that need the same
  boundary.

## Second Slice Can Still Stay Single-File

- Context: Adding the first state-policy response after the initial
  payer-negotiation proof.
- Symptom: A second command and second actor decision can make a module split
  feel immediately attractive.
- Cause: The design boundary is now visible, but the prototype still has one
  compact transition function and no reusable scenario, CLI, or persistence
  boundary.
- Resolution: The policy response reused the existing command, observation,
  event, effect, history, and replay shapes without adding dependencies or
  modules.
- Prevention: Split modules when reuse or independent testing needs become
  concrete, not merely because a second branch exists in the demo.

## Debriefing Can Start From Committed History

- Context: Adding the first educational debrief to the deterministic demo.
- Symptom: It is tempting to design a general reporting framework, scenario
  schema, or instructor export format before the first debrief exists.
- Cause: The existing transition history already contains observations, actor
  rationales, attributed effects, and final state needed for a useful teaching
  summary.
- Resolution: The first debrief is a deterministic report over committed
  history, with no new dependency, loader, or persistent artifact format.
- Prevention: Add reporting structure only when repeated debrief outputs need a
  shared format or external consumers.

## First Playability Step Can Be Hard-Coded

- Context: Adding the first player-facing CLI choice after the scripted
  deterministic demo and debrief were working.
- Symptom: It is tempting to add a command parser, scenario schema, or save/load
  path as soon as stdin appears.
- Cause: The immediate roadmap need is to test whether different strategic
  paths produce understandable outcomes, not to define durable content formats.
- Resolution: The first playable slice uses three compiled strategy paths and a
  small input boundary that selects among existing deterministic transitions.
- Prevention: Add parsers and scenario loaders only when repeated playable
  content needs external authoring or persistence.

## Seeded Inputs Belong Outside The Transition Core

- Context: Replacing per-path hard-coded `ResolvedInputs` with a seeded
  stochastic input boundary.
- Symptom: It is tempting to call RNG helpers inside `transition()` once
  exogenous variation is needed.
- Cause: The architecture requires stochasticity to be resolved before the
  deterministic core evaluates state changes.
- Resolution: Added `resolve_inputs(seed, prior, ruleset)` with named streams
  and splitmix64 outside `transition()`, then committed resolved inputs into
  history for replay and debrief.
- Prevention: Keep all random draws, measurement noise, and exogenous shocks in
  explicit pre-transition resolution steps; never hide RNG inside the core.

## Third Turn Can Reuse Command And Actor Patterns

- Context: Adding a workforce pressure turn after payer and policy interactions.
- Symptom: A third command and third actor decision can invite a general
  campaign framework or module split.
- Cause: The demo already has command validation, actor rationales, effects,
  history, replay, and debrief patterns that extend cleanly.
- Resolution: Added `RespondToWorkforcePressure` with a nursing workforce
  representative decision, extended strategy presets with `third_command`, and
  kept everything in `src/main.rs` without new dependencies.
- Prevention: Extend the existing command and actor-decision shapes turn by turn
  until reuse boundaries justify extraction into modules.

## Fourth Turn Can Reuse Coalition Patterns

- Context: Adding a regional access coalition turn after payer, policy, and
  workforce interactions.
- Symptom: A fourth command and fourth actor decision can invite a general
  coalition framework or module split.
- Cause: The demo already has command validation, actor rationales, effects,
  history, replay, and debrief patterns that extend cleanly.
- Resolution: Added `JoinRegionalAccessCoalition` with a coalition liaison
  decision, extended strategy presets with `fourth_command`, and kept everything
  in `src/main.rs` without new dependencies.
- Prevention: Extend the existing command and actor-decision shapes turn by turn
  until reuse boundaries justify extraction into modules.

## Observation Revisions Can Stay In Briefings

- Context: Adding prior-period access measurement revisions after the coalition
  turn without rewriting committed history.
- Symptom: It is tempting to retroactively edit prior transition observations
  when later data arrives.
- Cause: The architecture requires immutable committed observations while still
  teaching the difference between reported and revised estimates.
- Resolution: Added `access_measurement_revision` to resolved inputs and
  `prior_access_revision` to observations; debrief notes revisions while history
  remains append-only.
- Prevention: Keep revisions as explicit briefing inputs or notes; never mutate
  prior committed transition records.

## Phase 2 Docs Should Constrain Before They Format

- Context: Expanding the system-boundary and ontology draft after the first
  four-turn vertical-slice prototype.
- Symptom: It is tempting to introduce scenario schemas, actor-card templates,
  or parameter ledgers while documenting the conceptual boundary.
- Cause: The roadmap calls for ontology and causal boundaries before broader
  implementation conventions.
- Resolution: The Phase 2 document names actors, authority, observations,
  commands, causal categories, exclusions, and deferred ontology work without
  defining a file format or calibration process.
- Prevention: Use boundary docs to stabilize vocabulary and scope first; create
  loaders, schemas, and ledgers only when a later slice needs executable or
  evidence-backed artifacts.

## Actor And Scenario Docs Should Gate Runtime Expansion

- Context: Continuing from the Phase 2 boundary draft into the first Phase 3
  design artifacts.
- Symptom: It is tempting to add a fifth turn, a new actor, or a scenario
  schema as soon as the current demo has a coherent four-turn loop.
- Cause: The next roadmap need is to clarify actor authority, information,
  objectives, and learning goals before expanding runtime content.
- Resolution: Added an actor-card template and first scenario brief without
  changing Rust behavior, adding a loader, or introducing a runtime schema.
- Prevention: Before adding a strategic actor or scenario mechanism, write the
  actor card and scenario rationale first; only implement when the slice can be
  tested deterministically and explained in debrief.

## Replay Hashing Should Stay Canonical And Bounded

- Context: Adding stable state hashes to the deterministic replay proof.
- Symptom: It is tempting to add a serializer, save format, cryptographic hash
  dependency, or durable replay artifact as soon as hashes appear.
- Cause: The immediate Phase 4 need is drift detection during replay, not
  persistence or tamper-proof storage.
- Resolution: Added a labeled canonical state record and local 64-bit FNV-1a
  hash for committed transition checks without changing gameplay mechanics.
- Prevention: Keep replay hash inputs explicit and versioned; add external
  replay artifacts or stronger hash guarantees only when save/load, analysis,
  or release requirements make them necessary.

## CLI Playability Can Improve Without New Input Semantics

- Context: Adding a starting executive dashboard and strategy previews after
  the replay hash proof.
- Symptom: It is tempting to make the preview step a command parser, forecast
  engine, or per-turn choice system.
- Cause: The first Phase 5 playability need is better pre-run context, while
  the existing compiled strategy paths still provide the bounded behavior under
  test.
- Resolution: Added pure dashboard and commitment-preview helpers derived from
  existing state and `StrategyPlan` values, without changing transitions,
  resolved inputs, actor decisions, or replay hashes.
- Prevention: Keep CLI affordance improvements at the display boundary until
  the scenario action vocabulary justifies interactive per-turn command entry.

## Per-Turn Play Can Reuse Existing Command Shapes

- Context: Adding per-turn interactive command entry after the dashboard preview
  slice.
- Symptom: It is tempting to add a general command grammar, scenario schema, or
  per-turn posture menus before the first interactive loop exists.
- Cause: The four-turn demo already has typed commands, validation, observation
  briefings, actor decisions, and replay hashes that can be driven turn by turn.
- Resolution: Added play-mode selection, pure per-command parsers with
  access-stabilization defaults, executive briefings from observation data only,
  and concise turn summaries while preserving preset strategy paths for
  regression.
- Prevention: Add parsers and posture menus only when repeated playable content
  needs external authoring or more than numeric parameter entry.

## Replay Artifacts Can Stay Human-Readable and Dependency-Free

- Context: Adding deterministic replay artifact export after interactive play.
- Symptom: It is tempting to add JSON crates, cryptographic hashes, or a general
  save/load framework as soon as external replay is mentioned.
- Cause: The committed history already stores commands, resolved inputs, and
  per-turn state hashes needed for verification.
- Resolution: Added a versioned line-oriented `replay-artifact-0.1.15` format
  with pure serialize, deserialize, and verify helpers plus an optional
  post-run export prompt.
- Prevention: Keep artifact formats explicit and versioned; add stronger
  integrity guarantees or mid-run persistence only when analysis or classroom
  workflows require them.

## Competitive Track Justifies Scoped Command Parser

- Context: Designing the competitive regional market campaign with Stata-like CLI.
- Symptom: Earlier lessons deferred general command parsers for the stabilization
  vertical slice, which uses numeric prompts and turn-locked commands.
- Cause: The competitive sketch requires verb+argument entry, help, and
  autocomplete at a scale numeric prompts cannot support.
- Resolution: ADR-0006 limits the parser to the competitive campaign I/O layer
  only; stabilization demo unchanged; parse output is typed commands feeding the
  existing validation and transition boundary.
- Prevention: Do not generalize the REPL to stabilization until a concrete need
  appears; keep parser logic out of `transition()` per ADR-0001.
