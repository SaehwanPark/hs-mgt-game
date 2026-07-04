# Lessons Learned

Use this file to record practical lessons that would save future contributors or
agents meaningful time. Keep entries factual, concise, and tied to prevention.


## Keep Scenario Briefs Parameter-Complete to Avoid Downstream Gaps

- Context: Drafting the `competitive-exemplary-v1` scenario brief under Track 2.
- Symptom: Initial drafts of the scenario timeline referred to delayed consequences for underfunded EHR projects and nurse staffing ratios, but lacked initial parameters for starting staffing ratios or definitions of EHR project costs, duration, and Action Point requirements in the brief.
- Cause: Scenario authoring sometimes relies on mechanism-design documents or core codebase defaults without reflecting those constraints explicitly in the student/instructor-facing brief.
- Prevention: Every scenario brief must explicitly specify starting parameters, project costs, duration, Action Point requirements, and immediate vs. delayed consequences of events (such as strikes or underfunding) to remain actionable for future scenario developers.

## Post-Milestone SDD Reviews Should Rank, Not Expand

- Context: After the public playable prototype reached v0.2.0, the repo had a
  thorough runnable stabilization slice, a bounded competitive preview, MCP
  playtest evidence, and a long Future backlog.
- Symptom: Future work was specific but still read as a broad menu, making it
  too easy for the next agent to pick platform expansion, balance tuning, or
  new actors before the product risk was re-evaluated.
- Cause: Milestone completion changed the main uncertainty from "can the game
  run end to end?" to "is repeated play explainable, teachable, and strategically
  interesting?"
- Resolution: Keep `SPEC.md` `Present` empty, record the progress-review slice
  as completed, and rank Future tracks so debrief/instructor analysis,
  exemplary scenario authoring, and evidence-confidence work lead runtime
  expansion.
- Prevention: After major runnable milestones, perform an SDD review that
  explicitly names the next risk, ranks Future tracks, and refreshes stale
  companion docs before promoting a new implementation slice.

## End-Session Metrics Belong In Debrief, Not Active Observation

- Context: Closing the v0.1.49 competitive MCP evidence gap by exposing final
  player tradeoff metrics.
- Symptom: Competitive playtest findings could compare commands and hashes but
  could not make outcome-distribution claims.
- Cause: The active MCP observation surface correctly avoids omniscient state,
  but the end-session debrief had not yet summarized the final human-system
  metrics available in committed history.
- Resolution: Add final player tradeoff and resource lines to competitive
  `end_session` debrief only, derived from genesis and final committed human
  system state.
- Prevention: Put post-run analysis metrics in debrief or instructor surfaces,
  not active-play observations, unless a design explicitly changes the actor's
  information boundary.

## Playtest Policies Need Campaign-Stable Detection

- Context: Running the v0.1.49 automated MCP playtest batch after the AI-agent
  validation pivot.
- Symptom: The batch appeared to hang on the first stabilization `submit_turn`.
- Cause: Scripted policies detected stabilization by checking for the Turn 1
  `staffed_beds` legal-command hint. From Turn 2 onward the policies fell into
  the competitive branch, submitted invalid competitive commands to the
  stabilization parser, and retried forever.
- Resolution: Detect stabilization by the MCP legal-command surface shape,
  launch the built stdio MCP binary, and make scripted validation failures raise
  with campaign, turn, command, and error context.
- Prevention: In playtest automation, branch on stable campaign/session
  metadata or legal-command surface shape, not one turn-specific hint. Scripted
  policies should fail fast on validation errors rather than silently retrying.

## SDD Status Drift Needs A Cross-Doc Scan

- Context: Cleaning up `SPEC.md` after competitive preview, scenario-loader, MCP,
  and playtest slices had landed.
- Symptom: `SPEC.md` and `ARCHITECTURE.md` reflected the current runtime, while
  companion docs still described competitive work as design-only, stubbed, or
  planned I1-I8 runtime.
- Cause: Slice completion updated release history faster than older design docs
  that originally framed the implementation sequence.
- Resolution: Refresh `SPEC.md` Future into gated actionable tracks, archive
  displaced completion detail, and scan canonical/companion docs for stale
  status phrases before final verification.
- Prevention: For SDD cleanup PRs, run a targeted `rg` over `SPEC.md`,
  `README.md`, `ARCHITECTURE.md`, and `docs/*.md` for old version numbers,
  "stub", "design only", "runtime deferred", and completed slice names before
  calling the docs aligned.

## Broad Feedback Should Become Gates Before Features

- Context: Translating external assessment into future SDD planning after the
  architecture, MCP interface, scenario loader, and competitive preview already
  existed.
- Symptom: Strong conceptual feedback can invite broad new abstractions,
  diagnostics, scenario tooling, or calibration frameworks before gameplay has
  proved the need.
- Cause: The project can represent sophisticated health-policy simulation, but
  the next risk is whether repeated play is difficult, legible, interesting, and
  teachable.
- Resolution: Convert feedback into falsifiable playtest hypotheses,
  strategy-space diagnostics, debrief QA, canonical-scenario gates, and
  model-confidence labels rather than runtime expansion.
- Prevention: For future SDD planning updates, ask which finding would justify
  implementation. If no playtest, authoring, debrief, or domain-review evidence
  exists, keep the item in Future and label the needed evidence.

## Agent Playtests Need Evidence Labels

- Context: Replacing planned external human playtest recruitment with AI-agent
  and sub-agent playtests.
- Symptom: It is easy for validation language to drift from "agent traces show
  the debrief is inspectable" into "players learned the intended material."
- Cause: Agent runs are reproducible and useful, but they are simulated-player
  evidence rather than human educational measurement.
- Resolution: Added an active agent-playtest protocol, ADR-0009, glossary terms,
  and roadmap language that separate command/gameplay evidence from human
  learning and policy-validation claims.
- Prevention: When adding playtest findings, label the actor type, seed,
  profile or prompt, observations, commands, and evidence limits before making
  follow-up recommendations.

## MCP SDK Schema Derives Need Direct Dependencies

- Context: Adding the first local MCP stdio server with the official `rmcp`
  Rust SDK.
- Symptom: `JsonSchema` derives failed even though the SDK re-exports schema
  helpers.
- Cause: Derive macros resolve the `schemars` crate name directly.
- Resolution: Add `schemars` as a direct dependency and keep MCP DTOs in
  `src/mcp/` instead of adding serialization/schema derives to core model types.
- Prevention: For protocol adapter DTOs, depend directly on the derive macro's
  crate and keep schema-facing structs at the adapter boundary.

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

## Rustyline Helper Types Need Full Trait Set

- Context: Adding competitive verb Tab-autocomplete using `rustyline`.
- Symptom: Compilation fails with trait-bound errors even when a custom
  completer compiles in isolation.
- Cause: In `rustyline`, `Helper` requires `Completer + Hinter + Highlighter +
  Validator` on the same helper type.
- Resolution: Implemented empty/default `Hinter`, `Highlighter`, and `Validator`
  traits on the completer helper struct.
- Prevention: When introducing a new `rustyline` helper, scaffold all required
  helper trait impls first, then add completer logic.

## Scenario Loading Should Start As A Data Boundary

- Context: Adding the first runtime scenario loader after the scenario format
  draft was approved for a narrow slice.
- Symptom: It is tempting to make scenario files own presets, transition logic,
  arbitrary paths, competitive campaigns, or migration policy immediately.
- Cause: The first proven need is to externalize the existing stabilization
  genesis and schedule, not to create a general authoring platform.
- Resolution: Added `scenario-toml-0.1.40` with one bundled
  `stabilization-v1` TOML fixture and validation before fresh runs; transitions,
  replay artifacts, and session saves stayed unchanged.
- Prevention: Extend scenario loading only when playtest or authoring evidence
  identifies a concrete repeated need; keep executable logic out of scenario
  files.

## Interactive Terminal Tests Can Hang Without Stdin Redirection

- Context: Running `cargo test` in a pseudo-terminal (PTY) runner or workspace sandbox.
- Symptom: Tests that read standard input for campaigns (e.g. `competitive_month_loop_runs_three_months_in_non_tty_context`) hang or timeout.
- Cause: `std::io::stdin().is_terminal()` returns `true` inside a PTY, causing the game to block waiting for human command input instead of executing the fallback non-TTY batch.
- Resolution: `stdin_uses_fallback_input()` in `src/cli/io.rs` treats `cfg!(test)` like non-TTY stdin so competitive campaign tests use preset fallback batches instead of rustyline. Stdin redirection (`cargo test < /dev/null`) still works for manual runs.
- Prevention: Route any new CLI stdin prompts through `stdin_uses_fallback_input()` (or equivalent) so unit tests never block on terminal detection inside PTYs.

## Clippy CI Check Prevents Code Quality Decay

- Context: Integrating `cargo clippy --all-targets -- -D warnings` into the CI workflow.
- Symptom: The repository had accumulated 32 clippy errors (including manual prefix stripping, complex type signatures, collapsible ifs) because clippy was not enforced in the pipeline.
- Cause: The original `.github/workflows/ci.yml` only executed `cargo fmt` and `cargo test` without checks for code quality and compiler lints.
- Resolution: Resolved all 32 clippy issues across production and test code, and added a lint checking step to the CI pipeline.
- Prevention: Run `cargo clippy --all-targets -- -D warnings` locally before committing and always include clippy checks in the CI runner to catch lints early.

## Centralize Post-Run Debriefing Logic for Shared CLI/MCP Surface

- Context: Adding instructor-visible summaries and decision quality reviews for stabilization and competitive campaigns.
- Symptom: It is tempting to write separate CLI-only or MCP-only report string formatting functions or duplicate logic between the MCP session handler and the CLI campaign loop.
- Cause: The CLI campaign and MCP session end endpoint need the same structured information. Duplicating code violates modularity and invites drift.
- Resolution: Consolidated both stabilization and competitive campaign debriefing functions (including the new instructor run summaries) into the `src/debrief/report.rs` module. The CLI campaign runner and the MCP session end endpoint call the exact same module functions, sharing the same representations.
- Prevention: Keep all report formatting and debrief generation code in `src/debrief` and have other layers (CLI and MCP) consume it, ensuring a single source of truth for debriefing text.

## write_to_file Scopes and Parameter Mismatch Scrutiny

- Context: Updating workspace pipeline files (`_workspace/*`) under the harness team spec.
- Symptom: `write_to_file` returned a tool error when writing to `_workspace/00_input/request-summary.md` with `ArtifactMetadata` specified.
- Cause: Specifying `ArtifactMetadata` flags the file as an agent artifact, which the tool restricts to the absolute path `/home/saehwan/.gemini/antigravity-cli/brain/`.
- Resolution: Omit `ArtifactMetadata` entirely when creating or modifying standard workspace and codebase files outside the conversation-specific artifacts directory.
- Prevention: Do not include `ArtifactMetadata` in `write_to_file` arguments unless writing a conversation report/plan directly to the chat artifacts directory.

## Scenario starting parameters should be complete to prevent initial deficits

- Context: Implementing clinical capacity and staffing requirements (nurses, physicians, admins) in the competitive campaign.
- Symptom: A unit test for the nurse staffing deficit failed because workforce trust dropped more than the isolated nurse deficit.
- Cause: The system genesis template initialized administrator counts below their target ratio, creating a starting admin deficit that triggered immediate burnout penalties in turn 0/genesis calculations.
- Prevention: Ensure that all starting staffing headcounts are set to at least their target ratio levels in the genesis template unless a starting deficit is intentionally part of the scenario. In unit tests, explicitly set target counts for all supporting headcounts (like admins) to isolate the testing of a specific deficit (like nurses).

## Competitive Staffing and Capacity Design Safeguards

- Context: Addressing senior code reviewer findings for Track 5 clinical service line capacity and staffing.
- Symptoms: Compounding exponential decay of access/quality metrics; AI players unable to recruit physicians/admins; immediate understaffing penalties due to instant construction vs. delayed recruitment; leaking rival private events in CLI summaries; integer division budget exploits.
- Causes & Resolutions:
  - **In-place Metric Mutation vs. Additive Penalties:** Direct multiplication of state metrics (`access_index`, `quality_index`) by utility ratios compounds exponentially to 0. Resolved by replacing multiplication with a linear monthly additive drop proportional to the staffing deficit severity.
  - **AI Competitor Completeness:** AI players were restricted to `RecruitRole::Nurse`. Resolved by extending AI candidate command generation to check and generate recruitment options for physicians and admins when their counts fall below target ratios.
  - **Physical Capacity Construction Delays:** Instant physical bed expansion paired with delayed nurse recruitment resulted in immediate, unavoidable turn-0 penalties. Resolved by queuing bed capacity additions with a 1-month delay, matching outpatient clinics, allowing players to recruit beforehand.
  - **Rival Event Filtering:** Rival private operational events (burnout, etc.) were displayed to the player. Resolved by filtering player-facing summaries to skip events starting with competitor names.
  - **Budget Division Exploits:** Players could buy projects with non-multiple budgets, under-paying total costs due to integer truncation. Resolved by validating that project budgets must be a multiple of the duration.
- Prevention: Always use additive drops for ongoing penalties, ensure AI player vocabulary handles all roles, keep construction and recruitment delays aligned, maintain observation boundaries in displays, and validate budget divisibility.

## Scenario Deserialization Backward Compatibility & Systems Length Validation

- Context: Implementing competitive scenario loading and validation (Track 1 / Phase 6.2).
- Symptom: Extending the `Scenario` struct with new required fields broke parsing of the existing stabilization scenario TOML file. Also, difficulty selection had to align with the number of systems in the custom file.
- Cause: TOML deserializers using `#[serde(deny_unknown_fields)]` reject input when fields are added unless they are marked optional. Difficulty choice also determines how many AI rival controllers are initialized.
- Resolution: Wrapped all new competitive-specific fields (`initial_market`, `systems`) and existing stabilization-specific fields (`initial_state`, `turn_schedule`, `actor_stubs`) in `Option`. Validated in `validate_stabilization_scenario` and `validate_competitive_scenario` that the required fields for each campaign are present. In the CLI session runner, verified that `systems.len() == 1 + difficulty.k_rivals()` before initializing.
- Prevention: Make all campaign-specific scenario fields optional in the shared deserialization struct and enforce campaign-specific schema requirements during separate validation passes.

## Competitive Campaign Length Extension & Autosave Implementation

- Context: Extending the competitive regional campaign from a 3-month preview to a full 24-month horizon with mid-campaign serialization, autosave, and reload.
- Symptom: Serializing structs with `'static str` references (e.g. `AiProfile`, `Event`, `AttributedEffect`) causes compilation or runtime issues with serde, and simultaneous loop progression requires keeping track of the historical transition chain.
- Cause: Serde cannot directly deserialize `'static str` since it represents memory leaked references. Additionally, resuming a competitive campaign requires restoring both the starting state and all resolved transitions to date.
- Resolution: Derived `Serialize` and `Deserialize` on all competitive types. For structs with `'static str` fields, serialized them as standard strings, and manually leaked them using `Box::leak` on deserialization to reconstruct stable `'static str` references. Bounded campaign execution to 24 months, auto-saved the transition history on early quit (`q`/`quit`) into `.config/hs-mgt-game/competitive_session.save`, and added a resume menu selection to reload it. Finally, enabled exporting the complete `CompetitiveHistory` as a replay JSON file upon campaign completion.
- Prevention: Separate save structures (`session.save` and `competitive_session.save`) to isolate serialization logic. When deserializing lifetime-bound static strings, deserialize into owned strings and use `Box::leak` to construct stable `'static str` references safely. Ensure complete unit/integration tests cover round-trip serialization and delete-on-completion paths.


## Keep Changelog and Versioning Policy Aligned with Repository Rules

- Context: Updating `CHANGELOG.md` to align with the new versioning policy (0.0.1 bump per PR/PR-equivalent change, 0.1 minor bump for major features/milestones with lower digits reset).
- Symptom: Commit history shows versions (like `0.5.0`) merged to `main` in PRs without corresponding entries in `CHANGELOG.md`, causing a mismatch between `Cargo.toml` and the changelog.
- Cause: Developers sometimes bump `Cargo.toml` version during PR development but forget to add the changelog section for that version.
- Resolution: Added the release notes for `0.5.0` (campaign extension, autosave, replay export), bumped the package version to `0.5.1` in both `Cargo.toml` and `CHANGELOG.md` for the alignment change itself, and aligned `docs/versioning-policy.md` to match the exact rules in `AGENTS.md`.
- Prevention: Always check that `CHANGELOG.md` includes the entry for the version in `Cargo.toml` before merging a PR, and perform a `0.0.1` bump for every PR-equivalent change (including changelog/documentation updates).


## Prevent Test Suite and Automated Playtest Hangs / Crashes

- Context: Running standard cargo test and python automated playtests after campaign loop extension.
- Symptom: Test execution blocks indefinitely waiting for stdin in PTY/terminal-like test environments, and automated playtests crash with `IndexError` on turn index >= 4.
- Cause: Directly calling `std::io::IsTerminal::is_terminal(&io::stdin())` inside campaign completion checks bypassing the `stdin_uses_fallback_input()` safeguard, and fixed 3-command arrays in playtest policies when the competitive loop runs for 24 months.
- Resolution: Swapped `is_terminal` checks with `!stdin_uses_fallback_input()` in `src/cli/campaign.rs` and `src/cli/session.rs`. Modified `scripts/run_automated_playtests.py` policy functions to return `"hold"` once turns exceed the defined command sequence.
- Prevention: Never bypass fallback checks with direct terminal state checks in interactive prompt paths. Ensure automated scripts gracefully scale commands when campaign configurations (like loop duration) change.


## Keep Offline Replay Fixtures Up to Date via Integration Tests

- Context: Developing offline diagnostic scripts that parse replay JSON files which match the current Rust models.
- Symptom: Hardcoded offline JSON files quickly become out-of-date and cause parsers to fail when Rust models are updated or serialized keys change.
- Cause: Manually exporting and updating JSON replay files is slow and easily overlooked.
- Resolution: Created an integration test `generate_mock_replay_fixture` under `tests/golden_competitive_seed42.rs` that automatically builds a full 24-month `CompetitiveHistory` and writes it out as a pretty JSON file at `tests/fixtures/mock_replay.json` on every test run.
- Prevention: Leverage standard test runners to dynamically export serialization fixtures to maintain parity between engine structures and diagnostic tool inputs.




