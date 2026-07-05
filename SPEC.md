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
| Competitive Command Help Coverage | v0.2.9 | Support querying detailed help for specific commands (e.g. 'help recruit' or '? invest') in the competitive REPL | 244 | `bf0414a383634dd6` (competitive) |
| Clinical Service Lines and Staffing | v0.3.0 | Distinguish inpatient beds/outpatient clinics and implement nurses/physicians/admins staffing constraints | 246 | `a49a2f80540ecd9b` (competitive) |
| Competitive Scenario Loading and Validation | v0.4.0 | Load and validate custom multi-system scenarios for competitive campaigns via --scenario CLI option | 249 | `e73a38b3951cd8b6` (competitive) |
| Competitive Campaign Extension & Autosave | v0.5.0 | Extend competitive duration to 24 months, add autosave/resume, and replay export | 252 | `e73a38b3951cd8b6` (competitive) |
| Versioning Policy Alignment | v0.5.1 | Align version history and policy docs with repository governance standards | 252 | `e73a38b3951cd8b6` (competitive) |
| Test Hang and Playtest Fixes | v0.5.2 | Fix test suite hangs under interactive stdin and index out of bounds in playtests | 252 | `e73a38b3951cd8b6` (competitive) |
| Strategy-Space Diagnostics Tooling | v0.5.3 | Implement offline replay diagnostics script for strategy cluster and resource outcome analysis | 252 | `e73a38b3951cd8b6` (competitive) |
| MCP Custom Scenario Loading | v0.5.4 | Implement custom scenario path loading in the MCP start_session tool with validation and tests | 255 | `e73a38b3951cd8b6` (competitive) |
| Medicaid Public Payer Integration | v0.5.5 | Add Medicaid public payer, posture validation, resource costing, and access compliance effects | 261 | `e73a38b3951cd8b6` (competitive) |
| Competitive Exemplary Scenario | v0.5.6 | Add competitive-exemplary-v1 scenario, workforce wage settlements, nurse strike, CON legal challenge, and Blue Shield/EHR consequences | 260 | `e73a38b3951cd8b6` (competitive) |
| Medicare Public Payer Integration Plan | v0.5.7 | Design Medicare public payer quality-compliance integration plan | 260 | `e73a38b3951cd8b6` (competitive) |
| Medicare Public Payer Integration | v0.5.8 | Implement Medicare public payer quality compliance, validation, CLI REPL autocompletes, topic help, and unit tests | 270 | `e73a38b3951cd8b6` (competitive) |
| Active Projects Display Hardening | v0.5.9 | Harden competitive campaign CLI dashboard by detailing in-flight projects, durations, and monthly cash draws | 271 | `e73a38b3951cd8b6` (competitive) |
| Emergency Department Service Line | v0.6.0 | Add Emergency Department service line with capacity-staffing trade-offs, hierarchical staffing, and new command verbs | 272 | `0930e2bf6890aaba` (competitive) |
| ICU Service Line & ED Boarding | v0.7.0 | Add Intensive Care Unit service line, high-intensity staffing targets, ICU-first hierarchical allocation, and ED boarding bottleneck mechanics | 273 | `2904083fb91b2770` (competitive) |
| Obstetrics/L&D Service Line & Diversion Mechanics | v0.8.0 | Add Obstetrics service line, staffing targets, Obstetrics-second hierarchical allocation, and diversion mechanics under deficit | 274 | `e57cc6377e17ea09` (competitive) |
| Psychiatric Service Line & ED holding/diversion mechanics | v0.8.1 | Add Psychiatric service line, staffing targets, Psychiatric-fourth hierarchical allocation, and ED holding boarding/diversion mechanics | 275 | `7bd8a0c7a8312f4e` (competitive) |
| Project Document Alignment and Version Bump | v0.8.2 | Align project documentation with implemented 24-month campaign loop, autosave, scenario loading, and new service line features | 275 | `7bd8a0c7a8312f4e` (competitive) |
| Externalize Scenario Timeline Events | v0.8.3 | Externalize scenario timeline events to TOML and generalize transition triggers | 275 | `7bd8a0c7a8312f4e` (competitive) |
| Cardiology Service Line & Cath Lab Mechanics | v0.8.4 | Add Cardiology service line, staffing targets, Cardiology-fourth hierarchical allocation, and ED holding boarding/diversion mechanics | 276 | `7a771bad0a222f34` (competitive) |
| Oncology & Infusion Service Lines | v0.9.0 | Add inpatient Oncology and outpatient Infusion service lines, staffing ratios, hierarchical priority queues, and ED boarding/diversion/deferral mechanics | 277 | `6044273e2c6c1374` (competitive) |


- Feature: Oncology & Infusion Service Lines
  Status: Complete
  Started: 2026-07-05
  Version: 0.9.0

  Summary:
  Implemented Oncology (Inpatient) and Infusion Center (Outpatient Chemotherapy) Service Lines with specialized capacity-staffing trade-offs, hierarchical nurse and physician allocations prioritizing Oncology 6th and Infusion 7th (before ED), and clinical overflow rules (Oncology ED boarding/diversion with `-2` trust/quality penalties; Infusion deferrals with `-1` trust/market share penalties).

  Done:
  - Added `oncology_capacity` and `infusion_capacity` to competitive system state, player observations, and pending effects.
  - Configured `InvestDomain` and `ProjectKind` (OncologyUnit = 9 months / 3 AP; InfusionCenter = 6 months / 2 AP).
  - Implemented nurse/physician staffing targets and priority allocation logic.
  - Implemented inpatient Oncology ED boarding/diversion and outpatient Infusion deferral rules.
  - Bumped competitive state hash version to v6 (`onco=`, `infuse=`) with golden hash `6044273e2c6c1374`.
  - Added CLI parsing, autocompletions, REPL guidance documentation, and executive dashboard layout updates.
  - Created comprehensive unit tests validating Oncology and Infusion capacities, staffing, and strike/boarding penalties.

  Deferred / Non-Goals:
  - None.

  Verification:
  - `cargo test` passes all 277 tests.


- Feature: Cardiology Service Line & Cath Lab Mechanics
  Status: Complete
  Started: 2026-07-05
  Version: 0.8.4

  Summary:
  Implemented Cardiology (Cardiovascular Care) Service Line and Cardiac Cath Lab infrastructure with capacity-staffing trade-offs, specialized staffing targets, hierarchical allocation prioritizing Cardiology fourth (after Med-Surg and before Psychiatric), and ED boarding/diversion mechanics.

  Done:
  - Added `cardiology_capacity` to system state structure and `CardiologyCapacity` to `PendingEffectKind`.
  - Added `InvestDomain::Cardiology` and `ProjectKind::CardiologyUnit` (6-month build time).
  - Implemented target staffing requirements and 4th-priority nurse/physician hierarchical allocation for Cardiology.
  - Implemented Cardiology ED holding boarding and diversion mechanics under capacity/staffing deficit (incurring `-2` community trust and `-2` quality index penalties).
  - Integrated Cardiology capacity and diversion into observation mapping, REPL executive dashboard, parser, autocomplete, and guidance help pages.
  - Created comprehensive unit tests validating Cardiology priority allocation, diversion penalties under deficit, and project resolution.
  - Updated competitive state hash to v5 (adding `cardio=`) with value `7a771bad0a222f34`.

  Deferred / Non-Goals:
  - None.

  Verification:
  - `cargo test` passes all 276 tests.


- Feature: Externalize Scenario Timeline Events
  Status: Complete
  Started: 2026-07-05
  Version: 0.8.3

  Summary:
  Externalized scenario timeline events from the transition core to scenario TOML files and generalized event trigger logic in the effects engine.

  Done:
  - Added parsing support for `[[timeline_events]]` in `src/scenario/mod.rs`.
  - Added `timeline_events` field to `CompetitiveWorldState` and initialized it from scenario TOML configurations.
  - Generalized scenario trigger logic in `transition_competitive.rs` and `effects_competitive.rs`.
  - Fixed technology project completion flag bug setting `ehr_project_fully_funded` state.

  Deferred / Non-Goals:
  - None.

  Verification:
  - `cargo test` passes all 275 tests.


- Feature: Project Document Alignment and Version Bump
  Status: Complete
  Started: 2026-07-05
  Version: 0.8.2

  Summary:
  Aligned project documentation with implemented 24-month campaign loop, autosave/resume, scenario loading, and new service line features.

  Done:
  - Updated `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `docs/roadmap.md`, `docs/how-to-play.md`, `docs/versioning-policy.md`, `docs/core-loop-spec.md`, `docs/system-boundary.md`, `docs/competitive-scenario-brief.md`, `docs/first-scenario-brief.md`, and `docs/agent-playtest-protocol.md` to remove outdated "three-month" and "deferred" statements.
  - Bumped Cargo package version to `0.8.2`.

  Deferred / Non-Goals:
  - None.

  Verification:
  - `cargo test` passes all 275 tests.


- Feature: Psychiatric Service Line & ED holding/diversion mechanics
  Status: Complete
  Started: 2026-07-05
  Version: 0.8.1

  Summary:
  Implemented the Psychiatric Service Line & ED holding/diversion mechanics with capacity-staffing trade-offs, hierarchical allocation prioritizing Psychiatric, and ED holding boarding/diversion mechanics.

  Done:
  - Added Psychiatric-specific staffing targets (1 nurse per 4 beds, 1 physician per 10 beds, 1 admin per 15 beds) to transition rules.
  - Implemented hierarchical staffing allocation prioritizing ICU first, Obstetrics second, Med-Surg third, Psychiatric fourth, Clinics fifth, and ED last.
  - Implemented Psychiatric ED holding boarding (psychiatric overflow boards in ED, consuming ED bays) and diversion mechanics under capacity/staffing deficit (incurring `-2` community trust and `-1` market share index penalties).
  - Added `InvestDomain::Psychiatric` for direct Psychiatric bed investments and `ProjectKind::PsychiatricUnit` for 6-month capital projects.
  - Integrated Psychiatric capacity and holding into observation mapping, REPL executive dashboard, parser, autocomplete, and guidance help pages.
  - Created comprehensive unit tests validating Psychiatric priority allocation, ED boarding, diversion penalties under deficit, and project resolution.
  - Updated `LESSONS.md` to document Psychiatric ED boarding test constraints and hierarchical staffing priority.

  Deferred / Non-Goals:
  - No changes to stabilization campaign loop rules.

  Verification:
  - cargo test (all 275 tests pass)


- Feature: Obstetrics/L&D Service Line & Diversion Mechanics
  Status: Complete
  Started: 2026-07-05
  Version: 0.8.0

  Summary:
  Implemented the Obstetrics/L&D Service Line & Diversion Mechanics.

  Done:
  - Added Obstetrics-specific staffing targets (1 nurse per 2 beds, 1 physician per 5 beds, 1 admin per 10 beds) to transition rules.
  - Implemented hierarchical staffing allocation prioritizing ICU first, Obstetrics second, Med-Surg third, Clinics fourth, and ED last.
  - Implemented Obstetrics diversion mechanics where patients are diverted if Obstetrics capacity is under-staffed or under-capacitated, incurring `-2` community trust and `-1` market share index penalties.
  - Added `InvestDomain::Obstetrics` for direct Obstetrics bed investments and `ProjectKind::ObstetricsUnit` for 9-month capital projects.
  - Integrated Obstetrics capacity and diversion into observation mapping, REPL executive dashboard, parser, autocomplete, and guidance help pages.
  - Created comprehensive unit tests validating Obstetrics priority allocation, diversion penalties under deficit, and project resolution.

  Deferred / Non-Goals:
  - No changes to stabilization campaign loop rules.

  Verification:
  - cargo test (all 274 tests pass)


- Feature: ICU Service Line & ED Boarding
  Status: Complete
  Started: 2026-07-05
  Version: 0.7.0

  Summary:
  Implemented the Intensive Care Unit (ICU) Service Line with high-intensity capacity-staffing trade-offs, hierarchical allocation prioritizing ICU, and ED boarding bottleneck mechanics where ICU overflow boarded in ED consumes emergency capacity.

  Done:
  - Added `icu_capacity` to health system state (defaulting to 0 for scenario compatibility).
  - Extended command vocabulary with `InvestDomain::Icu` and `ProjectKind::IcuWing` (12-month capital project, 3 AP cost).
  - Implemented high-intensity staffing targets (1 nurse per bed, 1 physician per 2 beds, 1 admin per 5 beds).
  - Implemented hierarchical staffing allocation order prioritizing ICU first, med-surg beds second, outpatient clinics third, and ED last.
  - Implemented ED Boarding mechanics (5% of med-surg beds require ICU, overflow board in ED, boarding reduces effective emergency capacity).
  - Updated CLI parsers, REPL autocompletes, guidance help topics, and state record hashes.
  - Added focused unit tests verifying ICU allocation, ED boarding, and capacity-deficit index penalties.

  Deferred / Non-Goals:
  - No changes to stabilization campaign loop rules.
  - No outpatient ICU equivalents or general federal payment models.

  Verification:
  - cargo test (all 273 tests pass)


- Feature: Emergency Department Service Line
  Status: Complete
  Started: 2026-07-05
  Version: 0.6.0

  Summary:
  Implemented the Emergency Department (ED) Service Line with capacity-staffing targets, hierarchical staffing constraints, immediate investments, capital pavilion projects, and full REPL integration.

  Done:
  - Added `emergency_capacity` tracking to health system state (defaults to 0 for backward-compatible scenario/genesis preservation).
  - Extended command vocabulary with `InvestDomain::Emergency` and `ProjectKind::EmergencyPavilion` (6-month capital duration).
  - Implemented staffing targets (1 nurse per 2 bays, 1 physician per 4 bays, 1 admin per 10 bays).
  - Implemented hierarchical staffing allocation prioritizing Med-Surg beds first, Outpatient clinics second, and Emergency third.
  - Formatted ED capacities and projects in human observations, REPL autocompletes, guidance help topics, and state record hashes.
  - Added focused unit tests and verified all regression tests pass.

  Deferred / Non-Goals:
  - No changes to stabilization campaign loop rules.
  - No ambulance diversion mechanics or specific pediatric ED capabilities.

  Verification:
  - cargo test (all 272 tests pass)


- Feature: Active Projects Display Hardening
  Status: Complete
  Started: 2026-07-05
  Version: 0.5.9

  Summary:
  Hardened the competitive campaign CLI dashboard by detailing in-flight projects (project kind, remaining months to completion, and monthly cash draw) instead of a simple count.

  Done:
  - Designed the comprehensive active projects detailed observation plan (workspace request summary, mechanism design, and domain QA review).
  - Updated `in_flight_projects_label` in `src/sim/observe_competitive.rs` to inspect the `effect_queue` and construct a detailed description of each active project.
  - Added unit test coverage for active project observation formatting.

  Deferred / Non-Goals:
  - No changes to stabilization campaign loop.
  - No changes to transition engine rules.

  Verification:
  - cargo test (all 271 tests pass)


- Feature: Medicare Public Payer Integration
  Status: Complete
  Started: 2026-07-05
  Version: 0.5.8

  Summary:
  Implement Medicare public payer quality-compliance integration in the competitive regional campaign loop, modeling quality improvements (+3 quality) and policy pressure reduction (-3 policy pressure) with neutral posture and $10 compliance costs.

  Done:
  - Designed the comprehensive Medicare integration plan (evidence mapping, mechanism design, and domain QA review).
  - Added `Medicare` variant to `PayerId` in `src/model/competitive_command.rs` and updated `resource_costs` ($10 cash).
  - Updated `parse_payer` in `src/cli/competitive_parse.rs` and CLI autocompletion/guidance helpers.
  - Implemented `InvalidMedicarePosture` validation check in `src/sim/validate_competitive.rs`.
  - Implemented quality compliance effects (+3 quality, -3 policy pressure) in `src/sim/transition_competitive.rs`.
  - Added focused unit tests for Medicare validation and transition outcomes in `validate_competitive_tests.rs` and `transition_competitive.rs`.
  - Bumped crate version to `0.5.8` and documented changes in `CHANGELOG.md` and `Cargo.toml`.
  - Switched working branch to `feat/medicare-payer-implementation`.

  Deferred / Non-Goals:
  - No Medicare patient cohort tracking or FFS DRG-based billing rules.
  - No changes to stabilization campaign loop.

  Verification:
  - cargo test (all 270 tests pass)


- Feature: Competitive Exemplary Scenario
  Status: Complete
  Started: 2026-07-04
  Version: 0.5.6

  Summary:
  Implemented the `competitive-exemplary-v1` scenario, including its timeline events, delayed consequences, and the RNA strike / CON challenge mechanics.

  Done:
  - Created `scenarios/competitive-exemplary-v1.toml` with startup states matching the scenario brief.
  - Added `scenario_id` and `event_metadata` to state tracking and serialization.
  - Extended `PledgeType` with `Workforce` to represent wage settlements.
  - Implemented Month 8 nurse burnout crisis and strike warnings.
  - Implemented Month 10 active strike (halved capacity, project delays, travel nurse costs) and Certificate of Need (CON) legal objections.
  - Implemented Month 12 Blue Shield contract renewal out-of-network commercial volume drop.
  - Implemented Month 18 delayed strike and underfunded EHR migration project lag costs.
  - Added parser, autocompletion, and helper documentation for workforce pledges.
  - Added comprehensive unit and integration tests verifying all timeline events.

  Deferred / Non-Goals:
  - No changes to stabilization campaign loop rules.
  - No network multiplayer capabilities.
  - No database integration.

  Verification:
  - cargo test (all 260 tests pass)


- Feature: Medicaid Public Payer Integration
  Status: Complete
  Started: 2026-07-04
  Version: 0.5.5

  Summary:
  Implemented Medicaid public payer integration in the competitive regional campaign loop, supporting custom negotiation rules representing public regulatory compliance and access alignment.

  Done:
  - Added `PayerId::Medicaid` variant to command models, CLI parsing, autocompletes, and topic help guides.
  - Implemented Medicaid validation ensuring only neutral rate posture is valid and enforcing a $5 compliance cost.
  - Implemented transition effects where Medicaid negotiations deduct 1 AP, 2 PC, and $5 cash, resulting in +3 access index and -3 policy pressure.
  - Filtered out Medicaid negotiations from commercial payer pressure calculations.
  - Added unit tests for transition effects and validation rules.

  Deferred / Non-Goals:
  - No Medicaid patient cohort tracking.
  - No structural changes to HealthSystemState.

  Verification:
  - cargo test (all 261 tests pass)


- Feature: MCP Custom Scenario Loading
  Status: Complete
  Started: 2026-07-04
  Version: 0.5.4

  Summary:
  Implemented custom scenario file loading in the MCP stdio server's `start_session` tool via the optional `scenario_path` parameter, supporting validation and initial state derivation for both stabilization and competitive scenarios.

  Done:
  - Added `scenario_path: Option<String>` to `StartSessionRequest` in `src/mcp/session.rs`.
  - Refactored `start_stabilization` and `start_competitive` to validate and extract genesis states from custom loaded scenarios.
  - Implemented unit tests for custom scenario loading and validation error conditions in `src/mcp/session.rs`.
  - Bumped Cargo.toml version to `0.5.4`.

  Deferred / Non-Goals:
  - No network/HTTP scenario fetching.

  Verification:
  - cargo check
  - cargo test (all 255 tests pass)


- Feature: Strategy-Space Diagnostics Tooling
  Status: Complete
  Started: 2026-07-04
  Version: 0.5.3

  Summary:
  Implemented offline replay diagnostics python script to summarize command frequencies, resource trajectories, strategy clusters, and key events across exported runs.

  Done:
  - Created `scripts/diagnose_runs.py` supporting offline parsing and summarization of replay JSON logs.
  - Added a test in `tests/golden_competitive_seed42.rs` to automatically write the 24-month seed 42 run to `tests/fixtures/mock_replay.json`.
  - Bumped Cargo.toml and Cargo.lock version to v0.5.3.

  Deferred / Non-Goals:
  - None.

  Verification:
  - cargo check
  - cargo test (all 252 tests pass)
  - python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json (successfully reports metrics and classifications)


- Feature: Test Hang and Playtest Fixes
  Status: Complete
  Started: 2026-07-04
  Version: 0.5.2

  Summary:
  Fixed test suite hangs under interactive stdin and index out of bounds in automated playtest scripts.

  Done:
  - Replaced direct `std::io::IsTerminal::is_terminal(&io::stdin())` checks with `!stdin_uses_fallback_input()` in `src/cli/campaign.rs` and `src/cli/session.rs` to avoid blocking on stdin prompts under test contexts.
  - Fixed `IndexError` in `scripts/run_automated_playtests.py` for competitive campaign runs by defaulting turns beyond 3 to `"hold"`.
  - Bumped Cargo.toml and Cargo.lock package version to v0.5.2.

  Deferred / Non-Goals:
  - None.

  Verification:
  - cargo check
  - cargo test (all 252 tests pass)
  - python3 scripts/run_automated_playtests.py (all 24 runs pass)


- Feature: Versioning Policy Alignment
  Status: Complete
  Started: 2026-07-04
  Version: 0.5.1

  Summary:
  Aligned versioning policy documentation in docs/versioning-policy.md and version history in CHANGELOG.md with the repository rules (0.0.1 bump per PR/PR-equivalent change, 0.1 minor bump for major features/milestones with lower digits reset).

  Done:
  - Updated docs/versioning-policy.md to specify the exact semver bump rules.
  - Documented release notes for v0.5.0 and v0.5.1 in CHANGELOG.md.
  - Bumped Cargo.toml and Cargo.lock package version to v0.5.1.

  Deferred / Non-Goals:
  - None.

  Verification:
  - cargo check
  - cargo test (all 252 tests pass)


- Feature: Competitive Campaign Extension & Autosave
  Status: Complete
  Started: 2026-07-04
  Version: 0.5.0

  Summary:
  Extended competitive campaign duration from 3 to 24 months, implemented mid-run session autosave/resume REPL prompt, and added replay artifact export at the end of the competitive campaign.

  Done:
  - Changed competitive campaign loop length to 24 months.
  - Implemented session autosave and CLI recovery prompt for competitive campaigns.
  - Implemented replay artifact export at the end of the session.
  - Added monthly/annual event scheduler to the campaign loop.
  - Cleaned up unused parameters and imports based on code reviewer feedback.

  Deferred / Non-Goals:
  - Replay viewer UI or web-based session serialization.

  Verification:
  - cargo test (all 252 tests pass)


- Feature: Competitive Scenario Loading and Validation
  Status: Complete
  Started: 2026-07-04
  Version: 0.4.0

  Summary:
  Implemented loading, validation, and execution of custom competitive scenarios from TOML via the --scenario CLI option, parsing multi-system starting states and matching them to selected difficulties.

  Done:
  - Extended Scenario struct with optional systems and initial_market fields.
  - Implemented validate_competitive_scenario and initial_competitive_world_state.
  - Updated run CLI routing to support loading and running custom competitive scenarios.
  - Refactored run_competitive_preview to accept custom initial state.
  - Added competitive-v1-template.toml template.
  - Added unit/integration tests for competitive scenario loading and validation.
  - Bumped package version to v0.4.0.

  Deferred / Non-Goals:
  - No changes to stabilization campaign loop rules.
  - No changes to competitive transition engine rules.

  Verification:
  - cargo fmt --check
  - cargo clippy --all-targets -- -D warnings
  - cargo test (all 252 tests pass)


- Feature: Clinical Service Lines and Staffing
  Status: Complete
  Started: 2026-07-04
  Version: 0.3.0

  Summary:
  Implemented inpatient vs outpatient capacity structures and role-based staffing constraints (nurses, physicians, admins) in the competitive campaign, applying capacity caps and burnout penalties under deficit.

  Done:
  - Added outpatient_capacity, nurses, physicians, and admins fields to HealthSystemState.
  - Mapped recruit and invest commands to roles and respective physical capacities.
  - Implemented staffing ratio checks, effective capacity utility ratios, and trust/access/quality penalties.
  - Updated Tower and ClinicNetwork projects to grant physical capacities on completion.
  - Updated executive report display and state hash record.
  - Added unit test coverage for staffing constraints in transition_competitive.rs.
  - Bumped package version to v0.3.0.

  Deferred / Non-Goals:
  - No changes to stabilization campaign loop.
  - No multiplayer network capabilities.

  Verification:
  - cargo fmt --check
  - cargo clippy --all-targets -- -D warnings
  - cargo test (all 246 tests pass, golden competitive hash updated to a49a2f80540ecd9b)

- Feature: Competitive Command Help Coverage
  Status: Complete
  Started: 2026-07-04
  Version: 0.2.9

  Summary:
  Implemented topic-specific command help in the competitive campaign CLI. Players can query detailed help for specific commands (e.g., 'help recruit', '? invest'), displaying resource costs, parameter constraints, and strategic guidance.

  Done:
  - Extended the `GlobalInput` enum and parser to support help topic parameters.
  - Refactored `read_line_with_globals` and `read_competitive_command_line` to delegate to the new topic-specific guidance helpers.
  - Implemented detailed, styled help outputs for all 7 competitive command verbs (hold, invest, recruit, monitor, negotiate, commit, project).
  - Added comprehensive unit tests in `src/cli/input.rs` and `src/cli/guidance.rs` verifying input parsing, formatting, and safety checks.
  - Bumped package version to `0.2.9`.

  Deferred / Non-Goals:
  - No changes to stabilization campaign resolution rules.
  - No modifications to actual game rules or simulation logic.
  - Golden hash value remains unchanged.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test` (all 244 tests pass)

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



## Present

None. All scheduled features are complete.


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
  (autocomplete completed in v0.2.5; AI rationale visibility completed in v0.2.7;
  month-summary clarity completed in v0.2.8; command help coverage completed in v0.2.9),
  and address it without expanding campaign length.

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
