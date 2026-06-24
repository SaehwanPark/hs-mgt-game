# Project Specification

This file is the lightweight spec-driven-development index for the Health
Policy Strategy Game. It tracks what is already true, what is being changed now,
and what is intentionally deferred.

Canonical product and domain direction lives in:

- `README.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`

## Spec Maintenance Rule

Any active or incomplete item in `Present` must explicitly separate:

- `Done`: implemented, documented, or verified work that already exists on the
  active branch.
- `Not Yet Done`: planned goal or target scope for the active item that is not
  complete yet.
- `Deferred / Non-Goals`: excluded work, future work, or known limits that
  should not be mistaken for planned completion within the active item.

Do not rely only on summaries, verification lists, or out-of-scope notes for
active work; future contributors must be able to tell what exists versus what
is planned-but-incomplete versus what is deliberately out of scope without
reconstructing it from the diff.

## Past

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

## Present

- No active items.

## Future

- Define glossary, decision-record conventions, and versioning policy from
  roadmap Phase 0.
- Convert Phase 1 research into an evidence registry and research-to-design
  implications memo.
- Use the actor-card template before adding future strategic actors.
- Use the first scenario brief to guide the next narrow vertical-slice runtime
  expansion with deterministic replay and educational debrief hooks.
- Add scenario data loading only after the conceptual model and first action
  vocabulary settle.
