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
| Competitive design + runtime I1–I3 | v0.1.28–v0.1.30 | Design package, campaign router, action economy validation | 148 | `6fb1ebbea564274f` |

### Recent slices

- Feature: Forecast and uncertainty CLI preview
  Status: Complete
  Started: 2026-06-24
  Branch: feat/forecast-uncertainty-preview

  Summary:
  Add bounded observation-only uncertainty preview before each interactive turn
  and an observation note on the starting dashboard without changing transition
  logic or golden trajectories.

  Done:
  - `src/cli/display/forecast.rs` with turn uncertainty preview helper
  - Preview wired into interactive session before executive briefings
  - Observation uncertainty note on starting executive dashboard
  - Focused forecast preview tests; playtest findings v0.1.25
  - Package version bumped to `0.1.25`

  Deferred / Non-Goals:
  - No probabilistic forecast objects
  - No changes to `transition()`, hash semantics, or random streams

  Verification:
  - Golden hash `6fb1ebbea564274f` unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass (86 tests)

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

## Present

- Feature: Competitive campaign runtime I4
  Status: Active
  Started: 2026-06-24
  Branch: feat/competitive-multi-system-state

  Summary:
  Add `CompetitiveWorldState` with K+1 `HealthSystemState` entities, player
  slots, and difficulty-scoped genesis fixtures per ADR-0004. No
  `transition_competitive()` yet.

  Done:
  - (populated during implementation)

  Not Yet Done:
  - `CompetitiveWorldState`, `SharedMarketFields`, `HealthSystemState`,
    `PlayerSlot` types
  - Difficulty-scoped genesis fixtures (Easy–Expert)
  - Competitive stub roster/summary display from genesis (not mock-only)
  - Focused genesis and sizing tests; stabilization golden unchanged

  Deferred / Non-Goals:
  - `transition_competitive()` and monthly loop (I5)
  - AI players, events, Stata CLI (I6–I8)
  - Stabilization `WorldState` or golden hash changes
  - Replay artifact version bump for competitive runs

  Verification:
  - `systems.len() == K+1` for each `Difficulty` tier
  - Human player assigned to system 0; K AI slots with profiles
  - Golden stabilization hash unchanged at seed 42
  - `cargo fmt --check`, `cargo test` pass

## Future

- **Competitive campaign runtime I5** — simultaneous monthly action resolver
  and partial rival observability.
- **Competitive campaign runtime I6** — bounded game-theory AI players with
  rationales.
- **Competitive campaign runtime I7** — random events, delayed effect queue,
  annual policy tick.
- **Competitive campaign runtime I8** — Stata-like CLI (grammar, color, autocomplete,
  help).
- **External playtest protocol refresh** (Phase 7 prep): structured external
  session protocol.
- **Medicare/Medicaid strategic actors** (Phase 5.1 / 6.1, gated): excluded from
  first scenario until brief expands; actor cards required first.
- **Scenario data loading runtime** (Phase 6.2): after format design approval;
  see [`docs/scenario-format-draft.md`](docs/scenario-format-draft.md).
- **Clippy CI / release automation** (Phase 0 / 8): explicitly deferred.
