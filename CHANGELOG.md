# Changelog

All notable project changes should be recorded here.

The project follows lightweight semantic versioning during early development.

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
