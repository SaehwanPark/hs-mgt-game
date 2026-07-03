# Changelog

All notable project changes should be recorded here.

The project follows lightweight semantic versioning during early development.

## [Unreleased]

## [0.1.60] - 2026-07-03

### Added

- Added `cargo clippy --all-targets -- -D warnings` check to GitHub Actions CI workflow to enforce code quality and prevent lint regression.

### Changed

- Resolved 32 Clippy compiler warnings/errors across the codebase (including manual prefix stripping, collapsible `if` blocks, manual range contains checks, complex types, and unused variable/import warnings).
- Bumps project version to `0.1.60`.

## [0.1.59] - 2026-07-02

### Added

- Enhanced competitive campaign end-session debriefing with a detailed month-by-month history log of player commands, rival commands (flagged as publicly disclosed, observed via monitor, or unobserved by you), events, and effects.
- Added helper formatting for competitive commands in `competitive_debrief`.

### Changed

- Updated project status and SDD history for the debrief quality slice.
- Package version bumped to `0.1.59`.

## [0.1.58] - 2026-07-02

### Added

- Added `docs/playtest-findings-v0.1.58.md` detailing the follow-up playtest sessions using v0.1.57 command help and prompt cues.

### Changed

- Updated project status and SDD history for the AI-agent playtest synthesis slice.
- Package version bumped to `0.1.58`.

## [0.1.57] - 2026-07-02

### Added

- Added a capital projects strategic lesson to `competitive_debrief` in the MCP layer.

### Changed

- Expanded competitive command help (`PromptContext::CompetitiveCommand`) to output detailed descriptions and AP/cash/political capital costs for all 7 verbs.
- Hardened monthly command prompt cues in `print_competitive_month_report` to explicitly guide players to type `?` or `help` for detailed command explanations.
- Bumped package version to `0.1.57`.

## [0.1.56] - 2026-07-02

### Added

- Added `docs/playtest-findings-v0.1.56.md` with lightweight strategy-space
  diagnostics over existing scripted and free-form MCP playtest evidence.

### Changed

- Updated project status and SDD history for the diagnostics slice.
- Package version bumped to `0.1.56`.

## [0.1.55] - 2026-07-02

### Added

- Added `docs/playtest-findings-v0.1.55.md` with two additional free-form MCP
  profiles across both current campaigns at seed 42.

### Changed

- Updated project status and SDD history for the free-form profile synthesis
  slice.
- Package version bumped to `0.1.55`.

## [0.1.54] - 2026-07-02

### Added

- Added `docs/playtest-findings-v0.1.54.md` with a free-form MCP first-time
  executive profile across both current campaigns at seed 42.

### Changed

- Documented the operator-run MCP free-form playtest procedure in the
  playtesting guide.
- Package version bumped to `0.1.54`.

## [0.1.53] - 2026-07-02

### Fixed

- Fixed competitive campaign tests so PTY-backed test runs use fallback input
  instead of blocking on interactive prompts.

### Changed

- Package version bumped to `0.1.53`.

## [0.1.52] - 2026-07-01

### Added

- Added `docs/playtest-findings-v0.1.52.md` with scripted MCP naive-profile
  evidence across seeds 42, 43, and 44.

### Changed

- Updated the automated MCP playtest runner to include a `Naive First-Time`
  profile alongside the three existing scripted strategies.
- Package version bumped to `0.1.52`.

## [0.1.51] - 2026-07-01

### Added

- Added `docs/playtest-findings-v0.1.51.md` with scripted MCP seed-variation
  evidence across seeds 42, 43, and 44.

### Changed

- Updated the automated MCP playtest runner to execute the existing three
  scripted strategies across a fixed seed matrix and print per-seed metric
  summaries.
- Package version bumped to `0.1.51`.

## [0.1.50] - 2026-07-01

### Changed

- Added final competitive player tradeoff and resource metrics to the MCP
  `end_session` debrief using committed history.
- Updated the automated playtest summary to parse competitive final metrics
  from the MCP debrief.
- Documented the bounded competitive debrief evidence surface for MCP
  playtesting.
- Package version bumped to `0.1.50`.

## [0.1.49] - 2026-06-30

### Added

- Added `docs/playtest-findings-v0.1.49.md` with Phase 7 scripted MCP playtest
  findings for the current stabilization and competitive preview campaigns.

### Changed

- Fixed the automated MCP playtest harness so stabilization policies continue
  using stabilization commands after Turn 1.
- Updated the Python MCP client to launch the built stdio server by default,
  read responses with bounded byte-level waits, and fail scripted validation
  errors with context instead of looping silently.
- Package version bumped to `0.1.49`.

## [0.1.48] - 2026-06-30

### Changed

- Refreshed SDD Future planning from external project feedback, prioritizing
  gameplay validity hypotheses, strategy-space diagnostics, debrief quality, one
  exemplary scenario, and model-confidence annotations before broad new
  architecture.
- Clarified that future abstraction, scenario-tooling, and calibration work
  should be gated by playtest, authoring, or debrief evidence.
- Package version bumped to `0.1.48`.

## [0.1.47] - 2026-06-30

### Added

- Added `docs/agent-playtest-protocol.md` as the active Phase 7 validation
  protocol for AI-agent and sub-agent playtests.
- Added ADR-0009 accepting AI-agent playtests as the validation path replacing
  planned external human playtest recruitment.

### Changed

- Superseded the external human playtest protocol in active roadmap and SPEC
  planning language.
- Clarified that agent-playtest evidence does not claim measured human learning,
  empirical calibration, or policy-forecasting validity.
- Package version bumped to `0.1.47`.

## [0.1.46] - 2026-06-30

### Changed

- Reviewed deferred items in SPEC Past and archived slice records, then folded
  still-worthy follow-up work into SPEC Future tracks.
- Added Future coverage for evidence/parameter ledgers, instructor analysis,
  replay/export work, competitive command ergonomics, and broader simulation
  breadth gates.
- Package version bumped to `0.1.46`.

## [0.1.45] - 2026-06-30

### Changed

- Cleaned up `SPEC.md` so next development tracks are specific, gated, and
  verification-oriented.
- Refreshed SDD and companion design docs for the current bounded competitive
  preview, stabilization scenario-loader, and MCP agent-play state.
- Package version bumped to `0.1.45`.

## [0.1.44] - 2026-06-29

### Changed

- Clarified player-facing guidance for commercial payer leverage in stabilization
  Turn 1 help and beginner-mode choices.
- Clarified competitive recruitment timing and workforce-trust tradeoffs in
  player observations, MCP debrief output, and the player manual.
- Package version bumped to `0.1.44`.

## [0.1.43] - 2026-06-28

### Added

- Comprehensive gameplay playtest findings report at `docs/playtest-findings-v0.1.42.md` documenting play session results, winnability, strategic tension, and entertainment value.
- Automated Python playtest scripts (`play_fiscal.py`, `play_growth.py`, `play_balanced.py`) and logs verifying MCP stdio game sessions.

### Changed

- Package version bumped to `0.1.43`.

## [0.1.42] - 2026-06-27

### Added

- CLI `--scenario <PATH>` / `-s <PATH>` flags to load and play arbitrary stabilization TOML scenarios.
- Bypass of campaign selection and resume prompts when launching with a custom scenario file.
- Integration tests in `tests/scenario_selection_tests.rs` for scenario file loading and error paths.

### Changed

- Package version bumped to `0.1.42`.

## [0.1.41] - 2026-06-26

### Added

- Local stdio MCP server binary `hs-mgt-game-mcp` for AI-agent play of the
  bounded `stabilization-v1` and `competitive-regional-v1` campaigns.
- MCP tools for starting sessions, reading actor-visible observations,
  submitting one turn/month, inspecting append-only history summaries, and
  ending sessions with a debrief summary.
- `docs/mcp-agent-interface.md` and ADR-0008 documenting the MCP interface
  boundary, tool contract, and deferred transports.

### Changed

- Package version bumped to `0.1.41`.

### Notes

- MCP session state is in-memory per server process. Streamable HTTP, auth,
  persistence, competitive replay artifacts, and 24-month competitive play
  remain deferred.
- Transition semantics, replay artifact format, and golden hashes are unchanged.

## [0.1.40] - 2026-06-26

### Added

- Minimal TOML scenario loader for the bundled `stabilization-v1` scenario.
- `scenarios/stabilization-v1.toml` with current genesis state, learning
  objectives, actor stubs, and five-turn schedule.
- ADR-0007 accepting `scenario-toml-0.1.40` for the stabilization-only runtime
  slice.

### Changed

- Fresh stabilization runs now validate the bundled scenario before starting,
  while transition and replay semantics remain unchanged.
- Package version bumped to `0.1.40`.

### Notes

- Competitive scenario loading, arbitrary scenario path selection, and scenario
  migration tooling remain deferred.

## [0.1.39] - 2026-06-26

### Added

- External playtest protocol at `docs/external-playtest-protocol.md` covering
  stabilization and competitive-preview session scripts, observation rubric,
  post-session prompts, privacy cautions, and synthesis guidance.

### Changed

- `README.md` documentation index now links the external playtest protocol.
- Package version bumped to `0.1.39`.

## [0.1.38] - 2026-06-25

### Added

- New player-facing manual at `docs/how-to-play.md` covering quickstart,
  campaign flow, terminology, commands, worked interaction example, and
  difficulty recovery tips.

### Changed

- `README.md` documentation index now links the new player manual.
- Package version bumped to `0.1.38`.

## [0.1.37] - 2026-06-25

### Added

- Competitive verb-only Tab autocomplete for monthly command entry using a CLI-only REPL boundary.
- Competitive help now lists available command usages when `help`/`?` is entered at command prompt.
- Shared competitive command catalog metadata reused by parser help and REPL completion.

### Changed

- Competitive command usage text now styles command tokens separately from argument syntax when color is enabled.
- Competitive command prompt includes an explicit colored `riverside>` label with completion hint.
- Package version bumped to `0.1.37`.

### Notes

- Argument-key and enum-value autocomplete remain deferred.

## [0.1.36] - 2026-06-25

### Added

- Bounded three-month competitive loop in the CLI preview, reusing the existing
  one-month resolver for each evolving month.
- Per-month executive report, human command entry, simultaneous AI resolution,
  and resolution summary across months 1-3.
- Competitive command-entry prompt and help context for the monthly loop.
- Focused tests for non-TTY three-month loop behavior and fallback human batches.

### Changed

- Competitive preview no longer shows a separate preset months 2-3 preview after
  month 1; it resolves one coherent three-month history.
- Package version bumped to `0.1.36`.

### Notes

- Full 24-month competitive campaign, competitive autosave, replay export,
  syntax highlighting, autocomplete, and scenario loading remain deferred.

## [0.1.35] - 2026-06-25

### Added

- Stata-like competitive command parser (`src/cli/competitive_parse.rs`) for MVP verbs.
- Interactive human monthly batch entry in competitive campaign preview (slice I8).
- `competitive_command_help_lines` for in-session command reference.

### Changed

- Competitive month-1 resolution uses parsed human batch or preset on empty input.
- Package version bumped to `0.1.35`.

### Notes

- Full 24-month interactive competitive loop and autosave remain deferred.

## [0.1.34] - 2026-06-25

### Added

- `CompetitiveResolvedInputs` and `resolve_competitive_inputs` with `monthly_events`
  and `annual_policy` streams (`src/inputs/resolve_competitive.rs`).
- `PendingEffectKind` on competitive effect queue; `apply_due_pending_effects` and
  `apply_month_start_tick` (`src/sim/effects_competitive.rs`).
- Simplified payer/state institution phase after player resolution.
- `resolve_competitive_month` and `build_multi_month_resolution_history` in
  `src/competitive/month_loop.rs` (2–3 month demo loop).
- Competitive CLI preview for months 2–3 with environment and institution events.

### Changed

- Month-1 resolution applies environment tick before player decisions.
- Golden test `tests/golden_competitive_seed42.rs` hash `88d07f9e1bbd6f04`.
- Package version bumped to `0.1.34`.

### Notes

- Stata CLI deferred to I8.
- Stabilization golden seed-42 hash unchanged (`6fb1ebbea564274f`).

## [0.1.33] - 2026-06-25

### Added

- Competitive AI batch planner APIs: `compute_ai_batch()` and
  `month1_batches_with_ai()` (`src/competitive/resolution.rs`).
- Style-weighted AI command selection using lagged public-action pressure with
  deterministic tie-break stream mapping `ai_player_{id}`.
- AI rationale persistence on `SystemMonthlyBatch.rationale` for inspectable
  decision traces.
- Integration test coverage in `tests/competitive_ai_players.rs` for
  reproducibility and rationale presence.

### Changed

- Competitive month-1 resolver now uses AI-generated rival batches instead of
  fixed presets (human batch remains explicit).
- `resolve_preset_month1` and `build_month1_resolution_history` now take a run
  seed to keep AI tie-break behavior reproducible in tests and CLI.
- Golden competitive seed-42 hash updated to `e68f683da77d7c2f`.
- Bumped package version from `0.1.32` to `0.1.33`.

### Notes

- I7 (events/delays/annual tick) and I8 (Stata-like CLI) remain deferred.
- Stabilization golden seed-42 hash remains `6fb1ebbea564274f`.

## [0.1.32] - 2026-06-24

### Added

- `SystemMonthlyBatch`, `AggregatedMonthlyActions`, `CompetitiveTransition`, and
  `CompetitiveHistory` types (`src/model/competitive_batch.rs`,
  `src/model/competitive_history.rs`).
- `SimultaneousActionResolver` in `src/sim/resolve.rs` per ADR-0003.
- `transition_competitive()` with MVP command dispatch, public action log, and
  pending effect enqueue (`src/sim/transition_competitive.rs`).
- `observe_for_human()` with 1-month lag rival intel and monitor depth support
  (`src/sim/observe_competitive.rs`).
- Competitive state hash (`src/model/competitive_hash.rs`).
- Month-1 preset resolution helpers (`src/competitive/resolution.rs`).
- Competitive CLI path: month-1 resolution demo and month-2 executive report preview.
- Golden test `tests/golden_competitive_seed42.rs` (hash `05a422b51a2c24e8`).

### Changed

- `ARCHITECTURE.md`, `SPEC.md`, `README.md`, `docs/phase5-scope-register.md`,
  `_workspace/final/handoff.md`.

### Notes

- AI players, events/delays, and Stata CLI deferred to I6–I8.
- Stabilization golden seed-42 hash unchanged (`6fb1ebbea564274f`).

## [0.1.31] - 2026-06-24

### Added

- `CompetitiveWorldState`, `HealthSystemState`, `SharedMarketFields`, `PlayerSlot`,
  and `AiProfile` types per ADR-0004 (`src/model/competitive_world.rs`).
- Difficulty-scoped competitive genesis fixtures (`src/competitive/genesis.rs`).
- Genesis roster display in competitive campaign preview CLI flow.
- Six focused genesis sizing and controller-assignment tests.

### Changed

- `mock_observation_month1` derives human-system metrics from genesis state.
- `SPEC.md` reconciled with `docs/spec-past-archive.md` and restored `Present` section.
- `ARCHITECTURE.md`, `README.md`, `_workspace/final/handoff.md`, `docs/phase5-scope-register.md`.

### Notes

- No `transition_competitive()` or monthly loop yet (deferred to I5).
- Golden seed-42 stabilization hash unchanged (`6fb1ebbea564274f`).

## [0.1.30] - 2026-06-24

### Added

- Competitive command types and action-cost catalog (`src/model/competitive_command.rs`).
- Player resource and competitive ruleset types (`src/model/resources.rs`).
- `validate_competitive_batch` and `validate_competitive_command` in
  `src/sim/validate_competitive.rs` (AP, cash, political capital, concurrent projects).
- Executive report header shows political capital remaining (ADR-0005).
- Competitive validation demo presets and interactive stub loop (`src/competitive/`,
  `src/cli/campaign.rs`).

### Changed

- `ARCHITECTURE.md`, `SPEC.md`, `README.md`, `_workspace/final/handoff.md`.
- Bumped package version from `0.1.29` to `0.1.30`.

### Notes

- Competitive path validates preset command batches only; full play deferred to I4–I8.
- Golden seed-42 stabilization hash unchanged (`6fb1ebbea564274f`).

## [0.1.29] - 2026-06-24

### Added

- CLI campaign router: `stabilization-v1` (default) vs `competitive-regional-v1`
  preview (`src/cli/campaign.rs`, `src/cli/io.rs`).
- Competitive campaign types: `CampaignId`, `Difficulty`, `PolicyCalendar`,
  `PlayerObservation` (`src/model/campaign.rs`).
- Monthly executive report renderer with six sections per
  `docs/executive-report-format.md` (`src/cli/display/executive_report.rs`).
- Observation-only mock fixtures for competitive month-1 preview (`src/competitive/`).
- `SessionOutcome::CompetitivePreview` for competitive stub exit.

### Changed

- `run()` flow: campaign selection after autosave resume; stabilization path unchanged.
- `ARCHITECTURE.md`, `docs/core-loop-spec.md`, `docs/phase5-scope-register.md`,
  `SPEC.md`, `README.md`, `_workspace/final/handoff.md`.
- Bumped package version from `0.1.28` to `0.1.29`.

### Notes

- Competitive path shows month-1 executive report only; full play deferred to I3–I8.
- Golden seed-42 stabilization hash unchanged (`6fb1ebbea564274f`).

## [0.1.28] - 2026-06-24

### Added

- Competitive gameplay design package for parallel `competitive-regional-v1` campaign:
  `docs/gameplay-competitive-sketch.md`, `docs/core-loop-spec.md`,
  `docs/competitive-scenario-brief.md`, `docs/executive-report-format.md`,
  `docs/action-catalog-draft.md`, `docs/cli-command-grammar-draft.md`.
- ADRs 0003–0006: simultaneous monthly actions, multi-system player state,
  action economy, Stata-like CLI layer.
- AI health-system player card template in `docs/actor-cards.md`.
- Glossary entries for action points, simultaneous resolution, AI player vs NPC.

### Changed

- `docs/proposal.md`, `docs/roadmap.md` (Phase 6.0 competitive track),
  `docs/system-boundary.md`, `docs/scenario-format-draft.md`,
  `docs/first-scenario-brief.md`, `docs/phase5-scope-register.md`,
  `docs/phase1-implications-memo.md`, `LESSONS.md`.
- `SPEC.md`, `ARCHITECTURE.md`, workspace handoff artifacts, `README.md`, and
  `docs/decision-records/README.md`.
- Bumped package version from `0.1.27` to `0.1.28`.

### Notes

- Design and documentation only; no runtime behavior changes.
- Golden seed-42 stabilization hash unchanged (`6fb1ebbea564274f`).

## [0.1.27] - 2026-06-24

### Added

- Global quit (`q`/`quit`/`exit`) and help (`?`/`help`) at all CLI prompts.
- Mid-run session autosave on interactive quit (`session-save-0.1.27`) with resume
  or start-over on next launch.
- User-config persistence under `$XDG_CONFIG_HOME/hs-mgt-game/` (or `~/.config/...`).
- Contextual player guidance (`src/cli/guidance.rs`) and one-time new-player cues.
- Beginner mode (`b`) with per-turn multiple-choice options, pros/cons, and
  recommendability (`src/cli/beginner.rs`).
- ADR-0002: mid-run session save format and semantics.

### Changed

- `RunConfig` carries `ExperienceMode` and optional resume state.
- `run()` returns `SessionOutcome` (completed, quit saved, quit without save).
- Play mode menu documents beginner (`b`) and global commands on all footers.
- Bumped package version from `0.1.26` to `0.1.27`.

### Notes

- Golden seed-42 preset hash unchanged. Simulation core and replay artifact format
  unchanged.

## [0.1.26] - 2026-06-24

### Added

- Rich-terminal CLI display layer (`src/cli/display/style.rs`, `print.rs`, `prompt.rs`).
- Explicit per-turn command prompts with parameter legends, ruleset bounds, and
  global command footers.
- Focused style and prompt unit tests.

### Changed

- Interactive and preset CLI output use semantic color, emoji section headings,
  and blank-line section spacing on TTY stdout.
- Play mode, seed, turn command, and replay export prompts always show applicable
  global commands.
- CLI errors print in red on stderr when styling is enabled.
- Respects `NO_COLOR` and disables ANSI when stdout is not a terminal.
- Bumped package version from `0.1.25` to `0.1.26`.

### Notes

- Golden seed-42 hash unchanged. Simulation and replay artifact content unchanged.

## [0.1.25] - 2026-06-24

### Added

- Turn uncertainty preview in interactive CLI play (`src/cli/display/forecast.rs`).
- [`docs/playtest-findings-v0.1.25.md`](docs/playtest-findings-v0.1.25.md).

### Changed

- Interactive mode prints observation-only uncertainty preview before each
  executive briefing.
- Starting dashboard notes that reported measures may differ from true conditions.
- Phase 5 scope register forecast row marked mostly achieved.
- Bumped package version from `0.1.24` to `0.1.25`.

### Notes

- Golden seed-42 hash unchanged. Preset paths unaffected.

## [0.1.24] - 2026-06-24

### Added

- [`docs/decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md`](docs/decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md)
  — first accepted ADR for pure transition core and stochastic input boundary.
- [`docs/scenario-format-draft.md`](docs/scenario-format-draft.md) — Phase 6.2
  scenario format design draft (no runtime loader).

### Changed

- Updated [`ARCHITECTURE.md`](ARCHITECTURE.md) open decisions, competitor stream,
  and actor-information proof.
- Bumped package version from `0.1.23` to `0.1.24`.
- Updated README and SPEC bookkeeping.

### Notes

- Docs-only release; no runtime behavior changes. Golden hash unchanged.

## [0.1.23] - 2026-06-24

### Changed

- Refreshed [`docs/phase5-scope-register.md`](docs/phase5-scope-register.md) for
  five-turn v0.1.21+ closure, competitor achieved, and updated next-slice pointers.
- Updated [`docs/system-boundary.md`](docs/system-boundary.md) with
  `RespondToCompetitorCapacityMove` and rival capacity competition inclusion.
- Updated [`docs/evidence-registry.md`](docs/evidence-registry.md) competitor
  ledger row to `linked`; five-turn wording.
- Expanded [`SPEC.md`](SPEC.md) `Future` backlog and closed reconciliation slice
  in `Past`.
- Marked superseded next-slice note in
  [`docs/playtest-findings-v0.1.21.md`](docs/playtest-findings-v0.1.21.md).

### Notes

- Docs-only release; no runtime behavior changes. Golden hash unchanged.

## [0.1.22] - 2026-06-24

### Added

- [`docs/glossary.md`](docs/glossary.md) — core ontology terms for contributors.
- [`docs/decision-records/`](docs/decision-records/) — ADR README and template.
- [`docs/versioning-policy.md`](docs/versioning-policy.md) — code, ruleset, and
  replay artifact versioning rules.

### Changed

- Bumped package version from `0.1.21` to `0.1.22`.
- Updated README contributing section with governance doc links.

### Notes

- Docs-only release; no runtime behavior changes. Golden hash unchanged.

## [0.1.21] - 2026-06-24

### Added

- Fifth-turn competitor capacity interaction with
  `RespondToCompetitorCapacityMove` command and rival health system actor.
- Competitor actor card in [`docs/actor-cards.md`](docs/actor-cards.md).
- `competitor_market_signal` random stream (active on turn 5 only).
- [`docs/playtest-findings-v0.1.21.md`](docs/playtest-findings-v0.1.21.md).

### Changed

- Extended playable demo from four to five turns (interactive and preset paths).
- Bumped package version from `0.1.20` to `0.1.21`.
- Golden seed-42 final state hash updated to `6fb1ebbea564274f` (turns 1–4
  unchanged; turn 4 hash remains `bce02dff9b4b4ac6`).

### Notes

- Replay artifact format adds optional `competitor_market_signal` and
  `market_competition_briefing` fields with backward-compatible parsing.

## [0.1.20] - 2026-06-24

### Added

- Added [`docs/phase1-implications-memo.md`](docs/phase1-implications-memo.md)
  converting Phase 1 research into adopted, modified, and rejected design
  patterns plus mechanism implications for the stabilization slice.
- Added parameter-source ledger section to
  [`docs/evidence-registry.md`](docs/evidence-registry.md).

### Changed

- Bumped package version from `0.1.19` to `0.1.20`.
- Updated README documentation links and contributor priorities.
- Restored SPEC `Present` section bookkeeping after Phase 5 closure.

### Notes

- Docs-only release; no runtime behavior changes. Golden seed-42 hash unchanged.

## [0.1.19] - 2026-06-24

### Added

- Added [`docs/phase5-scope-register.md`](docs/phase5-scope-register.md) closing
  Phase 5 with achieved scope, deferrals, risks, exit-criteria assessment, and
  next-slice recommendation.
- Added [`docs/playtest-findings-v0.1.19.md`](docs/playtest-findings-v0.1.19.md)
  refreshing internal playtest notes for the post-refactor codebase and CI.

### Changed

- Bumped package version from `0.1.18` to `0.1.19`.
- Updated README documentation links and contributor priorities.
- Updated evidence registry and workspace handoff artifacts.

### Notes

- Docs-only release; no runtime behavior changes. Golden seed-42 hash unchanged.

## [0.1.18] - 2026-06-24

### Added

- Added GitHub Actions CI workflow running `cargo fmt --check` and `cargo test`
  on pushes to `main` and on pull requests.

### Changed

- Bumped package version from `0.1.17` to `0.1.18`.
- Updated README contributing notes with local CI commands and revised
  priorities.

## [0.1.17] - 2026-06-24

### Changed

- Colocated 77 characterization unit tests with owning library modules under
  `#[cfg(test)]` and added a crate-root golden integration test in
  `tests/golden_seed42.rs`.
- Added `src/test_support.rs` for shared test helpers (`demo_history`,
  `sample_replay_artifact`).
- Reduced `src/main.rs` to entry-point only (no embedded test module).
- Bumped package version from `0.1.16` to `0.1.17`.

## [0.1.16] - 2026-06-24

### Changed

- Split the monolithic `src/main.rs` prototype into library modules aligned
  with architecture boundaries: `model`, `inputs`, `sim`, `actors`, `replay`,
  `artifact`, `debrief`, and `cli`.
- Reduced the binary entry point to a thin `main()`; gameplay logic now lives
  under `src/lib.rs` module tree.
- Bumped package version from `0.1.15` to `0.1.16`.

### Notes

- All 78 existing tests pass unchanged in behavior; tests remain in `main.rs`
  pending a follow-up colocation slice.

## [0.1.15] - 2026-06-24

### Added

- Added versioned `replay-artifact-0.1.15` serialize, deserialize, and verify
  helpers for committed run history.
- Added optional post-run replay artifact export prompt in the CLI.
- Added focused tests for artifact round-trip, corruption handling, golden
  header stability, and interactive/preset history alignment.
- Added internal playtest findings for the four-turn vertical slice.

### Changed

- Bumped package version from `0.1.14` to `0.1.15`.
- Moved the merged per-turn interactive play slice into completed project state.

## [0.1.14] - 2026-06-24

### Added

- Added per-turn interactive command entry as the default CLI play mode.
- Added play-mode selection between interactive play and three preset strategy
  paths.
- Added executive turn briefings and concise turn-resolution summaries for
  interactive play.
- Added pure command parsers and `build_history_interactive` for testable
  interactive history construction.
- Added focused tests for play-mode parsing, command parsing, interactive
  history replay, and briefing purity.

### Changed

- Bumped package version from `0.1.13` to `0.1.14`.
- Preset strategy paths 1–3 remain available for regression and quick play.
- Moved the merged CLI dashboard preview slice into completed project state.

## [0.1.13] - 2026-06-24

### Added

- Added a starting executive dashboard to the CLI.
- Added strategy commitment previews for the three compiled strategy paths.
- Added focused tests for dashboard content, preview coverage, and avoiding
  future actor-outcome leakage in previews.

### Changed

- Bumped package version from `0.1.12` to `0.1.13`.
- Updated project-state bookkeeping for the merged state-hash replay proof.

## [0.1.12] - 2026-06-24

### Added

- Added stable per-transition state hashes over canonical state records.
- Added replay verification that detects committed state-hash drift.
- Added focused tests for deterministic hashing and hash mismatch detection.

### Changed

- Bumped package version from `0.1.11` to `0.1.12`.
- Updated demo output from state fingerprints to state hashes.
- Corrected project-state bookkeeping for the merged Phase 3 actor/scenario
  design slice.

## [0.1.11] - 2026-06-24

### Added

- Added a Phase 3 actor-card template for future strategic actor design.
- Added a first scenario brief for the regional-market stabilization slice.
- Updated workspace handoff artifacts for the actor/scenario design
  continuation.

### Changed

- Bumped package version from `0.1.10` to `0.1.11`.
- Updated project state to move the Phase 2 boundary slice into completed
  history.

## [0.1.10] - 2026-06-24

### Added

- Expanded the Phase 2 system-boundary and ontology draft for the current
  fictional regional US market slice.
- Added clearer actor, authority, observation, command, causal-category, and
  exclusion boundaries for future contributors.
- Added evidence-registry notes tying current mechanisms to roadmap scope while
  keeping prototype formulas labeled as abstractions.

### Changed

- Bumped package version from `0.1.9` to `0.1.10`.
- Corrected project-state bookkeeping for the merged coalition and observation
  revision work.

## [0.1.9] - 2026-06-23

### Added

- Added prior-period access measurement revisions via a named revision stream in
  resolved inputs.
- Added observation revision notes to the educational debrief without rewriting
  committed history.
- Added focused tests for genesis revision bounds, later-turn revision
  briefings, and debrief revision notes.
- Added initial `docs/system-boundary.md` and `docs/evidence-registry.md`
  design stubs.

### Changed

- Bumped package version from `0.1.8` to `0.1.9`.
- Updated ruleset version to `demo-ruleset-0.1.9`.
- Updated golden trajectory pinning for observation revision inputs.

## [0.1.8] - 2026-06-23

### Added

- Added a fourth-turn regional access coalition command with coalition liaison
  decisions and inspectable rationales.
- Added coalition investment and shared access commitment validation.
- Added a named coalition leverage stream to resolved inputs.
- Extended strategy paths with fourth compiled coalition posture presets.
- Added focused tests for coalition determinism, validation failures, unfavorable
  coalition outcomes, four-transition replay, and updated golden trajectory
  pinning.

### Changed

- Bumped package version from `0.1.7` to `0.1.8`.
- Extended demo history from three to four transitions.
- Updated educational debrief to include coalition rationales and a coalition
  tradeoff prompt.
- Moved the merged workforce pressure slice into completed project state.

## [0.1.7] - 2026-06-23

### Added

- Added a third-turn workforce pressure response command with nursing workforce
  representative decisions and inspectable rationales.
- Added retention spend and schedule relief validation for workforce commands.
- Extended strategy paths with third compiled workforce posture presets.
- Added focused tests for workforce determinism, validation failures, unfavorable
  labor outcomes, three-transition replay, and updated golden trajectory pinning.

### Changed

- Bumped package version from `0.1.6` to `0.1.7`.
- Extended demo history from two to three transitions.
- Updated educational debrief to include labor rationales and a workforce
  tradeoff prompt.
- Moved the merged seeded stochastic input boundary into completed project state.

## [0.1.6] - 2026-06-23

### Added

- Added a seeded stochastic input boundary with named streams for measurement
  noise, delayed access reporting, labor pressure, and policy signal resolution.
- Added optional CLI seed input with default seed `42`.
- Added focused tests for seed parsing, resolver determinism, seed variation,
  and canonical demo trajectory pinning.

### Changed

- Bumped package version from `0.1.5` to `0.1.6`.
- Removed per-path hard-coded `ResolvedInputs` from strategy plans.
- Moved the merged playable CLI slice into completed project state.

## [0.1.5] - 2026-06-23

### Added

- Added a minimal playable CLI choice over the deterministic two-turn demo.
- Added hard-coded access stabilization, fiscal caution, and aggressive
  bargaining strategy paths.
- Added focused tests for CLI choice parsing, invalid choices, path replay, and
  non-default actor outcomes.

### Changed

- Bumped package version from `0.1.4` to `0.1.5`.
- Moved the merged educational debrief slice into completed project state.

## [0.1.4] - 2026-06-23

### Added

- Added a deterministic educational debrief to the scripted two-turn demo.
- Added focused tests for actor rationale coverage, attributed tradeoff
  coverage, and deterministic debrief output.

### Changed

- Bumped package version from `0.1.3` to `0.1.4`.
- Updated project state and handoff documentation for the debrief slice.

## [0.1.3] - 2026-06-23

### Added

- Added a deterministic state-policy response command to the scripted demo.
- Added state policy official decisions with inspectable rationales for
  flexibility, mandate continuation, and oversight escalation.
- Extended demo replay to cover a two-transition history.
- Added focused tests for policy response determinism, validation failures,
  unfavorable valid policy outcomes, and two-transition replay.

### Changed

- Bumped package version from `0.1.2` to `0.1.3`.
- Updated project state and handoff documentation for the policy-process slice.

## [0.1.2] - 2026-06-23

### Added

- Replaced the placeholder CLI with a scripted deterministic architecture proof.
- Added typed world state, player command validation, resolved inputs,
  actor-specific observation, commercial-insurer decision rationale, attributed
  effects, append-only history, replay, and focused unit tests.
- Added `_workspace/` handoff artifacts for request framing, evidence mapping,
  and mechanism design.

### Changed

- Bumped package version from `0.1.1` to `0.1.2`.
- Updated `SPEC.md` and `ARCHITECTURE.md` to reflect the implemented prototype
  instead of a placeholder executable.

## [0.1.1] - 2026-06-23

### Added

- Initiated root-level spec-driven-development documents:
  - `SPEC.md`
  - `ARCHITECTURE.md`
  - `CHANGELOG.md`
- Initiated `LESSONS.md` for durable development lessons.

### Changed

- Bumped package version from `0.1.0` to `0.1.1` for this PR-equivalent
  documentation change.

## [0.1.0] - Initial

### Added

- Initial Rust package scaffold.
- Canonical project proposal, roadmap, and design principles.
- Repo-local health-policy strategy game agent harness.
