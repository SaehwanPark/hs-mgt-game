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
