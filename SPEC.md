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

Full per-slice completion history: [`docs/spec-past-archive.md`](docs/spec-past-archive.md)

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

### Phased rollup

| Phase / track | Version range | Highlights | Tests at closure | Golden hash (seed 42) |
| --- | --- | --- | --- | --- |
| Foundations | concept → v0.1.2 | Proposal, harness, deterministic spine | — | — |
| Stabilization vertical slice | v0.1.3–v0.1.15 | Two- to five-turn demo, debrief, interactive CLI, replay artifact | 67 | `bce02dff9b4b4ac6` (4-turn) |
| Module refactor + CI | v0.1.16–v0.1.18 | `src/lib.rs` modules, colocated tests, GitHub Actions CI | 78 | `bce02dff9b4b4ac6` |
| Phase 0–5 docs closure | v0.1.19–v0.1.24 | Scope register, implications memo, competitor turn, governance, ADR 0001 | 82 | `6fb1ebbea564274f` (5-turn) |
| Stabilization UX | v0.1.25–v0.1.27 | Forecast preview, rich-terminal display, session autosave, beginner mode | 114 | `6fb1ebbea564274f` |
| Competitive design + runtime I1–I4 | v0.1.28–v0.1.31 | Design package, campaign router, action economy, multi-system genesis | 154 | `6fb1ebbea564274f` |
| Competitive runtime I5 | v0.1.32 | Simultaneous resolver, transition_competitive, rival observability | 173 | `6fb1ebbea564274f` (stabilization) |
| Competitive runtime I6 | v0.1.33 | AI batch planner, style-weighted rival actions, inspectable rationale traces | 183 | `e68f683da77d7c2f` (competitive) |
| Competitive runtime I7 | v0.1.34 | Events, delayed effects, institution phase, multi-month loop | 189 | `88d07f9e1bbd6f04` (competitive) |
| Competitive runtime I8 | v0.1.35 | Stata-like CLI parser, interactive human batch entry | 189 | `88d07f9e1bbd6f04` (competitive) |
| Competitive bounded loop | v0.1.36 | Three-month interactive competitive loop over evolving world state | 193 | `88d07f9e1bbd6f04` (competitive) |
| Competitive prompt ergonomics | v0.1.37 | Competitive help command list, colored command/arg tokens, verb-only Tab autocomplete | 201 | `88d07f9e1bbd6f04` (competitive) |
| New-player manual | v0.1.38 | How-to-play manual for stabilization and competitive-preview flows | 201 | `88d07f9e1bbd6f04` (competitive) |
| External playtest protocol | v0.1.39 | Phase 7 prep protocol for stabilization and competitive-preview sessions | 201 | `88d07f9e1bbd6f04` (competitive) |
| Minimal stabilization scenario loader | v0.1.40 | TOML scenario format, bundled stabilization fixture, validation boundary | 208 | `88d07f9e1bbd6f04` (competitive) |
| MCP agent support | v0.1.41 | Local stdio MCP server for bounded autonomous play of both current campaigns | 216 | `88d07f9e1bbd6f04` (competitive) |

### Recent slices

- Feature: Rich-terminal CLI display
  Status: Complete
  Started: 2026-06-24
  Branch: feat/rich-terminal-cli-display

  Summary:
  Add semantic color, emoji section headings, and explicit per-turn command
  prompts with parameter legends on TTY stdout while respecting `NO_COLOR`.

  Done:
  - `src/cli/display/style.rs`, `print.rs`, `prompt.rs`
  - Interactive and preset CLI output use styled sections and global command footers
  - CLI errors print in red on stderr when styling is enabled
  - Package version bumped to `0.1.26`

  Deferred / Non-Goals:
  - No simulation or replay artifact content changes
  - No competitive campaign changes

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass

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
  - Resume/start-over startup flow; autosave on interactive quit
  - Contextual guidance and beginner mode (`src/cli/guidance.rs`, `src/cli/beginner.rs`)
  - ADR-0002; package version `0.1.27`

  Deferred / Non-Goals:
  - No autosave on every turn or for preset paths
  - No changes to `transition()`, golden hash, or replay artifact format

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (114 tests)

- Feature: Competitive gameplay design package
  Status: Complete
  Started: 2026-06-24
  Branch: feat/competitive-gameplay-design

  Summary:
  Develop the competitive gameplay sketch into durable design artifacts for a
  parallel regional-market campaign (1 human + K AI health systems) without
  changing stabilization demo runtime behavior.

  Done:
  - `docs/gameplay-competitive-sketch.md`, `docs/core-loop-spec.md`,
    `docs/competitive-scenario-brief.md`, action catalog and CLI grammar drafts
  - ADRs 0003–0006 accepted; canonical docs and workspace artifacts updated
  - Package version bumped to `0.1.28`

  Deferred / Non-Goals:
  - Runtime implementation slices I1–I8 (tracked in Future / Present)
  - Medicare/Medicaid actors in competitive v1

  Verification:
  - Design docs cross-link consistently; domain QA pass
  - `cargo fmt --check`, `cargo test` pass with golden hash unchanged

- Feature: Competitive campaign runtime I1+I2
  Status: Complete
  Started: 2026-06-24
  Branch: feat/campaign-router-executive-report

  Summary:
  Add CLI campaign router (`stabilization-v1` vs `competitive-regional-v1` preview)
  and monthly executive report renderer using observation-only mock fixtures.

  Done:
  - `CampaignId`, `Difficulty`, `PolicyCalendar`, `PlayerObservation` in
    `src/model/campaign.rs`
  - Campaign and difficulty selectors; executive report renderer
  - Mock fixtures in `src/competitive/fixtures.rs`; `SessionOutcome::CompetitivePreview`
  - Package version bumped to `0.1.29`

  Deferred / Non-Goals:
  - No `transition_competitive()` or stabilization `transition()` changes
  - Full competitive play deferred to I3–I8 (see archive and Future)
  - Session autosave remains stabilization-only

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (130 tests)
  - Competitive path shows month-1 executive report then stub message

- Feature: Competitive campaign runtime I3
  Status: Complete
  Started: 2026-06-24
  Branch: feat/competitive-action-economy

  Summary:
  Add competitive command types, action-cost catalog, and batch validation for
  AP, cash, and political capital per ADR-0005.

  Done:
  - `CompetitiveCommand`, `ActionCost` in `src/model/competitive_command.rs`
  - `PlayerResources`, `CompetitiveRuleset` in `src/model/resources.rs`
  - `validate_competitive_batch` in `src/sim/validate_competitive.rs`
  - Five preset validation demos; executive report AP/PC header
  - Package version bumped to `0.1.30`

  Deferred / Non-Goals:
  - Multi-system state, resolver, AI, events, Stata CLI (I4–I8)
  - No scenario file loader; no Medicare/Medicaid actors

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (148 tests)
  - Competitive demos 1–5 exercise pass/fail validation paths

- Feature: Competitive campaign runtime I4
  Status: Complete
  Started: 2026-06-24
  Branch: feat/competitive-multi-system-state

  Summary:
  Add `CompetitiveWorldState` with K+1 `HealthSystemState` entities, player
  slots, and difficulty-scoped genesis fixtures per ADR-0004.

  Done:
  - `CompetitiveWorldState`, `SharedMarketFields`, `HealthSystemState`,
    `PlayerSlot`, `AiProfile` in `src/model/competitive_world.rs`
  - `genesis_competitive_world` and roster display in `src/competitive/genesis.rs`
  - Executive observation derives human metrics from genesis
  - Competitive stub shows genesis roster before month-1 report
  - Six focused genesis tests; package version bumped to `0.1.31`

  Deferred / Non-Goals:
  - No `transition_competitive()` or monthly loop (I5–I8)
  - No stabilization golden hash changes

  Verification:
  - `systems.len() == K+1` for each `Difficulty` tier
  - Human at system 0; K AI rivals with style profiles
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (154 tests)

- Feature: Competitive campaign runtime I5
  Status: Complete
  Started: 2026-06-24
  Branch: feat/competitive-simultaneous-resolver

  Summary:
  Add simultaneous monthly action resolver, `transition_competitive()`, partial
  rival observability, and a one-month resolution CLI demo per ADR-0003.

  Done:
  - `SystemMonthlyBatch`, `AggregatedMonthlyActions` in `src/model/competitive_batch.rs`
  - `CompetitiveTransition`, `CompetitiveHistory` in `src/model/competitive_history.rs`
  - `resolve_monthly_batches` in `src/sim/resolve.rs`
  - `transition_competitive()` in `src/sim/transition_competitive.rs`
  - `observe_for_human()` in `src/sim/observe_competitive.rs`
  - Month-1 preset resolution in `src/competitive/resolution.rs`
  - CLI month-1 resolution demo + month-2 executive report preview
  - Golden `tests/golden_competitive_seed42.rs` hash `05a422b51a2c24e8`
  - Package version bumped to `0.1.32`

  Deferred / Non-Goals:
  - AI players (I6), events/delays (I7), Stata CLI (I8)
  - Full 24-month campaign loop, competitive replay artifact, competitive autosave
  - No stabilization golden hash changes

  Verification:
  - Permutation-invariance test for batch collection order
  - Stabilization golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (173 tests)

- Feature: Competitive campaign runtime I6
  Status: Complete
  Started: 2026-06-25
  Branch: feat/competitive-ai-players

  Summary:
  Add deterministic AI rival batch generation with style-weighted command
  scoring, lagged-public-log response, and inspectable rationale strings.

  Done:
  - `compute_ai_batch()` and `month1_batches_with_ai()` in `src/competitive/resolution.rs`
  - `SystemMonthlyBatch.rationale` persisted for AI action traceability
  - Competitive month-1 resolver switched from fixed rival presets to AI-generated batches
  - Seed plumbed through month-1 competitive resolution helpers for deterministic tie-breaks
  - New tests in `tests/competitive_ai_players.rs`; competitive golden updated in I7
  - Package version bumped to `0.1.33`

  Deferred / Non-Goals:
  - Events/delays/annual tick (I7) and Stata CLI (I8) — completed in follow-on slices
  - Full 24-month campaign loop, competitive replay artifact, competitive autosave
  - No stabilization golden hash changes

  Verification:
  - `cargo fmt --check`, `cargo test` pass (189 tests)
  - Competitive seed-42 golden hash `88d07f9e1bbd6f04` (updated in I7)
  - Stabilization seed-42 golden hash unchanged at `6fb1ebbea564274f`

- Feature: Competitive campaign runtime I7
  Status: Complete
  Branch: feat/competitive-events-delays
  Version: 0.1.34

  Done:
  - `resolve_competitive_inputs` with `monthly_events` and `annual_policy` streams
  - `PendingEffectKind` and `apply_due_pending_effects` at month start
  - Institution phase (payer/state) and `build_multi_month_resolution_history`
  - CLI months 2–3 preview; golden hash `88d07f9e1bbd6f04`

- Feature: Competitive campaign runtime I8
  Status: Complete
  Branch: feat/competitive-stata-cli
  Version: 0.1.35

  Done:
  - `src/cli/competitive_parse.rs` for MVP `verb arg=value` syntax
  - TTY interactive human batch entry wired to `resolve_competitive_month`
  - Non-TTY preset fallback for CI/tests

  Deferred / Non-Goals:
  - Full 24-month interactive loop, competitive autosave, syntax highlighting/autocomplete

- Feature: Competitive bounded multi-month loop
  Status: Complete
  Branch: feat/competitive-multi-month-loop
  Version: 0.1.36

  Done:
  - Competitive CLI preview resolves one coherent three-month loop from a single
    evolving `CompetitiveWorldState`
  - Per-month executive reports precede human command entry
  - TTY mode accepts Stata-like batches each month; non-TTY mode uses deterministic
    fallback batches for CI/tests
  - Focused tests cover three-month non-TTY progression and fallback batch policy

  Deferred / Non-Goals:
  - Full 24-month campaign loop, competitive autosave, replay artifact export
  - Scenario file loading

- Feature: Competitive command prompt ergonomics
  Status: Complete
  Branch: feat/competitive-prompt-ergonomics
  Version: 0.1.37

  Done:
  - Shared competitive command catalog metadata for parser help and REPL completion
  - Competitive help context now lists available commands for `help`/`?`
  - Colored command vs argument token rendering for competitive command reference lines
  - Verb-only Tab autocomplete in competitive TTY command entry (fallback to plain input when unavailable)
  - Focused parser, style, guidance, and REPL completion tests

  Deferred / Non-Goals:
  - Argument-key and enum-value autocomplete
  - Full 24-month campaign loop, competitive autosave, replay artifact export, scenario loading

- Feature: New-player How to Play manual
  Status: Complete
  Version: 0.1.38

  Summary:
  Add a player-facing manual for current stabilization and competitive-preview
  flows.

  Done:
  - `docs/how-to-play.md` with quickstart, campaign flow, terminology, command
    examples, worked interaction example, and difficulty recovery tips
  - README documentation index updated
  - Package version bumped to `0.1.38`

  Deferred / Non-Goals:
  - No runtime behavior changes
  - No full 24-month competitive campaign
  - No scenario loading

- Feature: External playtest protocol refresh
  Status: Complete
  Branch: feat/external-playtest-protocol
  Version: 0.1.39

  Summary:
  Add a Phase 7 prep protocol for informal external playtests of the current
  stabilization and competitive-preview CLI flows.

  Done:
  - `docs/external-playtest-protocol.md` with setup, stabilization and
    competitive session scripts, observation rubric, post-session prompts,
    note template, privacy cautions, and synthesis guidance
  - README documentation index and current-priority wording updated
  - Package version bumped to `0.1.39`

  Deferred / Non-Goals:
  - No runtime behavior changes
  - No scenario loader, 24-month competitive campaign, or new strategic actors
  - No formal human-subjects research process or policy-forecasting claim

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

## Present

No active slice. Competitive runtime I1–I8, bounded three-month loop,
competitive command-prompt ergonomics, external playtest protocol refresh, the
minimal stabilization scenario loader, and bounded MCP agent-play support are
complete for the MVP preview, Phase 7 prep, Phase 6.2 scenario-loading, and
agent-interface tracks.

## Future

### Parallel / gated tracks

- **External playtest synthesis** (Phase 7 prep): run protocol sessions and
  summarize findings in a versioned playtest findings document.
- **Medicare/Medicaid strategic actors** (Phase 5.1 / 6.1, gated): excluded until
  brief expands; actor cards required first.
- **Scenario data loading runtime** (Phase 6.2): after format design approval;
  minimal stabilization TOML loading is complete; competitive scenario loading,
  arbitrary scenario path selection, and migration tooling remain deferred.
- **MCP agent interface expansion**: HTTP transport, auth, durable MCP session
  persistence, full competitive campaign length, and replay/export integration
  remain deferred until bounded agent play produces evidence for those needs.
- **Clippy CI / release automation** (Phase 0 / 8): explicitly deferred.
