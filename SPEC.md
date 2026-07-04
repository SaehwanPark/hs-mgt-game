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
| CLI scenario loader selection | v0.1.42 | CLI `--scenario` / `-s` flag to load arbitrary stabilization-v1 TOML scenarios | 219 | `88d07f9e1bbd6f04` (competitive) |
| Automated MCP playtest findings | v0.1.43 | Three-strategy MCP playtest report for stabilization and competitive-preview campaigns | 224 | `88d07f9e1bbd6f04` (competitive) |
| Playtest-guided player guidance | v0.1.44 | Insurer leverage and recruitment-timing guidance from automated playtest findings | 228 | `88d07f9e1bbd6f04` (competitive) |
| SDD next-development cleanup | v0.1.45 | SPEC Future tracks made actionable; stale companion doc statuses refreshed | 228 | `88d07f9e1bbd6f04` (competitive) |
| Deferred item triage | v0.1.46 | Worthy deferred Past items folded into actionable Future tracks | 228 | `88d07f9e1bbd6f04` (competitive) |
| AI-agent playtest validation pivot | v0.1.47 | Phase 7 validation docs moved from external human recruitment to reproducible AI-agent playtests | 228 | `88d07f9e1bbd6f04` (competitive) |
| Feedback-aligned future planning | v0.1.48 | External feedback translated into validation-first SDD Future tracks | 228 | `88d07f9e1bbd6f04` (competitive) |
| AI-agent playtest evidence | v0.1.49 | Automated Phase 7 MCP playtest batch completed and findings recorded | 228 | `88d07f9e1bbd6f04` (competitive) |
| Competitive final debrief metrics | v0.1.50 | MCP competitive end-session debrief reports final player tradeoff metrics from committed history | 230 | `88d07f9e1bbd6f04` (competitive) |
| Seed-variation playtest evidence | v0.1.51 | Scripted MCP playtest batch completed across seeds 42, 43, and 44 | 230 | `88d07f9e1bbd6f04` (competitive) |
| Naive-profile playtest evidence | v0.1.52 | Scripted MCP playtest batch added a naive first-time profile across seeds 42, 43, and 44 | 230 | `88d07f9e1bbd6f04` (competitive) |
| Campaign test fallback fix | v0.1.53 | PTY-backed competitive campaign tests use fallback input instead of blocking | 230 | `88d07f9e1bbd6f04` (competitive) |
| Free-form agent playtest evidence | v0.1.54 | One free-form first-time profile completed both current MCP campaigns at seed 42 | 230 | `88d07f9e1bbd6f04` (competitive) |
| Free-form profile synthesis | v0.1.55 | Two additional free-form profiles completed both current MCP campaigns at seed 42 | 230 | `88d07f9e1bbd6f04` (competitive) |
| Strategy-space diagnostics | v0.1.56 | Lightweight diagnostics over existing scripted and free-form MCP playtest evidence | 230 | `88d07f9e1bbd6f04` (competitive) |
| Competitive guidance & debrief hardening | v0.1.57 | Expanded competitive command help, monthly prompt cues, and capital projects strategic lesson | 230 | `88d07f9e1bbd6f04` (competitive) |
| AI-agent playtest synthesis | v0.1.58 | Follow-up free-form playtest sessions at seed 42 verifying guidance changes | 230 | `bf0414a383634dd6` (competitive) |
| Debrief quality as product surface | v0.1.59 | Enhanced competitive end-session debrief with detailed player/rival action logs | 231 | `bf0414a383634dd6` (competitive) |
| Clippy CI / release automation | v0.1.60 | Enforce clippy checks in CI and resolve 32 compiler warnings/errors | 231 | `bf0414a383634d| SPEC.md cleanup and version bump | v0.1.61 | Archive old SPEC items to spec-past-archive.md, simplify Present section | 231 | `bf0414a383634dd6` (competitive) |
| Public playable prototype announcement prep | v0.2.0 | Public README, old README archive, repo hygiene cleanup, milestone version bump | 231 | `bf0414a383634dd6` (competitive) |
| Post-v0.2 SDD progress review | v0.2.1 | Review current prototype progress and rank next development tracks | 231 | `bf0414a383634dd6` (competitive) |
| Instructor-visible run summary & decision-quality review | v0.2.2 | Compare observed vs true state in stabilization and detailed observed/unobserved rival actions in competitive | 233 | `bf0414a383634dd6` (competitive) |
| Exemplary scenario brief | v0.2.3 | Draft the first exemplary scenario brief for the competitive campaign modeling workforce and payer conflicts | 233 | `bf0414a383634dd6` (competitive) |
| Evidence ledger (Workforce) | v0.2.4 | Create parameter/evidence ledger for Nursing Workforce & Retention; update evidence registry | 233 | `bf0414a383634dd6` (competitive) |
| Competitive campaign autocomplete hardening | v0.2.5 | Implement argument-key and enum-value autocomplete in the CLI REPL for competitive campaigns | 237 | `bf0414a383634dd6` (competitive) |
| Competitive debrief decision-quality review | v0.2.6 | Implement deterministic checks (runway, workforce trust, payer posture, rival response) in competitive debrief | 238 | `bf0414a383634dd6` (competitive) |
| AI Rationale Visibility Hardening | v0.2.7 | Dynamically track and display visibility sources for rival AI rationales in debrief and instructor summaries | 241 | `bf0414a383634dd6` (competitive) |
| Competitive Month-Summary Clarity | v0.2.8 | Display player's resolved commands, rival public action details, resolved effects, and next month's resources | 242 | `bf0414a383634dd6` (competitive) |


- Feature: Competitive Month-Summary Clarity
  Status: Complete
  Started: 2026-07-04
  Version: 0.2.8

  Summary:
  Enhanced the month resolution summary in the competitive campaign CLI to display player's resolved commands, detailed rival public actions, resolved attributed effects, and next month's starting resources.

  Done:
  - Formatted and printed the player's resolved commands in `resolution_summary_lines`.
  - Detailed each logged public action for the resolved month with system name and entry summary.
  - Formatted and listed resolved `AttributedEffect` entries.
  - Displayed the player's next-month starting resources.
  - Added unit test in `src/competitive/resolution.rs` validating formatting output correctness.
  - Bumped package version to `0.2.8`.

  Deferred / Non-Goals:
  - No changes to stabilization campaign resolution rules.
  - No database or telemetry collection addition.
  - State transition calculations and golden hash values remain unchanged.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test` (all 242 tests pass)

- Feature: AI Rationale Visibility Hardening
  Status: Complete
  Started: 2026-07-04
  Version: 0.2.7

  Summary:
  Dynamically track and display visibility sources for rival AI rationales in both student-facing debriefs and instructor summaries.

  Done:
  - Check and attribute rival AI rationales to `(observed via monitor)` or `(observed via public disclosure)` in `competitive_debrief`.
  - Refactor `competitive_instructor_summary` to attribute rationale visibility source dynamically during instructor review, showing `(unobserved during play - REVEALED FOR INSTRUCTOR REVIEW)` only for private, unobserved actions.
  - Colocate comprehensive unit tests in `src/debrief/report_tests.rs` covering all visibility state combinations.
  - Bump package version to `v0.2.7`.

  Deferred / Non-Goals:
  - No changes to stabilization campaign debrief structure.
  - No changes to core simulation transition logic or scenario files.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test` (all 241 tests pass)

- Feature: Competitive debrief decision-quality review
  Status: Complete
  Started: 2026-07-04
  Version: 0.2.6

  Summary:
  Implement a deterministic Decision-Quality Assessment block inside the competitive campaign debriefing system.

  Done:
  - Add `analyze_decision_quality` to `src/debrief/report.rs` evaluating cash runway safety, workforce trust drops, aggressive payer negotiation postures without leverage, and unanswered rival capacity expansion.
  - Append the decision-quality feedback to `competitive_instructor_summary`.
  - Add comprehensive unit tests in `src/debrief/report_tests.rs` to verify each strategic warning check triggers under mock transition states.
  - Bump package version to `0.2.6` across the package tracking files.

  Deferred / Non-Goals:
  - No LMS integration or automatic scoring.
  - No changes to stabilization campaign debrief logic.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test` (all 238 tests pass)

- Feature: Competitive campaign autocomplete hardening
  Status: Complete
  Started: 2026-07-03
  Version: 0.2.5

  Summary:
  Extend the competitive campaign CLI REPL autocompletion capability to support argument keys and enum values, ensuring no filesystem completion is triggered, deduplicating keys, and adding unit tests.

  Done:
  - Implement segment parsing in `src/cli/repl.rs` to identify current word being completed under cursor.
  - Complete argument keys (e.g. `domain=`) after space/key-prefix, excluding keys already present in segment.
  - Complete enum values (e.g. `beds`) after a key's `=`.
  - Add comprehensive unit tests in `src/cli/repl.rs` for argument key, enum value, and batch command autocomplete.
  - Bump project version to `0.2.5` in Cargo.toml.

  Deferred / Non-Goals:
  - No autocomplete for integer arguments.
  - No changes to stabilization campaign prompt behavior.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test` (all 237 tests pass)
  - `python3 scripts/run_automated_playtests.py`

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

- Feature: SPEC.md cleanup and version bump
  Status: Complete
  Started: 2026-07-03
  Version: 0.1.61

  Summary:
  Clean up SPEC.md to make the Past-Present-Future distinction straightforward and comprehensible. Archive completed slices older than the six most recent ones into docs/spec-past-archive.md. Simplify the Present section, and bump the project version to v0.1.61.

  Done:
  - Archive features from v0.1.40 through v0.1.55 into `docs/spec-past-archive.md`.
  - Retain only the six most recent slices (v0.1.56 through v0.1.61) in the active `SPEC.md` list.
  - Simplify the `## Present` section, removing the completed-features wall of text and outlining the active cleanup task.
  - Bump project version in Cargo.toml, Cargo.lock, and CHANGELOG.md.

  Deferred / Non-Goals:
  - No changes to transition rules, simulation physics, or state serialization logic.

  Verification:
  - All unit and integration tests pass successfully (231 tests).
  - `git diff` shows correct file movements.

- Feature: Clippy CI / release automation
  Status: Complete
  Started: 2026-07-03
  Version: 0.1.60

  Summary:
  Enforce strict code quality checking by adding Clippy validations to the GitHub Actions CI pipeline and fixing all 32 existing clippy lints across the codebase.

  Done:
  - Add `cargo clippy --all-targets -- -D warnings` step to `.github/workflows/ci.yml`
  - Refactor manual prefix checking/slicing to use `.strip_prefix()` in `src/artifact/parse.rs`, `src/artifact/session_save.rs`, and `src/artifact/verify.rs`
  - Collapse nested conditional `if` blocks into single `if` statements with `&&`
  - Define custom type aliases for complex type signatures in `src/cli/session.rs` and `src/mcp/session.rs`
  - Replace manual out-of-bounds check with `RangeInclusive::contains()` in `src/artifact/session_save.rs`
  - Annotate unused variables/imports and dead-code constants/functions with appropriate compiler warnings/dead code attributes
  - Bump package version to `0.1.60` in `Cargo.toml`

  Deferred / Non-Goals:
  - No changes to transition rules, simulation physics, or state serialization logic
  - No new MCP endpoints
  - No changes to gameplay or user-facing output messages

  Verification:
  - `cargo clippy --all-targets -- -D warnings` passes with zero warnings or errors
  - `cargo test` passes cleanly with all 231 tests

- Feature: Debrief quality as product surface
  Status: Complete
  Started: 2026-07-02
  Version: 0.1.59

  Summary:
  Enhance the competitive end-session debriefing logic to provide a detailed history log of player commands, rival commands (categorized by publicly disclosed, observed via monitor, or unobserved by you), events, and effects.

  Done:
  - Implement helper `format_command_debrief` in `src/mcp/session.rs` for formatting competitive commands
  - Update `competitive_debrief` to trace player and rival actions, mapping monitored status correctly
  - Output aggregated mechanisms and events in the end-session debrief
  - Add test coverage for detailed history trace and correct observation labels
  - Package version bumped to `0.1.59`

  Deferred / Non-Goals:
  - No changes to transition rules, simulation physics, or state serialization
  - No new MCP endpoints
  - No changes to stabilization campaign debrief structure

  Verification:
  - `cargo test` passes cleanly with 231 tests
  - `cargo fmt --check` passes
  - Automated playtests run and compare successfully

- Feature: AI-agent playtest synthesis
  Status: Complete
  Started: 2026-07-02
  Version: 0.1.58

  Summary:
  Execute follow-up free-form playtest sessions under the new v0.1.57 command help and prompt cues to verify if the guidance successfully reduces Hold overuse and aids first-time play understanding. Document the findings in docs/playtest-findings-v0.1.58.md.

  Done:
  - Run follow-up free-form playtest sessions for the `stabilization-v1` and `competitive-regional-v1` campaigns with seed 42
  - Verify that the agent utilizes the expanded command help (typing `?` or `help`) and uses commands like `project`, `recruit`, and `negotiate` instead of defaulting to `hold` where appropriate
  - Update `CHANGELOG.md` and `SPEC.md` to document the new playtest findings and present version bump
  - Package version bumped to `0.1.58`

  Deferred / Non-Goals:
  - No changes to core simulation transition logic, model structures, or validation thresholds
  - No changes to scenario TOML files or the campaign selection flow
  - No changes to golden hashes (the golden hashes for seed 42 must remain identical to main)
  - No new MCP endpoints or DTO changes

  Verification:
  - All automated playtests pass successfully
  - All unit and integration tests (230+) run and pass
  - `cargo fmt --check` passes
  - Playtest report matches the structure in `docs/agent-playtest-protocol.md`

- Feature: Competitive guidance & debrief hardening
  Status: Complete
  Started: 2026-07-02
  Version: 0.1.57

  Summary:
  Expand competitive command help with detailed descriptions and resource costs for all 7 verbs, update the monthly command prompt printing to explicitly cue ?/help for the command manual, and add a strategic projects lesson to the competitive end-session debrief to address playtest gaps.

  Done:
  - `src/cli/guidance.rs` `PromptContext::CompetitiveCommand` help text details effects, AP, cash, and political capital costs for all 7 competitive verbs
  - `src/cli/campaign.rs` and `src/cli/repl.rs` update prompt label to cue "? or help" for detailed command descriptions
  - `src/mcp/session.rs` `competitive_debrief` adds a strategic lesson about Action Points, monthly cash draws, duration, and concurrency limits of capital projects
  - Package version bumped to `0.1.57`

  Deferred / Non-Goals:
  - No changes to transition logic, simulation rules, scenario schemas, validation thresholds, or campaign selection
  - No changes to stabilization campaign help or debrief logic
  - No database or telemetry collection addition

  Verification:
  - Spoiler-free tests, MCP session tests, and all 230+ cargo tests pass successfully
  - `cargo fmt --check` passes

- Feature: Strategy-space diagnostics
  Status: Complete
  Started: 2026-07-02
  Version: 0.1.56

  Summary:
  Synthesize existing scripted and free-form MCP findings into a lightweight
  Phase 7 strategy-space diagnostic artifact, with strategy clusters, outcome
  ranges, action-frequency signals, evidence limits, and follow-up routing
  before any balance work.

  Done:
  - `docs/playtest-findings-v0.1.56.md` summarizes v0.1.51, v0.1.52, v0.1.54,
    and v0.1.55 evidence across both current campaigns
  - Stabilization diagnostics distinguish fiscal caution, access/capacity
    growth, balanced access, and naive low-complexity clusters
  - Competitive diagnostics identify passive/fiscal, scripted fiscal caution,
    capacity/access growth, and balanced/free-form clusters
  - Action-frequency signals note repeated use of monitor and access pledges,
    passive-profile overuse of `hold`, and no captured `project` use in the
    three-month preview
  - Package version bumped to `0.1.56`

  Deferred / Non-Goals:
  - No new MCP session matrix, LLM runner, diagnostics tooling, transition
    behavior, ruleset, scenario schema, replay format, MCP DTO, campaign length,
    active observation surface, golden hash, runtime guidance, or balance tuning
    changed
  - No human learning claim, empirical calibration claim, policy forecast claim,
    equilibrium analysis, or formula tuning from this diagnostic artifact

  Verification:
  - Diagnostic claims cite already-captured findings and preserve evidence
    limits
  - Rust checks, scripted MCP regression batch, and diff checks completed for
    the slice

## Present

No active slice.

## Future

### Ranked next-development queue

The first runnable prototype is complete enough that the next risk is not
engine proof. The next risk is whether repeated play remains explainable,
teachable, and strategically interesting before the project expands mechanics,
campaign length, or platform architecture.

1. Track: Competitive campaign hardening
  Phase / Gate: Phase 6/7; proceed only after playtest findings identify a
  concrete comprehension, pacing, exploit, or command-entry issue.

  Next actionable slice:
  Pick one bounded issue from playtest evidence, such as month-summary clarity,
  command help coverage, AI rationale visibility, or a three-month pacing problem
  (argument-key and enum-value autocomplete completed in v0.2.5), and address
  it without expanding campaign length.

  Verification target:
  Focused CLI/parser/simulation tests cover the changed behavior, competitive
  seed-42 golden hash is unchanged unless transition semantics intentionally
  change, and player-facing docs explain any new guidance.

  Deferred / Non-Goals:
  Full 24-month campaign loop, competitive autosave, competitive replay export,
  competitive scenario loading, multiplayer, and new strategic actor classes.

2. Track: Strategy-space diagnostics
  Phase / Gate: Phase 7; keep as analysis artifacts until repeated review needs
  justify tooling.

  Next actionable slice:
  Write a lightweight diagnostic report over newly captured runs, or implement
  dedicated tooling only after repeated playtest or authoring work needs
  action-frequency, outcome-distribution, or strategy-cluster extraction.

  Verification target:
  The diagnostic links claims to captured runs, separates simulated-player
  behavior from interpretation, and names which findings should affect guidance,
  debriefing, balance, or future tooling. No formula tuning should happen from a
  single profile, seed, or campaign.

  Deferred / Non-Goals:
  No analytics platform, policy forecast validation, automated optimization
  framework, or runtime export change unless a later slice proves the need.

3. Track: AI-agent playtest synthesis
  Phase / Gate: Phase 7 prep; use `docs/agent-playtest-protocol.md`,
  `docs/mcp-playtesting-guide.md`, and versioned findings as the evidence
  baseline.

  Next actionable slice:
  Review subsequent playtest findings under longer campaign horizons, different
  difficulty tiers, or new debrief/instructor-analysis surfaces when available.

  Verification target:
  Follow-up findings cite session counts, campaign(s), seeds, difficulty, agent
  profiles or prompts, actor-visible observations, submitted commands,
  validation failures, histories, debriefs, diagnostic summaries, evidence
  limits, and prioritized recommendations.

  Deferred / Non-Goals:
  No external human recruitment gate, formal human-subjects research process,
  measured human-learning claim, empirical calibration claim, scoring redesign,
  or broad balance pass.

4. Track: MCP agent interface expansion
  Phase / Gate: Agent-play support; proceed only after bounded stdio play
  exposes a specific need that cannot be met through current tools.

  Next actionable slice:
  Add one evidence-backed MCP improvement, such as a richer observation summary,
  safer error payload, or playtest automation affordance, while preserving the
  local stdio boundary.

  Verification target:
  MCP session tests cover both campaigns, invalid-command non-advancement,
  bounded completion, and same-seed determinism. Tool DTO shape changes are
  documented in `docs/mcp-agent-interface.md`.

  Deferred / Non-Goals:
  HTTP transport, auth, durable session persistence, multi-client coordination,
  full competitive campaign length, and replay/export integration.

5. Track: Broader simulation breadth and new strategic actors
  Phase / Gate: Phase 6.1; proceed only after playtest, instructor, scenario, or
  domain-review evidence shows that current campaign limits block meaningful
  strategy or learning.

  Next actionable slice:
  Add one bounded breadth element, such as one service-line decision, one patient
  or distributional outcome category, one capital-allocation tradeoff, one
  market-area concept, one additional strategic interaction, or one localized
  Medicare/Medicaid actor interaction.

  Verification target:
  The new mechanism has a documented actor/observation boundary, deterministic
  tests, debrief attribution, and clear player-facing tradeoffs. Public-payer
  work must distinguish actor utility from social welfare and label
  evidence-backed mechanisms versus design abstractions.

  Deferred / Non-Goals:
  Full US health-system model, individual patient simulation, broad federal
  policy lifecycle framework, national policy simulation, federal budget
  modeling, full Medicaid eligibility rules, Medicare payment reproduction,
  global equilibrium AI, and speculative generalized frameworks.

6. Track: Architecture and documentation discipline
  Phase / Gate: Cross-cutting SDD; apply before promoting any Future item into
  Present.

  Next actionable slice:
  Freeze major abstractions by default. Permit new architecture, scenario
  generalization, or documentation taxonomy only when a playtest, authoring, QA,
  or debrief finding names a concrete need that current structures cannot meet.

  Verification target:
  New slices cite the finding that justifies the abstraction, preserve
  deterministic replay boundaries, and record non-goals. Documentation updates
  should reduce ambiguity for future agents rather than expand the conceptual
  framework without validation evidence.

  Deferred / Non-Goals:
  No broad framework expansion, reusable comparative-policy platform work, or
  research-grade calibration until the compact educational strategy simulation
  proves difficult, legible, and interesting decisions.

7. Track: Release automation and contributor readiness
  Phase / Gate: Phase 0/8; proceed when contributor-readiness or release
  preparation becomes the active priority.

  Next actionable slice:
  Add one lightweight quality or release check with documented local command
  usage, starting with non-invasive checks before release packaging.

  Verification target:
  Local command passes, CI documentation is updated, and the change does not
  alter simulation behavior or require new release conventions beyond
  `docs/versioning-policy.md`.

  Deferred / Non-Goals:
  Public release packaging, publication automation, data/licensing finalization,
  or broad repository restructuring.
