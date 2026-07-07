# Changelog

All notable project changes should be recorded here.

The project follows the versioning policy defined in [`docs/versioning-policy.md`](docs/versioning-policy.md).

## [0.10.13] - 2026-07-07

### Added
- Added a Phase 7 static-vs-adaptive live-capture artifact across four existing
  automated playtest profiles, seeds `42`, `43`, and `44`, Normal/Hard
  competitive difficulty tiers, and static/adaptive policy variants.
- Generated `_workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md`
  from the static/adaptive artifact.
- Recorded `docs/playtest-findings-v0.10.13.md` with policy-wrapper comparison
  findings and evidence limits.

### Changed
- Documented the static-vs-adaptive live-capture command in the MCP playtesting
  guide.
- Bumped the package version to `0.10.13`.

## [0.10.12] - 2026-07-07

### Added
- Added a Phase 7 live difficulty-pressure capture artifact across four
  existing automated playtest profiles, seeds `42`, `43`, and `44`, and
  Normal/Hard competitive difficulty tiers.
- Generated `_workspace/experiments/v0.10.12-live-difficulty-pressure/diagnostics.md`
  from the pressure-policy artifact.
- Recorded `docs/playtest-findings-v0.10.12.md` with Normal/Hard pressure
  findings and evidence limits.

### Changed
- Documented the live difficulty-pressure capture command in the MCP playtesting
  guide.
- Bumped the package version to `0.10.12`.

## [0.10.11] - 2026-07-07

### Added
- Added a Phase 7 live-capture matrix artifact across three deterministic
  persona policies, seeds `42`, `43`, and `44`, and Normal/Hard competitive
  difficulty tiers.
- Generated `_workspace/experiments/v0.10.11-live-capture-matrix/diagnostics.md`
  from the matrix artifact.
- Recorded `docs/playtest-findings-v0.10.11.md` with findings and evidence
  limits for the live-capture matrix.

### Changed
- Documented the live-capture matrix command in the MCP playtesting guide.
- Bumped the package version to `0.10.11`.

## [0.10.10] - 2026-07-07

### Added
- Extended `scripts/diagnose_runs.py` to parse live MCP capture artifacts and
  report profile outcomes, action frequencies, validation failures, access
  pledges, final hashes, and evidence limits.
- Added a live-capture diagnostics fixture and generated
  `_workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md`.
- Recorded `docs/playtest-findings-v0.10.10.md` for the diagnostic report slice.

### Changed
- Documented the live-capture diagnostics command in the MCP playtesting guide.
- Bumped the package version to `0.10.10`.

## [0.10.9] - 2026-07-07

### Added
- Added live observation-by-observation MCP capture evidence for three Hard
  competitive persona policies at seed `42`.
- Added replayable capture artifacts at
  `_workspace/experiments/v0.10.9-live-mcp-capture/`.

### Changed
- Extended `scripts/play_game.py` with optional trace capture while preserving
  existing caller behavior.
- Bumped the package version to `0.10.9`.

## [0.10.8] - 2026-07-07

### Changed
- Aligned active project documentation with the current 24-month competitive
  campaign, competitive scenario loading, replay export, MCP boundaries, and
  command autocomplete status.
- Bumped the package version to `0.10.8`.

## [0.10.7] - 2026-07-07

### Added
- Recorded `docs/playtest-findings-v0.10.7.md` with a bounded sub-agent
  access-pledge evidence slice for Hard competitive play at seed `42`.
- Added replayable MCP artifact capture at
  `_workspace/experiments/v0.10.7-llm-access-pledge-evidence/`.

### Changed
- Bumped the package version to `0.10.7`.

## [0.10.6] - 2026-07-07

### Added
- Added a competitive debrief decision-quality warning for repeated public
  access pledges that are not paired with capacity, staffing, monitoring, or
  payer follow-through in the same three-month window.
- Added a student-facing debrief lesson distinguishing public access pledges
  from durable operational action.

### Changed
- Bumped the package version to `0.10.6`.

## [0.10.5] - 2026-07-07

### Added
- Recorded `docs/playtest-findings-v0.10.5.md` synthesizing the existing
  `v0.10.0` through `v0.10.4` free-form Hard competitive evidence.
- Documented evidence de-duplication and the next evidence gate for access
  pledge loops before any runtime cooldown or balance-tuning work.

### Changed
- Bumped the package version to `0.10.5`.

## [0.10.4] - 2026-07-06

### Added
- Recorded `docs/playtest-findings-v0.10.4.md` with post-guidance validation
  comparing unchanged free-form Hard policies against a guidance-aware access
  pledge policy across three profiles and seeds `42`, `43`, and `44`.
- Added operator capture script and JSON artifact at
  `_workspace/experiments/v0.10.4-post-guidance-validation/`.
- Documented the post-guidance validation procedure in
  `docs/mcp-playtesting-guide.md`.

### Changed
- Bumped the package version to `0.10.4`.

## [0.10.3] - 2026-07-06

### Changed
- Hardened competitive `commit` help and player-facing strategy notes to
  distinguish public access pledges from durable capacity, staffing,
  monitoring, and payer actions after the v0.10.2 access-loop diagnostic.
- Realigned general competitive help text with existing neurology and ASC
  invest/project vocabularies.
- Bumped the package version to `0.10.3`.

## [0.10.2] - 2026-07-06

### Added
- Recorded `docs/playtest-findings-v0.10.2.md` with a free-form Hard
  access-loop diagnostic comparing unchanged baseline policies against bounded
  access-pledge cooldown and reported-access-threshold variants.
- Added operator capture script and JSON artifact at
  `_workspace/experiments/v0.10.2-access-loop-diagnostic/`.
- Documented the access-loop diagnostic procedure in
  `docs/mcp-playtesting-guide.md`.

### Changed
- Bumped the package version to `0.10.2`.

## [0.10.1] - 2026-07-06

### Added
- Recorded `docs/playtest-findings-v0.10.1.md` with free-form Hard competitive
  MCP seed-variation evidence for three observation-driven profiles across
  seeds `42`, `43`, and `44`.
- Added operator capture script and JSON artifact at
  `_workspace/experiments/v0.10.1-free-form-hard-seed-variation/`.
- Documented the free-form Hard seed-variation procedure in
  `docs/mcp-playtesting-guide.md`.

### Changed
- Bumped the package version to `0.10.1`.

## [0.10.0] - 2026-07-06

### Added
- Recorded `docs/playtest-findings-v0.10.0.md` with free-form Hard competitive
  MCP playtest evidence for three observation-driven profiles on the full
  24-month campaign at seed 42.
- Added operator capture script and JSON artifact at
  `_workspace/experiments/v0.10.0-free-form-hard/` for reproducible free-form
  Hard sessions.
- Documented the free-form Hard competitive operator procedure in
  `docs/mcp-playtesting-guide.md`.

### Changed
- Bumped the package version to `0.10.0` (minor milestone for Phase 7 free-form
  Hard synthesis after the v0.9.x scripted playtest slice chain).

## [0.9.9] - 2026-07-06

### Added
- Added a targeted `--target difficulty-adaptive` automated MCP playtest mode with
  rival-aware scripted policy adjustments at Easy and Hard competitive difficulty.
- Extended strategy diagnostics with difficulty-adaptive action-frequency
  comparison notes for automated playtest batch artifacts.
- Recorded `docs/playtest-findings-v0.9.9.md` with the targeted Phase 7
  simulated-agent evidence and limits.

### Changed
- Bumped the package version to `0.9.9`.

## [0.9.8] - 2026-07-06

### Added
- Added a targeted `--target difficulty-sweep` automated MCP playtest mode for
  exercising competitive baseline profiles at Easy and Hard difficulty.
- Extended strategy diagnostics to report competitive outcomes grouped by
  difficulty and profile-by-difficulty cross-tabs for automated playtest batch
  artifacts.
- Recorded `docs/playtest-findings-v0.9.8.md` with the targeted Phase 7
  simulated-agent evidence and limits.

### Changed
- Bumped the package version to `0.9.8`.

## [0.9.7] - 2026-07-06

### Added
- Added a targeted `--target project-coverage` automated MCP playtest mode for
  exercising competitive capital-project command paths.
- Extended strategy diagnostics to report project-command counts, project kinds,
  final active projects, and final active project monthly draws for automated
  playtest batch artifacts.
- Recorded `docs/playtest-findings-v0.9.7.md` with the targeted Phase 7
  simulated-agent evidence and limits.

### Changed
- Bumped the package version to `0.9.7`.

## [0.9.6] - 2026-07-06

### Changed
- Extended competitive scripted MCP playtest policies beyond month 3 to improve
  24-month command coverage.
- Added direct scripted coverage for newer service-line investments, public
  payers, staffing, monitoring, and commitment commands without changing
  simulation behavior.
- Recorded `docs/playtest-findings-v0.9.6.md` with the updated Phase 7
  simulated-agent evidence and limits.
- Bumped the package version to `0.9.6`.

## [0.9.5] - 2026-07-06

### Added
- Added optional JSON batch artifact output to `scripts/run_automated_playtests.py` for Phase 7 strategy-space diagnostics.
- Extended `scripts/diagnose_runs.py` to read automated playtest batch JSON while preserving existing competitive replay JSON diagnostics.
- Recorded `docs/playtest-findings-v0.9.5.md` with strategy-space diagnostic findings for the current scripted MCP batch.

### Changed
- Documented the playtest JSON artifact and diagnostic workflow in `docs/mcp-playtesting-guide.md`.
- Bumped the package version to `0.9.5` for the diagnostics tooling and evidence PR-equivalent change.

## [0.9.4] - 2026-07-06

### Added
- Recorded a Phase 7 scripted AI-agent playtest synthesis for the current `v0.9.4` prototype in `docs/playtest-findings-v0.9.4.md`.
- Ran both playable campaigns across four scripted profiles and seeds `42`, `43`, and `44` through the local MCP playtest harness.

### Changed
- Bumped the package version to `0.9.4` for the playtest-synthesis PR-equivalent change.

## [0.9.3] - 2026-07-05

### Added
- Implemented the Ambulatory Surgery Center (ASC) Service Line mechanics.
- Configured nurse-to-bay (1:2), physician-to-bay (1:4), and admin-to-bay (1:12) staffing targets for ASC capacity.
- Implemented hierarchical staffing allocation prioritizing ASC 9th (after Infusion and before Outpatient Clinics).
- Added ASC outpatient surgery deferral rules (penalizing `-1` community trust and `-1` market share index per deferred patient).
- Added `InvestDomain::Asc` (direct bays) and `ProjectKind::AscUnit` (6-month capital project) commands and resolution logic.
- Extended CLI commands, autocomplete, REPL guidance documentation, and executive dashboard layout to support ASC capacity.
- Added comprehensive unit tests validating ASC priority allocation, strike halving, and deferral rules.

## [0.9.2] - 2026-07-05

### Fixed
- Addressed Codex PR review comments to account for `neurology_capacity` in AI player target staffing calculations (`target_nurses`, `target_physicians`, and `target_admins`).
- Added unit test `test_ai_candidate_generation_includes_neurology_staffing` confirming correct candidate generation under neurology staffing deficits.

## [0.9.1] - 2026-07-05

### Added
- Implemented Neurology & Stroke Center inpatient service line mechanics.
- Configured nurse-to-bed (1:3), physician-to-bed (1:6), and admin-to-bed (1:10) staffing targets for Neurology capacity.
- Implemented hierarchical staffing allocation prioritizing Neurology 6th (after Psychiatric and before Oncology).
- Added Neurology ED boarding & diversion rules (penalizing `-2` community trust and `-2` quality index under diversion).
- Added `InvestDomain::Neurology` (direct beds) and `ProjectKind::NeurologyUnit` (6-month capital project) commands and resolution logic.
- Extended CLI commands parser, autocomplete, REPL guidance documentation, and executive dashboard layout to support Neurology capacity.
- Added comprehensive unit tests validating Neurology priority allocation, strike halving, and overflow rules.

## [0.9.0] - 2026-07-05

### Added
- Implemented Oncology (Inpatient) and Infusion Center (Outpatient Chemotherapy) Service Line mechanics.
- Configured nurse-to-bed/bay, physician-to-bed/bay, and admin-to-bed/bay staffing targets for Oncology and Infusion capacity.
- Implemented hierarchical staffing allocation prioritizing Oncology 6th and Infusion 7th (before ED).
- Added Oncology ED boarding & diversion rules (penalizing `-2` community trust and `-2` quality index under diversion).
- Added Infusion session deferral rules (penalizing `-1` community trust and `-1` market share index under capacity constraints).
- Added `InvestDomain` (`Oncology` and `Infusion`) and `ProjectKind` (`OncologyUnit` (9-month) and `InfusionCenter` (6-month)) commands and resolution logic.
- Extended CLI commands, autocomplete, REPL guidance documentation, and executive dashboard layout to support Oncology/Infusion capacity.
- Added comprehensive unit tests validating Oncology/Infusion priority allocation, strike halving, and overflow rules.

## [0.8.4] - 2026-07-05

### Added
- Implemented the Cardiology Service Line & Cardiac Cath Lab mechanics.
- Added Cardiology-specific staffing targets (1 nurse per 3 beds, 1 physician per 8 beds, 1 admin per 12 beds) to transition rules.
- Implemented hierarchical staffing allocation prioritizing ICU first, Obstetrics second, Med-Surg third, Cardiology fourth, Psychiatric fifth, Clinics sixth, and ED last.
- Implemented Cardiology ED holding boarding and diversion mechanics under capacity/staffing deficit (incurring `-2` community trust and `-2` quality index penalties).
- Added `InvestDomain::Cardiology` for direct Cardiology bed investments and `ProjectKind::CardiologyUnit` for 6-month capital projects.
- Integrated Cardiology capacity and diversion into observation mapping, REPL executive dashboard, parser, autocomplete, and guidance help pages.
- Created comprehensive unit tests validating Cardiology priority allocation, diversion penalties under deficit, and project resolution.

## [0.8.3] - 2026-07-05

### Added
- Externalized scenario timeline events from the transition core to scenario TOML files.
- Added parsing support for `[[timeline_events]]` in `src/scenario/mod.rs` and added `timeline_events` field to `CompetitiveWorldState` (with `#[serde(default)]` for backward compatibility).
- Configured dynamic event triggers and ongoing scenario effects in the effects engine.
- Fixed a minor bug where completing the technology project did not correctly set `ehr_project_fully_funded` metadata state.

## [0.8.2] - 2026-07-05

### Changed
- Aligned project documentation (`README.md`, `ARCHITECTURE.md`, `SPEC.md`, `docs/roadmap.md`, `docs/how-to-play.md`, `docs/versioning-policy.md`, `docs/core-loop-spec.md`, `docs/system-boundary.md`, `docs/competitive-scenario-brief.md`, `docs/first-scenario-brief.md`, and `docs/agent-playtest-protocol.md`) with the implemented 24-month campaign loop, custom scenario loading, autosave/resume, and new service line additions.
- Bumped package version to `0.8.2`.

## [0.8.1] - 2026-07-05

### Added
- Implemented the Psychiatric Service Line & ED holding/diversion mechanics.
- Added Psychiatric-specific staffing targets (1 nurse per 4 beds, 1 physician per 10 beds, 1 admin per 15 beds) to transition rules.
- Implemented hierarchical staffing allocation prioritizing ICU first, Obstetrics second, Med-Surg third, Psychiatric fourth, Clinics fifth, and ED last.
- Implemented Psychiatric ED holding boarding (psychiatric overflow boards in ED, consuming ED bays) and diversion mechanics under capacity/staffing deficit (incurring `-2` community trust and `-1` market share index penalties).
- Added `InvestDomain::Psychiatric` for direct Psychiatric bed investments and `ProjectKind::PsychiatricUnit` for 6-month capital projects.
- Integrated Psychiatric capacity and holding into observation mapping, REPL executive dashboard, parser, autocomplete, and guidance help pages.
- Created comprehensive unit tests validating Psychiatric priority allocation, ED boarding, diversion penalties under deficit, and project resolution.
- Updated `LESSONS.md` to document Psychiatric ED boarding test constraints and hierarchical staffing priority.

## [0.8.0] - 2026-07-05

### Added
- Implemented the Obstetrics/L&D Service Line & Diversion Mechanics.
- Added Obstetrics-specific staffing targets (1 nurse per 2 beds, 1 physician per 5 beds, 1 admin per 10 beds) to transition rules.
- Implemented hierarchical staffing allocation prioritizing ICU first, Obstetrics second, Med-Surg third, Clinics fourth, and ED last.
- Added Obstetrics diversion mechanics where patients are diverted if Obstetrics capacity is under-staffed or under-capacitated, incurring `-2` community trust and `-1` market share index penalties.
- Added `InvestDomain::Obstetrics` for direct Obstetrics bed investments and `ProjectKind::ObstetricsUnit` for 9-month capital projects.
- Integrated Obstetrics capacity and diversion into observation mapping, REPL executive dashboard, parser, autocomplete, and guidance help pages.
- Created comprehensive unit tests validating Obstetrics priority allocation, diversion penalties under deficit, and project resolution.

## [0.7.0] - 2026-07-05

### Added
- Implemented the Intensive Care Unit (ICU) Service Line with capacity-staffing trade-offs.
- Added ICU-specific staffing targets (1 nurse per bed, 1 physician per 2 beds, 1 admin per 5 beds) to transition rules.
- Implemented hierarchical staffing allocation where staff are assigned to ICU first, med-surg beds second, clinics third, and ED last.
- Implemented ED Boarding mechanics where patients requiring ICU admission are boarded in the ED if ICU beds are full, consuming ED bays and reducing effective emergency capacity.
- Added `InvestDomain::Icu` for direct ICU bed investments and `ProjectKind::IcuWing` for 12-month capital projects (costing 3 AP).
- Integrated ICU capacity and boarding into observation mapping, REPL executive dashboard, parser, autocomplete, and guidance help pages.
- Created comprehensive unit tests validating ICU allocation, boarding, and trust/index penalties.

## [0.6.0] - 2026-07-05

### Added
- Implemented the Emergency Department (ED) Service Line with capacity-staffing trade-offs.
- Extended state structures to include `emergency_capacity` defaulting to 0 for scenario/genesis backward compatibility.
- Added ED-specific staffing targets (1 nurse per 2 bays, 1 physician per 4 bays, 1 admin per 10 bays) to transition rules.
- Implemented hierarchical staffing allocation where nurses and physicians are assigned to med-surg beds first, clinics second, and ED third.
- Added `InvestDomain::Emergency` for immediate investments and `ProjectKind::EmergencyPavilion` for 6-month capital projects.
- Integrated ED capacity and projects into observation mapping, REPL display, parser, autocompletion lists, help guidance pages, and state record hashes.
- Created comprehensive test coverage verifying transition outcomes and staffing constraint details.

## [0.5.9] - 2026-07-05

### Added
- Hardened the competitive campaign CLI dashboard by detailing in-flight projects (project kind, remaining months to completion, and monthly cash draw) instead of a simple count.
- Added comprehensive unit tests for active project observation formatting.

## [0.5.8] - 2026-07-05

### Added
- Implemented Medicare public payer integration in the competitive regional campaign loop.
- Added `PayerId::Medicare` variant supporting quality compliance alignment with neutral posture and $10 compliance cost.
- Implemented state transition effects for Medicare compliance (+3 quality index, -3 state policy pressure).
- Enforced neutral-posture-only validation checks and resource costing checks for Medicare negotiations.
- Excluded Medicare negotiations from commercial payer pressure calculations.
- Added CLI parsing, REPL autocomplete, brief and detailed guidance help support for Medicare.
- Added focused unit tests verifying Medicare validation checks and transition outcomes.

## [0.5.7] - 2026-07-05

### Added
- Designed the Medicare Public Payer integration plan and recorded design maps, evidence registers, and QA specifications in `_workspace/`.

## [0.5.6] - 2026-07-04

### Added
- Created the new `competitive-exemplary-v1` scenario defining Riverside Community Health, Northlake Health, and Summit Care.
- Added `scenario_id` and `event_metadata` fields to `CompetitiveWorldState` and `CompetitiveSessionSave` to track scenario state.
- Added `PledgeType::Workforce` to model workforce wage settlements.
- Implemented Month 8 nurse burnout crisis and strike warnings.
- Implemented Month 10 nurse strike active mode (halved capacity, project delays, travel nurse costs) and Certificate of Need (CON) legal challenge objections.
- Implemented Month 12 Blue Shield commercial contract renewal out-of-network volume drop.
- Implemented Month 18 delayed strike and underfunded EHR migration project lag costs.
- Added CLI parsing, REPL autocompletion, and help guidance support for workforce pledges.
- Added comprehensive unit and integration tests verifying all timeline events.

## [0.5.5] - 2026-07-04

### Added
- Implemented Medicaid public payer integration in the competitive regional campaign loop.
- Added `PayerId::Medicaid` variant to command models, CLI parsing, autocompletes, and topic help guides.
- Implemented custom Medicaid negotiation rules where compliance alignment costs 1 AP, 2 PC, and $5 cash, resulting in +3 access index and -3 policy pressure (with no market share or commercial payer pressure increments).
- Enforced neutral-posture-only validation checks for Medicaid negotiations.
- Added comprehensive unit and validation tests for Medicaid compliance alignment.

### Added
- Implemented custom scenario file loading in the MCP stdio server's `start_session` tool via the optional `scenario_path` parameter.
- Integrated validation and initial state derivation for both custom stabilization and competitive scenarios in the MCP server.
- Added unit tests for custom scenario loading and validation in `src/mcp/session.rs`.

## [0.5.3] - 2026-07-04

### Added
- Implemented `scripts/diagnose_runs.py` diagnostic command-line tool to analyze action frequencies, outcome distributions, and strategy-cluster classifications over exported replay JSON files.
- Added `generate_mock_replay_fixture` test in `tests/golden_competitive_seed42.rs` to automatically generate a mock 24-month replay file at `tests/fixtures/mock_replay.json` during test runs.

## [0.5.2] - 2026-07-04

### Fixed
- Fixed a test suite hang where interactive/PTY test contexts would block indefinitely on stdin prompts for replay export.
- Fixed `IndexError` in `scripts/run_automated_playtests.py` by ensuring simulated player policies default to holding on turns beyond the initial 3 months of the newly extended 24-month competitive campaign loop.

## [0.5.1] - 2026-07-04

### Changed
- Aligned versioning policy documentation in `docs/versioning-policy.md` and version history in `CHANGELOG.md` with the new repository rules.
- Documented release notes for `0.5.0` and bumped package version to `0.5.1`.

## [0.5.0] - 2026-07-04

### Added
- Extended the competitive campaign duration from 3 months to 24 months, enabling multi-year simulation loops.
- Implemented mid-run session autosave for competitive campaigns with a REPL prompt to resume or start over on launch.
- Implemented replay artifact export at the end of the competitive session.
- Added monthly and annual event scheduling for competitive campaigns.

### Changed
- Resolved code reviewer findings to clean up unused imports and parameters.

## [0.4.0] - 2026-07-04

### Added
- Implemented competitive scenario loading and validation, allowing custom multi-system campaign scenario files (`competitive-regional-v1`) to be parsed, validated, and run via the `--scenario` CLI option.
- Added custom competitive scenario template `scenarios/competitive-v1-template.toml`.
- Added unit and integration tests covering competitive scenario validation errors, ruleset validation, and initial state extraction.

## [0.3.1] - 2026-07-04

### Fixed
- Fixed compounding exponential decay of quality and access indices during understaffing by replacing it with a linear, additive monthly drop.
- Fixed active project draws never resolving by carrying `project_draw` values to completion effects and deducting ongoing draws from system cash at the start of transition.
- Fixed missing `workforce_trust` and `community_trust` in the competitive state hash record.
- Fixed AI player systems lacking candidate commands to recruit Physicians and Administrators.
- Fixed immediate understaffing penalties on starting turns by matching genesis template administrator levels to required targets.
- Fixed instant bed capacity mismatch by queuing physical bed expansions with a 1-month delay, matching outpatient clinics.
- Fixed private rival operational events leaking to the player in the monthly CLI summary report.
- Fixed budget division truncation exploits by validating that project budgets must be a multiple of the project duration.

## [0.3.0] - 2026-07-04

### Added
- Implemented clinical service lines and staffing requirements in the competitive campaign loop, distinguishing inpatient beds (`staffed_beds`) and outpatient clinics (`outpatient_capacity`).
- Added nurse, physician, and admin headcount metrics to `HealthSystemState`.
- Implemented dynamic staffing ratio targets (5 beds per nurse, 10 clinics per physician, 20 capacity units per admin) and understaffing penalties.
- Added effective capacity caps, access/quality index discounts, and workforce trust penalties due to staff burnout.
- Updated `ProjectKind::Tower` and `ProjectKind::ClinicNetwork` to grant physical capacity units.
- Updated state hashing and CLI display reports to render capacity and staffing metrics.
- Added unit tests for staffing constraints, capacity resolution, and trust penalties.
- Bumped package version to `0.3.0`.

## [0.2.9] - 2026-07-04

### Added
- Implemented command-specific help coverage in the competitive campaign CLI. Users can query detailed parameters, resource costs, constraints, and strategic guidance for specific command verbs (e.g. `help recruit`, `? invest`).
- Added robust validation and unit tests in `src/cli/input.rs` and `src/cli/guidance.rs` covering parsing, formatting, and safety checks for topics.
- Bumped package version to `0.2.9`.

## [0.2.8] - 2026-07-04

### Added
- Enhanced the month resolution summary in the competitive campaign CLI to display the player's resolved commands, detailed logged rival public actions, and resolved attributed effects.
- Added start-of-month starting resources summary (AP, Cash, Political Capital, active project draws) directly to the end of the turn resolution output to improve runway planning and strategy visibility.
- Added comprehensive unit tests verifying the formatting and correctness of the new resolution summary sections.
- Bumped package version to `0.2.8`.

## [0.2.7] - 2026-07-04

### Added
- Refactored competitive end-session debriefs and instructor summaries to track and display visibility sources for rival AI rationales.
- Rationales now explicitly show `(observed via monitor)` or `(observed via public disclosure)` when observed during play.
- Instructor summaries dynamically attribute visibility sources and display `(unobserved during play - REVEALED FOR INSTRUCTOR REVIEW)` only for private, unobserved actions.
- Added comprehensive unit tests in `src/debrief/report_tests.rs` covering all visibility state combinations.
- Bumped package version to `0.2.7`.

## [0.2.6] - 2026-07-04

### Added
- Implemented a deterministic Decision-Quality Assessment capability in the competitive campaign debriefing system.
- Checks evaluate cash runway safety (active project monthly draws under low cash), workforce trust (critical trust drops after recruitment), payer negotiation postures (aggressive rate requests without leverage), and rival capacity responses (unanswered competitor expansion).
- Appended the strategic decision-quality feedback to the instructor run summary and end-of-session debriefs.
- Created robust unit tests verifying all four check triggers in `src/debrief/report_tests.rs`.
- Bumped package version to `0.2.6`.

## [0.2.5] - 2026-07-03

### Added
- Implemented argument-key and enum-value autocomplete in the competitive campaign CLI REPL, allowing tab cycling through valid parameters and excluding already entered options.
- Added comprehensive unit tests in `src/cli/repl.rs` to verify autocomplete outcomes for command segments, batches, argument keys, and enum values.
- Bumped package version to `0.2.5`.

## [0.2.4] - 2026-07-03

### Added
- Created the first dedicated parameter and evidence ledger for the Nursing Workforce & Retention mechanism (`docs/workforce-ledger.md`), mapping game variables and formulas to literature context (BLS occupational reports, California AB 394 safe staffing, Aiken JAMA 2002 nurse burnout).
- Assigned confidence labels distinguishing empirical calibration candidates, literature-grounded behaviors, stylized abstractions, and gameplay-driven limits.
- Extended the main evidence registry (`docs/evidence-registry.md`) to link and index the new workforce ledger.
- Bumps package version to `0.2.4`.

## [0.2.3] - 2026-07-03

### Added
- Drafted the first exemplary scenario brief for the competitive campaign (`docs/exemplary-scenario-brief.md`), modeling workforce conflicts, certificate of need legal challenges, Blue Shield payer negotiations, and delayed EHR consequences.
- Created repository-local workspace pipeline artifacts (`_workspace/00_input/request-summary.md`, `_workspace/01_evidence_map.md`, `_workspace/02_mechanism_design.md`, `_workspace/03_domain_qa.md`, and `_workspace/final/handoff.md`).
- Bumps package version to `0.2.3`.

## [0.2.2] - 2026-07-03

### Added
- Added an instructor-visible run summary & decision-quality review block to stabilization and competitive debriefs.
- Stabilization summary lists turn-by-turn observed access vs true access index and calculates observation gaps.
- Competitive summary lists all true rival actions and rationales, explicitly labeling them as observed (if monitored or public) or unobserved.
- Added automatic printing of the competitive debrief at the end of the three-month competitive campaign loop in CLI mode.

### Changed
- Centralized competitive campaign debriefing in the `src/debrief/report.rs` module and cleaned up duplicates from MCP session logic.
- Bumped package version to `0.2.2`.

## [0.2.1] - 2026-07-03

### Changed

- Reviewed post-v0.2 project progress and reorganized `SPEC.md` Future into a
  ranked next-development queue while keeping `Present` empty.
- Refreshed stale companion planning notes that still pointed to already
  completed competitive runtime slices as future work.
- Recorded a lesson for post-milestone SDD reviews.
- Bumped package version to `0.2.1`.

## [0.2.0] - 2026-07-03

### Added

- Added a public-facing `README.md` focused on the playable CLI prototype,
  current campaigns, quickstart, limitations, and documentation paths.
- Archived the previous developer-focused README at
  `docs/README-dev-archive-v0.1.61.md`.

### Changed

- Repositioned the project as a playable public/portfolio prototype while
  preserving explicit non-claims around empirical calibration, human learning
  evidence, and policy forecasting.
- Set the Cargo default binary to `hs-mgt-game` so `cargo run` launches the
  playable CLI when the MCP binary is also present.
- Updated repository hygiene rules to ignore Python bytecode caches and macOS
  metadata.
- Bumped package version to `0.2.0`.

### Removed

- Removed a tracked generated Python bytecode file from `scripts/__pycache__/`.

## [0.1.61] - 2026-07-03

### Changed

- Cleaned up `SPEC.md` to simplify active and completed feature tracking, making the Past-Present-Future distinction more straightforward.
- Archived completed feature slices from `v0.1.40` through `v0.1.54` into `docs/spec-past-archive.md`.
- Reduced `Present` section in `SPEC.md` to focus strictly on active tasks.
- Bumps project version to `0.1.61`.

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
