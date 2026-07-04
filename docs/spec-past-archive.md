# SPEC Past Archive

**Archived:** 2026-06-24  
**Source:** Former `## Past` section of [`SPEC.md`](../SPEC.md)

This file preserves full per-slice completion records. Canonical release history
remains in [`CHANGELOG.md`](../CHANGELOG.md). The active spec index in
`SPEC.md` keeps a phased rollup and the six most recent slices only.

---

- Feature: Evidence, parameters, and model-confidence ledger
  Status: Complete
  Started: 2026-07-03
  Version: 0.2.4

  Summary:
  Create the first parameter and evidence ledger for the Nursing Workforce & Retention mechanism (focused on nurse staffing ratios, recruitment delays/costs, and retention spend), and update the main evidence registry to link it.

  Done:
  - Create a detailed parameter/evidence ledger at `docs/workforce-ledger.md` mapping workforce-related parameters and formulas to literature citations (BLS, California AB 394 safe staffing, Aiken JAMA 2002 nurse burnout).
  - Assign confidence labels matching the project schema (`Empirically calibrated`, `Literature-grounded`, `Stylized abstraction`, `Gameplay-driven`).
  - Update `docs/evidence-registry.md` to reference and link `docs/workforce-ledger.md`.
  - Bump project version to `0.2.4` across tracking files.

  Deferred / Non-Goals:
  - No changes to simulation transition logic or parameter values in the codebase.
  - No database or telemetry changes.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`

- Feature: Exemplary scenario brief
  Status: Complete
  Started: 2026-07-03
  Version: 0.2.3

  Summary:
  Draft the first exemplary scenario brief for the competitive regional campaign (`docs/exemplary-scenario-brief.md`), modeling workforce conflicts, certificate of need legal challenges, Blue Shield payer negotiations, and delayed EHR consequences, accompanied by workspace handoff documents.

  Done:
  - Draft exemplary scenario brief covering financial pressure, nurse staffing ratios, payer rate negotiations, CON objections, and delayed consequences.
  - Complete workspace handoffs (Phase 0 input, Phase 1 evidence map, Phase 2 mechanism design, Phase 4 domain QA, and Phase 5 final handoff).
  - Set tab size of 2 spaces and run existing tests.

  Deferred / Non-Goals:
  - No changes to simulation rules, scenario parser, or TOML loader.
  - No changes to existing scenarios.

  Verification:
  - All unit and integration tests pass successfully (233 tests).

- Feature: Instructor-visible run summary & decision-quality review
  Status: Complete
  Started: 2026-07-03
  Version: 0.2.2

  Summary:
  Add an instructor-visible run summary and decision-quality review capability to the end-of-session debrief for both stabilization and competitive campaigns. The summary evaluates decisions made under uncertainty and lists the state/observation gap and unobserved rival moves.

  Done:
  - Add `instructor_run_summary` for stabilization to compare turn-by-turn reported access vs true access index and display measurement gaps.
  - Add `competitive_instructor_summary` to reveal all true rival actions and rationales, explicitly labeling observed vs unobserved rival actions at debrief time.
  - Centralize competitive debriefing in the `src/debrief/report.rs` module and clean up duplicates from MCP session logic.
  - Print the competitive debrief at the end of the competitive campaign loop in CLI mode.
  - Expose the instructor summaries in both CLI and MCP end-of-session debrief outputs.
  - Set tabsize to 2 spaces and keep the simulation core deterministic and untouched.

  Deferred / Non-Goals:
  - No changes to transition rules or state/observation calculations during active play.
  - No grading system or automated LMS scoring.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`

- Feature: Post-v0.2 SDD progress review
  Status: Complete
  Started: 2026-07-03
  Version: 0.2.1

  Summary:
  Review current project progress after the public playable prototype milestone
  and organize the next development queue without promoting a runtime feature
  into active work. The current state is a thoroughly runnable prototype: the
  stabilization campaign and bounded competitive preview are playable,
  documented, deterministic, tested, and supported by reproducible AI-agent
  playtest evidence.

  Done:
  - Keep `Present` empty so no implementation slice is implied before the next
    explicit decision.
  - Reframe `Future` as a ranked, gated queue that prioritizes debrief and
    instructor-analysis quality, exemplary scenario authoring, evidence and
    parameter confidence work, and only evidence-backed competitive hardening.
  - Refresh stale companion documentation that still pointed to already
    completed competitive runtime slices as next work.
  - Record a lesson for post-milestone SDD reviews.
  - Bump package version in `Cargo.toml`, `Cargo.lock`, and `CHANGELOG.md`.

  Deferred / Non-Goals:
  - No changes to transition rules, simulation physics, command syntax,
    scenario schemas, replay formats, MCP DTOs, gameplay balance, or public
    product positioning.
  - No promotion of a Future item into `Present`.
  - No claim of empirical calibration, measured human learning, classroom
    effectiveness, or policy-forecasting validity.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`
  - Targeted `rg` scan for stale competitive runtime and SDD status phrases`git status --short`

- Feature: Public playable prototype announcement prep
  Status: Complete
  Started: 2026-07-03
  Version: 0.2.0

  Summary:
  Prepare the repository for public announcement and portfolio presentation as a
  playable CLI prototype. Replace the developer-focused README with a
  public-facing project introduction, archive the old README under `docs/`,
  remove tracked generated bytecode, and bump the project version to `0.2.0`.

  Done:
  - Replace `README.md` with a player/portfolio-oriented overview covering the
    current playable campaigns, quickstart, competitive command examples,
    design commitments, limitations, documentation paths, and development
    checks.
  - Archive the previous README at `docs/README-dev-archive-v0.1.61.md`.
  - Update `.gitignore` to exclude Python bytecode caches and `.DS_Store`.
  - Set Cargo `default-run` to `hs-mgt-game` so the public quickstart command
    launches the main CLI despite the secondary MCP binary.
  - Remove the tracked generated file
    `scripts/__pycache__/play_game.cpython-314.pyc`.
  - Bump package version in `Cargo.toml`, `Cargo.lock`, and `CHANGELOG.md`.
  - Refresh `ARCHITECTURE.md` status language so it describes the project as a
    playable prototype while preserving the non-claim that it is not a
    production simulation or calibrated policy model.

  Deferred / Non-Goals:
  - No changes to transition rules, simulation physics, command syntax,
    scenario schemas, replay formats, MCP DTOs, or gameplay balance.
  - No GitHub release, tag, push, repository visibility change, crates.io
    publication, or public packaging automation.
  - No claim of empirical calibration, measured human learning, classroom
    effectiveness, or policy-forecasting validity.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`
  - `python3 scripts/run_automated_playtests.py`
  - `cargo run -- --help`
  - `test ! -e scripts/__pycache__/play_game.cpython-314.pyc`
  - `git status --short`


- Project concept established as a Rust, CLI-first health-policy strategy game
  about leading a fictional nonprofit US health system.
- Canonical proposal, roadmap, and design principles created under `docs/`.
- Repo-local agent harness created for project-specific health-policy simulation
  workflow.
- Rust package scaffold and spec-driven documentation baseline established.
- Feature: Deterministic vertical-slice spine
  Status: Complete
  Started: 2026-06-23
  Branch: feat/deterministic-slice-spine

  Summary:
  Replace the placeholder CLI with a small deterministic architecture proof: a
  scripted health-system turn with explicit resolved inputs, validation,
  actor-specific observation, one commercial-insurer decision rationale,
  attributed effects, append-only history, and replay verification.

  Done:
  - Placeholder `Hello, world!` CLI replaced by a scripted deterministic demo
  - Package version bumped to `0.1.2`
  - Single-file Rust prototype added with typed world state, ruleset, resolved
    inputs, player command, validation errors, observation, actor decision
    record, events, attributed effects, transition, and history
  - Pure transition path added for the scripted slice:
    `prior state + command + resolved inputs + ruleset -> transition`
  - Commercial-insurer decision added with accept, counter, and reject outcomes
    plus inspectable rationale text
  - Append-only demo history and replay function added
  - State fingerprint string added for deterministic demo inspection
  - Focused tests added for deterministic repeatability, true-state versus
    observed-state separation, validation failures, unfavorable valid outcomes,
    accepted-rate handling, negative capital-spend rejection, and replay
  - Repo-local handoff artifacts added under `_workspace/`
  - `ARCHITECTURE.md`, `CHANGELOG.md`, and `LESSONS.md` updated for the slice
  - PR handoff opened as GitHub PR #2, and three review passes completed
  - PR #2 merged into `main`

  Deferred / Non-Goals:
  - No full campaign or multiple-turn playable scenario
  - No interactive CLI input or command parser
  - No scenario, ruleset, or save-file loader
  - No external data ingestion or official parameter ledger
  - No empirical calibration, validation against real data, or policy
    forecasting claim
  - No cryptographic state hash or durable replay artifact format
  - No module split; prototype remains in `src/main.rs` until another command or
    actor interaction justifies boundaries
  - No CI, release automation, or expanded contributor process

  Verification:
  - Identical prior state, command, resolved inputs, and ruleset produce the
    same transition
  - Observed access can differ from true access through explicit resolved inputs
  - Invalid commands fail validation separately from unfavorable modeled outcomes
  - Replay from genesis reproduces the committed final state
  - `cargo fmt`, `cargo test`, and `cargo run` pass

- Feature: State policy response slice
  Status: Complete
  Started: 2026-06-23
  Branch: feat/state-policy-response-slice

  Summary:
  Extend the scripted deterministic demo from one payer negotiation into a
  two-turn history by adding one state-policy response command. The new command
  models a health system response to a state access mandate using explicit
  advocacy spend, access commitment, actor-specific observation, state-official
  decision rationale, attributed effects, and replay verification.

  Done:
  - Package version bumped to `0.1.3`
  - Added `RespondToStateAccessMandate` with validation for advocacy spend and
    access commitment
  - Added state policy decisions for flexibility, mandate continuation, and
    oversight escalation
  - Demo history now commits the existing capacity/payer turn followed by one
    state-policy response turn
  - Replay now verifies the final state of a two-transition history
  - Focused tests added for deterministic policy response, invalid advocacy
    spend, invalid access commitment, unfavorable valid policy outcome, and
    two-transition replay
  - Completed three code-reviewer passes and addressed findings
  - PR #3 merged into `main`

  Deferred / Non-Goals:
  - No interactive CLI input or command parser
  - No scenario, ruleset, or save-file loader
  - No external data ingestion or empirical calibration
  - No full policy lifecycle framework
  - No module split yet

  Verification:
  - Existing payer negotiation behavior remains intact
  - Invalid operations remain separate from unfavorable modeled outcomes
  - Two-transition replay reproduces the committed final state
  - `cargo fmt`, `cargo test`, and `cargo run` pass

- Feature: Educational debrief slice
  Status: Complete
  Started: 2026-06-23
  Branch: feat/educational-debrief-slice

  Summary:
  Add a concise end-of-run educational debrief to the scripted deterministic
  demo. The debrief should use the existing history, actor rationales, and
  attributed effects to explain tradeoffs, distinguish decisions from realized
  outcomes, and support replayable classroom discussion without adding
  interactive input or scenario loading.

  Done:
  - Working branch created from `main`
  - Stale state-policy response bookkeeping identified from merged PR #3
  - Implement deterministic debrief generation and CLI display
  - Add focused debrief tests
  - Bump package version to `0.1.4`
  - Update architecture, changelog, lessons, and handoff files
  - `cargo fmt`, `cargo test`, and `cargo run` pass
  - PR handoff opened as GitHub PR #4
  - Three code-reviewer passes completed; one low-severity documentation
    wording finding was fixed
  - Merge after review and verification

  Deferred / Non-Goals:
  - No interactive CLI input or command parser
  - No scenario, ruleset, or save-file loader
  - No empirical calibration or policy forecasting claim
  - No full campaign or general debrief framework
  - No module split unless implementation proves the current file cannot stay
    understandable

  Verification:
  - Debrief output includes actor rationales from the committed history
  - Debrief output includes at least one explicit tradeoff from attributed
    effects
  - Identical histories produce identical debrief text
  - Existing transition and replay tests remain passing

- Feature: Playable CLI slice
  Status: Complete
  Started: 2026-06-23
  Branch: feat/playable-cli-slice

  Summary:
  Add the first minimal playable CLI choice over the existing deterministic
  two-turn demo. The player chooses one of three hard-coded strategy paths,
  while transition logic, resolved inputs, actor observations, replay, and
  debrief generation remain deterministic and inspectable.

  Done:
  - Working branch created from `main`
  - Merged educational debrief slice moved from active state into completed
    history
  - Package version bumped to `0.1.5`
  - Add hard-coded strategy path selection for access stabilization, fiscal
    caution, and aggressive bargaining
  - Keep invalid CLI choice handling separate from valid unfavorable modeled
    outcomes
  - Add focused CLI choice and strategy-path tests
  - Run final verification commands
  - Update architecture, changelog, lessons, and handoff files
  - PR handoff opened as GitHub PR #5
  - Three code-reviewer passes completed; one low-severity handoff wording
    finding was fixed
  - PR #5 merged into `main`

  Deferred / Non-Goals:
  - No full campaign
  - No scenario or ruleset file format
  - No general command parser framework
  - No external data ingestion or calibration
  - No new dependency
  - No broad module split
  - No CI, release automation, or contributor-process expansion

  Verification:
  - Empty CLI input defaults to access stabilization
  - CLI choices `1`, `2`, and `3` each build a valid two-transition history
  - Invalid CLI choice returns an explicit CLI error
  - Each strategy path replays to its committed final state
  - Fiscal caution produces insurer accept and mandate continuation
  - Aggressive bargaining produces insurer rejection and oversight escalation
  - Existing transition, observation, replay, validation, and debrief tests
    remain passing

- Feature: Seeded stochastic input boundary
  Status: Complete
  Started: 2026-06-23
  Branch: feat/seeded-stochastic-inputs

  Summary:
  Replace per-path hard-coded `ResolvedInputs` with deterministic derivation
  from an explicit seed and named random streams before the transition core
  runs. Strategy paths remain command presets; stochasticity stays outside
  `transition()`.

  Done:
  - Working branch created from `main`
  - Playable CLI slice moved from active state into completed history
  - Package version bumped to `0.1.6`
  - Add seed-scoped input resolver with named streams
  - Extend CLI to accept optional seed
  - Add focused seed, resolver, and golden-trajectory tests
  - Update architecture, changelog, lessons, and handoff files
  - PR handoff opened as GitHub PR #6, and three review passes completed
  - PR #6 merged into `main`

  Deferred / Non-Goals:
  - No scenario or ruleset file format
  - No new Cargo dependency
  - No cryptographic state hash or durable replay artifact
  - No module split unless unavoidable
  - No interactive per-turn command entry
  - No CI or release automation

  Verification:
  - Identical seed and commands produce identical resolved inputs and history
  - Different seeds can change resolved inputs while commands stay fixed
  - Default seed reproduces access-stabilization golden trajectory
  - Invalid seed input returns explicit CLI error
  - `transition()` contains no RNG, time, or I/O
  - `cargo fmt`, `cargo test`, and `cargo run` pass

- Feature: Workforce pressure slice
  Status: Complete
  Started: 2026-06-23
  Branch: feat/workforce-pressure-slice

  Summary:
  Extend the seeded two-turn playable demo with a third turn modeling workforce
  pressure. Add a workforce response command, nursing workforce representative
  decision with inspectable rationale, three-transition replay, and debrief
  coverage while keeping stochasticity outside `transition()`.

  Done:
  - Working branch created from `main`
  - Seeded stochastic input boundary moved from active state into completed
    history
  - Package version bumped to `0.1.7`
  - Implement workforce response command and labor actor decision
  - Extend strategy paths with third compiled command presets
  - Add focused workforce, replay, and golden-trajectory tests
  - Update architecture, changelog, lessons, and handoff files
  - PR handoff opened as GitHub PR #7, and three review passes completed
  - PR #7 merged into `main`

  Deferred / Non-Goals:
  - No full campaign or per-turn interactive command entry
  - No scenario or ruleset file format
  - No module split unless unavoidable
  - No new Cargo dependency
  - No CI or release automation

  Verification:
  - Three-transition history replays from genesis
  - Labor actor rationale appears in committed history and debrief
  - Invalid workforce spend remains separate from unfavorable labor outcomes
  - `transition()` contains no RNG, time, or I/O
  - `cargo fmt`, `cargo test`, and `cargo run` pass

- Feature: Coalition cooperative interaction slice
  Status: Complete
  Started: 2026-06-23
  Branch: feat/coalition-cooperative-slice

  Summary:
  Extend the seeded three-turn playable demo with a fourth turn modeling a
  regional access coalition opportunity. Add a coalition response command,
  coalition liaison decision with inspectable rationale, four-transition replay,
  and debrief coverage while keeping stochasticity outside `transition()`.

  Done:
  - Working branch created from `main`
  - Workforce pressure slice moved from active state into completed history
  - Mechanism design and domain QA artifacts updated
  - Package version bumped to `0.1.8` then `0.1.9`
  - Implement coalition command and liaison actor decision
  - Extend strategy paths with fourth compiled command presets
  - Add focused coalition, replay, and golden-trajectory tests
  - Implement observation revision stream and debrief notes
  - Add `docs/system-boundary.md` and `docs/evidence-registry.md` stubs
  - Update architecture, changelog, lessons, and handoff files
  - PR #8 merged into `main`
  - `cargo fmt`, `cargo test`, and `cargo run` pass

  Deferred / Non-Goals:
  - No full campaign or per-turn interactive command entry
  - No scenario or ruleset file format
  - No Medicare/Medicaid/competitor actors
  - No module split unless unavoidable
  - No new Cargo dependency
  - No CI or release automation

  Verification:
  - Four-transition history replays from genesis
  - Coalition liaison rationale appears in committed history and debrief
  - Invalid coalition inputs remain separate from unfavorable coalition outcomes
  - Later-turn observation revisions appear in briefings and debrief without
    rewriting committed history
  - `transition()` contains no RNG, time, or I/O
  - `cargo fmt`, `cargo test`, and `cargo run` pass

- Feature: Phase 2 system boundary and ontology slice
  Status: Complete
  Started: 2026-06-24
  Branch: feat/phase2-system-boundary-ontology

  Summary:
  Expand the initial system-boundary and ontology documentation for the current
  fictional regional US market slice. The slice clarifies actors, authority,
  state and observation boundaries, command vocabulary, causal categories,
  exclusions, and evidence gaps without changing runtime behavior.

  Done:
  - Working branch created from `main`
  - Coalition cooperative interaction slice moved from active state into
    completed history
  - `docs/system-boundary.md` expanded from a stub into a Phase 2 conceptual
    boundary draft
  - `docs/evidence-registry.md` updated to align current mechanisms with the
    expanded boundary while preserving evidence gaps
  - Package version bumped to `0.1.10`
  - README status updated to `v0.1.10`
  - Changelog and lessons updated for the documentation slice
  - PR handoff opened as GitHub PR #9
  - PR #9 merged into `main`

  Deferred / Non-Goals:
  - No runtime behavior changes
  - No scenario loader, command parser, save format, or ruleset schema
  - No module split
  - No new dependency
  - No empirical calibration or authoritative policy forecast
  - No broad actor expansion beyond documenting future actor classes

  Verification:
  - `cargo fmt --check` passed
  - `cargo test` passed with 52 tests
  - Default `cargo run` preserved the existing four-turn demo behavior
  - Three local code-reviewer passes completed before PR handoff

- Feature: Phase 3 actor cards and first scenario brief
  Status: Complete
  Started: 2026-06-24
  Branch: feat/phase3-actor-cards-scenario-brief

  Summary:
  Add the first Phase 3 design artifacts that should constrain future runtime
  expansion: a reusable actor-card template and a first scenario brief for the
  current fictional regional US market stabilization slice. The slice preserves
  existing runtime behavior.

  Done:
  - Working branch created from `main`
  - `docs/actor-cards.md` added with required actor design fields for future
    strategic actors
  - `docs/first-scenario-brief.md` added with the first scenario concept,
    learning objectives, included interactions, strategic tensions, observation
    use, debrief hooks, and non-goals
  - `docs/system-boundary.md` and `docs/evidence-registry.md` updated to point
    to the new design artifacts without approving a runtime schema
  - Package version bumped to `0.1.11`
  - README status updated to `v0.1.11`
  - Architecture, changelog, lessons, and workspace handoff artifacts updated
  - PR handoff opened as GitHub PR #10
  - Three code-reviewer passes completed with no actionable findings
  - PR #10 merged into `main`

  Deferred / Non-Goals:
  - No runtime behavior changes
  - No new commands, actors, state fields, or random streams
  - No scenario loader, command parser, save format, or ruleset schema
  - No empirical calibration or authoritative policy forecast
  - No broad campaign or MVP scenario system

  Verification:
  - `cargo fmt --check` passed
  - `cargo test` passed with 52 tests
  - Default `cargo run` with strategy `1` and seed `42` preserves the existing
    four-turn demo behavior
  - Domain QA passed before PR handoff
  - Three local code-reviewer passes found no Critical, High, Medium, or Low
    issues

- Feature: State hash and replay proof
  Status: Complete
  Started: 2026-06-24
  Branch: feat/state-hash-replay-proof

  Summary:
  Replace the readable state fingerprint with a stable per-transition state
  hash over a canonical state record. Replay should verify each committed hash,
  detect hash drift, and preserve the existing four-turn deterministic demo
  without adding persistence, scenario loading, or cryptographic guarantees.

  Done:
  - Working branch created from `main`
  - Phase 3 actor-card and scenario brief slice moved into completed history
  - Package version bumped to `0.1.12`
  - Added canonical state record and stable 64-bit FNV-1a state hash helpers
  - Updated committed transitions to store `state_hash`
  - Updated replay to return verification and fail on committed hash mismatch
  - Updated CLI output from state fingerprints to state hashes
  - Added focused hash determinism, hash drift, and replay mismatch tests

  Deferred / Non-Goals:
  - No scenario loader, command parser, save format, or replay artifact export
  - No cryptographic hash dependency or security guarantee
  - No new commands, actors, metrics, random streams, or gameplay turns
  - No empirical calibration or authoritative policy forecast
  - No module split

  Verification:
  - `cargo fmt --check` passed
  - `cargo test` passed with 55 tests
  - Default `cargo run` with strategy `1` and seed `42` prints per-turn state
    hashes and replay success
  - Domain QA passed for the bounded hash/replay proof
  - PR handoff opened as GitHub PR #11
  - Three code-reviewer passes completed; one low-severity replay diagnostic
    finding was fixed
  - PR #11 merged into `main`

- Feature: CLI dashboard preview slice
  Status: Complete
  Started: 2026-06-24
  Branch: feat/cli-dashboard-preview-slice

  Summary:
  Add a starting executive dashboard and commitment previews for the three
  compiled strategy paths. The slice improves pre-run player context while
  preserving the existing four-turn deterministic demo, transition core,
  resolved-input boundary, actor decisions, replay hashes, and educational
  debrief.

  Done:
  - Working branch created from `main`
  - State hash and replay proof moved into completed history
  - Package version bumped to `0.1.13`
  - Added pure CLI dashboard and strategy-preview helpers
  - Wired the dashboard and previews into the pre-run CLI flow
  - Added focused dashboard and preview tests
  - PR handoff opened as GitHub PR #12
  - Three code-reviewer passes completed; one low-severity handoff/spec
    PR-state wording issue was fixed
  - PR #12 merged into `main`

  Deferred / Non-Goals:
  - No per-turn interactive command entry
  - No scenario loader, command parser, save format, or replay artifact export
  - No new commands, actors, metrics, random streams, or gameplay turns
  - No changes to transition logic, resolved input generation, actor decisions,
    or committed replay hash semantics
  - No empirical calibration or authoritative policy forecast
  - No module split

  Verification:
  - New tests cover starting dashboard content, all three strategy previews, and
    avoiding future actor-outcome leakage in previews
  - `cargo fmt --check` passed
  - `cargo test` passed with 58 tests
  - Default `cargo run` with strategy `1` and seed `42` prints the starting
    dashboard, strategy previews, per-turn state hashes, and replay success
  - Domain QA passed for the bounded CLI dashboard preview slice

- Feature: Per-turn interactive play slice
  Status: Complete
  Started: 2026-06-24
  Branch: feat/per-turn-interactive-slice

  Summary:
  Add per-turn interactive command entry as the default play mode while
  preserving preset strategy paths 1–3 for regression and quick play. Each turn
  shows an executive briefing, accepts command parameters within existing
  ruleset bounds, and prints a concise turn-resolution summary before replay and
  debrief.

  Done:
  - Working branch created from `main`
  - CLI dashboard preview slice moved into completed history
  - Package version bumped to `0.1.14`
  - Added play-mode selection with interactive default and preset paths 1–3
  - Added per-turn command parsers with access-stabilization defaults
  - Added `build_history_interactive`, executive turn briefings, and
    turn-resolution summaries
  - Added interactive CLI session loop separate from preset technical dump
  - Added focused interactive parsing, history, and briefing tests
  - Updated architecture, changelog, lessons, and workspace handoff artifacts
  - `cargo fmt --check`, `cargo test` (67 tests), and `cargo run` pass
  - Domain QA passed for the bounded interactive play slice
  - PR handoff opened as GitHub PR #13
  - PR #13 merged into `main`

  Deferred / Non-Goals:
  - No new commands, actors, metrics, or random streams
  - No per-turn strategic posture menus beyond numeric parameter entry
  - No scenario loader, save format, or replay artifact export
  - No changes to `transition()`, hash semantics, or debrief generation logic
  - No module split, CI workflow, or new dependencies
  - No competitor/Medicare/Medicaid actors
  - No empirical calibration or authoritative policy forecast

  Verification:
  - Interactive path completes four turns from `cargo run` with default commands
  - Preset paths 1–3 remain bit-identical to pre-slice behavior
  - `build_history_interactive` with default commands matches access-stabilization
    preset at seed `42`
  - Turn briefings use observation data only, not future actor outcomes
  - `cargo fmt --check`, `cargo test`, and `cargo run` pass

- Feature: Replay artifact export and playtest findings slice
  Status: Complete
  Started: 2026-06-24
  Branch: feat/replay-artifact-export

  Summary:
  Add a versioned deterministic replay artifact format with serialize,
  deserialize, and verify helpers plus optional post-run CLI export. Record
  internal playtest findings for the current four-turn vertical slice.

  Done:
  - Working branch created from `main`
  - Per-turn interactive play slice moved into completed history
  - Package version bumped to `0.1.15`
  - Added `replay-artifact-0.1.15` serialize, deserialize, and verify helpers
  - Added optional post-run replay export prompt (empty input skips export)
  - Added focused round-trip, corruption, golden-header, and play-mode tests
  - Ran preset and interactive playtest sessions at seed `42`
  - Added `docs/playtest-findings-v0.1.15.md`
  - Updated architecture, changelog, lessons, and workspace handoff artifacts
  - Domain QA passed for the bounded replay artifact slice
  - PR handoff opened as GitHub PR #14
  - Three code-reviewer passes completed; High findings fixed (TTY-gated export
    prompt, redundant ruleset check removed, event/effect count validation)
  - PR #14 merged into main

  Deferred / Non-Goals:
  - No new commands, actors, metrics, or random streams
  - No mid-run save/load or scenario file format
  - No cryptographic hash guarantees or new dependencies
  - No changes to `transition()` or committed replay hash semantics
  - No module split or CI workflow

  Verification:
  - Artifact from preset path `1` and seed `42` round-trips and replays with
    zero hash mismatches
  - Corrupt committed hash fails closed on verification
  - Default `cargo run` still skips export when the path prompt is empty
  - `cargo fmt --check`, `cargo test`, and `cargo run` pass

- Feature: Module boundary refactor
  Status: Complete
  Started: 2026-06-24
  Branch: refactor/module-scaffold

  Summary:
  Split the 4,436-line monolithic `src/main.rs` into library modules aligned
  with `ARCHITECTURE.md` boundaries while preserving all gameplay behavior.

  Done:
  - Added `src/lib.rs` with `model`, `inputs`, `sim`, `actors`, `replay`,
    `artifact`, `debrief`, and `cli` modules
  - Reduced `main.rs` entry point to `cli::run()`
  - Largest implementation files now under ~650 lines (`artifact/parse.rs`,
    `sim/transition.rs`)
  - Package version bumped to `0.1.16`
  - Updated `ARCHITECTURE.md` and `CHANGELOG.md`
  - PR #15 merged into main

  Deferred / Non-Goals:
  - No workspace crate split
  - No new gameplay, actors, or dependencies
  - No scenario loader or CI workflow

  Verification:
  - `cargo fmt --check`, `cargo test`, and `cargo run` smoke pass
  - Golden seed-42 preset and interactive trajectories unchanged

- Feature: Test colocation slice (R8)
  Status: Complete
  Started: 2026-06-24
  Branch: refactor/module-scaffold

  Summary:
  Move characterization tests from `main.rs` into module-local `#[cfg(test)]`
  blocks and add a crate-root golden integration test for seed-42 trajectories.

  Done:
  - 77 unit tests colocated across `sim`, `replay`, `model`, `inputs`,
    `debrief`, `cli`, and `artifact` modules
  - `tests/golden_seed42.rs` integration test for canonical demo trajectory
  - `src/test_support.rs` shared helpers for cross-module test fixtures
  - `main.rs` reduced to thin entry point only
  - Package version bumped to `0.1.17`
  - PR #15 merged into main

  Verification:
  - `cargo test`: 77 lib unit tests + 1 integration test (78 total)
  - Golden final state hash `bce02dff9b4b4ac6` unchanged at seed 42

- Feature: Phase 0 CI baseline
  Status: Complete
  Started: 2026-06-24
  Branch: feat/phase0-ci-baseline

  Summary:
  Add GitHub Actions CI running `cargo fmt --check` and `cargo test` on pushes
  to `main` and on pull requests. Document local verification commands in the
  README.

  Done:
  - Working branch created from `main`
  - Added `.github/workflows/ci.yml` with formatting and test jobs
  - Updated README contributing section with local CI commands
  - Bumped package version to `0.1.18`
  - Updated `CHANGELOG.md`

  Deferred / Non-Goals:
  - No clippy policy or release automation
  - No workspace crate split or new gameplay behavior
  - No contributor guide beyond README CI notes

  Verification:
  - `cargo fmt --check` passes locally
  - `cargo test` passes locally (78 tests)

- Feature: Phase 5 scope and risk register
  Status: Complete
  Started: 2026-06-24
  Branch: feat/phase5-scope-register

  Summary:
  Close Phase 5 documentation by adding a revised scope and risk register,
  refreshed internal playtest findings for the post-refactor v0.1.19 codebase,
  and updated project state files. No runtime behavior changes.

  Done:
  - Working branch created from `main`
  - `docs/phase5-scope-register.md` added with achieved, deferred, risk, and
    exit-criteria assessment
  - `docs/playtest-findings-v0.1.19.md` added for post-refactor and CI state
  - `_workspace/final/handoff.md` and `_workspace/03_domain_qa.md` updated
  - Package version bumped to `0.1.19`
  - README, CHANGELOG, and evidence-registry cross-links updated
  - PR handoff opened as GitHub PR #17
  - Three code-reviewer passes completed; Medium findings fixed

  Deferred / Non-Goals:
  - No runtime behavior changes
  - No new commands, actors, metrics, or random streams
  - No scenario loader, parameter ledger, or empirical calibration
  - No competitor, Medicare, or Medicaid runtime implementation in this slice

  Verification:
  - `cargo fmt --check` passes
  - `cargo test` passes (78 tests)
  - Golden final state hash `bce02dff9b4b4ac6` unchanged at seed 42
  - Domain QA pass for scope register wording

- Feature: Phase 1 research-to-design implications memo
  Status: Complete
  Started: 2026-06-24
  Branch: feat/phase1-implications-memo

  Summary:
  Convert Phase 1 literature research into actionable design implications and
  add an initial parameter-source ledger without changing runtime behavior.

  Done:
  - Working branch created from `main`
  - SPEC Present section bookkeeping restored after Phase 5 closure
  - Added `docs/phase1-implications-memo.md`
  - Expanded `docs/evidence-registry.md` with parameter-source ledger
  - Package version bumped to `0.1.20`
  - README, CHANGELOG, and workspace handoff artifacts updated
  - `cargo fmt --check` and `cargo test` pass (golden hash unchanged)

  Deferred / Non-Goals:
  - No runtime behavior changes
  - No empirical calibration or numeric threshold replacement
  - No competitor actor implementation in this slice

  Verification:
  - Golden final state hash `bce02dff9b4b4ac6` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass

  - `cargo fmt --check`, `cargo test` pass

- Feature: Competitor capacity slice
  Status: Complete
  Started: 2026-06-24
  Branch: feat/competitor-capacity-slice

  Summary:
  Add a fifth turn modeling rival health system capacity competition with
  defensive player command, competitor actor decision, replay, debrief, and
  preset path extensions while preserving turns 1–4 behavior.

  Done:
  - Competitor actor card and mechanism design artifacts
  - `RespondToCompetitorCapacityMove` command and validation
  - Competitor actor with accelerate, hold, and partial retreat outcomes
  - `competitor_market_signal` stream active on turn 5 only
  - Extended interactive and preset paths to five turns
  - Golden hash updated; turn 4 hash unchanged at seed 42
  - Package version bumped to `0.1.21`
  - Playtest findings, system boundary, and scenario brief updated

  Deferred / Non-Goals:
  - No Medicare/Medicaid actors
  - No scenario loader or mid-run save
  - No market-entry relocation modeling

  Verification:
  - Five-transition replay from genesis
  - Turns 1–4 resolved inputs and turn 4 hash unchanged at seed 42
  - `cargo fmt --check`, `cargo test` (82 tests) pass

- Feature: Phase 0 governance docs
  Status: Complete
  Started: 2026-06-24
  Branch: feat/phase0-governance-docs

  Summary:
  Add glossary, architecture decision record conventions, and versioning policy
  for Phase 0 repository governance without changing runtime behavior.

  Done:
  - Added `docs/glossary.md`
  - Added `docs/decision-records/README.md` and `0000-template.md`
  - Added `docs/versioning-policy.md`
  - Package version bumped to `0.1.22`
  - README and CHANGELOG updated

  Deferred / Non-Goals:
  - No runtime behavior changes
  - No clippy policy or release automation
  - No first accepted ADR beyond template

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass

- Feature: SPEC reconciliation and Phase 5 register refresh
  Status: Complete
  Started: 2026-06-24
  Branch: feat/spec-doc-reconciliation

  Summary:
  Sync SPEC Future backlog and refresh stale Phase 5, system-boundary, and
  evidence-registry docs for five-turn v0.1.21+ state without runtime changes.

  Done:
  - Working branch created from `main`
  - `docs/phase5-scope-register.md` refreshed for five-turn closure and
    competitor achieved
  - `docs/system-boundary.md` updated with `RespondToCompetitorCapacityMove` and
    rival capacity inclusion
  - `docs/evidence-registry.md` updated for five-turn wording and competitor
    ledger `linked` status
  - `docs/playtest-findings-v0.1.21.md` next-slice note marked superseded
  - SPEC `Future` backlog expanded with prioritized roadmap-aligned items
  - Package version bumped to `0.1.23`
  - README, CHANGELOG, and workspace handoff updated

  Deferred / Non-Goals:
  - No runtime changes
  - No Medicare/Medicaid actors
  - No scenario loader

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (82 tests)

- Feature: First architecture decision record and scenario format draft
  Status: Complete
  Started: 2026-06-24
  Branch: feat/adr-deterministic-boundary

  Summary:
  Record the implemented deterministic transition and stochastic input boundary
  as ADR 0001 and add a Phase 6.2 scenario format design draft without runtime
  changes.

  Done:
  - Added `docs/decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md`
  - Added `docs/scenario-format-draft.md`
  - Updated `ARCHITECTURE.md` open decisions and stream/actor proof sections
  - Updated decision-records README with accepted ADR link
  - Package version bumped to `0.1.24`
  - README, CHANGELOG, and SPEC updated

  Deferred / Non-Goals:
  - No runtime changes
  - No scenario loader implementation

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass

- Feature: Forecast and uncertainty CLI preview
  Status: Complete
  Started: 2026-06-24
  Branch: feat/forecast-uncertainty-preview

  Summary:
  Add bounded observation-only uncertainty preview before each interactive turn
  and an observation note on the starting dashboard without changing transition
  logic or golden trajectories.

  Done:
  - Added `src/cli/display/forecast.rs` with turn uncertainty preview helper
  - Wired preview into interactive session before executive briefings
  - Added observation uncertainty note to starting executive dashboard
  - Added focused forecast preview tests
  - Updated phase5 scope register forecast row to mostly achieved
  - Added `docs/playtest-findings-v0.1.25.md`
  - Package version bumped to `0.1.25`
  - README, CHANGELOG, SPEC, and workspace artifacts updated

  Deferred / Non-Goals:
  - No probabilistic forecast objects
  - No changes to `transition()`, hash semantics, or random streams
  - No preset path output changes beyond dashboard note

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (86 tests)
  - Interactive mode shows uncertainty preview before turn 1 briefing

- Feature: CLI session UX (quit, autosave, guidance, beginner mode)
  Status: Complete
  Started: 2026-06-24
  Branch: feat/cli-session-ux

  Summary:
  Add global quit/help, interactive autosave and resume, new-player cues, and
  beginner-mode multiple-choice turns without changing the simulation core.

  Done:
  - Global input routing (`src/cli/input.rs`) with quit/help at all prompts
  - Session save format `session-save-0.1.27` and persistence (`src/cli/persistence.rs`)
  - Resume/start-over startup flow; autosave on interactive quit; clear on completion
  - Contextual guidance and one-time new-player block (`src/cli/guidance.rs`)
  - Beginner mode per-turn options from preset strategy paths (`src/cli/beginner.rs`)
  - ADR-0002, package version `0.1.27`, focused unit tests

  Deferred / Non-Goals:
  - No autosave on every turn or for preset paths
  - No multi-slot save library or encrypted saves
  - No changes to `transition()`, golden hash, or replay artifact format

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (114 tests)

- Feature: Competitive gameplay design package
  Status: Complete
  Started: 2026-06-24
  Branch: feat/competitive-gameplay-design

  Summary:
  Fully develop the competitive gameplay sketch into durable design artifacts and
  sync SDD/canonical docs for a parallel regional-market campaign (1 human + K AI
  health systems) without changing stabilization demo runtime behavior.

  Done:
  - `_workspace/00_input/request-summary.md` framed scope and non-goals
  - `_workspace/01_evidence_map.md` updated for competitive precedents
  - `_workspace/02_mechanism_design.md` rewritten for competitive campaign
  - `docs/gameplay-competitive-sketch.md` with acceptance criteria per sketch bullet
  - `docs/core-loop-spec.md` (Phase 3 deliverable) for both campaigns
  - `docs/competitive-scenario-brief.md`, `docs/executive-report-format.md`,
    `docs/action-catalog-draft.md`, `docs/cli-command-grammar-draft.md`
  - ADRs 0003–0006 accepted in `docs/decision-records/`
  - Canonical docs updated: proposal, roadmap §6.0, system-boundary, scenario
    format, actor-cards, glossary, LESSONS, phase registers, evidence-registry
  - `ARCHITECTURE.md` competitive modules documented (Needs Review until runtime)
  - Domain QA pass; three code-reviewer passes on doc diff
  - Package version bumped to `0.1.28`

  Deferred / Non-Goals:
  - Runtime implementation slices I1–I8 (tracked in Future)
  - Refactoring stabilization demo into competitive mode
  - Medicare/Medicaid actors in competitive v1
  - Classroom hot-seat multiplayer (Phase 9)
  - Empirical calibration and global equilibrium AI

  Verification:
  - All new design docs exist and cross-link consistently
  - Domain QA pass in `_workspace/03_domain_qa.md`
  - `cargo fmt --check`, `cargo test` pass with golden hash unchanged

- Feature: Competitive campaign runtime I1+I2
  Status: Complete
  Started: 2026-06-24
  Branch: feat/campaign-router-executive-report

  Summary:
  Add CLI campaign router (`stabilization-v1` vs `competitive-regional-v1` preview)
  and monthly executive report renderer using observation-only mock fixtures.
  Stabilization demo behavior unchanged.

  Done:
  - `CampaignId`, `Difficulty`, `PolicyCalendar`, `PlayerObservation` in
    `src/model/campaign.rs`
  - CLI campaign and difficulty selectors in `src/cli/campaign.rs` and `src/cli/io.rs`
  - Executive report renderer in `src/cli/display/executive_report.rs`
  - Mock fixtures in `src/competitive/fixtures.rs`
  - `SessionOutcome::CompetitivePreview` for stub exit
  - Focused unit tests for campaign parsing, calendar, report sections, stub flow
  - Package version bumped to `0.1.29`

  Not Yet Done:
  - Full competitive play (I3–I8): AP economy, multi-system state, simultaneous
    resolver, AI players, events, Stata CLI

  Deferred / Non-Goals:
  - No `transition_competitive()` or changes to stabilization `transition()`
  - No scenario file loader
  - No Medicare/Medicaid actors
  - Session autosave remains stabilization-only

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (130 tests)
  - Empty campaign input defaults to stabilization
  - Competitive path shows six-section month-1 executive report then stub message

- Feature: Competitive campaign runtime I3
  Status: Complete
  Started: 2026-06-24
  Branch: feat/competitive-action-economy

  Summary:
  Add competitive command types, action-cost catalog, and batch validation for
  AP, cash, and political capital per ADR-0005. Extend executive report and
  competitive stub with validation demo presets. Stabilization unchanged.

  Done:
  - `CompetitiveCommand`, `ActionCost`, and verb argument enums in
    `src/model/competitive_command.rs`
  - `PlayerResources`, `CompetitiveRuleset`, `CompetitiveValidationError` in
    `src/model/resources.rs`
  - `validate_competitive_batch` / `validate_competitive_command` in
    `src/sim/validate_competitive.rs`
  - Executive report shows AP and political capital remaining
  - Five preset validation demos in `src/competitive/mod.rs`
  - Competitive stub validation demo loop after month-1 report
  - Focused unit tests for catalog costs, batch validation, report header
  - Package version bumped to `0.1.30`

  Not Yet Done:
  - Full competitive play (I4–I8): multi-system state, simultaneous resolver,
    AI players, events, Stata CLI

  Deferred / Non-Goals:
  - No `transition_competitive()` or changes to stabilization `transition()`
  - No scenario file loader
  - No Medicare/Medicaid actors
  - Session autosave remains stabilization-only
  - No Stata-like command parser (I8)

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (148 tests)
  - Competitive demos 1–5 exercise pass/fail validation paths

- Feature: Competitive campaign runtime I4
  Status: Complete
  Version: 0.1.31

  Summary:
  Add `CompetitiveWorldState` with K+1 `HealthSystemState` entities, player
  slots, and difficulty-scoped genesis fixtures per ADR-0004.

  Done:
  - `CompetitiveWorldState`, shared market fields, health-system state, player
    slots, and AI profiles added under `src/model/competitive_world.rs`
  - Genesis fixtures and roster display added for competitive preview
  - Executive observation derives human metrics from competitive genesis
  - Package version bumped to `0.1.31`

  Deferred / Non-Goals:
  - No `transition_competitive()` or monthly loop
  - No stabilization golden hash changes

  Verification:
  - Difficulty tiers create K+1 systems with the human at system 0
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (154 tests)

- Feature: Competitive campaign runtime I5
  Status: Complete
  Version: 0.1.32

  Summary:
  Add simultaneous monthly action resolver, `transition_competitive()`, partial
  rival observability, and a one-month resolution CLI demo per ADR-0003.

  Done:
  - Monthly batch and competitive history types added
  - `resolve_monthly_batches`, `transition_competitive()`, and human
    observation helpers added
  - CLI month-1 resolution demo and month-2 executive report preview added
  - Package version bumped to `0.1.32`

  Deferred / Non-Goals:
  - AI players, events/delays, and Stata CLI remained deferred to I6-I8
  - Full 24-month campaign loop, competitive replay artifact, and competitive
    autosave remained deferred

  Verification:
  - Permutation-invariance test covers batch collection order
  - Stabilization golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (173 tests)

- Feature: Competitive campaign runtime I6
  Status: Complete
  Version: 0.1.33

  Summary:
  Add deterministic AI rival batch generation with style-weighted command
  scoring, lagged-public-log response, and inspectable rationale strings.

  Done:
  - AI batch planner APIs added for competitive month resolution
  - AI rationale strings persisted on monthly batches
  - Competitive month-1 resolver switched from fixed rival presets to
    AI-generated batches
  - Package version bumped to `0.1.33`

  Deferred / Non-Goals:
  - Events/delays/annual tick and Stata CLI remained deferred to follow-on
    slices
  - Full 24-month campaign loop, competitive replay artifact, and competitive
    autosave remained deferred

  Verification:
  - AI reproducibility and rationale tests pass
  - Stabilization seed-42 golden hash unchanged at `6fb1ebbea564274f`
  - `cargo fmt --check`, `cargo test` pass

- Feature: Competitive campaign runtime I7
  Status: Complete
  Version: 0.1.34

  Summary:
  Add competitive monthly events, delayed effects, annual policy inputs, and a
  simplified institution phase.

  Done:
  - `CompetitiveResolvedInputs` and competitive input resolver added
  - Pending-effect queue and month-start tick added
  - Payer/state institution phase and multi-month resolution history added
  - Package version bumped to `0.1.34`

  Deferred / Non-Goals:
  - Stata-like CLI remained deferred to I8
  - Full 24-month campaign, autosave, and replay export remained deferred

  Verification:
  - Competitive seed-42 golden hash `88d07f9e1bbd6f04`
  - Stabilization golden seed-42 hash unchanged at `6fb1ebbea564274f`
  - `cargo fmt --check`, `cargo test` pass

- Feature: Competitive campaign runtime I8
  Status: Complete
  Version: 0.1.35

  Summary:
  Add Stata-like competitive command parsing and interactive human monthly batch
  entry for the preview campaign.

  Done:
  - `src/cli/competitive_parse.rs` added for MVP `verb arg=value` syntax
  - TTY interactive monthly batch entry wired to competitive month resolution
  - Non-TTY preset fallback preserved for CI and tests
  - Package version bumped to `0.1.35`

  Deferred / Non-Goals:
  - Full 24-month interactive loop, competitive autosave, syntax highlighting,
    and autocomplete

  Verification:
  - Parser and competitive command-entry tests pass
  - Golden hashes remain stable except for documented competitive changes

- Feature: Competitive bounded multi-month loop
  Status: Complete
  Version: 0.1.36

  Summary:
  Extend the competitive preview into a coherent three-month loop over one
  evolving `CompetitiveWorldState`.

  Done:
  - Per-month executive reports precede human command entry
  - TTY mode accepts Stata-like batches each month
  - Non-TTY mode uses deterministic fallback batches for CI/tests
  - Package version bumped to `0.1.36`

  Deferred / Non-Goals:
  - Full 24-month campaign loop, competitive autosave, replay artifact export,
    and scenario loading

  Verification:
  - Focused tests cover three-month non-TTY progression and fallback batch
    policy
  - `cargo fmt --check`, `cargo test` pass (193 tests)

- Feature: Competitive command prompt ergonomics
  Status: Complete
  Version: 0.1.37

  Summary:
  Improve competitive command-entry help, token styling, and verb-only Tab
  autocomplete.

  Done:
  - Shared competitive command catalog metadata feeds parser help and REPL
    completion
  - Competitive help context lists available commands for `help` and `?`
  - Colored command and argument token rendering added
  - Verb-only Tab autocomplete added for TTY command entry
  - Package version bumped to `0.1.37`

  Deferred / Non-Goals:
  - Argument-key and enum-value autocomplete
  - Full 24-month campaign loop, competitive autosave, replay artifact export,
    and scenario loading

  Verification:
  - Parser, style, guidance, and REPL completion tests pass
  - `cargo fmt --check`, `cargo test` pass (201 tests)

- Feature: New-player How to Play manual
  Status: Complete
  Version: 0.1.38

  Summary:
  Add a player-facing manual for current stabilization and competitive-preview
  flows.

  Done:
  - `docs/how-to-play.md` added with quickstart, campaign flow, terminology,
    commands, worked example, and difficulty recovery tips
  - README documentation index updated
  - Package version bumped to `0.1.38`

  Deferred / Non-Goals:
  - No runtime behavior changes
  - No full 24-month competitive campaign
  - No scenario loading

  Verification:
  - `cargo fmt --check`, `cargo test` pass

- Feature: External playtest protocol refresh
  Status: Complete
  Version: 0.1.39

  Summary:
  Add a Phase 7 prep protocol for informal external playtests of the current
  stabilization and competitive-preview CLI flows.

  Done:
  - `docs/external-playtest-protocol.md` added with setup, session scripts,
    observation rubric, post-session prompts, note template, privacy cautions,
    and synthesis guidance
  - README documentation index and current-priority wording updated
  - Package version bumped to `0.1.39`

  Deferred / Non-Goals:
  - No runtime behavior changes
  - No scenario loader, 24-month competitive campaign, or new strategic actors
  - No formal human-subjects research process or policy-forecasting claim

  Verification:
  - `cargo fmt --check`, `cargo test` pass

- Feature: Minimal stabilization scenario loader
  Status: Complete
  Branch: feat/minimal-scenario-loader
  Version: 0.1.40

  Summary:
  Add a narrow TOML runtime scenario boundary for the existing five-turn
  `stabilization-v1` flow.

  Done:
  - ADR-0007 accepts `scenario-toml-0.1.40` for stabilization only
  - `scenarios/stabilization-v1.toml` records current genesis state, learning
    objectives, actor stubs, and fixed five-turn schedule
  - `src/scenario/` parses and validates the bundled scenario before fresh
    stabilization runs
  - Package version bumped to `0.1.40`

  Deferred / Non-Goals:
  - No competitive scenario loading
  - No arbitrary scenario path CLI option
  - No scenario migration tooling or schema generation
  - No transition, replay artifact, or session-save format changes

  Verification:
  - Scenario tests cover valid fixture, malformed TOML, ruleset mismatch,
    unsupported campaign, unsupported turn unit, missing actor stub, and current
    turn schedule
  - Stabilization seed-42 golden hash unchanged at `6fb1ebbea564274f`
  - Competitive seed-42 golden hash unchanged at `88d07f9e1bbd6f04`
  - `cargo fmt --check`, `cargo test` pass

- Feature: MCP agent support
  Status: Complete
  Branch: feat/mcp-agent-support
  Version: 0.1.41

  Summary:
  Add a local stdio MCP server so AI agents can play the current bounded
  `stabilization-v1` and `competitive-regional-v1` campaign sessions through
  structured tools.

  Done:
  - `src/bin/hs-mgt-game-mcp.rs` starts the stdio MCP server
  - `src/mcp/` exposes in-memory sessions, actor-visible observations,
    `submit_turn`, append-only history summaries, and end-session debriefs
  - MCP layer reuses existing scenario validation, command parsers,
    observations, validation, transition, and competitive month resolution
  - ADR-0008 and `docs/mcp-agent-interface.md`
  - Package version bumped to `0.1.41`

  Deferred / Non-Goals:
  - No Streamable HTTP transport, auth, persistence, or multi-client session
    coordination
  - No 24-month competitive campaign, competitive replay artifact, or scenario
    loading expansion
  - No transition, replay artifact, or session-save format changes

  Verification:
  - MCP session tests cover both campaigns, invalid-command non-advancement,
    bounded completion, and same-seed hash determinism
  - Stabilization seed-42 golden hash unchanged at `6fb1ebbea564274f`
  - Competitive seed-42 golden hash unchanged at `88d07f9e1bbd6f04`
  - `cargo check --bin hs-mgt-game-mcp`, `cargo test`, and `cargo fmt --check`
    pass

- Feature: CLI arbitrary scenario path selection
  Status: Complete
  Started: 2026-06-27
  Branch: feat/cli-scenario-loading
  Version: 0.1.42

  Summary:
  Add CLI support for `--scenario <PATH>` / `-s <PATH>` flags to load and play
  arbitrary scenario TOML files, bypassing campaign selection and resume prompts
  when a custom scenario is loaded.

  Done:
  - Parse CLI arguments in `src/main.rs`
  - Update `run()`, `read_stabilization_run_config()`, and `read_stabilization_run_setup()` in `src/cli/session.rs`
  - Add integration tests in `tests/scenario_selection_tests.rs`
  - Package version bumped to `0.1.42`

  Deferred / Non-Goals:
  - No competitive scenario loading from TOML (remains deferred)
  - No changes to transition logic, state hashes, or session save format

  Verification:
  - Golden hashes (`6fb1ebbea564274f` and `88d07f9e1bbd6f04`) are unchanged
  - All 219 tests pass successfully

- Feature: Automated MCP playtest findings
  Status: Complete
  Started: 2026-06-28
  Version: 0.1.43

  Summary:
  Run automated MCP sessions across stabilization and competitive-preview
  campaigns and record findings for strategy diversity, winnability, tension,
  and entertainment value.

  Done:
  - `docs/playtest-findings-v0.1.42.md` summarizes three strategy runs across
    both current campaigns
  - `scripts/play_game.py` and `scripts/run_automated_playtests.py` support
    bounded MCP playtest sessions
  - Package version bumped to `0.1.43`

  Deferred / Non-Goals:
  - No transition, scenario, MCP tool-contract, or campaign-length changes
  - No claim of external validation or empirical calibration

  Verification:
  - Automated MCP sessions completed for fiscal, growth, and balanced strategies
  - `cargo fmt --check` and `cargo test` pass

- Feature: Playtest-guided player guidance
  Status: Complete
  Started: 2026-06-29
  Branch: feat/playtest-guidance-fixes
  Version: 0.1.44

  Summary:
  Clarify player-facing guidance for commercial payer leverage and competitive
  recruitment timing based on the v0.1.42 automated playtest findings.

  Done:
  - Stabilization Turn 1 help explains that above-target commercial rate bids
    need visible leverage from reported access, capacity, or quality context
  - Beginner-mode Turn 1 option copy surfaces payer-leverage risk without
    exposing exact outcomes
  - Competitive observation and MCP debrief text explain that recruitment spends
    cash immediately, resolves after role-specific delays, and can strain
    workforce trust
  - `docs/how-to-play.md` records the same player-facing strategy notes
  - Package version bumped to `0.1.44`

  Deferred / Non-Goals:
  - No changes to transition logic, validation thresholds, scenario files, MCP
    DTO schemas, replay artifacts, or golden hashes
  - No competitive campaign length expansion or competitive scenario loading

  Verification:
  - `cargo fmt --check` and `cargo test </dev/null>` pass

- Feature: SDD next-development cleanup
  Status: Complete
  Started: 2026-06-30
  Version: 0.1.45

  Summary:
  Refresh the spec-driven-development index so the next development tracks are
  specific, gated, and verification-oriented while companion docs reflect the
  current bounded competitive preview, scenario-loader, and MCP interface state.

  Done:
  - `SPEC.md` Future now names actionable next slices with gates,
    verification targets, and deferred work
  - README status text summarizes current capabilities without repeating the
    full release history
  - Architecture, core-loop, roadmap, system-boundary, competitive-sketch, and
    CLI grammar docs no longer describe completed competitive runtime slices as
    only planned or design-only
  - Package version bumped to `0.1.45`

  Deferred / Non-Goals:
  - No runtime behavior, scenario files, schemas, replay artifacts, golden
    hashes, MCP DTOs, or test expectations changed
  - No active Future slice was promoted into `Present`

  Verification:
  - `cargo fmt --check` and `cargo test` pass
  - Stale status scan leaves only historical release/archive references

- Feature: Deferred item triage
  Status: Complete
  Started: 2026-06-30
  Version: 0.1.46

  Summary:
  Review deferred items from completed Past records and archived slice history,
  then preserve still-worthy follow-up work in Future without carrying forward
  items that are complete, obsolete, or permanent non-goals.

  Done:
  - Future tracks now explicitly cover evidence and parameter-ledger work,
    instructor analysis and replay/export capabilities, competitive command
    ergonomics, and broader simulation breadth gates
  - Completed deferred items such as per-turn command entry, module split,
    CI baseline, replay artifact export, and competitive runtime I1-I8 were not
    re-added as Future work
  - Package version bumped to `0.1.46`

  Deferred / Non-Goals:
  - No runtime behavior, scenario schemas, rulesets, replay artifacts, MCP DTOs,
    or golden hashes changed
  - No Future track was promoted into `Present`

  Verification:
  - Deferred-item scan reviewed `SPEC.md` and `docs/spec-past-archive.md`
  - `cargo fmt --check` and markdown whitespace checks pass

- Feature: AI-agent playtest validation pivot
  Status: Complete
  Started: 2026-06-30
  Version: 0.1.47

  Summary:
  Replace planned external human playtest recruitment with AI-agent and
  sub-agent playtests as the active Phase 7 validation path.

  Done:
  - Added `docs/agent-playtest-protocol.md` with required MCP evidence,
    profile matrix, rubric, synthesis template, and evidence limits
  - Added ADR-0009 accepting AI-agent playtests as the active validation path
  - Superseded the external human playtest protocol in active planning language
  - Package version bumped to `0.1.47`

  Deferred / Non-Goals:
  - No runtime behavior, scenario schemas, rulesets, replay artifacts, MCP DTOs,
    or golden hashes changed
  - No claim of measured human learning, empirical calibration, or policy
    forecasting validity from agent runs

  Verification:
  - MCP one-turn smoke test, Rust checks, markdown diff checks,
    stale-language scans, and domain QA completed for the docs-only pivot
  - Full `scripts/run_automated_playtests.py` was attempted twice and hung on
    the first stabilization batch `submit_turn`; script debugging remains
    outside this docs-only slice

- Feature: Feedback-aligned future planning
  Status: Complete
  Started: 2026-06-30
  Version: 0.1.48

  Summary:
  Review external project feedback and translate it into docs-only future plans
  that prioritize gameplay validation, strategy-space diagnostics, debrief
  quality, one exemplary scenario, and model-confidence annotations before
  broad new architecture.

  Done:
  - Future tracks now foreground falsifiable gameplay hypotheses, diagnostic
    evidence, debrief QA, canonical scenario quality, evidence/confidence
    labeling, and abstraction-freeze gates
  - Agent-playtest protocol now asks findings to test explicit gameplay
    validity hypotheses and strategy-space diagnostics when relevant
  - Roadmap and architecture planning language now makes validation evidence the
    gate for broader scenario tooling, calibration, and platform expansion
  - Package version bumped to `0.1.48`

  Deferred / Non-Goals:
  - No runtime behavior, scenario schemas, rulesets, replay artifacts, MCP DTOs,
    golden hashes, or transition semantics changed
  - No strategy-space diagnostic implementation, new scenario loader,
    calibration pass, human learning claim, or policy-forecasting claim

  Verification:
  - Rust checks, markdown diff checks, stale-claim scan, and domain QA completed
    for the docs-only planning refresh

- Feature: AI-agent playtest evidence
  Status: Complete
  Started: 2026-06-30
  Version: 0.1.49

  Summary:
  Fix the automated MCP playtest harness enough to complete the active Phase 7
  default scripted-policy batch, then record versioned findings for the current
  stabilization and competitive preview campaigns.

  Done:
  - Automated playtest policies now keep stabilization command selection on the
    stabilization legal-command surface after Turn 1
  - MCP Python client now launches the built stdio server by default, uses
    byte-level response reads, and reports scripted validation failures instead
    of looping silently
  - `docs/playtest-findings-v0.1.49.md` records six completed seed-42 sessions,
    gameplay-hypothesis results, rubric scores, evidence limits, and prioritized
    follow-up
  - Package version bumped to `0.1.49`

  Deferred / Non-Goals:
  - No runtime transition behavior, rulesets, scenario schemas, replay formats,
    MCP DTO shapes, campaign length, golden hashes, or gameplay formulas changed
  - No human learning claim, empirical calibration claim, policy forecast claim,
    balance tuning, or broad diagnostics platform

  Verification:
  - Automated MCP playtest batch completed for three profiles across both
    current campaigns
  - Rust checks and diff checks completed for the harness and docs slice

- Feature: Competitive final debrief metrics
  Status: Complete
  Started: 2026-07-01
  Version: 0.1.50

  Summary:
  Close the v0.1.49 competitive evidence gap by adding bounded final player
  tradeoff and resource metrics to the competitive MCP `end_session` debrief.

  Done:
  - Competitive MCP debrief now reports final human-system cash, access,
    quality, workforce trust, community trust, market share, political capital,
    active projects, active project monthly draws, and staffed beds from
    committed history
  - Automated playtest summaries now parse competitive final metrics from the
    MCP end-session debrief
  - Focused MCP session tests cover completed-session metric reporting and keep
    rival organization names out of the final metric lines
  - MCP playtesting and interface docs describe the end-session metric surface
  - Package version bumped to `0.1.50`

  Deferred / Non-Goals:
  - No transition behavior, rulesets, scenario schemas, replay formats, MCP DTO
    shapes, active observation surfaces, campaign length, golden hashes, or
    gameplay formulas changed
  - No seed-variation batch, free-form agent profile, human learning claim,
    empirical calibration claim, policy forecast claim, balance tuning, or
    diagnostics platform

  Verification:
  - MCP session tests cover the new competitive final debrief metrics
  - Full Rust checks and diff checks completed for the slice

- Feature: Seed-variation playtest evidence
  Status: Complete
  Started: 2026-07-01
  Version: 0.1.51

  Summary:
  Extend the scripted MCP Phase 7 playtest batch from the seed-42 baseline to a
  fixed seed matrix using the v0.1.50 competitive final metric debrief surface.

  Done:
  - Automated playtest runner now executes Fiscal Caution, Capacity Growth, and
    Balanced Strategy profiles for both current campaigns across seeds 42, 43,
    and 44
  - Script output now prints per-seed comparison rows and compact metric ranges
    for stabilization and competitive preview outcomes
  - `docs/playtest-findings-v0.1.51.md` records 18 completed scripted MCP
    sessions, seed-sensitivity observations, evidence limits, and follow-up
    recommendations
  - Package version bumped to `0.1.51`

  Deferred / Non-Goals:
  - No transition behavior, rulesets, scenario schemas, replay formats, MCP DTO
    shapes, active observation surfaces, campaign length, golden hashes, free-
    form agent profile, naive profile, balance tuning, or diagnostics platform
    changed
  - No human learning claim, empirical calibration claim, policy forecast claim,
    or formula tuning from this scripted seed matrix

  Verification:
  - Automated MCP seed-variation batch completed 18 sessions without validation
    failures
  - Full Rust checks and diff checks completed for the slice

- Feature: Naive-profile playtest evidence
  Status: Complete
  Started: 2026-07-01
  Version: 0.1.52

  Summary:
  Extend the scripted MCP Phase 7 playtest batch with a deliberately simple
  `Naive First-Time` profile to test whether current command hints and
  observations support legal low-complexity completion beyond the three
  optimized scripted strategies.

  Done:
  - Automated playtest runner now executes Fiscal Caution, Capacity Growth,
    Balanced Strategy, and Naive First-Time profiles for both current campaigns
    across seeds 42, 43, and 44
  - `docs/playtest-findings-v0.1.52.md` records 24 completed scripted MCP
    sessions, naive-profile command choices, outcome comparisons, evidence
    limits, and follow-up recommendations
  - The naive profile completed all sessions without validation failures while
    preserving cash and underusing some access, community-trust, and competitive
    action-space opportunities
  - Package version bumped to `0.1.52`

  Deferred / Non-Goals:
  - No transition behavior, rulesets, scenario schemas, replay formats, MCP DTO
    shapes, active observation surfaces, campaign length, golden hashes,
    free-form agent orchestration, balance tuning, or diagnostics platform
    changed
  - No human learning claim, empirical calibration claim, policy forecast claim,
    formula tuning, or command-surface change from this scripted naive profile

  Verification:
  - Automated MCP naive-profile batch completed 24 sessions without validation
    failures
  - Rust checks and diff checks completed for the slice

- Feature: Campaign test fallback fix
  Status: Complete
  Started: 2026-07-02
  Version: 0.1.53

  Summary:
  Fix competitive campaign tests so PTY-backed test runs use fallback input
  instead of blocking on interactive prompts.

  Done:
  - CLI stdin fallback detection treats unit tests like non-TTY input for the
    competitive preview loop
  - Package version bumped to `0.1.53`

  Deferred / Non-Goals:
  - No simulation behavior, scenario files, MCP contract, replay format, or
    golden hash changed

  Verification:
  - `cargo test` and `cargo fmt --check` pass on `main`

- Feature: Free-form agent playtest evidence
  Status: Complete
  Started: 2026-07-02
  Version: 0.1.54

  Summary:
  Run one bounded free-form `Free-Form First-Time Executive` profile through the
  existing MCP interface for both current campaigns, then record observations,
  legal-command hints, submitted commands, histories, debriefs, causal
  explanation, evidence limits, and follow-up recommendations.

  Done:
  - `docs/playtest-findings-v0.1.54.md` records one stabilization and one
    competitive free-form session at seed 42 with zero validation failures
  - The free-form stabilization run produced final cash 45, access 84,
    workforce trust 64, community trust 70, and hash `5beed26a91f1b739`
  - The free-form competitive run produced final cash 30, access 71, staffed
    beds 124, workforce trust 57, community trust 65, political capital 11, and
    hash `10c3060949fa8aa1`
  - `docs/mcp-playtesting-guide.md` documents the operator-run free-form
    evidence procedure
  - Package version bumped to `0.1.54`

  Deferred / Non-Goals:
  - No LLM runner, new playtest orchestration framework, transition behavior,
    ruleset, scenario schema, replay format, MCP DTO, campaign length, active
    observation surface, golden hash, balance tuning, or diagnostics platform
    changed
  - No human learning claim, empirical calibration claim, policy forecast claim,
    or formula tuning from one free-form simulated-agent profile

  Verification:
  - Free-form MCP profile completed both current campaigns at seed 42 without
    validation failures
  - Rust checks, scripted MCP regression batch, and diff checks completed for
    the slice

- Feature: Free-form profile synthesis
  Status: Complete
  Started: 2026-07-02
  Version: 0.1.55

  Summary:
  Run two additional bounded free-form profiles, `Free-Form Fiscal Steward` and
  `Free-Form Access Expansion Advocate`, through the existing MCP interface for
  both current campaigns at seed 42, then record observations, legal-command
  hints, submitted commands, histories, debriefs, causal explanation, evidence
  limits, and follow-up recommendations.

  Done:
  - `docs/playtest-findings-v0.1.55.md` records two stabilization and two
    competitive free-form sessions at seed 42 with zero validation failures
  - The fiscal stabilization run produced final cash 68, access 75, workforce
    trust 64, community trust 66, and hash `b5ba1b2a51d998f9`
  - The fiscal competitive run produced final cash 60, access 70, staffed beds
    118, workforce trust 60, community trust 65, political capital 11, and hash
    `4479e68d2a4516e3`
  - The access-expansion stabilization run produced final cash 30, access 90,
    workforce trust 67, community trust 73, and hash `20ad2f9a97dd9e00`
  - The access-expansion competitive run produced final cash 10, access 76,
    staffed beds 126, workforce trust 56, community trust 67, political capital
    11, and hash `34a4653b135f1e63`
  - Package version bumped to `0.1.55`

  Deferred / Non-Goals:
  - No LLM runner, new playtest orchestration framework, transition behavior,
    ruleset, scenario schema, replay format, MCP DTO, campaign length, active
    observation surface, golden hash, balance tuning, or diagnostics platform
    changed
  - No human learning claim, empirical calibration claim, policy forecast claim,
    or formula tuning from these free-form simulated-agent profiles

  Verification:
  - Free-form MCP profiles completed both current campaigns at seed 42 without
    validation failures
  - Rust checks, scripted MCP regression batch, and diff checks completed for
    the slice


