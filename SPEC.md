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

Full per-slice completion history: [`docs/history/archives/spec-past-archive.md`](docs/history/archives/spec-past-archive.md)

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
| Neurology & Stroke Center | v0.9.1–v0.9.2 | Add inpatient Neurology service line, staffing ratios, hierarchical priority queue 6th, and ED holding boarding/diversion mechanics | 279 | `807fcbc8edeea8e3` (competitive) |
| Ambulatory Surgery Center | v0.9.3 | Add outpatient ASC service line, staffing ratios, hierarchical priority queue 9th, and outpatient surgery deferral mechanics | 280 | `8926f71296f39efc` (competitive) |
| Agent Playtest Synthesis After Service-Line Expansion | v0.9.4 | Record scripted Phase 7 MCP playtest evidence across current campaigns, seeds, and profiles | 282 | `8926f71296f39efc` (competitive) |
| Strategy-Space Diagnostics Artifact | v0.9.5 | Add automated playtest JSON artifact output and diagnostic report support for Phase 7 scripted batches | 282 | `8926f71296f39efc` (competitive) |
| Competitive Playtest Policy Coverage | v0.9.6 | Extend scripted competitive MCP policies beyond month 3 and exercise newer service-line commands | 282 | `8926f71296f39efc` (competitive) |
| Project-Command Playtest Diagnostics | v0.9.7 | Add targeted project-command MCP playtest mode and diagnostic reporting for project kinds, active projects, and monthly draws | 282 | `8926f71296f39efc` (competitive) |
| Difficulty-Tier Playtest Synthesis | v0.9.8 | Add targeted difficulty-sweep MCP playtest mode and per-difficulty diagnostic reporting for Easy and Hard competitive runs | 282 | `8926f71296f39efc` (competitive) |
| Difficulty-Adaptive Playtest Policies | v0.9.9 | Add targeted difficulty-adaptive MCP playtest mode with rival-aware scripted policy adjustments at Easy and Hard competitive runs | 282 | `8926f71296f39efc` (competitive) |
| Free-Form Hard Competitive Playtest Synthesis | v0.10.0 | Record observation-driven free-form MCP competitive sessions at Hard difficulty on the full 24-month campaign | 282 | `8926f71296f39efc` (competitive) |
| Free-Form Hard Seed Variation | v0.10.1 | Extend free-form Hard competitive sessions across seeds 42, 43, and 44 | 282 | `8926f71296f39efc` (competitive) |
| Access-Loop Diagnostic | v0.10.2 | Compare free-form Hard baseline policies against bounded access-pledge cooldown and reported-access-threshold variants | 282 | `8926f71296f39efc` (competitive) |
| Access Commitment Guidance Hardening | v0.10.3 | Clarify competitive access pledge guidance without changing runtime mechanics or balance | 284 | `8926f71296f39efc` (competitive) |
| Post-Guidance Validation | v0.10.4 | Compare unchanged free-form Hard policies against a guidance-aware access-pledge policy | 284 | `8926f71296f39efc` (competitive) |
| Phase 7 Evidence Synthesis | v0.10.5 | Synthesize v0.10.0-v0.10.4 free-form Hard evidence and preserve the next evidence gate before runtime tuning | 284 | `8926f71296f39efc` (competitive) |
| Competitive Access-Pledge Debrief QA | v0.10.6 | Add debrief review for repeated public access pledges without operational follow-through | 287 | `8926f71296f39efc` (competitive) |
| LLM Access-Pledge Evidence | v0.10.7 | Record bounded sub-agent Hard competitive evidence for access-pledge repetition after guidance and debrief QA | 287 | `8926f71296f39efc` (competitive) |
| Active Project Document Alignment | v0.10.8 | Align active docs with current competitive campaign, scenario loading, replay export, MCP boundaries, and autocomplete status | 287 | `8926f71296f39efc` (competitive) |
| Live MCP Capture Evidence | v0.10.9 | Record observation-by-observation Hard competitive MCP capture evidence without changing runtime mechanics | 287 | `8926f71296f39efc` (competitive) |
| Live-Capture Diagnostics | v0.10.10 | Add diagnostic report support for live MCP capture artifacts without changing runtime mechanics | 287 | `8926f71296f39efc` (competitive) |
| Live-Capture Matrix Evidence | v0.10.11 | Extend live MCP capture across seeds 42-44 and Normal/Hard difficulty without changing runtime mechanics | 287 | `8926f71296f39efc` (competitive) |
| Live Difficulty-Pressure Capture | v0.10.12 | Reuse automated pressure policies through live MCP capture for Normal/Hard competitive comparison without changing runtime mechanics | 287 | `8926f71296f39efc` (competitive) |
| Static-vs-Adaptive Live Capture | v0.10.13 | Compare static and adaptive deterministic policies in one live MCP capture artifact without changing runtime mechanics | 287 | `8926f71296f39efc` (competitive) |
| Independent Reviewer-Agent Live Capture | v0.10.14 | Run observation-conditioned reviewer policies through live MCP capture without changing runtime mechanics | 287 | `8926f71296f39efc` (competitive) |
| Live LLM Difficulty Gate | v0.10.15 | Capture live month-by-month sub-agent decisions for Normal/Hard difficulty comparison without changing runtime mechanics | 287 | `8926f71296f39efc` (competitive) |
| Live Difficulty Evidence Synthesis | v0.10.16 | Synthesize v0.10.12-v0.10.15 live difficulty evidence and select cash-pressure retry visibility as the next bounded issue before runtime tuning | 287 | `8926f71296f39efc` (competitive) |
| Live Retry Cash-Pressure Diagnostics | v0.10.17 | Add live retry signal reporting to diagnostics for optional live-capture retry metadata, separating cash-overrun retries from final replay validation failures | 287 | `8926f71296f39efc` (competitive) |
| MCP Structured Validation Errors | v0.10.18 | Add additive structured MCP competitive validation error fields for resource-limit and retry classification without changing runtime mechanics | 290 | `8926f71296f39efc` (competitive) |
| Live-Capture Structured Retry Metadata | v0.10.19 | Preserve additive MCP structured retry fields in Python live-capture artifacts and prefer them in diagnostics without changing runtime mechanics | 294 | `8926f71296f39efc` (competitive) |
| Live Retry Visibility Checkpoint | v0.10.20 | Close the current live retry visibility gate and defer runtime tuning until a later evidence slice identifies a concrete mechanic issue | 294 | `8926f71296f39efc` (competitive) |
| Live Evidence Synthesis | v0.10.21 | Synthesize live-capture, difficulty, and retry-visibility evidence and route the next bounded gate toward access-heavy player understanding | 294 | `8926f71296f39efc` (competitive) |
| Access-Heavy Comprehension Evidence Review | v0.10.22 | Review existing live-capture evidence for access-heavy player understanding and route the next bounded follow-up toward explanatory debrief wording | 294 | `8926f71296f39efc` (competitive) |
| Access Follow-Through Debrief Note | v0.10.23 | Add explanatory competitive debrief wording for low-cash access-heavy runs where public pledges outnumber durable operational follow-through | 297 | `8926f71296f39efc` (competitive) |
| Access Debrief Validation | v0.10.24 | Validate the access follow-through debrief note through bounded MCP trigger/control runs without changing runtime mechanics | 294 | `8926f71296f39efc` (competitive) |
| Access Evidence Synthesis | v0.10.25 | Synthesize the v0.10.21-v0.10.24 access-heavy evidence chain and keep runtime tuning deferred until a later concrete mechanics finding | 294 | `8926f71296f39efc` (competitive) |
| Competitive Teachability Synthesis | v0.10.26 | Compare recent competitive playtest findings for teachability, debrief coherence, and repeated-play interest | 294 | `8926f71296f39efc` (competitive) |
| Competitive Instructor Comparison Note | v0.10.27 | Turn existing competitive evidence into instructor-facing prompts about decision quality versus outcome quality | 294 | `8926f71296f39efc` (competitive) |
| Competitive Strategy-Space Synthesis | v0.10.28 | Compare finance-first, access-heavy, workforce-protective, and growth-oriented signals across existing competitive evidence | 294 | `8926f71296f39efc` (competitive) |
| Competitive Debrief Comparison Surface | v0.10.29 | Add an instructor/reviewer comparison surface for decision quality, outcome quality, cash runway, follow-through, rival pressure, and debrief traceability | 294 | `8926f71296f39efc` (competitive) |
| Workforce-Protective Evidence Review | v0.10.30 | Review workforce-protective competitive play as an interpretive evidence axis across staffing, trust, pacing, monitoring, and commitment discipline | 294 | `8926f71296f39efc` (competitive) |
| Expansion Proposal Review | v0.10.31 | Review difficulty, regional M&A, and GUI expansion proposals before roadmap and SDD propagation | 294 | `8926f71296f39efc` (competitive) |
| Future Queue Re-ranking and SDD Alignment | v0.10.32 | Re-rank SPEC Future tracks around validation-first promotion gates and align SDD handoff docs | 294 | `8926f71296f39efc` (competitive) |
| Growth/Capacity-Oriented Evidence Review | v0.10.33 | Review growth/capacity-oriented competitive play as an interpretive evidence axis across projects, investments, staffed capacity, cash runway, access, and rival pressure | 294 | `8926f71296f39efc` (competitive) |
| Instructor Debrief Facilitation Note | v0.10.34 | Sequence recent competitive comparison, workforce-protective, and growth/capacity evidence into instructor debrief prompts | 294 | `8926f71296f39efc` (competitive) |
| Difficulty Pressure Dimension Gate | v0.10.35 | Select rival information and monitoring pressure visibility as the next bounded difficulty surface before any runtime tuning | 294 | `8926f71296f39efc` (competitive) |
| Rival Information Pressure Design | v0.10.36 | Define information delay, monitor value, and public disclosure as reviewable difficulty pressure surfaces before runtime tuning | 294 | `8926f71296f39efc` (competitive) |
| Rival Information Monitor Evidence | v0.10.37 | Compare monitored versus unmonitored Hard/Expert live MCP captures for rival-information observation value | 294 | `8926f71296f39efc` (competitive) |
| Advisor Market Proposal Review | v0.10.38 | Paper-evaluate differentiated in-house advisors and defer runtime promotion pending generic advice repair | 294 | `8926f71296f39efc` (competitive) |
| Live Consultant Advice and Advisory History | v0.10.39 | Restore four deterministic actor-visible consultant options across competitive CLI/MCP observations and retain them for debrief comparison | 294 | `8926f71296f39efc` (competitive) |
| Consultant Advice Traceability Evidence | v0.10.40 | Verify rendered consultant options, committed history, and debrief continuity across existing deterministic competitive captures | 294 | `8926f71296f39efc` (competitive) |
| Consultant Advice Usage Evidence | v0.10.41 | Compare advice-aware and advice-ignoring simulated policies using visible cues, resource-safe fallback, and exact observation/history/debrief continuity | 285 | `8926f71296f39efc` (competitive) |
| Consultant Advice Evidence Synthesis | v0.10.42 | Synthesize generic advice visibility, traceability, and usage evidence and retain the advisor-market promotion gate | 285 | `8926f71296f39efc` (competitive) |
| Rival Information Follow-Through Evidence | v0.10.43 | Compare monitor-reactive, monitor-ignoring, and unmonitored policies for visible signal-to-next-turn response traceability | 285 | `8926f71296f39efc` (competitive) |
| Information-to-Action Comparison Evidence | v0.10.44 | Connect consultant-advice and rival-monitor evidence into an instructor-facing comparison of visibility, response, follow-through, outcomes, and debrief traceability | 285 | `8926f71296f39efc` (competitive) |
| Instructor Debrief-Use Audit Evidence | v0.10.45 | Audit existing Phase 7 artifacts for visibility, response, follow-through, outcome, and explanation trace coverage before runtime promotion | 285 | `8926f71296f39efc` (competitive) |


- Feature: Consultant Advice Evidence Synthesis
  Status: Complete
  Started: 2026-07-10
  Version: 0.10.42

  Summary:
  Synthesized the v0.10.39–v0.10.41 generic consultant-advice evidence chain
  and confirmed that current artifacts do not identify a concrete limitation
  requiring a differentiated advisor market.

  Done:
  - Added findings covering generic advice restoration, exact history/debrief
    continuity, visible-cue policy usage, fallback behavior, and control hashes.
  - Updated playtesting guidance, evidence handoffs, domain QA, changelog,
    README milestone, lessons, and package metadata.
  - Preserved the advisor-market promotion gate and recorded explicit evidence
    limits.

  Deferred / Non-Goals:
  - No advisor roster, payroll, candidate pool, hire/fire command, AI advisor,
    scenario, replay, state-hash, ruleset, balance, difficulty, scoring, or
    runtime mechanics change.
  - No new playtest matrix, causal advice claim, human-learning claim,
    policy-validity claim, or empirical-calibration claim.

  Verification:
  - v0.10.40 and v0.10.41 JSON artifacts parse successfully.
  - v0.10.41 artifact regeneration is byte-for-byte stable.
  - `python3 -m unittest discover -s tests -p 'test_*.py'`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test --all -- --test-threads=1`
  - `python3 scripts/run_automated_playtests.py`
  - `git diff --check`


- Feature: Consultant Advice Usage Evidence
  Status: Complete
  Started: 2026-07-10
  Version: 0.10.41

  Summary:
  Added a bounded Phase 7 evidence slice that compares deterministic advice-aware
  and advice-ignoring competitive policies. The advice-aware wrapper reads only
  actor-visible consultant options and resources, records its selected option or
  fallback, and preserves exact continuity with committed history and debriefs.

  Done:
  - Added a 24-run matrix for Fiscal Caution and Naive First-Time profiles,
    seeds 42–44, and Normal/Hard difficulty.
  - Added focused tests for option parsing, visible-cue priority, resource
    guards, and safe fallback to hold.
  - Verified advice-ignoring control hashes match the v0.10.40 artifact.
  - Bumped package metadata to `0.10.41`.

  Deferred / Non-Goals:
  - No advisor roster, payroll, candidate pool, hire/fire command, AI advisor,
    scenario, replay, state-hash, ruleset, balance, or runtime mechanics change.
  - No advice-quality, causal-impact, human-learning, policy-validity, or
    empirical-calibration claim.

  Verification:
  - `python3 -m unittest discover -s tests -p 'test_*.py'`
  - `python3 _workspace/experiments/v0.10.41-consultant-advice-usage/run_sessions.py`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test --all -- --test-threads=1`
  - `python3 scripts/run_automated_playtests.py`
  - `git diff --check`


- Feature: Advisor Market Proposal Review
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.38

  Summary:
  Added a Phase 7 paper evaluation for differentiated in-house advisors as an
  advice-only, shared-market candidate. The review defers runtime promotion:
  the generic monthly-advice baseline is absent, and all tested positive
  integer salary schedules make a four-advisor roster infeasible at the default
  60-cash scale.

  Done:
  - Extended `docs/design/expansion-proposal-review.md` with evidence limits, fixture
    outcomes, a 24-month payroll sensitivity matrix, promotion conditions, and
    non-goals.
  - Documented future-only architecture, roadmap, scenario, command, evidence,
    and debrief boundaries without changing runtime behavior.
  - Corrected consultant-report documentation to distinguish the intended
    monthly advisory section from its current fixture-only implementation.
  - Bumped package metadata to `0.10.38`.

  Deferred / Non-Goals:
  - No advisor state, command, salary, candidate pool, firing behavior, AI
    change, schema, replay, state hash, ruleset, balance, or scenario change.
  - No calibrated compensation, labor-market, layoff, or educational-effect
    claim; the four-advisor cap and all cadence/price choices remain gameplay
  abstractions pending future validation.

  Verification:
  - `git diff --check`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`


- Feature: Live Consultant Advice and Advisory History
  Status: Complete
  Started: 2026-07-10
  Version: 0.10.39

  Summary:
  Restored four deterministic, non-binding consultant options for every
  competitive human observation and retained the exact options shown with each
  committed transition for debrief comparison.

  Done:
  - Unified genesis, live CLI, and MCP observations through the shared
    actor-visible advice generator.
  - Added serialized per-transition consultant options with legacy empty-field
    compatibility and no state-hash change.
  - Added MCP rendering, debrief comparison lines, focused tests, and updated
    competitive loop/report documentation.
  - Bumped package metadata to `0.10.39`.

  Deferred / Non-Goals:
  - No advisor market, roster, payroll, candidate pool, hire/fire command, AI
    advice behavior, scenario schema, ruleset, balance, or transition semantics.
  - No advice quality, learning, calibration, or policy-validity claim.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test --all -- --test-threads=1` (285 tests pass)
  - `python3 scripts/run_automated_playtests.py`
  - `git diff --check`


- Feature: Rival Information Monitor Evidence
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.37

  Summary:
  Added a paired Phase 7 live MCP evidence slice comparing monitored and
  unmonitored rival-information policies on Hard and Expert difficulty at seed
  42. The slice keeps runtime mechanics and balance unchanged.

  Done:
  - Added `_workspace/experiments/v0.10.37-rival-info-monitor-evidence/` with
    the paired capture script, `results.json`, and diagnostics report.
  - Extended live-capture diagnostics with optional rival-information signal
    counts for monitor intel, public rival lines, private activity gaps, and no
    public signal lines.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.37.md` and updated the MCP playtesting
    guide with the evidence-routing checkpoint.
  - Preserved runtime mechanics, command validation, stochastic inputs,
    scenarios, MCP DTOs, replay formats, state hashes, ruleset values,
    difficulty values, scoring, and balance.
  - Bumped package metadata to `0.10.37`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python MCP wrapper protocol, command-surface, AP-budget,
    command-cost, scoring, difficulty-value, or rival-AI behavior change.
  - No Expert winnability claim, hidden rival omniscience, broad balance pass,
    monitor-cost tuning, public-disclosure tuning, GUI, M&A, release
    automation, human-learning claim, empirical calibration claim, or
    policy-validity claim.

  Verification:
  - `python3 -m py_compile scripts/diagnose_runs.py _workspace/experiments/v0.10.37-rival-info-monitor-evidence/run_sessions.py`
  - `python3 _workspace/experiments/v0.10.37-rival-info-monitor-evidence/run_sessions.py`
  - `python3 -m json.tool _workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json --output _workspace/experiments/v0.10.37-rival-info-monitor-evidence/diagnostics.md`
  - `git diff --check`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`


- Feature: Rival Information Pressure Design
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.36

  Summary:
  Added a Phase 7 design note that defines rival information delay, monitor
  value, and public disclosure as the bounded difficulty pressure surfaces to
  test before any runtime tuning. The slice keeps runtime mechanics and balance
  unchanged.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.36.md` with the design intent, tier
    shape, promotion criteria, non-promotions, and evidence limits for rival
    information pressure.
  - Updated the MCP playtesting guide with a `v0.10.36` routing checkpoint.
  - Preserved runtime mechanics, command validation, stochastic inputs,
    scenarios, MCP DTOs, replay formats, state hashes, diagnostics logic,
    action costs, project costs, capacity effects, difficulty values, scoring,
    and balance.
  - Bumped package metadata to `0.10.36`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, diagnostic parser, or command-surface change.
  - No Expert winnability claim, difficulty value change, hidden rival
    omniscience, punitive player-resource cut, broad balance pass, command-cost
    change, AP-budget change, access-pledge cooldown, scoring redesign, new
    strategic actor class, GUI, M&A, release, or runtime tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new live-capture run, hidden score, validated learner archetype, assessment
    instrument, instructor export format, analytics platform, or broad evidence
    taxonomy.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.9.8-difficulty-sweep/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.9.9-difficulty-adaptive/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `git diff --check`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`


- Feature: Difficulty Pressure Dimension Gate
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.35

  Summary:
  Added a Phase 7 difficulty evidence gate that reviews current Easy/Normal/Hard
  difficulty artifacts and selects rival information and monitoring pressure
  visibility as the next bounded difficulty dimension to design or test. The
  slice keeps runtime mechanics and balance unchanged.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.35.md` with the current difficulty
    surface, selected dimension, recommended next slice, non-promotions, and
    evidence limits.
  - Updated the MCP playtesting guide with a `v0.10.35` routing checkpoint.
  - Preserved runtime mechanics, command validation, stochastic inputs,
    scenarios, MCP DTOs, replay formats, state hashes, diagnostics logic,
    action costs, project costs, capacity effects, difficulty values, scoring,
    and balance.
  - Bumped package metadata to `0.10.35`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, diagnostic parser, or command-surface change.
  - No Expert winnability claim, difficulty value change, hidden rival
    omniscience, punitive player-resource cut, broad balance pass, command-cost
    change, AP-budget change, access-pledge cooldown, scoring redesign, new
    strategic actor class, GUI, M&A, release, or runtime tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new live-capture run, hidden score, validated learner archetype, assessment
    instrument, instructor export format, analytics platform, or broad evidence
    taxonomy.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.9.8-difficulty-sweep/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.9.9-difficulty-adaptive/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.35-diagnostics.md`
  - `git diff --check`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`


- Feature: Instructor Debrief Facilitation Note
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.34

  Summary:
  Added a Phase 7 instructor facilitation note that connects recent competitive
  comparison, workforce-protective, and growth/capacity evidence into a
  repeated-run debrief sequence. The slice keeps runtime mechanics and balance
  unchanged.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.34.md` with a facilitation sequence,
    comparison prompts, routing guidance, and evidence limits.
  - Updated the MCP playtesting guide with a `v0.10.34` routing checkpoint.
  - Preserved runtime mechanics, command validation, stochastic inputs,
    scenarios, MCP DTOs, replay formats, state hashes, diagnostics logic,
    action costs, project costs, capacity effects, difficulty values, scoring,
    and balance.
  - Bumped package metadata to `0.10.34`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, diagnostic parser, or command-surface change.
  - No access-pledge cooldown, project-cost, capacity-effect,
    staffing-allocation, action-availability, difficulty, scoring, or
    balance-tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new live-capture run, hidden score, validated learner archetype, assessment
    instrument, instructor export format, analytics platform, or broad evidence
    taxonomy.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.34-live-diagnostics.md`
  - `git diff --check`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`


- Feature: Growth/Capacity-Oriented Evidence Review
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.33

  Summary:
  Added a Phase 7 focused evidence review for interpreting growth/capacity-
  oriented competitive play across existing simulated-agent,
  deterministic-policy, reviewer-policy, and operator-authored artifacts. The
  slice keeps runtime mechanics and balance unchanged.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.33.md` with growth/capacity signals,
    evidence reading, instructor prompts, routing guidance, and evidence limits.
  - Updated the MCP playtesting guide with a `v0.10.33` routing checkpoint.
  - Preserved runtime mechanics, command validation, stochastic inputs,
    scenarios, MCP DTOs, replay formats, state hashes, diagnostics logic,
    action costs, project costs, capacity effects, difficulty values, scoring,
    and balance.
  - Bumped package metadata to `0.10.33`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, diagnostic parser, or command-surface change.
  - No project-cost, capacity-effect, staffing-allocation, action-availability,
    difficulty, scoring, or balance-tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new live-capture run, hidden score, validated learner archetype, instructor
    export format, analytics platform, or broad evidence taxonomy.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json --output /tmp/hs-mgt-game-v0.10.33-static-adaptive-diagnostics.md`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.33-live-diagnostics.md`
  - `git diff --check`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`


- Feature: Future Queue Re-ranking and SDD Alignment
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.32

  Summary:
  Reviewed and restructured the `SPEC.md` Future queue so future work is easier
  to promote into bounded `Present` slices. The queue now separates promotion
  rules from ranked product/runtime tracks and keeps validation, teachability,
  and evidence gates ahead of broader expansion.

  Done:
  - Replaced the mixed 10-item Future queue with explicit promotion rules, a
    six-track ranked queue, and cross-cutting SDD guardrails.
  - Re-ranked next work around competitive teachability/validation before
    difficulty depth, regional affiliation/acquisition, GUI proof, broader
    simulation breadth, and release readiness.
  - Updated SDD handoff artifacts and changelog/version metadata for `0.10.32`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, MCP DTO, replay artifact, state hash,
    ruleset, GUI implementation, asset download, or scenario file change.
  - No difficulty tuning, Expert clearability claim, M&A legal forecast, merger
    outcome formula, GUI toolkit choice, desktop packaging, or asset pipeline.
  - No broad archive rewrite, new documentation framework, release convention,
    public package workflow, human-learning claim, empirical calibration claim,
    or policy-validity claim.

  Verification:
  - `rg` stale-queue/version scan over SDD and companion docs
  - `git diff --check`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`


- Feature: Expansion Proposal Review
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.31

  Summary:
  Added a validation-first proposal review and propagated roadmap/SDD guidance
  for three future expansion candidates: richer Capitalism-style difficulty
  tiers, one regional healthcare affiliation/acquisition slice, and a GUI thin
  client over the existing deterministic core.

  Done:
  - Added `docs/design/expansion-proposal-review.md` with proposal-review posture,
    source links, recommended gates, design implications, risks, and promotion
    rules.
  - Updated `docs/roadmap.md` with a Phase 7 expansion proposal review gate and
    Phase 9 routing for difficulty depth, regional consolidation, and GUI
    thin-client work.
  - Propagated future-boundary guidance into `ARCHITECTURE.md`,
    `docs/design_principles.md`, `docs/design/competitive-scenario-brief.md`,
    `docs/design/system-boundary.md`, `docs/design/scenario-format-draft.md`, and
    `docs/research/evidence-registry.md`.
  - Bumped package metadata to `0.10.31`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, MCP DTO, replay artifact, state hash,
    ruleset, GUI implementation, asset download, or scenario file change.
  - No difficulty tuning, Expert clearability claim, M&A legal forecast, merger
    outcome formula, GUI toolkit choice, desktop packaging, or asset pipeline.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new playtest run, broad scenario-authoring framework, national deal-market
    model, private-equity rollup simulator, or replacement of CLI/MCP.

  Verification:
  - `rg` stale-phrase scan over roadmap, SDD, and companion docs
  - `git diff --check`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`


- Feature: Workforce-Protective Evidence Review
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.30

  Summary:
  Added a Phase 7 focused evidence review for interpreting workforce-protective
  competitive play across existing simulated-agent, deterministic-policy,
  reviewer-policy, and operator-authored artifacts. The slice keeps runtime
  mechanics and balance unchanged.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.30.md` with workforce-protective
    signals, interpretation limits, instructor prompts, routing guidance, and
    evidence limits.
  - Updated the MCP playtesting guide with a `v0.10.30` routing checkpoint.
  - Preserved runtime mechanics, command validation, stochastic inputs,
    scenarios, MCP DTOs, replay formats, state hashes, diagnostics logic,
    action costs, pledge effects, difficulty values, scoring, and balance.
  - Bumped package metadata to `0.10.30`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, diagnostic parser, or command-surface change.
  - No workforce-trust formula, recruitment-cost, staffing allocation,
    action-availability, difficulty, scoring, or balance-tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new live-capture run, hidden score, validated learner archetype, instructor
    export format, analytics platform, or broad evidence taxonomy.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json >/dev/null`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json --output /tmp/hs-mgt-game-v0.10.30-difficulty-diagnostics.md`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json --output /tmp/hs-mgt-game-v0.10.30-static-adaptive-diagnostics.md`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`
  - `git diff --check`


- Feature: Competitive Debrief Comparison Surface
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.29

  Summary:
  Added a Phase 7 debrief comparison surface that helps instructors and
  reviewers compare repeated competitive runs across decision quality, outcome
  quality, cash runway, durable follow-through, rival pressure, and debrief
  traceability. The slice keeps runtime mechanics and balance unchanged.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.29.md` with a compact comparison table,
    strategy posture prompts, recommended use, follow-up routing, and evidence
    limits.
  - Updated the MCP playtesting guide with a `v0.10.29` routing checkpoint.
  - Preserved runtime mechanics, command validation, stochastic inputs,
    scenarios, MCP DTOs, replay formats, state hashes, diagnostics logic,
    action costs, pledge effects, difficulty values, scoring, and balance.
  - Bumped package metadata to `0.10.29`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, diagnostic parser, or command-surface change.
  - No access-pledge effect, cooldown, command-cost, action-availability,
    difficulty, scoring, or balance-tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new live-capture run, hidden score, validated learner archetype, instructor
    export format, analytics platform, or broad evidence taxonomy.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json >/dev/null`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.29-live-diagnostics.md`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.29-access-diagnostics.md`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`
  - `git diff --check`


- Feature: Competitive Strategy-Space Synthesis
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.28

  Summary:
  Added a Phase 7 strategy-space synthesis that compares finance-first,
  access-heavy, workforce-protective, and growth-oriented signals across
  existing competitive evidence. The slice keeps runtime mechanics and balance
  unchanged.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.28.md` with cross-run strategy-space
    signals, interpretation limits, follow-up routing, and evidence limits.
  - Updated the MCP playtesting guide with a `v0.10.28` routing checkpoint.
  - Preserved runtime mechanics, command validation, stochastic inputs,
    scenarios, MCP DTOs, replay formats, state hashes, diagnostics logic,
    action costs, pledge effects, difficulty values, scoring, and balance.
  - Bumped package metadata to `0.10.28`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, diagnostic parser, or command-surface change.
  - No access-pledge effect, cooldown, command-cost, action-availability,
    difficulty, scoring, or balance-tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new live-capture run, validated learner archetype, instructor export
    format, analytics platform, or broad evidence taxonomy.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json >/dev/null`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.28-live-diagnostics.md`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.28-access-diagnostics.md`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`
  - `git diff --check`


- Feature: Competitive Instructor Comparison Note
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.27

  Summary:
  Added an instructor-facing Phase 7 comparison note that turns existing
  competitive evidence into prompts about decision quality versus outcome
  quality. The slice keeps runtime mechanics and balance unchanged.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.27.md` with prompts for public
    commitments, cash runway, workforce follow-through, payer posture, rival
    pressure, and repeated-play comparison.
  - Updated the MCP playtesting guide with a `v0.10.27` routing checkpoint.
  - Preserved runtime mechanics, command validation, stochastic inputs,
    scenarios, MCP DTOs, replay formats, state hashes, diagnostics logic,
    action costs, pledge effects, difficulty values, scoring, and balance.
  - Bumped package metadata to `0.10.27`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, diagnostic parser, or command-surface change.
  - No access-pledge effect, cooldown, command-cost, action-availability,
    difficulty, scoring, or balance-tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new live-capture run, new instructor export format, analytics platform, or
    broad evidence taxonomy.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.27-diagnostics.md`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`
  - `git diff --check`


- Feature: Competitive Teachability Synthesis
  Status: Complete
  Started: 2026-07-09
  Version: 0.10.26

  Summary:
  Synthesized recent competitive Phase 7 evidence around teachability, debrief
  coherence, and repeated-play interest. The slice broadens the `v0.10.25`
  routing checkpoint without reopening runtime tuning.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.26.md` comparing the recent live
    difficulty, live-capture, access comprehension, and access evidence
    synthesis findings.
  - Updated the MCP playtesting guide with a `v0.10.26` routing checkpoint.
  - Preserved runtime mechanics, command validation, stochastic inputs,
    scenarios, MCP DTOs, replay formats, state hashes, diagnostics logic,
    action costs, pledge effects, difficulty values, and balance.
  - Bumped package metadata to `0.10.26`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, or diagnostic parser change.
  - No access-pledge effect, cooldown, command-cost, action-availability,
    difficulty, guidance wording, scoring, or balance-tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new live-capture run, analytics platform, or broad evidence taxonomy.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.26-diagnostics.md`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`
  - `git diff --check`


- Feature: Access Evidence Synthesis
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.25

  Summary:
  Synthesized the `v0.10.21` through `v0.10.24` access-heavy evidence chain.
  The synthesis closes the access follow-through mini-loop as debrief/guidance
  evidence and routes future access-related runtime work back behind a concrete
  mechanics finding.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.25.md` summarizing the live-capture
    synthesis, access comprehension review, debrief wording slice, and bounded
    trigger/control validation.
  - Updated the MCP playtesting guide with a `v0.10.25` routing checkpoint.
  - Preserved runtime mechanics, command validation, scenarios, MCP DTOs,
    replay formats, state hashes, diagnostics logic, action costs, pledge
    effects, difficulty values, and balance.
  - Bumped package metadata to `0.10.25`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, or diagnostic parser change.
  - No access-pledge effect, cooldown, command-cost, action-availability,
    difficulty, or balance-tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    new live-capture run, new analytics platform, or broad evidence taxonomy.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.25-diagnostics.md`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`
  - `git diff --check`


- Feature: Access Debrief Validation
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.24

  Summary:
  Validated that the `v0.10.23` access follow-through note appears through the
  MCP end-session debrief surface for bounded trigger runs and stays absent in
  nearby control runs.

  Done:
  - Added `_workspace/experiments/v0.10.24-access-debrief-validation/` with a
    deterministic MCP trigger/control runner and generated `results.json`.
  - Covered Normal and Hard difficulty runs at seed `42`, including
    under-followed repeated access pledges, a single-pledge low-cash control,
    and a repeated-pledge followed-through control.
  - Documented the validation results and evidence limits in
    `docs/history/playtests/v0.10/playtest-findings-v0.10.24.md`.
  - Updated the MCP playtesting guide and bumped package metadata to `0.10.24`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, or diagnostic parser change.
  - No access-pledge effect, cooldown, command-cost, action-availability,
    difficulty, or balance-tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    or new organic live-capture run.

  Verification:
  - `python3 _workspace/experiments/v0.10.24-access-debrief-validation/run_sessions.py`
  - `python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.24-diagnostics.md`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`
  - `git diff --check`


- Feature: Access Follow-Through Debrief Note
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.23

  Summary:
  Added a student-facing competitive debrief note for access-heavy low-cash
  runs. The note separates public access pledges from durable operational
  follow-through and remains explanatory rather than punitive.

  Done:
  - Added an `Access follow-through note:` to `competitive_debrief` when
    committed history shows at least two access pledges, final human cash below
    `20`, and fewer durable follow-through actions than pledges.
  - Counted durable follow-through from committed player recruitment,
    investment, monitoring, payer negotiation, and project commands.
  - Added focused debrief tests for the trigger and non-trigger cases.
  - Documented the slice and bumped package metadata to `0.10.23`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, or diagnostic parser change.
  - No access-pledge effect, cooldown, command-cost, action-availability,
    difficulty, guidance wording, or balance-tuning change.
  - No human-learning claim, empirical calibration claim, policy-validity claim,
    or new live-capture run.

  Verification:
  - `cargo test debrief::report_tests -- --test-threads=1`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`
  - `git diff --check`


- Feature: Access-Heavy Comprehension Evidence Review
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.22

  Summary:
  Reviewed the existing `v0.10.15` live-capture artifact and diagnostic report
  for whether access-heavy players can distinguish public access pledges from
  durable operational follow-through under cash pressure. The review routes the
  next bounded follow-up toward explanatory competitive debrief wording, not
  runtime tuning.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.22.md` comparing the Live Access
    Operator Normal and Hard runs, access pledge counts, live retry counts,
    cash-overrun retries, final tradeoff metrics, and debrief visibility.
  - Updated the MCP playtesting guide with the v0.10.22 routing note.
  - Kept runtime tuning, access-pledge cooldowns, command-cost changes,
    difficulty adjustments, and player-facing wording changes deferred.
  - Bumped package metadata to `0.10.22`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, or diagnostic parser change.
  - No new live-capture runs, analytics platform, optimizer, LLM runner, CI
    workflow, release system, or broad documentation taxonomy.
  - No guidance wording, debrief runtime wording, command-surface messaging,
    access-pledge cooldown, command-cost tuning, action-availability change,
    difficulty adjustment, human-learning claim, empirical calibration,
    policy-validity claim, or balance-tuning claim.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.22-diagnostics.md`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`
  - `git diff --check`


- Feature: Live Evidence Synthesis
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.21

  Summary:
  Synthesized the recent live-capture, difficulty, and retry-visibility evidence
  path from `v0.10.12` through `v0.10.20` without adding new runs or changing
  runtime behavior. The next bounded evidence gate is access-heavy player
  understanding of public access pledges versus durable operational
  follow-through under cash pressure.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.21.md` summarizing the live evidence
    matrix, retry-visibility interpretation, evidence limits, and recommended
    next gate.
  - Updated the MCP playtesting guide with the v0.10.21 routing note.
  - Kept runtime tuning, access-pledge cooldowns, command-cost changes,
    difficulty adjustments, and retry-metadata expansion deferred until a later
    evidence slice identifies a concrete mechanic problem.
  - Bumped package metadata to `0.10.21`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, replay artifact, state hash, ruleset,
    Rust MCP DTO, Python wrapper, or diagnostic parser change.
  - No new analytics platform, optimizer, LLM runner, CI workflow, release
    system, or broad documentation taxonomy.
  - No access-pledge cooldown, command-cost tuning, action-availability change,
    difficulty adjustment, human-learning claim, empirical calibration,
    policy-validity claim, or balance-tuning claim.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
  - `python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.21-diagnostics.md`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`


- Feature: Live Retry Visibility Checkpoint
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.20

  Summary:
  Recorded the Phase 7 checkpoint that the current live retry visibility gate is
  complete for live-capture classification: structured MCP validation fields are
  emitted, preserved by the Python wrapper, and preferred by diagnostics with
  legacy fallback.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.20.md` summarizing the v0.10.17-v0.10.19
    retry visibility path and its limits.
  - Updated the MCP playtesting guide with the v0.10.20 routing note.
  - Kept runtime tuning, command-cost changes, access-pledge cooldowns, and
    difficulty adjustments deferred until a later evidence slice names a
    concrete mechanic issue.
  - Bumped package metadata to `0.10.20`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, Rust MCP DTO, Python
    wrapper logic, diagnostic parser logic, command grammar, scenario schema,
    replay artifact, state hash, action-cost, or ruleset change.
  - No broad historical artifact rewrite, analytics platform expansion, CI
    workflow change, or diagnostic table redesign.
  - No human-learning claim, empirical calibration, policy-validity claim,
    access-pledge cooldown, command-cost tuning, or balance-tuning claim.

  Verification:
  - `python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.20-diagnostics.md`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test -- --test-threads=1`


- Feature: Live-Capture Structured Retry Metadata
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.19

  Summary:
  Updated the Python live-capture wrapper and diagnostics to preserve additive
  MCP structured retry metadata in artifacts so cash-overrun classification no
  longer depends on parsing human-readable error prose when structured fields
  are available.

  Done:
  - Added wrapper-side normalization of MCP structured tool errors into
    additive `code`, `resource_limit`, and `hint` fields while preserving the
    existing `error` string.
  - Added focused Python tests for structured-error normalization and
    structured-versus-legacy cash-retry classification.
  - Updated diagnostics to prefer structured retry metadata with fallback to
    legacy string-only artifact entries.
  - Refreshed the `v0.10.15` live difficulty-gate exemplar retry metadata and
    regenerated its diagnostic report.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.19.md` and updated the MCP playtesting
    guide.
  - Bumped package metadata to `0.10.19`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, Rust MCP DTO, command
    grammar, scenario schema, replay artifact, state hash, action-cost, or
    ruleset change.
  - No broad historical artifact rewrite, analytics platform expansion, CI
    workflow change, or diagnostic table redesign.
  - No access-pledge cooldown, command-cost tuning, action-availability change,
    human-learning claim, empirical calibration, or balance-tuning claim.

  Verification:
  - `python3 -m unittest discover -s tests -p 'test_playtest_wrapper*.py'`
  - `python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json`
  - `python3 _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: MCP Structured Validation Errors
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.18

  Summary:
  Added additive structured MCP error fields for competitive validation failures
  so live-capture wrappers can classify resource-limit retries, especially
  cash-overrun attempts, without parsing human-readable text.

  Done:
  - Extended MCP structured errors with optional `code`, `resource_limit`, and
    `hint` fields while preserving the existing `error` string.
  - Mapped competitive validation errors to stable snake_case codes.
  - Added resource-limit payloads for insufficient cash, AP budget exceeded,
    and insufficient political capital.
  - Added focused MCP session tests for cash-overrun structure, code-only
    validation errors, parser-error plain shape, and non-advancement.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.18.md` and updated MCP docs.
  - Bumped package metadata to `0.10.18`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command grammar,
    stochastic input, scenario schema, replay artifact, state hash, action-cost,
    or ruleset change.
  - No MCP transport, auth, durable session persistence, multi-client support,
    or broad tool DTO redesign.
  - No access-pledge cooldown, command-cost tuning, action-availability change,
    human-learning claim, empirical calibration, or balance-tuning claim.

  Verification:
  - `cargo test mcp::session::tests::competitive_ --lib`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Live Retry Cash-Pressure Diagnostics
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.17

  Summary:
  Added diagnostic visibility for optional `live_validation_retries` metadata in
  live-capture artifacts, making cash-overrun retry pressure visible separately
  from final replay validation failures.

  Done:
  - Updated `scripts/diagnose_runs.py` to report live retries, cash-overrun
    retries, other retries, and representative retry details.
  - Updated `tests/fixtures/live_capture_batch.json` with retry metadata for a
    compact diagnostic check.
  - Regenerated `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
    with a `Live Retry Signals` table.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.17.md` and updated
    `docs/guides/mcp-playtesting-guide.md`.
  - Bumped package metadata to `0.10.17`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
    change.
  - No access-pledge cooldown, command-cost tuning, action-availability change,
    general analytics platform, or broad diagnostic framework.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Live Difficulty Evidence Synthesis
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.16

  Summary:
  Compared recent Phase 7 live-capture difficulty evidence from `v0.10.12`
  through `v0.10.15` and selected cash-pressure / validation-retry visibility
  for access-heavy Hard live agents as the next bounded follow-up issue before
  any runtime tuning.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.16.md`.
  - Synthesized session counts, seeds, difficulty tiers, profile families,
    validation failures/retries, access-heavy behavior, and evidence limits
    across `v0.10.12` through `v0.10.15`.
  - Preserved the current evidence gate: guidance, debrief, or diagnostic
    visibility should precede runtime tuning.
  - Bumped package metadata to `0.10.16`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
    change.
  - No access-pledge cooldown, command-cost tuning, action-availability change,
    or broad analytics platform.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Live LLM Difficulty Gate
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.15

  Summary:
  Added a bounded Phase 7 live-decision difficulty gate using month-by-month
  simulated-agent decisions from actor-visible MCP observations across three
  profiles, seed `42`, and Normal/Hard competitive difficulty tiers.

  Done:
  - Added `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py`.
  - Captured six accepted 24-month competitive command streams with zero final
    replay validation failures.
  - Preserved live retry/source metadata, including Access Operator retries and
    the replacement Competitive Analyst Normal stream after the delegated run
    did not complete.
  - Generated `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
    and `diagnostics.md`.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.15.md` and updated the MCP playtesting
    guide.
  - Bumped package metadata to `0.10.15`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
    change.
  - No general LLM runner, analytics platform, optimizer, or broad diagnostics
    framework.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 -m py_compile scripts/play_game.py`
  - `python3 -m py_compile scripts/diagnose_runs.py`
  - `python3 -m py_compile _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py`
  - `python3 _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
  - `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Independent Reviewer-Agent Live Capture
  Status: Complete
  Started: 2026-07-08
  Version: 0.10.14

  Summary:
  Added a bounded Phase 7 live-capture matrix using independent
  observation-conditioned reviewer policies across seeds `42`, `43`, and `44`,
  Normal/Hard competitive difficulty tiers, and three reviewer profiles.

  Done:
  - Added `_workspace/experiments/v0.10.14-independent-reviewer-agent-capture/run_sessions.py`.
  - Captured 18 observation-by-observation competitive MCP runs with zero
    validation failures.
  - Generated `_workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json`
    and `diagnostics.md`.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.14.md` and updated the MCP playtesting
    guide.
  - Bumped package metadata to `0.10.14`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
    change.
  - No LLM runner, analytics platform, optimizer, or broad diagnostics
    framework.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 -m py_compile scripts/play_game.py`
  - `python3 -m py_compile scripts/run_automated_playtests.py`
  - `python3 -m py_compile scripts/diagnose_runs.py`
  - `python3 -m py_compile _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/run_sessions.py`
  - `python3 _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/run_sessions.py`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json --output _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/diagnostics.md`
  - `python3 -m json.tool _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Static-vs-Adaptive Live Capture
  Status: Complete
  Started: 2026-07-07
  Version: 0.10.13

  Summary:
  Added a bounded Phase 7 live-capture matrix comparing static deterministic
  profile policies against the existing difficulty-adaptive wrapper across
  seeds `42`, `43`, and `44`, Normal/Hard competitive difficulty tiers, and four
  existing automated playtest profiles.

  Done:
  - Added `_workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py`.
  - Captured 48 observation-by-observation competitive MCP runs with zero
    validation failures.
  - Generated `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
    and `diagnostics.md`.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.13.md` and updated the MCP playtesting
    guide.
  - Bumped package metadata to `0.10.13`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
    change.
  - No LLM runner, analytics platform, optimizer, or broad diagnostics
    framework.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 -m py_compile scripts/play_game.py`
  - `python3 -m py_compile scripts/run_automated_playtests.py`
  - `python3 -m py_compile _workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py`
  - `python3 _workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json --output _workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md`
  - `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Live Difficulty-Pressure Capture
  Status: Complete
  Started: 2026-07-07
  Version: 0.10.12

  Summary:
  Added a bounded Phase 7 live-capture matrix that reuses existing automated
  playtest profiles and the Hard difficulty-adaptive wrapper for Normal/Hard
  competitive comparison across seeds `42`, `43`, and `44`.

  Done:
  - Added `_workspace/experiments/v0.10.12-live-difficulty-pressure/run_sessions.py`.
  - Captured 24 observation-by-observation competitive MCP runs with zero
    validation failures.
  - Generated `_workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
    and `diagnostics.md`.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.12.md` and updated the MCP playtesting
    guide.
  - Bumped package metadata to `0.10.12`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
    change.
  - No LLM runner, analytics platform, optimizer, or broad diagnostics
    framework.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 -m py_compile scripts/play_game.py`
  - `python3 -m py_compile scripts/run_automated_playtests.py`
  - `python3 -m py_compile _workspace/experiments/v0.10.12-live-difficulty-pressure/run_sessions.py`
  - `python3 _workspace/experiments/v0.10.12-live-difficulty-pressure/run_sessions.py`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json --output _workspace/experiments/v0.10.12-live-difficulty-pressure/diagnostics.md`
  - `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Live-Capture Matrix Evidence
  Status: Complete
  Started: 2026-07-07
  Version: 0.10.11

  Summary:
  Added a bounded Phase 7 live-capture matrix over the existing deterministic
  persona policies, seeds `42`, `43`, and `44`, and Normal/Hard competitive
  difficulty tiers.

  Done:
  - Added `_workspace/experiments/v0.10.11-live-capture-matrix/run_sessions.py`.
  - Captured 18 observation-by-observation competitive MCP runs with zero
    validation failures.
  - Generated `_workspace/experiments/v0.10.11-live-capture-matrix/results.json`
    and `diagnostics.md`.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.11.md` and updated the MCP playtesting
    guide.
  - Bumped package metadata to `0.10.11`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
    change.
  - No LLM runner, analytics platform, optimizer, or broad diagnostics
    framework.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 -m py_compile scripts/play_game.py`
  - `python3 -m py_compile _workspace/experiments/v0.10.11-live-capture-matrix/run_sessions.py`
  - `python3 _workspace/experiments/v0.10.11-live-capture-matrix/run_sessions.py`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.11-live-capture-matrix/results.json --output _workspace/experiments/v0.10.11-live-capture-matrix/diagnostics.md`
  - `python3 -m json.tool _workspace/experiments/v0.10.11-live-capture-matrix/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Live-Capture Diagnostics
  Status: Complete
  Started: 2026-07-07
  Version: 0.10.10

  Summary:
  Extended the existing strategy-space diagnostics script to parse the v0.10.9
  live MCP capture artifact shape and report profile outcomes, action
  frequencies, validation failures, access pledges, final hashes, and evidence
  limits.

  Done:
  - Added live-capture artifact parsing and markdown output to
    `scripts/diagnose_runs.py`.
  - Added a compact live-capture fixture under `tests/fixtures/`.
  - Generated `_workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md`
    from the v0.10.9 capture artifact.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.10.md` and updated the MCP playtesting
    guide.
  - Bumped package metadata to `0.10.10`.

  Deferred / Non-Goals:
  - No runtime simulation, balance formula, transition, command validation,
    stochastic input, scenario schema, MCP DTO, replay artifact, or state hash
    change.
  - No LLM runner, analytics platform, optimizer, or broad diagnostics
    framework.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 -m py_compile scripts/diagnose_runs.py`
  - `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
  - `python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.9-live-mcp-capture/results.json --output _workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md`
  - `python3 -m json.tool _workspace/experiments/v0.10.9-live-mcp-capture/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Live MCP Capture Evidence
  Status: Complete
  Started: 2026-07-07
  Version: 0.10.9

  Summary:
  Added a bounded Phase 7 live-capture evidence slice that records actor-visible
  observations, legal command hints, submitted commands, validation outcomes,
  transition hashes, final observations, and debriefs for Hard competitive MCP
  sessions.

  Done:
  - Extended `scripts/play_game.py` with optional trace capture while preserving
    existing caller behavior.
  - Captured three deterministic persona-policy runs for Hard competitive play
    at seed `42`, all completing 24 months with zero validation failures.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.9.md` and replay artifacts under
    `_workspace/experiments/v0.10.9-live-mcp-capture/`.
  - Bumped package metadata to `0.10.9`.

  Deferred / Non-Goals:
  - No runtime access-pledge cooldown, pledge-effect tuning, command validation,
    transition, stochastic input, scenario schema, MCP DTO, state hash, or
    balance change.
  - No general LLM runner, networked agent integration, hidden-state exposure,
    or MCP transport change.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 _workspace/experiments/v0.10.9-live-mcp-capture/run_sessions.py`
  - `python3 -m json.tool _workspace/experiments/v0.10.9-live-mcp-capture/results.json >/dev/null`


- Feature: Active Project Document Alignment
  Status: Complete
  Started: 2026-07-07
  Version: 0.10.8

  Summary:
  Reviewed active project documents for stale current-facing statements and
  aligned them with the implemented 24-month competitive campaign, competitive
  scenario loading, replay export, MCP boundaries, and command autocomplete
  status.

  Done:
  - Updated active architecture, scenario, MCP, player-facing, and competitive
    design docs to remove obsolete preview/deferred wording for completed
    features.
  - Kept historical changelog entries, archived docs, and versioned playtest
    findings unchanged.
  - Bumped package metadata to `0.10.8`.

  Deferred / Non-Goals:
  - No runtime behavior, command grammar, MCP DTO, scenario schema, replay
    artifact, state hash, balance, or validation change.
  - No edits to historical playtest findings, archived docs, or old changelog
    entries.
  - No empirical calibration, policy-validity, forecasting, human-learning, or
    classroom-effectiveness claim.

  Verification:
  - `cargo fmt --check`
  - `cargo test`
  - Targeted stale-marker search over active project documents


- Feature: LLM Access-Pledge Evidence
  Status: Complete
  Started: 2026-07-07
  Version: 0.10.7

  Summary:
  Recorded a bounded Phase 7 sub-agent evidence slice testing whether repeated
  access pledges appear outside deterministic operator heuristics after the
  v0.10.3 guidance and v0.10.6 debrief QA work.

  Done:
  - Captured three sub-agent generated command plans for Hard competitive play
    at seed `42`.
  - Replayed the accepted command sequences through the MCP harness with zero
    validation failures across three completed 24-month sessions.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.7.md` and replay artifacts under
    `_workspace/experiments/v0.10.7-llm-access-pledge-evidence/`.
  - Bumped package metadata to `0.10.7`.

  Deferred / Non-Goals:
  - No runtime access-pledge cooldown, pledge-effect tuning, command validation,
    transition, stochastic input, scenario schema, MCP DTO, replay artifact,
    state hash, or balance change.
  - No general LLM runner, live LLM integration, new strategic actor, or MCP
    transport change.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 _workspace/experiments/v0.10.7-llm-access-pledge-evidence/run_sessions.py`
  - `python3 -m json.tool _workspace/experiments/v0.10.7-llm-access-pledge-evidence/results.json >/dev/null`


- Feature: Competitive Access-Pledge Debrief QA
  Status: Complete
  Started: 2026-07-07
  Version: 0.10.6

  Summary:
  Added a competitive debrief decision-quality check for repeated public access
  pledges that are not paired with capacity, staffing, monitoring, or payer
  follow-through in the same three-month window. This keeps access-loop
  follow-up in the educational debrief layer without changing runtime mechanics
  or balance values.

  Done:
  - Added deterministic debrief-only warning logic derived from committed
    competitive human command history.
  - Added a student-facing access pledge lesson to the competitive debrief.
  - Added focused tests for warning, follow-through suppression, and lesson text.
  - Bumped package metadata to `0.10.6`.

  Deferred / Non-Goals:
  - No runtime access-pledge cooldown, pledge-effect tuning, command validation,
    transition, stochastic input, scenario schema, MCP DTO, replay artifact,
    state hash, or balance change.
  - No new playtest runs, LLM runner, analytics tooling, or default scripted
    batch replacement.
  - No human-learning, classroom-effectiveness, empirical calibration,
    policy-validity, or balance-tuning claim.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Phase 7 Evidence Synthesis
  Status: Complete
  Started: 2026-07-07
  Version: 0.10.5

  Summary:
  Synthesized the existing v0.10.0-v0.10.4 free-form Hard competitive
  artifacts. Recorded completion, access-pledge loop, guidance-aware behavior,
  endpoint tradeoff, and evidence de-duplication conclusions without adding new
  runs or changing runtime behavior.

  Done:
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.5.md` with source matrix, synthesis
    findings, evidence limits, and next evidence gate.
  - Updated the MCP playtesting guide to point access-pledge follow-up work to
    the v0.10.5 synthesis.
  - Recorded a `LESSONS.md` entry about de-duplicating repeated baseline
    controls in Phase 7 synthesis.
  - Bumped package metadata to `0.10.5`.

  Deferred / Non-Goals:
  - No new run capture, script change, runtime simulation, command grammar, MCP
    DTO, scenario schema, replay artifact, state hash, or balance change.
  - No automatic command cooldown, pledge-effect tuning, default scripted batch
    replacement, LLM runner, or new analytics tooling.
  - No human-learning, empirical calibration, classroom-effectiveness,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 -m json.tool _workspace/experiments/v0.10.0-free-form-hard/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.1-free-form-hard-seed-variation/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.2-access-loop-diagnostic/results.json >/dev/null`
  - `python3 -m json.tool _workspace/experiments/v0.10.4-post-guidance-validation/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Post-Guidance Validation
  Status: Complete
  Started: 2026-07-06
  Version: 0.10.4

  Summary:
  Tested whether the v0.10.3 access-commitment guidance can be represented as a
  bounded simulated-agent policy change. Compared unchanged free-form Hard
  policies against a guidance-aware variant that suppresses repeated/high-access
  pledges and redirects to existing legal fallback actions.

  Done:
  - Ran 18 Hard competitive sessions: three free-form profiles, three seeds,
    and two policy variants, with zero validation failures across 24 months
    each.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.4.md` with command totals, endpoint
    comparison, hypotheses, evidence limits, and follow-up routing.
  - Added `_workspace/experiments/v0.10.4-post-guidance-validation/` operator
    capture script and generated JSON artifact.
  - Updated the MCP playtesting guide with the post-guidance validation
    procedure.
  - Bumped package metadata to `0.10.4`.

  Deferred / Non-Goals:
  - No runtime simulation, command grammar, MCP DTO, scenario schema, replay
    artifact, state hash, or balance change.
  - No automatic command cooldown, pledge-effect tuning, default scripted batch
    replacement, or LLM runner.
  - No human-learning, empirical calibration, classroom-effectiveness,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 _workspace/experiments/v0.10.4-post-guidance-validation/run_sessions.py`
  - `python3 -m json.tool _workspace/experiments/v0.10.4-post-guidance-validation/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Access Commitment Guidance Hardening
  Status: Complete
  Started: 2026-07-06
  Version: 0.10.3

  Summary:
  Converted the v0.10.2 access-loop diagnostic into player-facing competitive
  guidance. Clarified that public access pledges are legitimacy commitments,
  not substitutes for durable capacity, staffing, monitoring, or payer work.

  Done:
  - Updated competitive general help and `help commit` guidance.
  - Realigned general competitive help with already-supported neurology and ASC
    invest/project vocabularies.
  - Added focused CLI guidance tests for the new access-pledge language and
    vocabulary coverage.
  - Updated How to Play strategy notes and package metadata to `0.10.3`.

  Deferred / Non-Goals:
  - No runtime command cooldown, pledge-effect tuning, balance pass, playtest
    runner change, scenario schema change, MCP DTO change, replay artifact
    change, or state hash change.
  - No new evidence batch, LLM runner, human-learning claim, empirical
    calibration claim, classroom-effectiveness claim, or policy-validity claim.

  Verification:
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Access-Loop Diagnostic
  Status: Complete
  Started: 2026-07-06
  Version: 0.10.2

  Summary:
  Tested whether the repetitive access-commitment loop found in v0.10.1 could be
  reduced at the operator-policy layer. Compared unchanged baseline free-form
  Hard policies against cooldown and reported-access-threshold variants across
  the same three profiles and seeds 42, 43, and 44.

  Done:
  - Ran 27 Hard competitive sessions: three free-form profiles, three seeds, and
    three policy variants, with zero validation failures across 24 months each.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.2.md` with variant definitions, command
    totals, endpoint comparison, evidence limits, and follow-up routing.
  - Added `_workspace/experiments/v0.10.2-access-loop-diagnostic/` operator
    capture script and generated JSON artifact.
  - Updated the MCP playtesting guide with the access-loop diagnostic procedure.
  - Bumped package metadata to `0.10.2`.

  Deferred / Non-Goals:
  - No runtime simulation, command grammar, MCP DTO, scenario schema, replay
    artifact, state hash, or balance change.
  - No automatic command cooldown, pledge-effect tuning, default scripted batch
    replacement, or LLM runner.
  - No human-learning, empirical calibration, classroom-effectiveness,
    policy-validity, or balance-tuning claim.

  Verification:
  - `python3 _workspace/experiments/v0.10.2-access-loop-diagnostic/run_sessions.py`
  - `python3 -m json.tool _workspace/experiments/v0.10.2-access-loop-diagnostic/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Free-Form Hard Seed Variation
  Status: Complete
  Started: 2026-07-06
  Version: 0.10.1

  Summary:
  Extended the bounded free-form MCP competitive Hard artifact from seed 42 to
  seeds 42, 43, and 44. Documented seed-variation evidence for the same three
  observation-driven profiles and preserved explicit evidence limits.

  Done:
  - Ran three free-form profiles (Fiscal Steward, Access Expansion Advocate,
    First-Time Executive) at Hard difficulty across seeds 42, 43, and 44, with
    zero validation failures across 24 months each.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.1.md` with session matrix, outcome
    table, action-frequency signals, evidence limits, and follow-up routing.
  - Added `_workspace/experiments/v0.10.1-free-form-hard-seed-variation/`
    operator capture script and generated JSON artifact.
  - Updated the MCP playtesting guide with the free-form Hard seed-variation
    procedure.
  - Bumped package metadata to `0.10.1`.

  Deferred / Non-Goals:
  - No runtime simulation, command grammar, MCP DTO, scenario schema, replay
    artifact, state hash, or balance change.
  - No profile-policy tuning, validation-failure retry loop, Expert difficulty
    sweep, or stabilization re-run requirement.
  - No human-learning, empirical calibration, classroom-effectiveness,
    policy-validity, or balance-tuning claim.
  - No default baseline batch replacement in `scripts/run_automated_playtests.py`.

  Verification:
  - `python3 _workspace/experiments/v0.10.1-free-form-hard-seed-variation/run_sessions.py`
  - `python3 -m json.tool _workspace/experiments/v0.10.1-free-form-hard-seed-variation/results.json >/dev/null`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Free-Form Hard Competitive Playtest Synthesis
  Status: Complete
  Started: 2026-07-06
  Version: 0.10.0

  Summary:
  Collected bounded free-form MCP competitive sessions at Hard difficulty on the
  full 24-month campaign. Documented observation-driven play evidence and compared
  outcomes against v0.9.9 difficulty-adaptive scripted Hard baselines.

  Done:
  - Ran three free-form profiles (Fiscal Steward, Access Expansion Advocate,
    First-Time Executive) at Hard difficulty, seed 42, with zero validation
    failures across 24 months each.
  - Added `docs/history/playtests/v0.10/playtest-findings-v0.10.0.md` with session matrix, outcome
    comparison vs v0.9.9 adaptive Hard baselines, evidence limits, and
    follow-up routing.
  - Updated the MCP playtesting guide with the free-form Hard competitive
    procedure.
  - Bumped package metadata to `0.10.0`.

  Deferred / Non-Goals:
  - No runtime simulation, command grammar, MCP DTO, scenario schema, replay
    artifact, state hash, or balance change.
  - No new LLM runner, Expert difficulty sweep, seed-variation batch, or
    human-learning / calibration claim.
  - No default baseline batch replacement in `scripts/run_automated_playtests.py`.

  Verification:
  - `python3 _workspace/experiments/v0.10.0-free-form-hard/run_sessions.py`
  - `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
  - `cargo fmt --check`
  - `cargo clippy --all-targets -- -D warnings`
  - `cargo test`


- Feature: Difficulty-Adaptive Playtest Policies
  Status: Complete
  Started: 2026-07-06
  Version: 0.9.9

  Summary:
  Added a targeted Phase 7 automated MCP playtest mode for difficulty-adaptive
  competitive policies. The harness runs baseline scripted profiles at Easy and
  Hard difficulty with rival-aware command adjustments on Hard while preserving
  the default Normal-only baseline batch.

  Done:
  - Added `--target difficulty-adaptive` to `scripts/run_automated_playtests.py`
    with `adapt_command` and `with_difficulty` policy wrappers.
  - Extended `scripts/diagnose_runs.py` with difficulty-adaptive action-frequency
    comparison notes for batch artifacts.
  - Added `docs/history/playtests/v0.9/playtest-findings-v0.9.9.md` documenting the completed targeted
    batch, evidence limits, and follow-up routing.
  - Updated the MCP playtesting guide with the difficulty-adaptive target.
  - Bumped package metadata to `0.9.9`.

  Deferred / Non-Goals:
  - No runtime simulation, command grammar, MCP DTO, scenario schema, replay
    artifact, state hash, or balance change.
  - No human-learning, empirical calibration, classroom-effectiveness,
    equilibrium, policy-validity, or balance-tuning claim.
  - No Expert difficulty sweep, default baseline replacement, or free-form agent
    profiles in this slice.

  Verification:
  - `python3 scripts/run_automated_playtests.py --target difficulty-adaptive --json-output _workspace/experiments/v0.9.9-difficulty-adaptive/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.9-difficulty-adaptive/results.json --output _workspace/experiments/v0.9.9-difficulty-adaptive/diagnostics.md`


- Feature: Difficulty-Tier Playtest Synthesis
  Status: Complete
  Started: 2026-07-06
  Version: 0.9.8

  Summary:
  Added a targeted Phase 7 automated MCP playtest mode for competitive
  difficulty-tier coverage. The harness runs baseline scripted profiles at Easy
  and Hard difficulty while preserving the default Normal-only baseline batch.
  Diagnostics now report outcomes grouped by difficulty.

  Done:
  - Added `--target difficulty-sweep` to `scripts/run_automated_playtests.py`
    while preserving the default baseline batch.
  - Extended `scripts/diagnose_runs.py` with per-difficulty and
    profile-by-difficulty outcome tables for batch artifacts.
  - Added `docs/history/playtests/v0.9/playtest-findings-v0.9.8.md` documenting the completed targeted
    batch, evidence limits, and follow-up routing.
  - Updated the MCP playtesting guide with the difficulty-sweep target.
  - Bumped package metadata to `0.9.8`.

  Deferred / Non-Goals:
  - No runtime simulation, command grammar, MCP DTO, scenario schema, replay
    artifact, state hash, or balance change.
  - No human-learning, empirical calibration, classroom-effectiveness,
    equilibrium, policy-validity, or balance-tuning claim.
  - No Expert difficulty sweep, default baseline replacement, or difficulty-
    adaptive scripted policies in this slice.

  Verification:
  - `python3 scripts/run_automated_playtests.py --target difficulty-sweep --json-output _workspace/experiments/v0.9.8-difficulty-sweep/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.8-difficulty-sweep/results.json --output _workspace/experiments/v0.9.8-difficulty-sweep/diagnostics.md`


- Feature: Project-Command Playtest Diagnostics
  Status: Complete
  Started: 2026-07-06
  Version: 0.9.7

  Summary:
  Added a targeted Phase 7 automated MCP playtest mode for competitive
  capital-project command coverage. The diagnostic script now reports
  project-command counts, project kinds, final active projects, and final
  monthly project draws for automated batch artifacts without changing runtime
  simulation behavior or balance values.

  Done:
  - Added `--target project-coverage` to `scripts/run_automated_playtests.py`
    while preserving the default baseline batch.
  - Added a Project Coverage policy that completes both current campaigns across
    seeds `42`, `43`, and `44`.
  - Extended `scripts/diagnose_runs.py` to report project-command counts,
    project kinds, final active projects, and final monthly draws.
  - Added `docs/history/playtests/v0.9/playtest-findings-v0.9.7.md` documenting the completed targeted
    batch, evidence limits, and follow-up routing.
  - Updated the MCP playtesting guide with the target command.
  - Recorded a project-command concurrency lesson in `LESSONS.md`.
  - Bumped package metadata to `0.9.7`.

  Deferred / Non-Goals:
  - No runtime simulation, command grammar, MCP DTO, scenario schema, replay
    artifact, state hash, or balance change.
  - No human-learning, empirical calibration, classroom-effectiveness,
    equilibrium, policy-validity, or balance-tuning claim.
  - No default baseline-policy replacement, analytics platform, optimizer, or
    raw transcript archive.

  Verification:
  - `python3 scripts/run_automated_playtests.py --target project-coverage --json-output _workspace/experiments/v0.9.7-project-command-coverage/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.7-project-command-coverage/results.json --output _workspace/experiments/v0.9.7-project-command-coverage/diagnostics.md`


- Feature: Competitive Playtest Policy Coverage
  Status: Complete
  Started: 2026-07-06
  Version: 0.9.6

  Summary:
  Extended Phase 7 scripted competitive MCP playtest policies beyond month 3.
  The automated playtest runner now exercises more of the 24-month competitive
  command space, including newer service-line investments, public-payer
  negotiations, staffing, monitoring, and commitments, without changing runtime
  simulation behavior or balance values.

  Done:
  - Updated the competitive branches of the four scripted policies in
    `scripts/run_automated_playtests.py`.
  - Added `docs/history/playtests/v0.9/playtest-findings-v0.9.6.md` documenting the completed batch,
    action-frequency diagnostics, evidence limits, and follow-up routing.
  - Updated the MCP playtesting guide with the v0.9.6 artifact commands and
    coverage description.
  - Recorded a long-run scripted-policy budgeting lesson in `LESSONS.md`.
  - Bumped package metadata to `0.9.6`.

  Deferred / Non-Goals:
  - No runtime simulation, command grammar, MCP DTO, scenario schema, replay
    artifact, state hash, or balance change.
  - No human-learning, empirical calibration, classroom-effectiveness,
    equilibrium, policy-validity, or balance-tuning claim.
  - No new analytics platform, optimizer, raw transcript archive, or broad
    project-command coverage push.

  Verification:
  - `python3 scripts/run_automated_playtests.py --json-output _workspace/experiments/v0.9.6-playtest-policy-coverage/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.6-playtest-policy-coverage/results.json --output _workspace/experiments/v0.9.6-playtest-policy-coverage/diagnostics.md`
  - `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`


- Feature: Strategy-Space Diagnostics Artifact
  Status: Complete
  Started: 2026-07-06
  Version: 0.9.5

  Summary:
  Added a lightweight Phase 7 diagnostics artifact path for scripted MCP
  playtest batches. The automated playtest runner can now write compact JSON
  evidence, and the diagnostic script can summarize that batch without changing
  simulation behavior, MCP DTOs, replay formats, command grammar, or balance.

  Done:
  - Added optional `--json-output` support to
    `scripts/run_automated_playtests.py`.
  - Extended `scripts/diagnose_runs.py` to accept automated playtest batch JSON
    in addition to existing competitive replay JSON.
  - Added `docs/history/playtests/v0.9/playtest-findings-v0.9.5.md` documenting strategy-space
    diagnostic results, evidence limits, and follow-up routing.
  - Updated the MCP playtesting guide with the JSON artifact and diagnostic
    commands.
  - Bumped package metadata to `0.9.5`.

  Deferred / Non-Goals:
  - No runtime simulation, command grammar, MCP DTO, scenario schema, replay
    artifact, state hash, or balance change.
  - No human-learning, empirical calibration, classroom-effectiveness,
    equilibrium, or policy-validity claim.
  - No broad raw transcript archive committed.

  Verification:
  - `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
  - `python3 scripts/run_automated_playtests.py --json-output _workspace/experiments/v0.9.5-playtest-batch/results.json`
  - `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.5-playtest-batch/results.json --output _workspace/experiments/v0.9.5-playtest-batch/diagnostics.md`


- Feature: Agent Playtest Synthesis After Service-Line Expansion
  Status: Complete
  Started: 2026-07-06
  Version: 0.9.4

  Summary:
  Recorded a Phase 7 scripted AI-agent playtest synthesis after the recent
  service-line expansion through ASC. The slice validates that both current
  campaigns complete through the local MCP playtest harness across four
  scripted profiles and seeds `42`, `43`, and `44`, while keeping evidence
  limits explicit.

  Done:
  - Added `docs/history/playtests/v0.9/playtest-findings-v0.9.4.md` with session matrix, metric
    ranges, representative hashes, rubric scores, evidence limits, and
    follow-up recommendations.
  - Verified 12 stabilization and 12 competitive scripted MCP sessions
    completed without validation failures.
  - Bumped package metadata to `0.9.4`.

  Deferred / Non-Goals:
  - No simulation behavior, command grammar, MCP DTO, scenario schema, golden
    hash, balance, or strategic actor change.
  - No claims about human learning, empirical calibration, classroom
    effectiveness, or real-world policy validity.

  Verification:
  - `python3 scripts/run_automated_playtests.py` completed all scripted
    sessions.


- Feature: Ambulatory Surgery Center Service Line
  Status: Complete
  Started: 2026-07-05
  Version: 0.9.3

  Summary:
  Implemented the Ambulatory Surgery Center (ASC) Service Line mechanics representing outpatient surgery infrastructure. Configured specialized staffing targets, hierarchical nurse and physician allocations prioritizing ASC 9th (after Infusion and before Outpatient Clinics), and clinical overflow rules (outpatient surgery deferrals with `-1` community trust and `-1` market share index penalties).

  Done:
  - Added `asc_capacity` to competitive system state, player observations, and pending effects.
  - Configured `InvestDomain::Asc` and `ProjectKind::AscUnit` (6-month build time).
  - Implemented nurse/physician staffing targets and priority allocation logic.
  - Implemented outpatient surgery deferral rules.
  - Bumped competitive state hash version to v8 (`asc=`) with golden hash `8926f71296f39efc`.
  - Added CLI parsing, autocompletions, REPL guidance documentation, and executive dashboard layout updates.
  - Created comprehensive unit tests validating ASC capacity, staffing, and strike/deferral penalties.

  Deferred / Non-Goals:
  - None.

  Verification:
  - `cargo test` passes all tests.


- Feature: Neurology & Stroke Center Service Line
  Status: Complete
  Started: 2026-07-05
  Version: 0.9.1–v0.9.2

  Summary:
  Implemented the Neurology & Stroke Center inpatient service line with capacity-staffing trade-offs, specialized staffing targets, hierarchical allocation prioritizing Neurology sixth (after Psychiatric and before Oncology), and ED boarding/diversion mechanics.

  Done:
  - Added `neurology_capacity` to system state structure and `NeurologyCapacity` to `PendingEffectKind`.
  - Added `InvestDomain::Neurology` and `ProjectKind::NeurologyUnit` (6-month build time).
  - Implemented target staffing requirements and 6th-priority nurse/physician hierarchical allocation for Neurology.
  - Implemented Neurology ED holding boarding and diversion mechanics under capacity/staffing deficit (incurring `-2` community trust and `-2` quality index penalties).
  - Integrated Neurology capacity and diversion into observation mapping, REPL executive dashboard, parser, autocomplete, and guidance help pages.
  - Created comprehensive unit tests validating Neurology priority allocation, diversion penalties under deficit, and project resolution.
  - Updated competitive state hash to v7 (adding `neuro=`) with value `807fcbc8edeea8e3`.

  Deferred / Non-Goals:
  - None.

  Verification:
  - `cargo test` passes all tests.


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
  - Updated `README.md`, `ARCHITECTURE.md`, `SPEC.md`, `docs/roadmap.md`, `docs/guides/how-to-play.md`, `docs/reference/versioning-policy.md`, `docs/design/core-loop-spec.md`, `docs/design/system-boundary.md`, `docs/design/competitive-scenario-brief.md`, `docs/design/first-scenario-brief.md`, and `docs/validation/playtesting.md` to remove outdated "three-month" and "deferred" statements.
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
  Aligned versioning policy documentation in docs/reference/versioning-policy.md and version history in CHANGELOG.md with the repository rules (0.0.1 bump per PR/PR-equivalent change, 0.1 minor bump for major features/milestones with lower digits reset).

  Done:
  - Updated docs/reference/versioning-policy.md to specify the exact semver bump rules.
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



- Feature: Rival Information Follow-Through Evidence
  Status: Complete
  Started: 2026-07-10
  Version: 0.10.43

  Summary:
  Added a bounded Phase 7 MCP evidence matrix testing whether deterministic
  policies respond on the next turn to rival intelligence exposed by the
  actor-visible monitor surface.

  Done:
  - Added monitor-reactive, monitor-ignoring, and unmonitored policies across
    seeds 42–44 and Hard/Expert difficulty for 18 total runs.
  - Recorded visible signal source months, next-turn response commands, ignored
    controls, and safe resource-aware behavior.
  - Verified monitor-ignoring and unmonitored control hashes match across all
    seed/difficulty pairs.
  - Updated the Phase 7 findings, MCP playtesting guide, handoffs, changelog,
    README milestone, lessons, and package metadata.

  Deferred / Non-Goals:
  - No runtime monitor, difficulty, balance, scoring, rival-AI, MCP schema,
    scenario, replay, ruleset, or state-hash change.
  - No causal monitor-value, human-learning, policy-validity, or calibration
    claim.

  Verification:
  - 18 runs completed 24 transitions each with zero validation failures.
  - Evidence artifact regeneration was byte-for-byte stable.
  - Focused and full Python tests, formatting, clippy, Rust tests, automated
    playtests, JSON validation, and diff checks passed.


- Feature: Information-to-Action Comparison Evidence
  Status: Complete
  Started: 2026-07-10
  Version: 0.10.44

  Summary:
  Added a bounded Phase 7 synthesis connecting the generic consultant-advice
  and rival-monitor evidence chains into one instructor-facing comparison
  surface.

  Done:
  - Added visibility, response, follow-through, outcome, and explanation
    prompts for comparing completed competitive runs.
  - Linked each comparison claim to existing v0.10.37, v0.10.40, v0.10.41,
    v0.10.42, and v0.10.43 evidence artifacts.
  - Preserved the distinction between actor-visible information, organizational
    outcomes, social welfare, and educational evaluation.

  Deferred / Non-Goals:
  - No new capture matrix, runtime simulation, command, scenario, replay,
    state-hash, MCP schema, advisor market, difficulty, scoring, or balance
    change.
  - No causal monitor/advice, human-learning, policy-validity, or calibration
    claim.

  Verification:
  - Source evidence JSON artifacts parse successfully.
  - Full Python tests, formatting, clippy, Rust tests, automated playtests, and
    diff checks pass.


- Feature: Instructor Debrief-Use Audit Evidence
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.45

  Summary:
  Audited the existing v0.10.37, v0.10.40, v0.10.41, and v0.10.43 evidence
  artifacts for the five information-to-action review steps before promoting
  runtime work.

  Done:
  - Added a deterministic read-only audit with JSON and Markdown outputs across
    70 complete source runs.
  - Added focused tests for complete, partial, and deterministic audit output.
  - Confirmed all four source artifacts expose trace coverage for visibility,
    response, follow-through, outcomes, and explanation.
  - Preserved the distinction between traceability, educational clarity,
    decision quality, outcome quality, and causal claims.

  Deferred / Non-Goals:
  - No new sessions, runtime simulation, command, scenario, replay, state-hash,
    MCP schema, advisor market, difficulty, scoring, or balance change.
  - No human-learning, advice-quality, monitor-value, calibration, policy-
    validity, or validated-assessment claim.

  Verification:
  - Source artifacts parse and regenerated audit output is byte-for-byte stable.
  - Focused and full Python tests, formatting, clippy, Rust tests, automated
    playtests, and diff checks pass.


- Feature: Expert Clearability Evidence
  Status: Complete
  Started: 2026-07-10
  Version: 0.10.46

  Summary:
  Captured a bounded Expert competitive completion matrix using the four
  existing scripted profiles across seeds 42, 43, and 44.

  Done:
  - Added 12 deterministic MCP runs with actor-visible traces, commands,
    transition histories, state hashes, and debriefs.
  - Confirmed all profiles completed 24 months with zero validation failures.
  - Added focused coverage for matrix completeness, recorded failures, and
    deterministic diagnostics.
  - Kept completion evidence separate from general winnability, balance,
    causal, learning, and policy-validity claims.

  Deferred / Non-Goals:
  - No difficulty values, rival behavior, action costs, scoring, balance,
    runtime mechanics, command, scenario, replay, MCP schema, or state-hash
    change.
  - No general Expert winnability, human-learning, calibration, or policy-
    validity claim.

  Verification:
  - All 12 runs complete 24 months with zero validation failures.
  - Generated JSON and Markdown diagnostics are deterministic.
  - Focused and full Python tests, formatting, clippy, Rust tests, automated
    playtests, and diff checks pass.


- Feature: Command-to-Effect Explainability Evidence
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.47

  Summary:
  Added a bounded Phase 7 read-only audit connecting player commands in the
  v0.10.46 Expert traces to action-specific transition evidence and monthly
  debrief records.

  Done:
  - Reviewed all 12 existing Expert runs without launching new MCP sessions.
  - Confirmed every command has action-specific event/effect evidence or an
    explicit neutral classification, plus a preserved monthly player record.
  - Added deterministic JSON/Markdown audit output and focused Python tests.
  - Found no unmatched commands or concrete explainability gap in this matrix.

  Deferred / Non-Goals:
  - No runtime, command, scenario, replay, MCP schema, state-hash, difficulty,
    scoring, balance, or debrief behavior change.
  - No causal, decision-quality, human-learning, calibration, or policy-validity
    claim.

  Verification:
  - All 12 source runs are represented and supported.
  - Audit JSON and Markdown regenerate deterministically.
  - Focused and full Python tests, formatting, clippy, Rust tests, automated
    playtests, and diff checks pass.


- Feature: Strategy-Diversity Evidence
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.48

  Summary:
  Added a bounded Phase 7 read-only audit comparing command-family trajectories
  and descriptive tradeoff records across the existing v0.10.46 Expert runs.

  Done:
  - Reviewed all 12 existing runs without launching new MCP sessions.
  - Confirmed four distinct profile trajectories across the tested matrix, with
    no common first-turn action family across every profile.
  - Added deterministic JSON/Markdown diagnostics and focused Python tests.
  - Preserved the evidence boundary around strategy variation, causality,
    optimality, balance, human learning, and policy validity.

  Deferred / Non-Goals:
  - No runtime, command, scenario, replay, MCP schema, state-hash, difficulty,
    scoring, balance, or debrief behavior change.
  - No causal strategy comparison, dominance claim, general winnability claim,
    human-learning claim, calibration claim, or policy-validity claim.

  Verification:
  - All 12 source runs are represented and supported.
  - Generated JSON and Markdown output regenerate deterministically.
  - Focused and full Python tests, formatting, clippy, Rust tests, automated
    playtests, and diff checks pass.


- Feature: Teachability-Gate Synthesis
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.49

  Summary:
  Synthesized the existing v0.10.45–v0.10.48 Phase 7 evidence chain to check
  source continuity and whether a concrete unexplained teachability or debrief
  gap justified runtime promotion.

  Done:
  - Added a deterministic read-only audit across four existing evidence
    artifacts.
  - Confirmed all source audits are supported and the v0.10.46–v0.10.48
    profile/seed matrix remains continuous across 12 members.
  - Confirmed no concrete unexplained player-facing, instructor-facing, or
    domain-review gap was identified.
  - Preserved the distinction between traceability, causality, strategy value,
    balance, winnability, learning, and policy validity.

  Deferred / Non-Goals:
  - No new sessions, runtime simulation, command, scenario, replay, state-hash,
    MCP schema, advisor market, difficulty, scoring, balance, or debrief change.
  - No causal strategy comparison, human-learning, calibration, or policy-
    validity claim.

  Verification:
  - All four source artifacts are supported and the 12-member matrix is
    continuous.
  - Audit JSON and Markdown regenerate deterministically.
  - Focused and full Python tests, formatting, clippy, Rust tests, automated
    playtests, and diff checks pass.


- Feature: Teachability Observation Capture
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.50

  Summary:
  Captured deterministic observation-driven Hard competitive traces across
  three profiles and seeds 42, 43, and 44 as the next Phase 7 validation slice.

  Done:
  - Added a wrapper-boundary MCP capture with actor-visible observations, legal
    hints, submitted commands, failures/retries, transitions, hashes, history,
    and debrief records.
  - Confirmed all nine runs completed the 24-month campaign with zero validation
    failures and zero retries.
  - Confirmed descriptive profile differences without identifying a concrete
    unexplained runtime or interface gap.

  Deferred / Non-Goals:
  - No runtime, command, scenario, replay, state-hash, MCP schema, difficulty,
    scoring, balance, or debrief behavior change.
  - No human-learning, causal strategy, winnability, calibration, or policy-
    validity claim.

  Verification:
  - Focused capture tests and deterministic artifact checks pass.
  - Full Python tests, formatting, clippy, Rust tests, automated playtests, and
    diff checks pass.


- Feature: Adversarial Resource-Probe Evidence
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.51

  Summary:
  Added a deterministic Hard competitive capture that probes cash,
  action-point, and concurrent-project validation boundaries across seeds 42,
  43, and 44.

  Done:
  - Added expected-probe and retry metadata for all three complete 24-month
    runs.
  - Confirmed five expected validation failures and five safe retries per run;
    rejected commands did not advance the session turn.
  - Added deterministic diagnostics, findings, domain QA, project-state notes,
    and PR handoff documentation.
  - Found no concrete unexplained runtime, command-surface, or debrief gap.

  Deferred / Non-Goals:
  - No runtime, command, scenario, replay, state-hash, MCP schema, difficulty,
    scoring, balance, or debrief behavior change.
  - No exploit, human-learning, causal strategy, winnability, calibration, or
    policy-validity claim.

  Verification:
  - Three Hard runs completed 24 transitions with expected validation codes.
  - Generated JSON and diagnostics regenerate deterministically.
  - Focused and full Python tests, formatting, clippy, Rust tests, automated
    playtests, and diff checks pass.


- Feature: Decision-Load and Pacing Proxy Evidence Audit
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.52

  Summary:
  Audited the existing v0.10.50 observation-driven competitive traces at the
  month/turn level so action concentration and active-month cadence are
  available as bounded Phase 7 pacing proxies.

  Done:
  - Audited the v0.10.50 nine-run matrix without launching new sessions.
  - Added deterministic per-turn action, hold, active-month, multi-action,
    and maximum monthly action metrics.
  - Confirmed all source runs are complete, source-identifiable, and stable
    across seeds 42, 43, and 44.
  - Preserved runtime promotion as deferred because no concrete unexplained
    player-facing, instructor-facing, or domain-review gap was found.

  Deferred / Non-Goals:
  - No new MCP sessions, runtime, command, scenario, replay, MCP schema,
    state-hash, scoring, balance, difficulty, or debrief change.
  - No human-learning, cognitive-load, causal strategy, winnability,
    calibration, or policy-validity claim.

  Verification:
  - Focused decision-load tests and deterministic artifact generation pass.
  - Full Python tests, formatting, clippy, Rust tests, automated playtests,
    and diff checks pass.


- Feature: Phase 7 Evidence Chain Synthesis
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.53

  Summary:
  Synthesized the v0.10.50 observation-driven capture, v0.10.51 adversarial
  resource probe, and v0.10.52 decision-load audit into one continuity check.

  Done:
  - Validated source identity and declared evidence coverage for all three
    artifacts without launching new sessions.
  - Confirmed v0.10.51 First-Time Executive control hashes match v0.10.50 and
    the nine-member profile/seed matrix remains continuous through v0.10.52.
  - Preserved source-specific trace shapes and recorded runtime promotion as
    deferred because no concrete unexplained product gap was found.

  Deferred / Non-Goals:
  - No new MCP sessions, runtime, command, scenario, replay, MCP schema,
    state-hash, scoring, balance, difficulty, or debrief change.
  - No generalized evidence schema, causal strategy, human-learning,
    winnability, calibration, or policy-validity claim.

  Verification:
  - Six focused synthesis tests and deterministic artifact generation pass.
  - Full Python tests, formatting, clippy, Rust tests, automated playtests, and
    diff checks pass.


- Feature: Project-Limit Recovery Evidence Gate
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.54

  Summary:
  Captured a bounded Phase 7 evidence matrix for the existing two-project
  concurrency limit across Hard seeds 42, 43, and 44. The artifact preserves
  the rejected command, actor-visible surface, same-turn observation, safe
  retry, transition history, and debrief without changing runtime behavior.

  Done:
  - Recovered the v0.10.53 checkpoint and confirmed a clean `main` baseline.
  - Selected the v0.10.51 `too_many_concurrent_projects` trace fact as the
    narrow evidence question.
  - Added a deterministic three-seed Hard MCP capture with the actor-visible
    rejected-turn surface, safe retry, hashes, history, and debrief.
  - Confirmed stable error codes, unchanged turns and observations, one safe
    retry per run, no unexpected failures, and retrospective debrief coverage.
  - Kept validation-hint and runtime promotion deferred because the artifact
    identifies no unexplained recovery failure.

  Deferred / Non-Goals:
  - No validation-hint, runtime, CLI, MCP schema, scenario, replay, state-hash,
    difficulty, scoring, balance, or debrief behavior change.
  - No human-comprehension, learning, causal-strategy, calibration, or policy-
    validity claim.

  Verification:
  - Three Hard runs completed 24 transitions with one expected project-limit
    rejection and one safe same-turn retry each.
  - Generated JSON and Markdown regenerate deterministically with stable SHA-256
    hashes.
  - Eight focused and 73 full Python tests, formatting, clippy, Rust tests,
    automated playtests, and diff checks pass.


- Feature: ASC Project Observation Coverage
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.55

  Summary:
  Corrected the actor-visible competitive project observation so accepted ASC
  projects appear with remaining duration and monthly draw, while preserving
  the existing project-limit recovery behavior.

  Done:
  - Added the missing `AscCapacity` observation formatter branch and focused
    Rust regression test.
  - Added a deterministic Hard capture across seeds 42, 43, and 44.
  - Confirmed both active project labels, same-turn rejection preservation,
    safe retry, debrief coverage, and v0.10.54 state-hash continuity.
  - Bumped the package version to `0.10.55`.

  Deferred / Non-Goals:
  - No project-limit hint, resource payload, transition, MCP schema, balance,
    difficulty, scoring, or broader project-guidance change.
  - No human-comprehension, learning, calibration, winnability, or policy-
    validity claim.

  Verification:
  - Five focused ASC observation evidence tests pass.
  - Three Hard runs complete 24 transitions with expected project-limit
    rejection and one safe retry each.
  - State-hash sequences match the v0.10.54 source artifact.
  - Full Python/Rust checks, formatting, clippy, automated playtests, and diff
    checks pass.


- Feature: Project-Recovery Use Evidence
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.56

  Summary:
  Added a deterministic response-conditioned project-limit recovery capture
  across Hard seeds 42, 43, and 44. The simulated policy uses only the plain
  validation error and unchanged actor-visible observation to select a safe
  `hold` retry.

  Done:
  - Added the v0.10.56 MCP capture, diagnostics, and focused Python coverage.
  - Confirmed expected rejection classification, same-turn observation
    preservation, response-conditioned recovery, safe retry, debrief coverage,
    and v0.10.55 state-hash continuity.
  - Documented the evidence limits and kept project hints, resource payloads,
    and runtime promotion deferred.
  - Bumped the package version to `0.10.56`.

  Deferred / Non-Goals:
  - No runtime, command, scenario, replay, state-hash, MCP schema, structured
    validation hint, resource payload, difficulty, scoring, or balance change.
  - No human-comprehension, learning, calibration, winnability, or policy-
    validity claim.

  Verification:
  - Three Hard runs complete 24 transitions with one expected project-limit
    rejection and one response-conditioned `hold` retry each.
  - Generated JSON and Markdown regenerate deterministically.
  - Focused/full Python tests, formatting, clippy, Rust tests, automated
    playtests, and diff checks pass.


- Feature: Debrief-Use Audit
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.57

  Summary:
  Added a deterministic read-only audit of event-specific trace continuity
  across rival-pressure, strategy-tradeoff, resource-retry, and project-
  recovery evidence artifacts.

  Done:
  - Audited six source artifacts and 39 completed runs for visibility,
    response, follow-through, outcome, and explanation coverage.
  - Confirmed v0.10.54→v0.10.55→v0.10.56 project state-hash continuity across
    seeds 42, 43, and 44.
  - Added focused tests, generated deterministic JSON/Markdown, findings,
    guidance, lessons, and required handoff artifacts.
  - Bumped package metadata to `0.10.57`.

  Deferred / Non-Goals:
  - No runtime, MCP, scenario, replay, state-hash, scoring, difficulty,
    balance, or debrief wording change.
  - No human-learning, classroom-effectiveness, causal strategy, calibration,
    or policy-validity claim.

  Verification:
  - Eight focused audit tests and 95 full Python tests pass.
  - 286 Rust tests, formatting, clippy, automated playtests, JSON validation,
    and diff checks pass.
  - All six source artifacts and 39 runs report supported coverage; no source
    evidence gap was identified.


- Feature: Debrief-Coherence Audit
  Status: Complete
  Started: 2026-07-11
  Version: 0.10.58

  Summary:
  Added a deterministic read-only audit joining decision-time observations,
  submitted commands, accepted transitions, delayed or partial context,
  outcomes, and retrospective debrief markers across the existing Phase 7
  evidence chain.

  Done:
  - Audited six source artifacts and 39 completed competitive runs.
  - Verified decision context, response/retry handling, transition follow-through,
    delayed or partial context where applicable, outcome context, and
    decision-versus-outcome debrief framing.
  - Preserved v0.10.54→v0.10.55→v0.10.56 project state-hash continuity across
    seeds 42, 43, and 44.
  - Added deterministic JSON/Markdown output, focused tests, findings, guidance,
    lessons, and required handoff artifacts.
  - Bumped package metadata to `0.10.58`.

  Deferred / Non-Goals:
  - No runtime, MCP, scenario, replay, state-hash, scoring, difficulty,
    balance, or debrief wording change.
  - No human-learning, classroom-effectiveness, causal strategy, calibration,
    or policy-validity claim.

  Verification:
  - Seven focused audit tests and the full Python test suite pass.
  - Generated JSON and Markdown regenerate deterministically.
  - Rust tests, formatting, clippy, automated playtests, JSON validation, and
    diff checks pass.
  - All six source artifacts and 39 runs report supported coverage.


- Feature: Operating-Loop AI Validation Matrix
  Status: Complete
  Started: 2026-07-11
  Version: 0.11.1

  Summary:
  Capture and audit five deterministic operating-loop policy lanes across
  seeds 42–44 and Easy, Normal, Hard, and Expert competitive configurations.

  Done:
  - Completed 60 competitive runs and 1,440 committed operating months.
  - Preserved player-owned demand, treated volume, unmet demand, revenue, cost,
    margin, cash, attribution, hashes, observations, commands, and debriefs.
  - Confirmed 10 distinct command trajectories, 140 capacity/demand bottleneck
    months, 269 operating-loss months, 60 workforce-capacity months, and 76
    threshold-crossing candidates.
  - Kept runtime promotion deferred because the findings are descriptive and do
    not identify a concrete unexplained player-facing gap.

  Deferred / Non-Goals:
  - No runtime, MCP, scenario, replay, ruleset, state-hash, balance, or
    difficulty change.
  - No causal marginal-effect, dominance, calibration, winnability,
    human-learning, or policy-validity claim.

  Verification:
  - Six focused Python tests, 108 full Python tests, 289 Rust tests, clippy,
    formatting, JSON validation, deterministic artifact regeneration, and diff
    checks pass.
  - Seed-42 Normal hold-control retains month-one hash `61357596d8800592`.


- Feature: Operating-Loss Explainability Audit
  Status: Complete
  Started: 2026-07-11
  Version: 0.11.2

  Summary:
  Audited the v0.11.1 competitive operating traces for decision-time context,
  player-owned transition attribution, and month-level debrief linkage.

  Done:
  - Reused the deterministic 60-run, 1,440-month v0.11.1 artifact without
    launching new sessions or changing runtime behavior.
  - Classified 140 capacity/demand, 269 operating-loss, and 60 workforce-
    capacity signal-months.
  - Confirmed 469/469 decision-context, transition-attribution, and monthly
    decision links.
  - Identified 0/469 month-specific operating-outcome links while preserving
    60/60 global debrief attribution summaries as a separate category.

  Deferred / Non-Goals:
  - No runtime, MCP, scenario, replay, ruleset, state-hash, balance,
    difficulty, or debrief wording change.
  - No causal marginal-effect, dominance, calibration, winnability,
    human-learning, or policy-validity claim.

  Verification:
  - Eight focused Python tests, 116 full Python tests, 289 Rust tests, clippy,
    formatting, JSON validation, deterministic regeneration, and diff checks
    pass.


- Feature: Monthly Operating-Outcome Debrief Linkage
  Status: Complete
  Started: 2026-07-11
  Version: 0.11.3

  Summary:
  Added a month-specific player-owned operating-result line to the competitive
  end-of-run debrief so each committed month links its player decision to its
  realized demand, treated volume, unmet demand, revenue, cost, and margin.

  Done:
  - Derived the line from the player system in each committed transition's
    `next` state.
  - Preserved rival-private operating state, active observations, global
    attribution summaries, transition semantics, and state hashes.
  - Added focused direct-debrief and MCP end-session tests.

  Deferred / Non-Goals:
  - No new operating mechanism, actor, command, scenario, replay format,
    ruleset, balance, difficulty, calibration, or learning claim.
  - Reported values remain visible game units rather than calibrated dollars,
    encounters, or policy forecasts.

  Verification:
  - Focused debrief and MCP tests, full Rust/Python suites, formatting, clippy,
    golden seed-42 coverage, and diff checks pass.


- Feature: Post-v0.11.3 Operating-Outcome Debrief Validation
  Status: Complete
  Started: 2026-07-11
  Version: 0.11.4

  Summary:
  Re-ran the competitive operating-loop matrix against the v0.11.3 debrief
  surface and verified month-specific outcome linkage for categorized player
  operating signals.

  Done:
  - Captured 60 deterministic competitive runs across five policy profiles,
    seeds 42/43/44, and Easy/Normal/Hard/Expert.
  - Audited 1,440 committed months and 469 categorized signal-months.
  - Confirmed one player-owned operating-result line per committed month and
    469/469 categorized month-level outcome links.

  Deferred / Non-Goals:
  - No runtime, MCP, scenario, replay, ruleset, state-hash, balance,
    difficulty, calibration, winnability, human-learning, or policy-validity
    claim.
  - Runtime promotion remains deferred until a new concrete gameplay,
    instructor, or domain-review gap is identified.

  Verification:
  - Matrix capture, audit tests, full Python/Rust suites, formatting, clippy,
    JSON validation, golden seed-42 coverage, and diff checks pass.


- Feature: Operating-Outcome Use Audit
  Status: Complete
  Started: 2026-07-12
  Version: 0.11.5

  Summary:
  Audited whether the v0.11.4 operating outcomes remain aligned across
  actor-visible prior-month observations, subsequent command traces, committed
  transitions, and player-owned monthly debrief results.

  Done:
  - Reused the frozen v0.11.4 capture without launching new sessions or
    changing runtime behavior.
  - Confirmed 60 complete runs, 1,440 traces, 1,380 prior-month observation
    matches, 1,440 trace/hash matches, and 1,440 exact debrief outcome matches.
  - Reported 441 non-terminal signal-to-next-command opportunities and 28
    expected terminal signals without treating response distributions as
    causal strategy evidence.

  Not Yet Done:
  - No human comprehension, classroom, causal, balance, winnability,
    calibration, or policy-validity evaluation has been performed.

  Deferred / Non-Goals:
  - No runtime, MCP, scenario, replay, ruleset, state-hash, balance, difficulty,
    scoring, or debrief wording change.
  - No generalized evidence schema, new capture matrix, or runtime promotion.

  Verification:
  - Eight focused audit tests, full Python/Rust suites, formatting, clippy,
    JSON validation, deterministic regeneration, golden seed-42 coverage, and
    diff checks pass.


- Feature: Strategy-Comparison Use Audit
  Status: Complete
  Started: 2026-07-12
  Version: 0.11.6

  Summary:
  Grouped the frozen v0.11.4 competitive capture by profile, seed, and
  difficulty to test whether the existing operating-outcome evidence supports
  descriptive strategy comparison without weakening observation or debrief
  boundaries.

  Done:
  - Reused the frozen capture without launching new sessions or changing
    runtime behavior.
  - Confirmed 60 complete runs, 1,440 committed months, 1,380 prior-month
    observation matches, 1,440 exact debrief outcome matches, 441 response
    opportunities, and 28 terminal signals.
  - Reported profile and difficulty trajectory summaries, action-family
    coverage, hold rates, and signal-to-command counts.
  - Identified no structural strategy-comparison, traceability, or debrief-use
    gap.

  Not Yet Done:
  - No human comprehension, classroom, causal, balance, winnability,
    calibration, or policy-validity evaluation has been performed.

  Deferred / Non-Goals:
  - No runtime, MCP, scenario, replay, ruleset, state-hash, balance, difficulty,
    scoring, or debrief wording change.
  - No strategy-quality, dominance, causal, learning, or general-balance claim.

  Verification:
  - Seven focused audit tests, full Python/Rust suites, formatting, clippy,
    JSON validation, deterministic regeneration, golden seed-42 coverage, and
    diff checks pass.


- Feature: Difficulty Expansion
  Status: Complete
  Started: 2026-07-12
  Version: 0.11.7

  Summary:
  Implement an institutionally expressive difficulty system by introducing explicit AI strategic risk postures based on active campaign difficulty, scaling AI scoring preferences and rationales while maintaining backwards compatibility and state-hash invariance.

  Done:
  - Defined the `RiskPosture` enum (`Conservative`, `Moderate`, `Aggressive`) with default `Moderate` implementation.
  - Added `risk_posture` field to `AiProfile` and updated serialization/deserialization logic on `PlayerController` with defaults to maintain backwards-compatible saves.
  - Dynamic mapping from `Difficulty` to `RiskPosture` (Easy -> Conservative, Normal -> Moderate, Hard/Expert -> Aggressive) configured at genesis and scenario loading.
  - Implemented scoring modifiers and risk-posture-conditioned offsets to AI player batch computation logic for holds, aggressive negotiations, large capital investments, and cash pressure.
  - Included active risk posture in generated AI rationale messages.
  - Added focused unit tests verifying difficulty-driven risk-posture scoring variations.

  Deferred / Non-Goals:
  - No global difficulty balance pass, hidden rival omniscience, or punitive player AP cuts.
  - No changes to state-hash calculation logic (state-hash invariance is preserved).

  Verification:
  - All 292 Rust tests (including new focused unit tests) and 138 Python tests pass.
  - Formatting, clippy, and diff checks pass.


- Feature: Difficulty Resource Scaling (v0.11.8)
  Summary:
  Scale rival starting resources (cash and political capital) at genesis according to difficulty levels (Easy: 40/5, Normal: 60/8, Hard: 80/12, Expert: 100/15) and present these resource details in the difficulty selection menu.
  Done:
  - Scaled starting cash and political capital for rivals based on difficulty in the genesis generator.
  - Kept human player (Riverside) starting resources invariant at 60 cash and 8 PC.
  - Updated CLI difficulty selection menu to present rival starting cash, PC, and risk posture.
  - Added focused unit tests verifying starting resource scaling across all difficulties.
  Verification:
  - All 293 Rust tests and 138 Python tests pass successfully.
  - State-hash invariance for Normal seed-42 is preserved.

- Feature: Expert Difficulty Validation (v0.11.9)
  Summary:
  Validate Expert difficulty after the v0.11.7 AI risk-posture and v0.11.8
  rival resource-scaling changes using a deterministic Phase 7 evidence matrix
  across five scripted policy lanes and seeds 42, 43, and 44.
  Done:
  - Added `_workspace/experiments/v0.11.9-expert-difficulty-validation/` with
    a reproducible Expert-only runner, JSON results, and diagnostics.
  - Confirmed 15/15 Expert runs completed the 24-month campaign with zero
    validation failures.
  - Added focused Python artifact-contract tests and recorded findings in
    `docs/history/playtests/v0.11/playtest-findings-v0.11.9.md`.
  Deferred / Non-Goals:
  - No runtime mechanics, difficulty values, scoring, balance, scenario,
    ruleset, replay, MCP schema, or state-hash changes.
  - No general Expert winnability, human-learning, empirical-calibration,
    causal, or policy-validity claim.
  Verification:
  - Focused Python tests, artifact generation, JSON validation, full Rust and
    Python suites, formatting, clippy, automated playtests, and diff checks pass.

- Feature: Phase 7 Difficulty Evidence Synthesis (v0.11.10)
  Summary:
  Synthesize the v0.11.6 all-tier strategy-comparison evidence with the v0.11.9
  post-change Expert validation artifact while preserving source-specific
  evidence contracts and runtime deferral.
  Done:
  - Added `_workspace/experiments/v0.11.10-phase7-difficulty-synthesis/` with
    deterministic source validation, coverage summaries, and diagnostics.
  - Validated 60 all-tier baseline runs, 15 Expert runs, and 15 overlapping
    profile/seed coordinates without launching new sessions.
  - Recorded no structural evidence gap and retained deferred runtime promotion.
  - Added focused Python tests for malformed sources, incomplete traces,
    coverage, and deterministic rendering.
  Deferred / Non-Goals:
  - No runtime mechanics, difficulty values, scoring, balance, scenario,
    ruleset, replay, MCP schema, or state-hash changes.
  - No causal strategy, general Expert winnability, human-learning,
    empirical-calibration, or policy-validity claim.
  Verification:
  - Focused synthesis tests, deterministic artifact generation, JSON validation,
    full Python/Rust suites, formatting, clippy, automated playtests, and diff
    checks pass.

- Feature: Post-Change All-Tier Difficulty Validation (v0.11.11)
  Summary:
  Capture and audit current-code all-tier competitive behavior after the v0.11.7
  AI risk-posture and v0.11.8 rival-resource changes.
  Done:
  - Added `_workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/`
    with a reproducible 60-run capture and current-version audit adapter.
  - Validated 60/60 complete 24-month runs, 1,440 operating months, and 60/60
    decision-to-debrief traces across five profiles, three seeds, and four tiers.
  - Recorded ten distinct command trajectories, varied operating bottlenecks,
    and no candidate common or near-dominant first-month action.
  - Preserved runtime promotion deferral and recorded findings in
    `docs/history/playtests/v0.11/playtest-findings-v0.11.11.md`.
  Deferred / Non-Goals:
  - No runtime mechanics, difficulty values, AI scoring, balance, scenario,
    ruleset, replay, MCP schema, or state-hash changes.
  - No causal strategy, general winnability, human-learning,
    empirical-calibration, or policy-validity claim.
  Verification:
  - Focused artifact tests, 60-run generation, audit validation, JSON parsing,
    full Python/Rust suites, formatting, clippy, automated playtests, and diff
    checks pass.

- Feature: Current-Code Teachability Capture (v0.11.12)
  Summary:
  Capture current-code observation-driven teachability and pacing evidence after
  the v0.11.7 risk-posture and v0.11.8 rival-resource changes.
  Done:
  - Added `_workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/`
    with a retry-aware MCP capture and deterministic audit.
  - Validated 9/9 complete Hard-difficulty runs, 216 committed months, and
    complete player observation, history/hash, and debrief trace coverage across
    three profiles and seeds 42, 43, and 44.
  - Preserved the Normal seed-42 hold-control hash and excluded rival operating
    events from player-owned evidence.
  - Recorded findings in `docs/history/playtests/v0.11/playtest-findings-v0.11.12.md` and retained
    deferred runtime promotion.
  Deferred / Non-Goals:
  - No runtime mechanics, difficulty values, AI scoring, balance, scenario,
    ruleset, replay, MCP schema, or state-hash changes.
  - No human-learning, cognitive-load, causal strategy, general winnability,
    calibration, or policy-validity claim.
  Verification:
  - Focused artifact tests, current-code capture, audit validation, JSON
    validation, full Python/Rust suites, formatting, clippy, and diff checks
    pass.

- Feature: Regional Affiliation Design Gate (v0.11.13)
  Status: Complete
  Started: 2026-07-12
  Version: 0.11.13

  Summary:
  Define the smallest credible regional consolidation design as an
  affiliation-first partnership between Riverside and one fictional nonprofit
  system, while preserving runtime and legal-boundary deferral.

  Done:
  - Added evidence, mechanism, domain-QA, and final-handoff artifacts.
  - Defined partner fit, institutional review, community benefit, labor, payer
    leverage, integration drag, capital access, service continuity, and
    access/quality tradeoffs.
  - Updated the expansion review, roadmap, system boundary, evidence registry,
    lessons, changelog, README, and package metadata.
  - Recorded separate distinctions for actor utility, organizational outcomes,
    social welfare, community effects, and educational evaluation.

  Not Yet Done:
  - A future runtime proposal must identify minimum state, observations,
    commands, resolved inputs, and debrief contracts before implementation.

  Deferred / Non-Goals:
  - No runtime mechanics, commands, scenario schema, replay, MCP, ruleset,
    state-hash, acquisition, transaction-finance, or legal-forecasting work.
  - No new playtest, calibration, balance, human-learning, or policy-validity
    claim.

  Verification:
  - Domain QA returned `Pass`.
  - `cargo fmt --check` passed.
  - `cargo clippy --all-targets -- -D warnings` passed.
  - `cargo test --all -- --test-threads=1` passed: 293 Rust tests.
  - `cargo test --test golden_competitive_seed42 -- --test-threads=1` passed:
    2 competitive golden tests.
  - `python3 -m unittest discover -s tests -p 'test_*.py'` passed: 163 tests.
  - `git diff --check` passed.

- Feature: Regional Affiliation Runtime Proposal (v0.11.14)
  Status: Complete
  Started: 2026-07-12
  Version: 0.11.14

  Summary:
  Define an opt-in `regional-affiliation-v1` scenario proposal that reuses
  competitive primitives without changing the default campaign.

  Done:
  - Defined a six-stage monthly flow for partner assessment, independence or
    deferral, affiliation commitments, institutional review, and early
    integration.
  - Defined minimum true-state, actor-observation, resolved-input, history,
    replay, and debrief contracts.
  - Added proposed ADR-0010 and synchronized roadmap, boundary, scenario,
    architecture, evidence, QA, and final-handoff artifacts.
  - Bumped package metadata to `0.11.14`.

  Not Yet Done:
  - A separate implementation PR must choose concrete Rust types, scenario
    fields, command syntax, numeric ruleset bounds, and replay/hash versioning.

  Deferred / Non-Goals:
  - No runtime mechanics, commands, scenario files, schema version, replay
    format, MCP behavior, ruleset, state-hash, acquisition, deal finance, or
    legal forecasting changes.
  - No new playtest, calibration, balance, human-learning, or policy-validity
    claim.

  Verification:
  - Domain QA returned `Pass`.
  - Existing Rust, Python, golden-trajectory, formatting, clippy, and diff
    checks pass.

- Feature: Regional Affiliation Runtime (v0.12.0)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.0

  Summary:
  Implement the opt-in `regional-affiliation-v1` six-stage runtime slice while
  preserving the competitive campaign and its golden state-hash contract.

  Done:
  - Added typed affiliation state, commands, ruleset, observations, explicit
    resolved inputs, deterministic transitions, immutable history, hashing,
    replay verification, and debrief output.
  - Added the bundled TOML scenario plus CLI and MCP campaign routing.
  - Added focused scenario, transition, MCP, campaign-selection, and replay
    regression coverage.
  - Bumped package metadata to `0.12.0`.

  Not Yet Done:
  - Broader playtest evidence and educational review of balance remain future
    validation work; this slice is not a claim of general winnability.

  Deferred / Non-Goals:
  - No full acquisition/deal market, legal or financial forecast, autosave
    expansion, AI-rival affiliation behavior, GUI, or competitive hash change.

  Verification:
  - Rust, Python, formatting, clippy, golden, replay, MCP, and diff checks pass.

- Feature: Regional Affiliation Phase 7 Playtest Validation (v0.12.1)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.1

  Summary:
  Capture deterministic MCP evidence for the opt-in affiliation runtime across
  three observation-driven postures and seeds 42, 43, and 44.

  Done:
  - Added a 9-run capture covering independent, deferred, and pursuit policies
    with six committed stages per run and no validation failures.
  - Validated 54 observation-before-command entries, transition/state-hash
    alignment, actor-response coverage, and 54 debrief stage lines.
  - Identified one bounded decision-time context gap: typed alternatives,
    assumptions, and commitments are not rendered by the MCP observation.
  - Preserved runtime promotion deferral for balance, ruleset, legal, and
    educational-effect claims.
  - Bumped package metadata to `0.12.1`.

  Not Yet Done:
  - A follow-up interface slice must decide whether to render the omitted typed
    observation context, add focused MCP coverage, and rerun the capture.

  Deferred / Non-Goals:
  - No transition, ruleset, balance, replay/hash, command, scenario, GUI,
    AI-rival, legal, calibration, winnability, or human-learning changes.

  Verification:
  - 9/9 matrix runs complete; 54/54 histories, hashes, observations, and
    debrief stage links validated.
  - Focused artifact tests, deterministic capture, full Rust/Python suites,
    formatting, clippy, golden, and diff checks pass.

- Feature: Regional Affiliation Observation Context (v0.12.2)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.2

  Summary:
  Close the v0.12.1 MCP observation-context gap by rendering safe typed
  commitments, staged alternatives, and explicit assumptions.

  Done:
  - Added `Commitments:`, `Alternative:`, and `Assumption:` lines to the MCP
    affiliation observation using only `AffiliationObservation`.
  - Added a Rust session-boundary regression covering initial, choose-posture,
    and post-commitment observations.
  - Preserved the v0.12.1 artifact and added a separate post-fix 9-run × 3-seed
    artifact with 54/54 observations carrying the required context.
  - Closed the structural context gap with zero validation failures while
    keeping balance, transition, legal, and learning promotion deferred.
  - Bumped package metadata to `0.12.2`.

  Not Yet Done:
  - A new concrete player-facing, instructor-facing, or domain-review gap is
    required before any further runtime or balance change is promoted.

  Deferred / Non-Goals:
  - No state, transition, ruleset, threshold, balance, replay/hash, command,
    scenario, GUI, AI-rival, legal, calibration, winnability, or human-learning
    changes.

  Verification:
  - 9/9 post-fix runs complete; 54 stages, zero validation failures, and zero
    missing typed-context fields.
  - 307 Rust tests, 173 Python tests, formatting, clippy, golden, and diff
    checks pass.

- Feature: Phase 7 Teachability Evidence Review (v0.12.3)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.3

  Summary:
  Audit the v0.12.2 affiliation post-fix artifact against the approved
  v0.11.12 competitive teachability capture for structural decision-to-debrief
  continuity and source-specific context.

  Done:
  - Added a deterministic read-only audit over the two pinned source artifacts.
  - Added a test-only mutex around the shared competitive persistence-path tests
    after CI exposed a pre-existing parallel filesystem race; production
    persistence behavior is unchanged.
  - Validated 18/18 complete runs and 270 committed transitions across the
    affiliation and competitive evidence lanes.
  - Confirmed actor-visible decision context, action/response, transition/hash,
    outcome, debrief, profile/seed matrix, and source-specific context coverage
    with zero structural gaps.
  - Preserved source versions, campaign-specific semantics, the competitive
    control hash, and deferred runtime promotion.
  - Bumped package metadata to `0.12.3`.

  Not Yet Done:
  - A new concrete player-facing, instructor-facing, or domain-review gap is
    required before runtime or interface promotion.

  Deferred / Non-Goals:
  - No new capture, state, transition, ruleset, threshold, balance, difficulty,
    command, scenario, GUI, replay/hash, legal, calibration, winnability, or
    human-learning changes.

  Verification:
  - 2 source artifacts, 18 runs, 270 transitions, and zero structural gaps.
  - 307 Rust tests pass under serial and default parallel execution; 178 Python
    tests, formatting, clippy, CLI smoke, golden, and diff checks pass.

- Feature: Difficulty Depth Evidence Review (v0.12.4)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.4

  Summary:
  Audit the existing v0.11.11 all-tier and v0.11.9 Expert artifacts for a
  visible difficulty pressure signal and bounded Expert clearability.

  Done:
  - Added a deterministic read-only audit preserving both source versions and
    source-specific contracts.
  - Validated 75/75 complete runs and 1,800 committed transitions across the
    all-tier and standalone Expert matrices.
  - Recomputed per-tier operating bottlenecks, action-family counts, trajectory
    diversity, final tradeoff ranges, history/state-hash alignment, and debrief
    coverage.
  - Identified a candidate `workforce_capacity` pressure signal rising from 0,
    15, 30, and 160 operating months across Easy, Normal, Hard, and Expert.
  - Preserved runtime promotion deferral because the finding is descriptive and
    does not establish causality, balance, or general Expert winnability.
  - Bumped package metadata to `0.12.4`.

  Not Yet Done:
  - A separate difficulty design gate must specify visible pressure semantics,
    player/actor observation boundaries, and winnability limits before runtime
    tuning is considered.

  Deferred / Non-Goals:
  - No difficulty values, resource scaling, rival AI, scoring, balance,
    transition, command, scenario, GUI, replay/hash, calibration, winnability,
    or human-learning changes.

  Verification:
  - 2 source artifacts, 75 runs, 1,800 transitions, and zero source-contract
    gaps.
  - 307 Rust tests, 184 Python tests, formatting, clippy, CLI smoke, golden,
    and diff checks pass.

- Feature: Workforce Capacity Difficulty Design Gate (v0.12.5)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.5

  Summary:
  Decide whether the v0.12.4 workforce-capacity pressure signal is sufficiently
  visible at decision time and specify the smallest safe observation follow-up.

  Done:
  - Reviewed the v0.12.4 artifact and the typed observation, MCP formatter,
    staffing transition, and debrief boundaries.
  - Confirmed visible trust/labor/operations/consultant/debrief context while
    identifying omitted typed Riverside staffing and physical-capacity counts.
  - Added a deterministic design contract requiring an observation-only
    follow-up using `PlayerObservation` and excluding hidden targets, effective
    allocations, future hires, and rival private state.
  - Preserved runtime difficulty, balance, scoring, transition, replay/hash,
    and winnability deferral.
  - Bumped package metadata to `0.12.5`.

  Follow-up:
  - Delivered in v0.12.6 through the bounded MCP projection and compatible
    evidence matrix with exact history/state-hash comparison.

  Deferred / Non-Goals:
  - No difficulty values, balance pass, scoring, transition, command, scenario,
    replay/hash, GUI, hidden-state, calibration, winnability, or human-learning
    changes.

  Verification:
  - Design source markers supported; observation follow-up required; runtime
    difficulty change unauthorized.
  - 307 Rust tests, 189 Python tests, formatting, clippy, CLI smoke, golden,
    and diff checks pass.

- Feature: Workforce Capacity Observation Context (v0.12.6)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.6

  Summary:
  Render the safe typed staffing and physical-capacity context at the MCP
  boundary and validate that the candidate pressure signal remains
  observation-only.

  Done:
  - Added the exact `Staffing:` and `Physical capacity:` lines from
    `PlayerObservation` to competitive MCP observations.
  - Added a focused Rust session-boundary regression test for the exact
    seed-42 starting values.
  - Captured 75 complete runs and 1,800 transitions across the five-profile,
    three-seed, four-tier compatibility matrix plus the standalone Expert
    overlap.
  - Confirmed that all 60 all-tier histories and all 15 Expert histories match
    their immutable source controls exactly, including state-hash sequences.
  - Confirmed all 1,800 trace observations include both safe lines and no
    excluded hidden markers.
  - Kept difficulty, balance, scoring, transition, command, replay/hash,
    winnability, and human-learning promotion deferred.
  - Bumped package metadata to `0.12.6`.

  Deferred / Non-Goals:
  - No difficulty tuning, broad balance pass, hidden rival omniscience, derived
    effective-capacity model, scoring redesign, GUI, legal forecast, calibration,
    winnability, or human-learning claim.

  Verification:
  - 308 Rust tests, 194 Python tests, formatting, clippy, CLI smoke, golden,
    and diff checks pass.
  - Observation artifact and diagnostics report 75/75 complete runs,
    1,800/1,800 exact source history matches, 1,800/1,800 exact state-hash
    matches, and deferred runtime promotion.

- Feature: Competitive Teachability Queue Closure (v0.12.8)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.8

  Summary:
  Close the already-supported competitive teachability and validation-loop
  Future item using the v0.12.3 cross-campaign evidence review.

  Done:
  - Revalidated 2 source lanes, 18 complete runs, and 270 committed
    transitions with source-specific decision, response, transition, outcome,
    debrief, strategy-comparison, and context coverage.
  - Confirmed zero structural gaps and removed the completed teachability item
    from the Future queue.
  - Preserved explicit evidence limits and a reopening condition for any future
    comprehension, pacing, traceability, strategy-comparison, or debrief-use
    finding.
  - Kept runtime, difficulty, balance, and human-learning promotion deferred.
  - Bumped package metadata to `0.12.8`.

  Deferred / Non-Goals:
  - No human-learning claim, classroom study, balance change, difficulty tuning,
    new interface, transition/ruleset change, or new strategic actor.

  Verification:
  - Closure artifact reports 18/18 complete runs, 270 transitions, 0 gaps, and
    supported source markers.
  - 308 Rust tests, 204 Python tests, formatting, clippy, CLI smoke, golden,
    diff checks, focused closure tests, and deterministic audit validation pass.

- Feature: Difficulty Depth Queue Closure (v0.12.9)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.9

  Summary:
  Close the difficulty-depth and winnability Future item after reconciling the
  v0.12.4 pressure/clearability evidence with the v0.12.6 observation controls.

  Done:
  - Revalidated 75 runs and 1,800 transitions with workforce-capacity counts
    Easy 0, Normal 15, Hard 30, Expert 160.
  - Revalidated the 15/15 named Expert profile/seed clearability overlap.
  - Revalidated exact v0.12.6 observation histories and state hashes with zero
    hidden markers.
  - Confirmed no unexplained pressure, clearability, or player-facing gap
    authorizes difficulty or balance tuning.
  - Removed the completed difficulty item from the Future queue and preserved a
    reopening condition and source-version limits.
  - Bumped package metadata to `0.12.9`.

  Deferred / Non-Goals:
  - No difficulty values, resource scaling, balance pass, scoring change, rival
    AI change, hidden omniscience, winnability claim, or transition change.

  Verification:
  - Closure artifact reports the pinned pressure signal, 15-run clearability
    overlap, exact observation controls, and deferred runtime promotion.
  - 308 Rust tests, 209 Python tests, formatting, clippy, CLI smoke, golden,
    diff checks, focused closure tests, and deterministic audit validation pass.

- Feature: Affiliation Queue Closure (v0.12.10)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.10

  Summary:
  Synchronize the affiliation/acquisition Future item with the already
  implemented v0.12.7 runtime-boundary proposal.

  Done:
  - Revalidated six minimum contracts, supported source markers, and the
    existing 9/9-run, 54-stage, 54-observation affiliation evidence.
  - Removed the completed affiliation/acquisition item from the Future queue.
  - Preserved direct acquisition, deal finance, legal forecasting, generic
    actor expansion, and competitive-campaign isolation as deferred scope.
  - Recorded a concrete reopening condition requiring new evidence.
  - Bumped package metadata to `0.12.10`.

  Deferred / Non-Goals:
  - No new affiliation mechanism, acquisition branch, deal-financing system,
    legal forecast, generic actor framework, or competitive-campaign change.

  Verification:
  - Closure artifact reports six supported contracts, 9/9 runs, 54 stages,
    54 observations, and deferred runtime promotion.
  - 308 Rust tests, 214 Python tests, formatting, clippy, CLI smoke, golden,
    diff checks, focused closure tests, and deterministic audit validation pass.

- Feature: GUI Thin-Client Proof (v0.12.11)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.11

  Summary:
  Prototype one dependency-free browser surface over existing MCP-shaped
  observation, command-hint, history/replay, and debrief outputs.

  Done:
  - Added `gui/index.html`, `gui/app.mjs`, and an adapter contract that keeps
    command legality and transitions server/core-owned.
  - Added static contract tests, JavaScript syntax validation, local HTTP
    serving verification, and a zero-external-asset/network audit.
  - Removed the GUI thin-client item from the Future queue while preserving
    hosting, richer interaction, and production usability as gated work.
  - Recorded the unavailable in-app browser backend as a visual-QA limitation
    without making a visual usability claim.
  - Bumped package metadata to `0.12.11`.

  Deferred / Non-Goals:
  - No simulation state, parser, transition, network service, authentication,
    hosting, GUI-only scenario behavior, downloaded assets, or CLI/MCP change.

  Verification:
  - Static GUI tests, JavaScript syntax, adapter smoke, and local HTTP serving
    pass; no external assets or network calls are bundled.
  - 308 Rust tests, 219 Python tests, formatting, clippy, CLI smoke, golden,
    and diff checks pass.

- Feature: Simulation Breadth and Strategic Actors Queue Closure (v0.12.12)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.12

  Summary:
  Audit the existing competitive campaign against the bounded breadth and
  strategic-actor Future item, using committed repeated-play and traceability
  evidence before authorizing any new runtime mechanism.

  Done:
  - Inventoried existing service-line/capacity, operating/community outcome,
    capital/market, public-payer, rival-information, and debrief surfaces.
  - Revalidated 60/60 all-tier runs, 1,440 transitions, 10 distinct command
    trajectories, no dominant first-month action, and varied final tradeoffs.
  - Revalidated 9/9 current-code runs and the v0.12.3 review's 18/18 runs,
    270 transitions, and zero structural gaps.
  - Documented true state, player observation, private rival information, and
    debrief boundaries without promoting a new actor or patient model.
  - Removed the breadth and strategic-actors item from the Future queue while
    preserving deferred scope and a concrete reopening condition.
  - Bumped package metadata to `0.12.12`.

  Deferred / Non-Goals:
  - No new state, command, transition, strategic actor, individual patient,
    public-payer utility, portfolio optimizer, or scenario-authoring framework.
  - No human-learning, causal balance, calibration, social-welfare,
    equilibrium, or policy-validity claim.

  Verification:
  - Closure artifact source markers and focused breadth tests pass.
  - Full Rust/Python suites, formatting, clippy, CLI smoke, golden, and diff
    checks pass.

- Feature: Release Metadata Check (v0.12.13)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.13

  Summary:
  Add one read-only package-version consistency check with documented local
  usage and the same command in CI, then close the final release Future item.

  Done:
  - Added `scripts/check_release_metadata.py` to compare the package version in
    `Cargo.toml` with `Cargo.lock`, the README milestone, and the latest
    changelog heading.
  - Added focused tests for the current repository, valid modified-semver
    shape, projection mismatch, and invalid package version.
  - Documented local usage in `docs/guides/contributor-release-check.md` and README,
    and added the command to `.github/workflows/ci.yml`.
  - Removed the release automation and contributor-readiness item from the
    Future queue while preserving publication, licensing, deployment, and
    packaging as deferred scope.
  - Bumped package metadata to `0.12.13`.

  Deferred / Non-Goals:
  - No package publication, tag automation, registry access, licensing,
    deployment, broad CI restructuring, or simulation/runtime behavior change.

  Verification:
  - Local metadata command, focused checker tests, full Rust/Python suites,
    formatting, clippy, CLI smoke, golden, JSON, and diff checks pass.

- Feature: Affiliation Runtime Boundary Proposal (v0.12.7)
  Status: Complete
  Started: 2026-07-12
  Version: 0.12.7

  Summary:
  Reconcile the completed affiliation-first design with the existing opt-in
  runtime and verify the minimum state, observation, resolved-input,
  history/replay, and debrief contracts.

  Done:
  - Audited the ADR, model, observation, input-resolution, transition, replay,
    MCP, scenario, and debrief source boundaries.
  - Confirmed the existing `regional-affiliation-v1` runtime satisfies all six
    minimum proposal contracts.
  - Validated the committed v0.12.2 artifact with 9/9 complete runs, 54/54
    stages, and typed commitments, alternatives, and assumptions in every
    decision-time observation.
  - Confirmed no new runtime change is authorized; direct acquisition, deal
    finance, national markets, legal forecasts, generic actor frameworks, and
    changes to `competitive-regional-v1` remain deferred.
  - Bumped package metadata to `0.12.7`.

  Deferred / Non-Goals:
  - No acquisition expansion, deal financing, new actor class, legal forecast,
    multi-transaction framework, competitive-campaign change, or new runtime
    implementation.

  Verification:
  - Proposal source markers supported across all required boundaries.
  - 308 Rust tests, 199 Python tests, formatting, clippy, CLI smoke, golden,
    diff checks, focused proposal tests, and deterministic artifact validation
    pass.

### Project document alignment and version bump (v0.12.14)

- Reconciled the canonical proposal, roadmap, design principles, architecture,
  README, and player guide with the three implemented campaigns, the GUI
  thin-client proof, and the evidence-gated maintenance posture.
- Replaced obsolete roadmap startup actions with the remaining bounded Phase 8
  gaps and the promotion gate for any future runtime work.
- Bumped package and public milestone metadata to `0.12.14` without changing
  simulation behavior.

Verification:

- Release metadata, documentation diff/link review, Rust quality checks, and
  GUI syntax/static contract checks pass.

### Visual and audio SDD planning (v0.12.15)

- Adapted the visual/audio proposal so reproducible AI-agent playtests replace
  budget-dependent human testplays while human-experience claims remain
  explicitly deferred.
- Added the complete phased Future contract, first competitive-month slice,
  visual/audio/asset/accessibility requirements, promotion gates, AI-testplay
  protocol, evidence limits, contributor boundaries, risk controls, and stop
  rules to this specification.
- Added the planned thin-client presentation boundary to `ARCHITECTURE.md` and
  ranked only Phase 0 as the next promotion candidate.
- Bumped package and public milestone metadata to `0.12.15` without changing
  runtime behavior.

Verification:

- Proposal-to-SPEC coverage, domain-boundary QA, AI-testplay wording review,
  release metadata consistency, and documentation diff checks pass.

## Past

### Visual/audio Phase 6 closure (v0.12.22)

Phase 6 closed the bounded schematic regional-world slice with its typed host
read, browser map/overlay/navigation surface, observation-lag checks, and
explicit missingness. Package and public metadata were bumped to `0.12.22`.

- Feature: Visual/audio Phase 6 regional world
  Status: Closed; merged in PR #173
  Started: 2026-07-15
  Branch: feat/visual-audio-phase6-regional-world-v0.12.22

  Summary:
  Phase 6 adds a host-derived, actor-visible schematic regional world to the
  one-month competitive presentation. The host supplies stable institutional
  identity, owned detail, visible overlays, lagged public rival signals, source
  labels, navigation targets, and explicit missingness; the browser supplies
  selection, layout, overlays, and local navigation.

  Done:
  - Added the typed `competitive-regional-world-v1` envelope and non-mutating
    `get_regional_world` MCP read for competitive sessions.
  - Exposed player-owned facilities, visible capacity/process detail, demand,
    access, unmet-demand, and pending-process overlays with source/equivalent
    labels; public rivals expose identity and only one-month-lagged public
    action signals.
  - Kept rival private operations, facilities, resources, projects, true
    coordinates, effect queues, and hidden state outside the DTO; missing
    signal and unavailable private detail are explicit.
  - Added browser map/entity selection, overlay rendering, keyboard-reachable
    navigation links, and recoverable empty/unsupported/adapter-error handling
    without replacing the existing action, resolution, audio, history, or
    debrief paths.
  - Added host/browser visibility, lag, non-mutation, no-formula, no-network,
    and no-geography contract tests and Phase 6 design/QA documentation.
  - Bumped package and public metadata to `0.12.22`.

  Closure note:
  - Phase 7 campaign coverage was subsequently completed in PR #174; this
    record remains scoped to the Phase 6 regional-world slice.

  Deferred / Non-Goals:
  - No true geography, distances, routes, patient movement, city-builder
    mechanics, relationship/equilibrium model, map assets, campaign expansion,
    packaging, deployment, or human evaluation.
  - No private rival reveal, true-state view, resolved stochastic-input
    exposure, browser-owned regional state, or map-derived audio/state.
  - No transition formulas, randomness, replay verification, history/hash
    semantics, scenario rules, or existing command families changed.
  - Phases 7–9 remain sequentially gated by their own evidence and acceptance
    criteria.

  Verification:
  - Regional-world, audio, resolution, and contextual/read-only GUI contracts
    pass with visible sources/equivalents, lag, hidden-field exclusion,
    non-mutation, error recovery, controls, and JavaScript syntax.
  - Release metadata, documentation, formatting, clippy, and the full Python
    and Rust suites pass.

### Phase 7 campaign coverage closure

- Feature: Visual/audio Phase 7 campaign coverage
  Status: Closed; merged in PR #174
  Started: 2026-07-15
  Branch: feat/visual-audio-phase7-campaign-coverage-v0.12.23

  Summary:
  Phase 7 extends the additive presentation boundary to the existing
  `stabilization-v1` and `regional-affiliation-v1` campaigns. A shared browser
  shell renders each campaign's own stage, briefing, visible metrics, actors,
  processes, decisions, history, replay metadata, and debrief without making
  their observations or decision semantics interchangeable.

  Done:
  - Added the typed `campaign-coverage-v1` envelope and non-mutating
    `get_campaign_coverage` MCP read for stabilization and affiliation sessions.
  - Added stabilization coverage for its five-turn executive loop and
    stage-specific host commands, visible cash/capacity/access/quality reports,
    policy/market signals, uncertainty, history, and educational debrief.
  - Added affiliation coverage for partner condition, posture, commitments,
    review, labor/payer/community responses, integration/decline, explicit
    actor distinctions, visible obligations, history, and affiliation debrief.
  - Added host-shaped browser decision forms that substitute only host-provided
    parameters into canonical command templates; the existing `submit_turn`
    path remains the only mutation boundary and rejection is recoverable.
  - Reused the existing visible-only audio catalog for campaign pressure,
    completion, and affiliation milestone cues; written content remains
    complete when audio is unavailable or muted.
  - Added typed Rust, browser, static, documentation, and non-mutation contract
    tests and the Phase 7 evidence/design/QA artifacts.
  - Bumped package and public metadata to `0.12.23`.

  Closure note:
  - Phase 8 readiness was subsequently completed in PR #175; this record
    remains scoped to the Phase 7 campaign-coverage slice.

  Deferred / Non-Goals:
  - No new simulation state, command family, transition formula, stochastic
    input, effect queue, true-state/instructor view, universal campaign model,
    asset-backed identity, mobile redesign, deployment, or human evaluation.
  - No browser legality engine, client-side cost formula, private future outcome,
    partner forecast, competitive-regional-world semantic change, or campaign
    flattening.
  - Phases 8–9 remain sequentially gated by their own evidence and acceptance
    criteria.

  Verification:
  - Stabilization/affiliation coverage, competitive regional-world, audio,
    resolution, action, and read-only GUI contracts pass with source labels,
    hidden-field exclusion, non-mutation, rejection recovery, and JavaScript
    syntax checks.
  - Release metadata, documentation, formatting, clippy, and the full Python
    and Rust suites pass.

### Phase 8 AI-agent testplay readiness closure

- Feature: Visual/audio Phase 8 AI-agent testplay readiness
  Status: Closed; merged in PR #175
  Started: 2026-07-15
  Branch: feat/visual-audio-phase8-ai-testplay-v0.12.24

  Summary:
  Phase 8 adds a dependency-free browser readiness boundary for declared
  AI-agent interface tasks. It makes first-run guidance, local presentation
  settings, read/submission recovery, and sanitized interaction evidence
  inspectable without changing host authority or simulation semantics.

  Done:
  - Added the optional `gui-playtest-v1` recorder with declared campaign,
    role/task, interface/accessibility mode, capture method, and optional
    externally supplied screenshot references.
  - Added allowlisted onboarding, settings, retry, semantic snapshot,
    command, validation, audio, committed history/hash, failure, and task
    completion evidence lanes; raw payload and hidden-state fields are
    excluded by construction and diagnostics fail closed.
  - Added local reduced-motion and written-equivalent controls, actionable
    adapter/submission recovery, the role/task protocol, deterministic
    diagnostics, a fixture, and focused contract tests.
  - Bumped package and public metadata to `0.12.24`.

  Closure note:
  - No further Phase 8 implementation is planned; preserve its readiness
    limits and the Phase 9 evidence boundary.

  Deferred / Non-Goals:
  - No browser automation, network/service, deployment, screenshot
    generation/upload, external model orchestration, or new dependency.
  - No Rust simulation, MCP schema, command legality, transition formula,
    stochastic input, effect queue, history/hash/replay, debrief, or campaign
    observation change.
  - No true/private/raw state exposure, hidden DOM/model reasoning capture, or
    human usability, lived accessibility, learning, engagement, calibration,
    balance, policy, legal, or domain-expert claim.

  Verification:
  - Focused recorder/diagnostic and Node syntax checks, full Rust/Python
    suites, formatting, clippy, metadata, and whitespace checks pass.
  - Exactly one code-review pass completed; unsupported-schema exit behavior,
    nested forbidden-field checks, timing-independent audio capture, and
    malformed snapshot handling were fixed and reverified.

## Past

- Feature: Visual/audio Phase 9 AI-agent evaluation and revision
  Status: Closed; merged in PR #176
  Started: 2026-07-15
  Branch: feat/visual-audio-phase9-agent-evaluation-v0.12.25

  Summary:
  Phase 9 compares repeated validated `gui-playtest-v1` capture artifacts
  across declared campaigns, roles, tasks, seeds, and accessibility modes. It
  produces deterministic evidence-gap/recovery hypotheses and a product
  decision log without ranking strategies or changing the product automatically.

  Done:
  - Added `scripts/analyze_gui_playtests.py`, which reuses the Phase 8 validator,
    preserves declared matrix dimensions, emits stable capture/event/failure/
    evidence summaries, and assigns fixed P0–P2 triage priorities.
  - Added a five-capture synthetic protocol matrix covering stabilization,
    competitive, affiliation, first-time, access, strategy-review, and recovery
    paths, including context-aware rejected-command handling.
  - Added the Phase 9 evaluation/revision document with the matrix, product
    decision log, accepted analyzer revision, deferred UI/runtime revision, and
    explicit evidence limits.
  - Bumped package and public metadata to `0.12.25`.

  Closure note:
  - No further Phase 9 implementation is planned; preserve the decision-log
    gate for any future visual/audio proposal.

  Deferred / Non-Goals:
  - No browser automation, model/network service, screenshots, deployment,
    external orchestration, new dependency, or new capture schema.
  - No simulation/MCP/GUI transition/audio/history/hash/replay/debrief/campaign
    change and no automatic product mutation from analysis output.
  - No strategy score, causal inference, calibration, balance, policy validity,
    human usability, lived accessibility, learning, engagement, or domain claim.

  Verification:
  - Focused analysis/Phase 8 tests, deterministic repeated-output comparison,
    full Rust/Python/Node/metadata/formatting/clippy checks pass.
  - Exactly one code-review pass completed; missing-input reporting and
    schema-valid versus task-evidence-valid classification were fixed and
    reverified.

- Feature: Visual/audio Phase 10 accessibility and visual-language hardening
  Status: Closed; merged in PR #177
  Started: 2026-07-15
  Branch: feat/visual-audio-phase10-accessibility-v0.12.26

  Summary:
  Phase 10 closes a concrete part of the remaining accessibility and visual
  language contract: keyboard skip/landmark navigation, explicit non-color
  status language, persistent text scaling, and a functional optional
  cue-explanation preference. The slice remains presentation-only and does not
  create a browser-owned simulation or campaign-launch path.

  Done:
  - Added the Phase 10 request, evidence, mechanism, and implementation-plan
    handoffs plus a bounded protocol document.
  - Added keyboard-focus skip navigation, a presentation navigation landmark,
    stable anchors, targeted live/status semantics, and visible focus styling.
  - Added the non-color status vocabulary/legend, persistent Standard/Large
    text scaling, and a functional optional cue-explanation preference while
    keeping essential written content visible.
  - Added focused contract tests for stable landmarks, status vocabulary and
    metadata, settings persistence, targeted live regions, and boundary
    exclusions.
  - Completed domain QA and exactly one general code-review pass; the review's
    skip-focus, unused-variable, and duplicate-rule findings were fixed.

  Closure note:
  - No further Phase 10 implementation is planned; preserve its technical
    accessibility proxy limits.

  Deferred / Non-Goals:
  - No host/MCP endpoint, simulation, command, transition, stochastic input,
    history/hash/replay, debrief, campaign, audio-source, asset, or deployment
    change.
  - No browser automation, screen-reader certification, contrast study, or
    human usability/lived-accessibility/learning/engagement claim.

  Verification:
  - Focused Phase 10/accessibility, existing GUI, and release tests: 56 passed;
    full Python discovery: 288 passed.
  - Rust, formatting, clippy, Node syntax, release metadata, and diff checks
    pass; no Rust simulation or host-boundary tests changed.
  - Domain QA passed and exactly one general code-review pass completed with
    all actionable findings fixed and reverified.

- Feature: Visual/audio Phase 11 first-session launch/load boundary
  Status: Closed; merged in PR #178
  Started: 2026-07-15
  Branch: feat/visual-audio-phase11-session-launch-v0.12.27

  Summary:
  Phase 11 closes the first remaining entry-point gap in the planned competitive
  vertical slice: a first-time executive can start a competitive session with
  host-supported seed/difficulty inputs or load an existing session ID, then
  reach the existing actor-visible GUI surfaces. The browser remains a thin
  client over the existing host session operation.

  Done:
  - Added the Phase 11 request, evidence map, mechanism design,
    implementation plan, and protocol document.
  - Confirmed the existing MCP `start_session` request/envelope is sufficient;
    no Rust/MCP schema change is planned.
  - Added accessible start/load controls for the fixed competitive campaign,
    seed/difficulty validation, existing session loading, recoverable failures,
    and host-typed presentation refresh for read-only and action clients.
  - Added focused boundary tests and updated GUI/project documentation and
    release metadata to `0.12.27`.
  - Completed domain QA and exactly one general code-review pass; the review's
    actionable findings were fixed and reverified.

  Closure note:
  - No further Phase 11 implementation is planned; preserve its technical
    launch/load proxy limits.

  Deferred / Non-Goals:
  - No scenario picker, saved-session persistence, auth, web transport,
    campaign expansion, auto-action, asset/audio change, or simulation change.
  - No human usability, accessibility, learning, onboarding, or policy-validity
    claim follows from technical launch tests.

  Verification:
  - Focused Phase 11/accessibility/release tests: 17 passed; full Python suite:
    294 passed.
  - Rust, formatting, Clippy, Node syntax, release metadata, and diff checks
    pass; no Rust/MCP behavior changed.

- Feature: Visual/audio Phase 12 visual identity and marker provenance
  Status: Closed; merged in PR #179
  Started: 2026-07-15
  Branch: feat/visual-audio-phase12-visual-identity-v0.12.28

  Summary:
  Phase 12 narrows the remaining first-slice visual-language gap to a stable,
  generated vocabulary for system identity, facility/metric/process markers,
  and the existing non-color status language. The browser uses only visible
  IDs, names, kinds, labels, and categories; the host remains authoritative.

  Done:
  - Added the Phase 12 request, evidence map, mechanism design,
    implementation plan, and protocol document.
  - Added the generated `visual-catalog-v1` module and machine-readable
    registry for system identities, category markers, status vocabulary, and
    explicit generic fallback.
  - Added semantic identity/marker tokens to the regional map, selected detail,
    facilities, overlays, pending processes, and campaign process rows while
    retaining source/status text.
  - Added focused visual identity tests, provenance credits, and bumped release
    metadata to `0.12.28`.

  Closure note:
  - No further Phase 12 implementation is planned; preserve its technical
    visual-vocabulary and provenance limits.

  Deferred / Non-Goals:
  - No Rust/MCP schema, simulation, command, transition, stochastic,
    history/hash/replay, debrief, audio-source, network, geography, animation,
    licensed asset, campaign, or human-evaluation change.

  Verification:
  - Focused visual-catalog plus existing GUI/audio/accessibility/regional/static/
    release tests: 32 passed; full Python discovery: 299 passed.
  - Node syntax, Rust tests/formatting/Clippy, release metadata, diff checks,
    and domain QA pass; no Rust/MCP source changed.

- Feature: Visual/audio Phase 13 first-month continuity
  Status: Closed; merged in PR #180
  Started: 2026-07-15
  Branch: feat/visual-audio-phase13-first-month-continuity-v0.12.29

  Summary:
  Phase 13 connects the existing launch/load, actor-visible inspection,
  contextual action, validation, submission, resolution, and refreshed-read
  surfaces with a local, text-first first-month path rail. The rail reports
  presentation handoffs only; the host remains authoritative for commands,
  transitions, stochastic outcomes, history, hashes, replay, and debrief.

  Done:
  - Add the `competitive-first-month-v1` stage catalog and pure local stage
    derivation for start, inspect, draft, validate, submit, resolution, and
    continue.
  - Render current, completed, and upcoming stage text in the competitive
    desktop without relying on color, audio, or motion.
  - Advance stages only after the existing host-shaped client operations
    succeed; preserve rejection/recovery and read-only submit exclusion.
  - Verify a complete adapter-driven one-month handoff with at least two local
    draft actions and no host/simulation boundary change.

  Closure note:
  - CI/PR/merge completed in PR #180; the post-merge contract audit is recorded
    as the v0.12.30 follow-up closure below.

  Deferred / Non-Goals:
  - No Rust/MCP schema, simulation, command, transition, stochastic,
    history/hash/replay, debrief, campaign, audio-source, asset, network,
    dependency, or browser-transport change.
  - No human usability, lived accessibility, learning, engagement,
    calibration, balance, policy-validity, or domain-expert claim.

  Verification:
  - Focused stage, semantic rendering, adapter-sequence, rejection/recovery,
    read-only, boundary, full Python, Rust, release-metadata, Node syntax,
    formatting, Clippy, and diff checks pass; no Rust/MCP source changed.

### Visual/audio first-month contract closure (v0.12.30)

- Feature: Visual/audio first-month contract audit
  Status: Closed; bounded technical sequence complete
  Started: 2026-07-15
  Branch: feat/visual-audio-first-month-contract-v0.12.30

  Summary:
  The deterministic `visual-audio-first-month-contract-v1` audit reconciles
  the proposal's exact one-month experience with the merged Phase 0–13 source
  and focused tests. It closes the technical presentation sequence without
  turning technical evidence into a human, educational, calibration, balance,
  policy-validity, or domain-expert claim.

  Done:
  - Added the fail-closed source/test audit for launch/load, market and
    facility inspection, visible pressure and payer/rival context, contextual
    drafts, canonical validation/submission, resolution metrics/effects,
    optional audio, and continuation.
  - Added phase-document, generated-provenance, and presentation-boundary
    checks plus a compact JSON evidence artifact and contract tests.
  - Updated the active spec, architecture, README, changelog, lessons, and
    release metadata to record the bounded closure at `0.12.30`.

  Deferred / Non-Goals:
  - No Rust/MCP, simulation, stochastic, history/hash/replay, debrief,
    campaign, browser transport, dependency, asset, audio-source, or runtime
    behavior change.
  - No browser transport, viewport, contrast, screen-reader, hardware-audio,
    human usability, lived accessibility, learning, engagement, calibration,
    balance, policy-validity, or domain-expert claim.

  Verification:
  - Audit status `complete`: ten first-month requirements pass, all 14 phase
    documents and three provenance files are present, and boundary violations
    are empty.
  - Focused/full Python, Node syntax, release metadata, Rust formatting,
    Clippy, serial Rust tests, and diff checks pass.

### Live competitive GUI host repair (v0.12.31)

- Feature: Loopback live GUI host and player quickstart
  Status: Closed; implementation and verification complete
  Started: 2026-07-15

  Summary:
  The shipped browser page can now start and play `competitive-regional-v1`
  through one local Cargo command. A loopback-only HTTP edge delegates to the
  existing in-memory session store; the browser remains non-authoritative.

  Done:
  - Added the `hs-mgt-game-gui` binary, embedded static serving, same-origin
    adapter, structured errors, and non-loopback rejection.
  - Fixed no-session live bootstrap and removed unsupported competitive
    campaign-coverage reads from the live presentation/action path.
  - Added real transport, adapter, documentation, and existing GUI regression
    coverage.
  - Added exact README and player-guide instructions for launch, first-month
    flow, audio, alternate ports, in-memory sessions, shutdown, and recovery.

  Deferred / Non-Goals:
  - No stabilization/affiliation GUI, persistence, remote host, authentication,
    multiplayer, packaging, simulation, balance, or audio-source change.
  - No human usability, lived accessibility, learning, calibration, policy, or
    domain-expert claim.

### Visual/audio agent harness (v0.12.33)

- Status: Closed; harness implementation and structural verification complete
- Started: 2026-07-20

  Done:
  - Added a presentation-contract specialist that maps every semantic visual,
    motion, and audio signal to actor-visible sources, fallbacks, provenance,
    authority boundaries, and evidence limits before production.
  - Added a presentation-domain QA specialist with pass/fix/redo review for
    hidden-state leakage, unsupported causality, accessibility equivalence,
    asset rights/provenance, graceful degradation, and replay isolation.
  - Extended the existing orchestrator and team spec with selective simulation
    and presentation tracks plus deterministic handoffs and failure scenarios.

  Verification:
  - New skills contain valid discovery frontmatter and complete input, output,
    workflow, validation, and reference contracts.
  - Orchestrator and team-spec paths and handoff names agree; documentation-link
    and release-metadata checks pass.

  Deferred / Non-Goals:
  - No visual/audio roadmap milestone was started or promoted.
  - No GUI, asset, audio, simulation, command, stochastic, history/hash/replay,
    debrief, calibration, policy-validity, or human-evaluation change.

### Visual/audio Phase 0 foundation (v0.12.34)

- Status: Closed; product brief, asset repository, validation, and credits
  implementation and verification complete
- Started: 2026-07-20
- Branch: `feat/visual-audio-phase0-foundation-v0.12.34`

  Done:
  - Added the product brief for the flat-vector executive direction, first
    competitive-month slice, supported desktop targets, optional hybrid audio,
    reduced motion, accessibility, license allowlist/denylist, AI-generation
    policy, review ownership, and host-authority boundary.
  - Added separated `assets/source`, `assets/generated`, `assets/release`, and
    `assets/registry` paths with visual/audio schemas and project-generated
    baseline manifests.
  - Added dependency-free validation for metadata, semantic roles, licenses,
    approvals, stable IDs, source/release hashes, and unregistered release
    files, plus deterministic generated credits and a contributor checklist.
  - Checked only the demonstrated Phase 0.1 and 0.2 roadmap items.

  Verification:
  - Focused and full Python tests, asset validation/credits, documentation
    links, release metadata, Rust format/clippy/tests, Node syntax, and diff
    checks pass.

  Deferred / Non-Goals:
  - No asset acquisition or generation, GUI redesign, host/MCP schema, command,
    transition, stochastic input, history/hash/replay, debrief, or human,
    legal, artistic, hardware-audio, learning, calibration, balance, or policy
    validity claim.

### Visual/audio Phase 1.1 art direction (v0.12.35)

- Status: Closed; reference board, selection ADR, registry, and technical
  verification complete
- Started: 2026-07-20
- Branch: `feat/visual-audio-phase1-art-direction-v0.12.35`

  Done:
  - Added three labeled, source-only SVG references: institutional flat, civic
    terrain, and editorial desktop.
  - Scored strategic clarity, semantic compactness, institutional tone,
    color-independent accessibility path, modular reuse, and implementation
    risk; selected Variant A and rejected B/C with explicit reasons.
  - Recorded color-blind, small-size, large-text, reduced-motion, provenance,
    and schematic/non-geographic boundaries in a design board and ADR-0012.
  - Checked only the demonstrated Phase 1.1 roadmap items.

  Verification:
  - XML/static SVG, registry/credits, focused/full Python, documentation-link,
    release-metadata, formatting, Node syntax, and diff checks pass.

  Deferred / Non-Goals:
  - No SVG renderer, GUI integration, facility/map production kit, animation,
    audio, third-party asset, runtime host/simulation change, or human design,
    accessibility, learning, calibration, balance, or policy-validity claim.

### Visual/audio Phase 1.2 SVG proof (v0.12.36)

- Status: Closed; fixture-driven renderer, keyboard proof, and technical
  verification complete
- Started: 2026-07-20
- Branch: `feat/visual-audio-phase1-svg-proof-v0.12.36`

  Done:
  - Added `gui/scene.mjs` with a narrow visible scene model, deterministic SVG
    output, text/symbol status semantics, uncertainty pattern, and generic
    identity/marker/status fallbacks.
  - Added `gui/svg-proof.html` with local institution/facility keyboard
    selection and reduced-motion controls; it never loads or mutates a host.
  - Added snapshot, keyboard/fallback, reduced-motion, boundary, and render-time
    tests; registered the renderer as project-generated source provenance.
  - Checked only the demonstrated Phase 1.2 roadmap items.

  Verification:
  - 327 Python tests, 328 Rust library tests plus integration/golden/doc targets,
    Clippy, asset/credits, documentation links, release metadata, formatting,
    Node syntax, and diff checks pass.

  Deferred / Non-Goals:
  - No live GUI integration, host DTO, command, transition, stochastic input,
    browser simulation state, true geography, animation, audio, third-party
    asset, or human usability/accessibility/design claim.

### Visual/audio Phase 1.3 audio direction (v0.12.37)

- Status: Partial; fixture-only standards and recipe board complete
- Branch: `feat/visual-audio-phase1-audio-direction-v0.12.37`
- Added seven generated Web Audio direction recipes and a static preview board.
- Documented loudness, peak, cue duration, loop, crossfade, ducking, and
  low-volume targets with visible-source/text-equivalent mappings.
- Checked the first seven Phase 1.3 roadmap items only; priority scheduling,
  cooldowns, audio modes, and reduced-audio preference behavior remain Future.
- No live audio-client, host, simulation, history/hash/replay, or debrief change.

### Visual/audio Phase 1.3 audio policy (v0.12.38)

- Status: Closed; recipe policy prototype and verification complete
- Branch: `feat/visual-audio-phase1-audio-policy-v0.12.38`
- Added deterministic event/interface/music/ambience priority, -8 dB music
  ducking metadata, per-entry cooldowns, full/cues-only/muted modes, and
  reduced-audio preference behavior to the fixture proof.
- Preserved visible sources and text equivalents for allowed, filtered,
  throttled, unsupported, and muted results.
- Checked all Phase 1.3 roadmap items; no live audio-client or host behavior
  changed.

### Visual/audio Phase 2.1 Riverside identity kit (v0.12.39)

- Status: Partial; Riverside kit and fixture proof complete
- Branch: `feat/visual-audio-phase2-riverside-identity-v0.12.39`
- Added fictional source/release SVG variants for logo, monochrome, marker,
  signage, report header, compact badge, and RV monogram, plus a linked
  Riverside audio motif reference and generic fallback.
- Checked the Riverside per-system checklist only; Northlake and Summit remain
  Future slices.
- No live GUI, host, simulation, history/hash/replay, or debrief behavior
  changed.

### Visual/audio Phase 2.1 Northlake identity kit (v0.12.40)

- Status: Partial; Northlake kit and shared fixture proof complete
- Branch: `feat/visual-audio-phase2-northlake-identity-v0.12.40`
- Added a distinct fictional Northlake source/release SVG kit and
  `audio.direction-northlake-motif`; the shared proof selector covers both
  systems and generic fallback.
- Checked Riverside and Northlake per-system lanes; Summit remains Future.
- No live GUI, host, simulation, history/hash/replay, or debrief behavior
  changed.

### Visual/audio Phase 2.1 Summit identity kit (v0.12.41)

- Status: Closed; all three fictional system identity lanes complete
- Branch: `feat/visual-audio-phase2-summit-identity-v0.12.41`
- Added a distinct fictional Summit source/release SVG kit and
  `audio.direction-summit-motif`; the shared proof covers Riverside, Northlake,
  Summit, and generic fallback.
- Checked all Phase 2.1 per-system identity items; no live GUI or host behavior
  changed.

### Visual/audio Phase 2.2 actor-family identity language (v0.12.42)

- Status: Closed; shared actor-family catalog and fixture proof complete
- Branch: `feat/visual-audio-phase2-actor-family-language-v0.12.42`
- Added stable payer, regulator, labor, employer, community, board, policy
  coalition, and independent-provider records with glyphs, report frames,
  notification styles, optional identity-sonic tags, visible sources, written
  equivalents, and generic fallback.
- Added registry-backed provenance and deterministic proof/tests for semantic
  labels, color-independent pattern cues, unknown-family fallback, and the
  presentation-only boundary.
- Checked all Phase 2.2 actor-family identity-language items; no live GUI or
  host behavior changed.

### Visual/audio Phase 3.1 general-hospital base component (v0.12.43)

- Status: Partial; general-hospital base component and fixture proof complete
- Branch: `feat/visual-audio-phase3-general-hospital-base-v0.12.43`
- Added registry-backed source/release SVG derivatives with shared 8px grid,
  system color variables, accessible labels, and seven composable layers for
  base, identity, capacity, project, pressure, selection, and uncertainty.
- Added a fixture component catalog, generic facility fallback, non-color layer
  patterns, deterministic hashes, and focused boundary tests.
- Checked all 13 general-hospital-base per-component items; other Phase 3.1
  facility types remain separate future slices and no live GUI or host behavior
  changed.

### Visual/audio Phase 3.1 patient-tower component (v0.12.44)

- Status: Partial; patient-tower component and shared fixture proof complete
- Branch: `feat/visual-audio-phase3-patient-tower-v0.12.44`
- Added a distinct fictional patient-tower source/release SVG pair using the
  shared 8px grid, system color variables, accessible labels, and the same
  seven base/identity/capacity/project/pressure/selection/uncertainty layers.
- Extended the shared facility catalog/proof selector with patient tower,
  generic fallback, deterministic hashes, and boundary tests.
- Checked all 13 patient-tower per-component items; other Phase 3.1 facility
  types remain separate future slices and no live GUI or host behavior changed.

### Visual/audio Phase 3.1 emergency-department component (v0.12.45)

- Status: Partial; emergency-department component and shared fixture proof
  complete
- Branch: `feat/visual-audio-phase3-emergency-department-v0.12.45`
- Added a distinct fictional emergency-department source/release SVG pair using
  the shared 8px grid, system color variables, accessible labels, and the same
  seven base/identity/capacity/project/pressure/selection/uncertainty layers.
- Extended the shared facility catalog/proof selector with emergency
  department, generic fallback, deterministic hashes, and boundary tests.
- Checked all 13 emergency-department per-component items; other Phase 3.1
  facility types remain separate future slices and no live GUI or host behavior
  changed.

### Visual/audio Phase 3.1 ambulatory-center component (v0.12.46)

- Status: Partial; ambulatory-center component and shared fixture proof
  complete
- Branch: `feat/visual-audio-phase3-ambulatory-center-v0.12.46`
- Added a distinct fictional ambulatory-center source/release SVG pair using
  the shared 8px grid, system color variables, accessible labels, and the same
  seven base/identity/capacity/project/pressure/selection/uncertainty layers.
- Extended the shared facility catalog/proof selector with ambulatory center,
  generic fallback, deterministic hashes, and boundary tests.
- Checked all 13 ambulatory-center per-component items; other Phase 3.1
  facility types remain separate future slices and no live GUI or host behavior
  changed.

### Visual/audio Phase 3.1 specialty-center component (v0.12.47)

- Status: Partial; specialty-center component and shared fixture proof complete
- Branch: `feat/visual-audio-phase3-specialty-center-v0.12.47`
- Added a distinct fictional specialty-center source/release SVG pair using
  the shared 8px grid, system color variables, accessible labels, and the same
  seven base/identity/capacity/project/pressure/selection/uncertainty layers.
- Extended the shared facility catalog/proof selector with specialty center,
  generic fallback, deterministic hashes, and boundary tests.
- Checked all 13 specialty-center per-component items; other Phase 3.1
  facility types remain separate future slices and no live GUI or host behavior
  changed.

### Visual/audio Phase 3.1 rural-clinic component (v0.12.48)

- Status: Partial; rural-clinic component and shared fixture proof complete
- Branch: `feat/visual-audio-phase3-rural-clinic-v0.12.48`
- Added a distinct fictional rural-clinic source/release SVG pair using the
  shared 8px grid, system color variables, accessible labels, and the same
  seven base/identity/capacity/project/pressure/selection/uncertainty layers.
- Extended the shared facility catalog/proof selector with rural clinic,
  generic fallback, deterministic hashes, and boundary tests.
- Checked all 13 rural-clinic per-component items; other Phase 3.1 facility
  types remain separate future slices and no live GUI or host behavior changed.

### Visual/audio Phase 3.1 administrative-headquarters component (v0.12.49)

- Status: Partial; administrative-headquarters component and shared fixture
  proof complete
- Branch: `feat/visual-audio-phase3-administrative-headquarters-v0.12.49`
- Added a distinct fictional administrative-headquarters source/release SVG
  pair using the shared 8px grid, system color variables, accessible labels,
  and the same seven base/identity/capacity/project/pressure/selection/
  uncertainty layers.
- Extended the shared facility catalog/proof selector with administrative
  headquarters, generic fallback, deterministic hashes, and boundary tests.
- Checked all 13 administrative-headquarters per-component items; parking
  structure, utility plant, research/education building, construction crane,
  and undeveloped parcel remain separate future slices and no live GUI or host
  behavior changed.

### Visual/audio Phase 3.1 parking-structure component (v0.12.50)

- Status: Partial; parking-structure component and shared fixture proof
  complete
- Branch: `feat/visual-audio-phase3-parking-structure-v0.12.50`
- Added a distinct fictional parking-structure source/release SVG pair using
  the shared 8px grid, system color variables, accessible labels, and the same
  seven base/identity/capacity/project/pressure/selection/uncertainty layers.
- Extended the shared facility catalog/proof selector with parking structure,
  generic fallback, deterministic hashes, and boundary tests.
- Checked all 13 parking-structure per-component items; utility plant,
  research/education building, construction crane, and undeveloped parcel remain
  separate future slices and no live GUI or host behavior changed.

### Visual/audio Phase 3.1 utility-plant component (v0.12.51)

- Status: Partial; utility-plant component and shared fixture proof complete
- Branch: `feat/visual-audio-phase3-utility-plant-v0.12.51`
- Added a distinct fictional utility-plant source/release SVG pair using the
  shared 8px grid, system color variables, accessible labels, and the same
  seven base/identity/capacity/project/pressure/selection/uncertainty layers.
- Extended the shared facility catalog/proof selector with utility plant,
  generic fallback, deterministic hashes, and boundary tests.
- Checked all 13 utility-plant per-component items; research/education building,
  construction crane, and undeveloped parcel remain separate future slices and
  no live GUI or host behavior changed.

### Visual/audio Phase 3.1 research-education-building component (v0.12.52)

- Status: Partial; research-education-building component and shared fixture
  proof complete
- Branch: `feat/visual-audio-phase3-research-education-building-v0.12.52`
- Added a distinct fictional research-and-education-building source/release
  SVG pair using the shared 8px grid, system color variables, accessible
  labels, and the same seven base/identity/capacity/project/pressure/
  selection/uncertainty layers.
- Extended the shared facility catalog/proof selector with research and
  education building, generic fallback, deterministic hashes, and boundary
  tests.
- Checked all 13 research-education-building per-component items; construction
  crane and undeveloped parcel remain separate future slices and no live GUI or
  host behavior changed.

### Visual/audio Phase 3.1 construction-crane component (v0.12.53)

- Status: Partial; construction-crane component and shared fixture proof
  complete
- Branch: `feat/visual-audio-phase3-construction-crane-v0.12.53`
- Added a distinct fictional construction-crane source/release SVG pair using
  the shared 8px grid, system color variables, accessible labels, and the same
  seven base/identity/capacity/project/pressure/selection/uncertainty layers.
- Extended the shared facility catalog/proof selector with construction crane,
  generic fallback, deterministic hashes, and boundary tests.
- Checked all 13 construction-crane per-component items; undeveloped parcel
  remains the final separate future slice and no live GUI or host behavior
  changed.

### Visual/audio Phase 3.1 undeveloped-parcel component (v0.12.54)

- Status: Complete; all explicit Phase 3.1 facility component lanes are
  implemented and verified
- Branch: `feat/visual-audio-phase3-undeveloped-parcel-v0.12.54`
- Added a distinct fictional undeveloped-parcel source/release SVG pair using
  the shared 8px grid, system color variables, accessible labels, and the same
  seven base/identity/capacity/project/pressure/selection/uncertainty layers.
- Extended the shared facility catalog/proof selector with undeveloped parcel,
  generic fallback, deterministic hashes, and boundary tests.
- Checked all 13 undeveloped-parcel per-component items; later map, environment,
  and optional facility modules remain separate future slices and no live GUI
  or host behavior changed.

### Visual/audio Phase 3.2 map-grid contract (v0.12.55)

- Status: Partial; deterministic fixture-only map-grid contract complete
- Branch: `feat/visual-audio-phase3-map-grid-v0.12.55`
- Added `gui/map-environment.mjs` with a 960x600 symbolic viewport, 24px
  coordinate cells, named origin, explicit geography boundary, and a pure
  `mapGridCell` helper.
- Added registry/hash/credits provenance and deterministic coordinate tests.
- Checked the Phase 3.2 map-grid item; road tiles, districts, parcels,
  relationship lines, overlays, event markers, and interaction behavior remain
  separate future slices with no live GUI or host behavior changed.

### Visual/audio Phase 3.2 road-tiles contract (v0.12.56)

- Status: Partial; deterministic fixture-only road tile-set contract complete
- Branch: `feat/visual-audio-phase3-road-tiles-v0.12.56`
- Added `gui/map-tiles.mjs` with horizontal, vertical, and quarter-curve
  symbolic road tokens, 24px grid metadata, path-role labels, and generic
  fallback.
- Added registry/hash/credits provenance and deterministic road-token tests.
- Checked the Phase 3.2 road tile-set item; intersections, districts, parcels,
  relationship lines, overlays, event markers, and interaction behavior remain
  separate future slices with no live GUI or host behavior changed.

### Visual/audio Phase 3.2 district-tiles contract (v0.12.57)

- Status: Partial; deterministic fixture-only district tile-set contract
  complete
- Branch: `feat/visual-audio-phase3-district-tiles-v0.12.57`
- Added `gui/map-districts.mjs` with commercial, residential, employer-center,
  and government symbolic district tokens on the shared 24px grid, plus
  non-color patterns and a generic fallback.
- Added registry/hash/credits provenance and deterministic district-token tests.
- Checked the Phase 3.2 district tile-set item; intersections, parcels,
  relationship lines, overlays, event markers, and interaction behavior remain
  separate future slices with no live GUI or host behavior changed.

### Visual/audio Phase 3.2 parcel-system contract (v0.12.58)

- Status: Partial; deterministic fixture-only parcel-system contract complete
- Branch: `feat/visual-audio-phase3-parcel-system-v0.12.58`
- Added `gui/map-parcels.mjs` with facility and undeveloped-land symbolic parcel
  tokens on the shared 24px grid, plus non-color patterns and a generic
  fallback.
- Added registry/hash/credits provenance and deterministic parcel-system tests.
- Checked the Phase 3.2 parcel-system item; relationship lines, overlays, event
  markers, and interaction behavior remain separate future slices with no live
  GUI or host behavior changed.

### Visual/audio Phase 3.2 relationship-lines contract (v0.12.59)

- Status: Partial; deterministic fixture-only relationship-line style catalog
  complete
- Branch: `feat/visual-audio-phase3-relationship-lines-v0.12.59`
- Added `gui/map-relationships.mjs` with peer, service, policy, and uncertain
  non-color line styles, no-arrowhead defaults, and a generic fallback.
- Added registry/hash/credits provenance and deterministic relationship-style
  tests.
- Checked the Phase 3.2 relationship-line styles item; overlays, event markers,
  and interaction behavior remain separate future slices with no live GUI or
  host behavior changed.

### Visual/audio Phase 3.2 service-area-overlays contract (v0.12.60)

- Status: Partial; deterministic fixture-only service-area overlay catalog
  complete
- Branch: `feat/visual-audio-phase3-service-area-overlays-v0.12.60`
- Added `gui/map-service-areas.mjs` with primary, shared, and coordinated
  symbolic contour/fill patterns, metric-free defaults, and a generic fallback.
- Added registry/hash/credits provenance and deterministic service-area tests.
- Checked the Phase 3.2 service-area overlays item; uncertainty overlays, event
  markers, and interaction behavior remain separate future slices with no live
  GUI or host behavior changed.

### Visual/audio Phase 3.2 uncertainty-overlays contract (v0.12.61)

- Status: Partial; deterministic fixture-only uncertainty-overlay catalog
  complete
- Branch: `feat/visual-audio-phase3-uncertainty-overlays-v0.12.61`
- Added `gui/map-uncertainty.mjs` with stale, missing, and revised visible
  information patterns, no-severity defaults, static reduced-motion behavior,
  and a generic fallback.
- Added registry/hash/credits provenance and deterministic uncertainty tests.
- Checked the Phase 3.2 uncertainty overlays item; event markers and
  interaction behavior remain separate future slices with no live GUI or host
  behavior changed.

### Visual/audio Phase 3.2 event-markers contract (v0.12.62)

- Status: Complete; deterministic fixture-only event-marker and map-interaction
  proof implemented and verified
- Branch: `feat/visual-audio-phase3-event-markers-v0.12.62`
- Added `gui/map-event-markers.mjs` with policy, workforce, community, and
  project visible-category markers, written equivalents, no severity/priority
  encoding, static reduced-motion behavior, and a generic fallback.
- Added `gui/map-environment-proof.html` with shared map vocabulary, symbolic
  geography disclaimer, compact/standard/wide target metadata, fixed keyboard
  order, bounded zoom/pan controls, and visible local-state text.
- Added registry/hash/credits provenance and deterministic event-marker and
  interaction tests; checked every explicit Phase 3.2 map/environment item.
- Deferred: operational overlay library, live regional board integration, and
  host-sourced event semantics remain separately gated Future work.

### Visual/audio Phase 3.3 operational-overlays contract (v0.12.63)

- Status: Complete; deterministic fixture-only operational-overlay catalog and
  collision proof implemented and verified
- Branch: `feat/visual-audio-phase3-operational-overlays-v0.12.63`
- Added all twelve required overlay categories with semantic role, actor-visible
  triggering field, non-color pattern, static reduced-motion behavior, text
  equivalent, collision behavior, display-only priority rule, and generic
  fallback.
- Added deterministic ordering, stable-ID tie-breaking, bounded simultaneous
  stack layout, explicit overflow count, proof page, registry/hash/credits,
  and focused tests.
- Checked the Phase 3.3 operational overlay checklist; live board integration,
  host DTO changes, and outcome inference remain separately gated Future work.

### Visual/audio Phase 4.1 static regional-board contract (v0.12.64)

- Status: Complete; static regional-board adapter, GUI mount, and deterministic
  SVG snapshot proof implemented and verified
- Branch: `feat/visual-audio-phase4-static-board-v0.12.64`
- Added `gui/regional-board.mjs` to map the existing
  `competitive-regional-world-v1` actor-visible DTO into scene entities,
  facilities, overlays, sources, statuses, and explicit missingness.
- Integrated the SVG board into `gui/index.html`/`gui/app.mjs` with local
  institution/facility focus, report-to-board links, generic fallbacks,
  keyboard-reachable controls, and synchronized semantic detail panels.
- Added `gui/regional-board-proof.html`, a static snapshot hash fixture, focused
  adapter tests, and registry/credits provenance. No host DTO, simulation,
  command, transition, stochastic, history, hash, replay, audio, or debrief
  behavior changed.
- Checked every Phase 4.1 static regional-board checklist item. Visible
  consequence linkage and first-month integration remain Phase 4.2 work.

### Visual/audio Phase 4.2 visible consequence linkage contract (v0.12.65)

- Status: Complete; deterministic regional/process/effect links and replay
  sequence projection implemented and verified
- Branch: `feat/visual-audio-phase4-consequence-links-v0.12.65`
- Added `gui/consequence-links.mjs` for public regional signals, visible
  processes, host-committed resolution effects, targetless effects, and
  immutable replay turn/hash sequence entries.
- Integrated bidirectional report/entity focus and linked consequence board
  focus in `gui/app.mjs`/`gui/index.html`; focus uses local selection and does
  not depend on animation.
- Preserved observed-month rival delay, private-detail/missingness boundaries,
  deterministic ordering, historical state, and host-provided project/process
  status. Existing resolution and first-month tests remain the integration
  evidence; no Rust DTO or simulation change was required.
- Checked every Phase 4.2 visible consequence linkage item. Later roadmap
  phases remain separate slices.

### Visual/audio Phase 5.1 semantic information-container contract (v0.12.66)

- Status: Complete; eight semantic information-container contracts, GUI
  differentiation, and responsive/print proof implemented and verified
- Branch: `feat/visual-audio-phase5-semantic-containers-v0.12.66`
- Added `gui/semantic-containers.mjs` for board packet, operations ledger,
  intelligence report, regulatory letter, project sheet, news wire, executive
  action queue, and after-action report classes.
- Each class documents semantic purpose, header treatment, marker, compact and
  expanded variants, accessibility semantics, large-text/narrow-width/print
  behavior, reduced motion, and source/status preservation. The existing GUI
  applies the classes without changing text or host/simulation authority.
- Added `gui/semantic-container-proof.html`, focused tests, registry/credits,
  and completed every Phase 5.1 checklist item.

### Visual/audio Phase 5.2 metric and trend visualization contract (v0.12.67)

- Status: Complete; eight deterministic actor-visible metric visualization
  contracts, SVG proof, deterministic snapshot, and opt-in GUI rendering verified
- Branch: `feat/visual-audio-phase5-metric-visualization-v0.12.67`
- Added `gui/metric-visualizations.mjs` for sparklines, deltas, capacity bars,
  staffing composition, project progress, payer mix, trust trends, and visible
  uncertainty intervals.
- Each contract documents source precision, uncertainty, missingness, exact
  text, color-independent interpretation, large-text behavior, and proof
  fixture coverage. `gui/app.mjs` renders only explicit actor-visible metric
  descriptors and retains their written value/source/status text.
- Added deterministic SVG snapshot hash and focused tests, registry/credits,
  and completed every Phase 5.2 checklist item without consuming hidden state.

### Visual/audio Phase 6.1 motion specification contract (v0.12.68)

- Status: Complete; nine deterministic motion categories, replay/interruption
  planning, reduced-motion proof, load-budget smoke test, and fixture proof
  verified
- Branch: `feat/visual-audio-phase6-motion-spec-v0.12.68`
- Added `gui/motion-catalog.mjs` for focus, report arrival, month transition,
  project progress/completion, visible rival action, status, metric delta, and
  relationship-line changes.
- Every category documents semantic purpose, duration, easing, reduced-motion
  replacement, interruption behavior, replay behavior/order, input behavior,
  and a declared performance budget. The catalog never starts timers or changes
  host/simulation state.
- Added `gui/motion-proof.html`, focused tests, registry/credits, and completed
  every Phase 6.1 checklist item; local performance evidence is a smoke budget
  check, not a hardware or usability claim.

### Visual/audio Phase 6.2 first-month resolution sequence (v0.12.69)

- Status: Complete; the committed monthly resolution now has an explicit pure
  storyboard, display-only attention ordering, synchronized surface metadata,
  optional stage-aligned cues, keyboard-visible advance/skip controls, and
  deterministic skip/replay checks.
- Added `gui/resolution-sequence.mjs` over the existing
  `competitive-resolution-v1` envelope. Missing canonical steps render explicit
  written fallbacks and unknown host stages remain visible rather than being
  dropped.
- Updated `gui/app.mjs` and `gui/index.html` so every host step is rendered
  before local pacing; local play, pause, advance, skip, review, and reduced
  motion never change host state or remove committed reports.
- Evidence is technical contract coverage only. The keyboard-oriented
  first-time task proxy is not a human-comprehension, usability, accessibility,
  learning, calibration, or policy-validity claim.

### Visual/audio Phase 7.1 UI and event cue refinement (v0.12.70)

- Status: Complete; all 16 existing interface/event cue IDs now use one
  generated-audio standards contract and optional cues-only control.
- Added `gui/audio-cue-contract.mjs` with semantic purpose, priority class,
  duration, loudness target, peak ceiling, normalization gain, cooldown,
  visible trigger source, distinction label, and text equivalent for each cue.
- Updated `gui/audio.mjs` to decorate runtime cues from the contract and expose
  local `full`/`cues-only` mode. Cues-only suppresses music/ambience while
  interface/event cues, visible sources, and written equivalents remain.
- Added `gui/audio-cue-proof.html`, focused tests, and registry/credits
  provenance. No recorded or third-party audio was introduced.
- Contract/tests are technical consistency evidence only; they do not claim
  measured loudness, fatigue, musical quality, lived accessibility, human
  comprehension, learning, calibration, or policy validity.

### Visual/audio Phase 7.2 environmental ambience library (v0.12.71)

- Status: Complete; seven deterministic fictional-setting ambience recipes,
  provenance/rights metadata, loop/noise/loudness/safety contracts,
  reduced-audio behavior, fixture proof, and registry coverage verified
- Branch: `feat/visual-audio-phase7-ambience-library-v0.12.71`
- Added `gui/ambience-contract.mjs` for executive office, hospital lobby,
  hospital campus exterior, construction site, boardroom, press/policy event,
  and regional city bed settings. `gui/audio.mjs` exposes these entries while
  selecting only the actor-visible regional city bed as the default.
- Each setting uses a deterministic filtered-noise recipe, retains a written
  equivalent and fallback, forbids identifying speech, copyrighted music, real
  institution names, and clinical alarms, and records source hash basis plus
  the explicit no-release-file derivative rule.
- Added `gui/ambience-proof.html`, focused tests, and catalog/registry/credits
  provenance. The per-setting catalog repeats the source hash; release hashes
  are explicitly null because no release audio file is distributed. No
  recorded audio, host/simulation state, hidden-state selection, or
  clinical-severity claim was introduced.
- Contract/tests are technical consistency evidence only; they do not claim
  measured loudness, fatigue, musical quality, lived accessibility, human
  comprehension, learning, calibration, or policy validity.

### Visual/audio Phase 7.3 adaptive music stems (v0.12.72)

- Status: Complete; seven visible-state music contracts, five bounded stem
  roles per state, visible-only classifier/replay planning, crossfade metadata,
  music-only/full mute behavior, fixture proof, and registry coverage verified
- Branch: `feat/visual-audio-phase7-adaptive-music-v0.12.72`
- Added `gui/music-stem-contract.mjs` for menu/planning, stable operations,
  pressure, regulatory scrutiny, competitive escalation,
  affiliation/negotiation, and debrief. Existing IDs remain stable while the
  new states use the same generated-audio boundary.
- Updated `gui/audio.mjs` and `gui/index.html` to play bounded base-pulse,
  institutional-motif, visible-pressure, policy, and transition-cadence stems
  from actor-visible state only. Music-only mute, full mute, cues-only, focus,
  reduced, and unavailable-audio fallbacks retain written context.
- Added `gui/music-stem-proof.html`, focused tests, catalog/registry/credits
  provenance, and deterministic replay-state sequence checks. No recorded
  audio, hidden-state selection, host/simulation/replay change, or Phase 7.4
  priority/fatigue manager was introduced.
- Contract/tests are technical consistency evidence only; they do not claim
  measured loudness, musical quality, fatigue, lived accessibility, human
  comprehension, learning, calibration, or policy validity.

### Visual/audio Phase 7.4 audio priority and fatigue manager (v0.12.73)

- Status: Complete; fixed priority policy, one-critical batching, routine
  aggregation, duplicate suppression, bounded queue/voice behavior, ducking,
  preference persistence, proof fixture, and stress coverage verified
- Added `gui/audio-priority-contract.mjs` for pure deterministic cue-batch
  planning. Critical cues precede major cues; routine requests aggregate; one
  critical cue is selected per local batch; and queue/voice limits remain fixed.
- Updated `gui/audio.mjs` to dispatch at most one transient cue voice, duck
  ambience for major/critical cues and music for critical cues, and persist
  only explicit local audio preferences when browser storage is available.
- Added `gui/audio-priority-proof.html` and focused fake-Web-Audio/timer tests.
  Written results, source/status text, mute/fallback controls, and live-region
  behavior remain complete while queueing, aggregation, ducking, or storage
  failure are local presentation states.
- No host DTO, simulation transition, actor observation, history, hash, replay,
  debrief, recorded-audio, network, or hidden-state change was introduced.
- Contract/tests are technical consistency evidence only; they do not claim
  measured loudness, fatigue reduction, lived accessibility, screen-reader
  usability, human comprehension, learning, calibration, or policy validity.

### Visual/audio Phase 8.1 approved local generation workflow (v0.12.74)

- Status: Complete; local generation provenance capture, model/license scope,
  prompt templates, human review, registry bridging, proof, and fail-closed
  validation are verified
- Added `assets/generation/approved-models.json`,
  `generation-workflow.json`, `prompt-templates.json`,
  `human-review-checklist.json`, and an intentionally empty
  `generation-manifest.json`. The model listing records a primary model-card
  basis and access/review limitations; it does not establish training-data
  provenance, output ownership, or legal clearance.
- Added `scripts/capture_generation_metadata.py` and
  `scripts/validate_generation_metadata.py` to capture prompts, negative
  prompts, seed/settings, dimensions, application, source references,
  post-processing, accessibility, human-review fields, source/release paths,
  and SHA-256 hashes. Unknown models/licenses, missing or mismatched hashes,
  incomplete review, unapproved releases, and invalid registry bridges fail
  closed.
- Added `gui/generation-workflow-proof.html` and focused tests. No model
  weights, inference, generated asset, hosted service, runtime presentation,
  host DTO, simulation transition, history, replay, or debrief change was
  introduced.
- Technical checks demonstrate metadata consistency and release gating only;
  they do not establish legal clearance, output quality, human resemblance,
  clinical plausibility, lived accessibility, learning, or policy validity.

### Visual/audio Phase 8.2 first fictional actor portrait slice (v0.12.75)

- Status: In progress; seven-role identity contract, shared editorial style,
  fallback/accessibility requirements, and a preserved rival-system-executive
  preview are verified, while the preview remains pending and outside release
- Added `assets/generation/portrait-set.json` for rival system executive, payer
  negotiator, regulator, labor representative, community leader, board chair,
  and affiliation partner executive roles. The contract keeps portraits
  decorative and identity-only; they do not encode score, severity, intent,
  outcome, private action, or hidden simulation state.
- Added `assets/generation/portrait-previews.json`, the preserved preview PNG,
  `gui/portrait-workflow-proof.html`, and focused tests. The preview records its
  source hash, prompt, negative prompt, accessible equivalent, generic
  fallback, and pending review, but has no approved local model/seed
  provenance, release derivative, asset registry ID, or generation-manifest
  entry.
- No runtime GUI, host DTO, simulation transition, actor observation, history,
  hash, replay, debrief, or asset-registry release entry was changed. Technical
  checks do not establish human recognition, legal clearance, quality, lived
  accessibility, or educational benefit.

### Visual/audio Phase 8.2 remaining fictional actor portrait previews (v0.12.76)

- Status: In progress; all seven canonical role previews are preserved as
  unverified candidates, with six added in this slice. None is approved for
  runtime or release use.
- Added six role-specific PNG previews, source hashes, prompt/negative-prompt
  records, dimensions, capture dates, contributors, written equivalents,
  generic fallbacks, and pending portrait-review fields. The built-in preview
  tool does not expose the approved local model revision or actual seed, so
  those fields remain null and release remains blocked.
- Extended the generation validator to require exact role coverage and to
  reject unverified model/revision/seed metadata, and extended the proof/tests
  to show and check all seven candidates and the six current-slice targets.
- No runtime GUI authority, host DTO, simulation transition, actor
  observation, history, hash, replay, debrief, or asset-registry entry
  changed. Checks do not establish legal clearance, quality, accessibility,
  learning, or policy validity.

### Visual/audio Phase 8.2 review-ready portrait approval worksheet (v0.12.77)

- Status: In progress; the seven preserved preview candidates now have
  per-role review packets, but no packet is approved or release eligible.
- Added `assets/generation/portrait-review-queue.json` with source path/hash
  bindings, written equivalents, generic fallbacks, explicit review gates,
  pending human-review metadata, and null release/registry fields.
- Added `gui/portrait-review-proof.html` and focused tests. The validator
  rejects role/hash/path drift, incomplete reviewer metadata, attempted
  promotion, and any registry bridge while release eligibility is false.
- No runtime GUI, host DTO, simulation transition, actor observation, history,
  hash, replay, debrief, or asset-registry entry changed. The worksheet makes
  human review actionable but does not perform or imply human approval.

### Visual/audio Phase 9.1 provenance and notices (v0.12.78)

- Status: Closed; implementation and verification complete for automated
  technical gates. Canonical visual/audio registry entries now carry
  machine-checked provenance kind, source URL, retrieval date, and license
  reference fields.
- Repository-authored entries use the project policy reference with null
  external URL/date fields. External and local-generation entries are
  fail-closed until source/license references and retrieval dates are present.
- Credits now include provenance columns and the third-party notice projection
  is generated from the same registries. No external release asset or pending
  portrait preview entered the registry.
- No runtime GUI, host DTO, simulation transition, actor observation, history,
  hash, replay, or debrief authority changed. Automated checks do not perform
  a legal or human license audit.

### Visual/audio Phase 9.1 in-game credits (v0.12.79)

- Status: Closed; implementation and verification complete for automated
  technical gates. The static executive desktop now exposes a text-first,
  keyboard-accessible asset credits/provenance disclosure before and after
  host/session loading.
- The generated `gui/asset-credits.mjs` projection lists canonical registry
  entries with source, license, attribution, approval, provenance, release
  status, and written equivalents. Stale projection output fails CI.
- The renderer uses `textContent` and local static data only. No runtime GUI,
  host DTO, command, simulation transition, actor observation, history, hash,
  replay, or debrief authority changed; the panel is not human accessibility
  or legal-review evidence.

### Visual/audio Phase 9.2 asset security scanner (v0.12.80)

- Status: Closed; implementation and verification complete for automated
  technical gates. `scripts/validate_asset_security.py` scans current
  source/release files and preserved portrait previews without mutation or
  network access.
- The gate rejects unsafe SVG content, malformed XML, oversized files,
  excessive dimensions, and mismatched PNG/JPEG/GIF/WAV/OGG/MP3/FLAC
  signatures. It is independent of runtime, host, simulation, and replay
  authority.
- Automated file-shape checks do not establish legal clearance, decoder safety,
  audio quality, human accessibility, ownership, or human approval.

### Visual/audio Phase 9.2 release reproducibility (v0.12.81)

- Status: Closed; implementation and verification complete for automated
  technical gates. `scripts/verify_asset_release.py` derives a stable
  manifest from approved registry release paths with sorted paths, byte sizes,
  SHA-256 values, and a canonical manifest digest.
- Release-only image/audio metadata checks fail closed for unexpected text,
  EXIF/comment, application, tag, and descriptive metadata markers. Source
  previews remain non-release inputs and are not rewritten by the audit.
- The manifest and metadata checks are contributor/release artifacts only;
  they cannot enter host DTOs, commands, simulation state, observations,
  history, hashes, replay artifacts, or debrief facts. They do not establish
  legal clearance, decoder safety, accessibility, ownership, or human review.

### Visual/audio Phase 9.2 graceful asset fallback (v0.12.82)

- Status: Closed; implementation and verification complete. `gui/asset-availability.mjs` maps caller-supplied
  loaded, missing, failed, malformed, and unknown results to deterministic
  presentation statuses without loading files or reading host state.
- Facility and identity adapters preserve requested labels and written
  equivalents while removing the release path and switching to an explicit
  generic fallback when an optional asset is unavailable. The proof is
  keyboard-visible and uses no network, commands, hidden fields, or simulation
  authority.
- The fallback contract is not browser decoder, human accessibility, legal,
  quality, ownership, or educational evidence.

### Visual/audio Phase 9.2 audio playback fallback (v0.12.83)

- Status: Closed; implementation and verification complete. `audioPresentationFor` reuses the fail-closed local
  availability contract for existing cue, music, and ambience catalog entries.
- Unsupported Web Audio setup and thrown generated-cue/background playback
  publish a visible local fallback status and preserve the catalog source and
  written equivalent. A later local cue can retry after a transient failure.
- No recorded audio, decoder, network, host field, command, simulation state,
  observation, history, hash, replay, or debrief authority is added.
- Evidence remains limited to pure projections, fake-context recovery, and
  static/automated checks; it does not establish browser compatibility,
  loudness, audio quality, fatigue, accessibility, or human review.

### Visual/audio Phase 9.2 SVG metadata sanitizer (v0.12.84)

- Status: Closed; implementation and verification complete. A dependency-free transform removes SVG `<metadata>`
  from explicit derivatives while preserving `<title>`/`<desc>` content.
- The approved-release check is read-only and fails closed on removable
  metadata, malformed input, unsafe paths, symlinks, missing files, or output
  collisions. It never updates canonical hashes or manifests.
- Evidence is limited to transformation fixtures and release/security checks;
  it does not establish decoder safety, legal clearance, accessibility,
  ownership, quality, or human review.

### Visual/audio Phase 9 technical closure (v0.12.85)

- Status: Closed; implementation and verification complete. The Phase 9.1/9.2
  roadmap checklist is reconciled with passing automated license, provenance,
  credits, security, metadata, fallback, hash, and reproducibility gates.
- A regression test requires the exact technically evidenced checklist entries
  and all v0.12.78–v0.12.84 completion statuses while preserving explicit human
  legal, portrait, decoder, accessibility, ownership, quality, and review
  boundaries.
- No asset, registry, release hash, manifest, runtime, host, simulation,
  history, replay, or debrief artifact is changed.

### Visual/audio Phase 10.1 first-month technical slice (v0.12.86)

- Status: Closed; implementation and verification complete. A machine-checkable
  acceptance test binds every Phase 10.1 technical checklist item to the existing integrated GUI, host DTO,
  resolution, replay, accessibility, audio, fallback, and provenance surfaces.
- The probe remains deterministic and presentation-only. It cannot submit a
  command, advance a session, read hidden state, or rewrite history/hashes.
- Phase 10.2 first-time-user, accessibility-quality, audio-fatigue,
  educational-usability, legal, ownership, and human-review questions remain
  explicit external gates.

### Visual/audio Phase 10.2 evaluation preparation (v0.12.87)

- Status: In progress; the protocol, facilitator guide, anonymized revision
  template, and regression test are present, but no participant evidence has
  been collected.
- Done: stable first-session, recognition, consequence-tracing,
  accessibility, and audio tasks; bounded rating dimensions; exact finding
  categories; privacy restrictions; and a blank human decision record.
- Not Yet Done: audio feedback collection, quantitative ratings, qualitative
  interviews, classified findings, revisions, and go/no-go authorization.
- Deferred / Non-Goals: no participant data or recordings, legal or
  accessibility conclusions, educational claims, runtime behavior, asset
  changes, or host/simulation authority changes.

### Visual/audio Phase 11.1 campaign-coverage evidence (v0.12.88)

- Status: In progress; bounded catalog parity and fallback evidence are being
  recorded, while full-campaign coverage remains incomplete.
- Done: exact facility, overlay, actor-family, event-marker, event-cue, and
  music-state ledger IDs; visible source/equivalent checks; unknown fallback
  checks; and bounded first-month continuity surface references.
- Not Yet Done: full facility/overlay/event/history/debrief/save-load/replay
  coverage, screenshot suite, performance/compatibility validation, and human
  quality review.
- Deferred / Non-Goals: no runtime, asset, host, simulation, stochastic,
  history, replay, debrief, or authority change.

### Visual/audio Phase 11.1 live facility-component binding (v0.12.89)

- Status: In progress; the current actor-visible player facility groups now
  have stable catalog bindings, while full campaign facility coverage remains
  incomplete.
- Done: explicit `component_id` fields in the regional-world DTO; exact
  bindings for inpatient, outpatient, emergency/ICU, and specialty groups;
  catalog-backed generic fallback; accessible board metadata; selected-detail
  component label/source/equivalent; and deterministic Rust/Node/Python
  evidence.
- Not Yet Done: complete campaign facility taxonomy, asset-registry coverage,
  screenshots, save/load/replay continuity, performance/compatibility, and
  human quality review.
- Deferred / Non-Goals: no new asset, host authority, simulation rule,
  stochastic input, hidden-state projection, rival facility detail, history,
  replay, or external network path.

### Visual/audio Phase 11.1 live operational-overlay binding (v0.12.90)

- Status: In progress; directly visible live operational conditions now carry
  optional catalog bindings, while full campaign overlay coverage remains
  incomplete.
- Done: host-shaped bindings for nonzero unmet demand, active capital projects,
  reported financial distress, community-trust watch status, and explicit
  uncertain/stale intelligence; raw metric preservation; catalog resolution;
  generic fallback; source/equivalent text; and deterministic Rust/Node/Python
  evidence.
- Not Yet Done: remaining event/history/debrief/save-load/replay continuity,
  full overlay taxonomy, screenshots, performance/compatibility validation,
  asset-quality review, and human quality evaluation.
- Deferred / Non-Goals: no new assets, audio, simulation mechanism, stochastic
  input, hidden-state projection, rival detail, command, history, replay hash,
  or client authority change.

### Contributor documentation information architecture (v0.12.32)

- Status: Closed; implementation and verification complete
- Started: 2026-07-20
- Branch: `codex/docs-information-architecture`

  Done:
  - Added equal software, design/research, and validation routes from one
    `docs/README.md` landing page while preserving the canonical proposal,
    roadmap, design-principles, and harness paths.
  - Moved current guidance into purpose-based directories and all 85 playtest
    plus 15 visual/audio evidence records into indexed history cohorts without
    changing their conclusions.
  - Consolidated current AI-agent guidance and reusable historical human-session
    guidance into one active validation protocol.
  - Added a dependency-free CI check for broken repository-local Markdown links
    and machine-local filesystem paths.

  Verification:
  - Exactly four Markdown files remain at the `docs/` root; the checker passes
    across 258 Markdown files; release metadata and the 14-phase visual/audio
    contract audit pass.
  - All 318 Python tests pass with the bundled Python/Node runtimes.
  - Rust formatting, Clippy, 328 library tests, and all integration, golden,
    scenario-selection, and doc-test targets pass.

  Deferred / Non-Goals:
  - No runtime, simulation, scenario, command, stochastic, history/hash/replay,
    debrief, GUI, calibration, policy-validity, or research-conclusion change.
  - No redirect stubs for old external document URLs.

## Present

The Phase 1.3 audio direction standards and policy fixture proof are complete
through v0.12.38. Broader production and human or educational evaluation remain
separately gated Future work.

## Future

### Visual and audio experience upgrade

Source: [`docs/history/initiatives/visual-audio/visual-audio-upgrade-proposal.md`](docs/history/initiatives/visual-audio/visual-audio-upgrade-proposal.md)
Status: Bounded technical sequence closed at v0.12.30 and local competitive
transport repaired at v0.12.31; human evaluation and explicit non-goals remain
separately gated Future work.
No later feature should be read as implemented merely because the current `gui/`
prototype or Phase 6–10 documents exist.

#### Existing foundation (`Done`)

- The deterministic Rust engine, explicit resolved stochastic inputs,
  actor-visible observations, canonical commands, immutable history, replay
  hashes, CLI, bounded MCP adapter, and educational debrief surfaces exist.
- The dependency-free `gui/` surface renders typed actor-visible data,
  competitive action/resolution, regional-world, and bounded campaign-coverage
  workflows with optional generated audio, plus Phase 8 onboarding, local
  settings/recovery, allowlisted testplay capture/diagnostics, and a
  non-authoritative repeated-capture analyzer/decision log, plus Phase 10
  keyboard navigation, status language, text scaling, and cue-explanation
  controls, Phase 11 session launch/load, the Phase 12 visual identity catalog,
  and the Phase 13 first-month continuity rail on merged `main`. The v0.12.30
  contract audit closes the bounded technical sequence. It remains a thin
  client and is not the campaign-complete GUI described here.

#### Phase 0 alignment (`Done`)

- The browser-native presentation stack, host/MCP authority boundary, one-month
  competitive experience, current actor-visible source inventory, preliminary
  wireframe, audio catalog, asset policy, and hidden-state exclusions are
  recorded in `docs/history/initiatives/visual-audio/visual-audio-phase0-alignment-v0.12.16.md`.
- ADR-0011 accepts semantic HTML/CSS/ES modules plus native SVG for the initial
  client and keeps optional future audio playback outside the simulation core.
- Phase 0 acceptance does not promote structured DTOs, live actions, animation,
  audio playback, assets, or later campaigns.

#### Phase 1 static executive desktop (`Done`)

- `gui/` now renders a responsive fixture-driven executive desktop with header
  metrics, briefing, regional system cards, selected detail/facilities,
  contextual action previews, pending processes, monthly result, history, and
  debrief.
- Entity-card selection changes presentation detail only. Existing
  `HsMgtGameAdapter.submitTurn` remains the only non-empty command submission
  path, and live envelopes without the fixture still render through fallback
  contracts.
- The fixture and tests expose finance, workforce, capacity, access, quality,
  and public rival information while labeling private activity unavailable.
- Phase 1 remains a static information-architecture prototype; it does not
  establish live DTO parity, human usability, or polished visual design.

#### Phase 2 live read-only integration (`Done`)

- The MCP host now exposes a versioned `competitive-read-only-v1` projection
  through non-mutating `get_presentation` for live or recorded adapter use.
- The projection contains actor-visible session/resources/observation fields,
  player capacity/facility detail, public signals and information gaps, pending
  processes, committed transition summaries, state hashes, and replay metadata.
- Rust serialization tests exclude legal commands, true world state, effect
  queues, event metadata, resolved stochastic inputs, private rival actions,
  and non-observation flags; repeated reads preserve the session.
- The browser read-only client renders the typed envelope and explicit loading,
  empty, missing, adapter-error, and unsupported-schema states without calling
  `submitTurn`. Phase 2 did not establish human usability or replay playback.

#### Phase 3 contextual action submission (`Done`)

- The MCP host exposes `competitive-actions-v1` and
  `competitive-validation-v1` through non-mutating catalog/validation tools
  for `hold`, `invest`, `recruit`, `monitor`, `negotiate`, `commit`, and
  `project`.
- The browser action adapter renders generic forms from the host catalog,
  maintains local draft add/revise/remove state, previews canonical command
  text, displays host-returned exact costs and descriptive timing/uncertainty/
  constraint metadata, and submits only unchanged valid batches.
- Invalid validation and rejected submission are recoverable without replacing
  the current session; existing parser, batch validator, action costs, and
  `submit_turn` remain authoritative. No local formula or GUI-only command was
  added.
- Phase 3 is documented in
  [`docs/history/initiatives/visual-audio/visual-audio-phase3-contextual-actions-v0.12.19.md`](docs/history/initiatives/visual-audio/visual-audio-phase3-contextual-actions-v0.12.19.md).
  Static contracts and Rust tests are technical evidence only; no human
  usability, accessibility, learning, calibration, or policy-validity claim
  follows.

#### Phase 4 resolution and causal feedback (`Done`)

- The MCP host exposes `competitive-resolution-v1` through non-mutating
  `get_resolution`, selecting the latest committed competitive transition or
  an immutable historical turn.
- The envelope contains eight ordered, source-labeled steps: submitted batch,
  visible responses, process advancement, operating result, resource changes,
  direct committed effects, newly visible information, and updated pending
  processes.
- Before/after resources and operations are derived from actor-visible
  projections. Direct effects reuse committed transition summaries; the
  browser does not infer causal graphs, reveal hidden state, or calculate
  outcomes.
- The browser renders the complete textual result immediately and adds local
  play/pause/skip/review pacing, historical loading, state-hash display, and
  reduced-motion behavior without mutating the session.
- Phase 4 is documented in
  [`docs/history/initiatives/visual-audio/visual-audio-phase4-resolution-causal-v0.12.20.md`](docs/history/initiatives/visual-audio/visual-audio-phase4-resolution-causal-v0.12.20.md).
  Technical/interface-task checks do not establish human comprehension,
  usability, lived accessibility, learning, engagement, calibration, balance,
  domain validity, or policy validity.

#### Phase 5 foundational audio (`Done`)

- The browser exposes `audio-catalog-v1` with four visible-state music modes and
  all Phase 0 interface/event cue IDs, each with a source and visual/text
  equivalent.
- Generated Web Audio recipes are selected only from explicit page stage,
  actor-visible observation, committed resolution text/effects, or explicit
  local UI outcomes. Private rival behavior, true state, stochastic inputs, and
  effect queues are unavailable to the classifier.
- Master, music, interface, event, and ambience controls are independent;
  mute, focus loss, reduced notifications, repeated-cue throttling, user-gesture
  enablement, and unsupported-audio fallback preserve complete visual/text play.
- A machine-readable registry and credits record project-generated ownership
  and the absence of third-party audio files. Recording-sink tests verify cue
  IDs/source/equivalent without loading assets.
- Phase 5 is documented in
  [`docs/history/initiatives/visual-audio/visual-audio-phase5-foundational-audio-v0.12.21.md`](docs/history/initiatives/visual-audio/visual-audio-phase5-foundational-audio-v0.12.21.md).
  Technical/interface-task checks do not establish human comprehension,
  usability, lived accessibility, learning, engagement, calibration, balance,
  domain validity, or policy validity.

#### Phase 6 persistent regional world (`Done`)

- The host exposes `competitive-regional-world-v1` through the non-mutating
  `get_regional_world` read for `competitive-regional-v1` sessions.
- The envelope contains stable schematic entities, owned player facilities and
  processes, actor-visible demand/access/unmet-demand/capacity overlays,
  source/equivalent labels, navigation targets, replay metadata, and explicit
  missingness.
- Public rivals expose identity and public action signals only through the
  existing one-month observation lag. Private rival operations, facilities,
  resources, projects, true coordinates, effect queues, and hidden state are
  excluded by construction and tests.
- The browser renders the host projection as a selectable schematic map with
  detail, overlays, and keyboard-reachable links to existing briefing/detail/
  timeline surfaces. Empty, unsupported, and adapter-error paths preserve the
  base presentation and do not submit commands.
- Phase 6 is documented in
  [`docs/history/initiatives/visual-audio/visual-audio-phase6-regional-world-v0.12.22.md`](docs/history/initiatives/visual-audio/visual-audio-phase6-regional-world-v0.12.22.md).
  Technical/interface-task checks do not establish human comprehension,
  usability, lived accessibility, learning, engagement, calibration, balance,
  domain validity, or policy validity.

#### Phase 7 campaign coverage (`Done`)

- The host exposes `campaign-coverage-v1` through the non-mutating
  `get_campaign_coverage` read for `stabilization-v1` and
  `regional-affiliation-v1` sessions.
- Stabilization retains its onboarding-oriented five-turn executive loop with
  visible reports, stage-specific commands, uncertainty, immutable history, and
  existing educational debrief output.
- Affiliation retains its partner/fit/obligation semantics with condition,
  posture, commitments, review, labor/payer/community responses,
  integration/decline, explicit actors, and campaign-specific debrief output.
- Shared browser primitives render each coverage field with source labels,
  host-shaped parameter forms, recoverable rejection, keyboard/reduced-motion
  text completeness, history/replay metadata, and terminal debrief content.
- Existing generated audio maps only visible campaign pressure, completion, and
  affiliation milestone events; audio remains optional and outside state,
  history, hashes, replay, and transitions.
- Phase 7 is documented in
  [`docs/history/initiatives/visual-audio/visual-audio-phase7-campaign-coverage-v0.12.23.md`](docs/history/initiatives/visual-audio/visual-audio-phase7-campaign-coverage-v0.12.23.md).
  Technical/interface-task checks do not establish human comprehension,
  usability, lived accessibility, learning, engagement, calibration, balance,
  domain validity, policy validity, or legal validity.

#### Product contract (`Done for bounded technical sequence`)

- Make `competitive-regional-v1` the first target and preserve the executive,
  turn-based perspective. The player allocates attention, resources, workforce,
  payer and policy posture, commitments, and long-term strategy rather than
  managing individual patients or workers.
- Extend the implemented schematic regional world so facilities, systems,
  rivals, demand zones, workforce markets, payer/policy influence, projects,
  commitments, and delayed processes have visible institutional homes without
  implying unsupported geography or private knowledge.
- Reduce command-entry and onboarding friction without simplifying simulation
  rules. Contextual graphical actions must preview and submit the same canonical
  commands accepted by CLI/MCP and must never promise stochastic outcomes.
- Make direct, committed causal attribution, pending effects, observation-time
  information, realized results, revisions, and unavailable information easy to
  distinguish. Do not invent inferred causal graphs or false precision.
- Use visual and audio feedback to communicate category, direction,
  significance, and timing without collapsing organizational outcomes, actor
  utility, social welfare, or decision quality into a universal good/bad signal.
- Support screenshots, demonstrations, remote AI-agent testplay, later replay
  visualization, campaign-specific identity, possible instructor/analyst views,
  localization, and accessibility as bounded follow-ups after the first slice.

#### Intended experience and screen surfaces (`Done for bounded first month`)

- A responsive executive desktop for typical laptop and desktop widths with:
  a resource/status header; regional market view; executive briefing; selected
  institution/facility detail; contextual actions; pending-process timeline;
  monthly result view; causal overlays; replay; and debrief. Mobile is not a
  first-release requirement.
- The header must expose actor-visible date/stage, cash, monthly margin, action
  points, political capital, workforce/community trust, strategic alerts, and
  save/session status where the campaign provides them.
- Briefing items must cover major risks, changes, decisions, delayed reports,
  rival intelligence, policy developments, and advisor recommendations and link
  to their relevant entity or process.
- Inspectable entities must use actor-visible capacity, treated volume, unmet
  demand, quality/access, workforce, game-unit finance, payer pressure,
  projects, commitments, events, and legal actions. Plain-language bottleneck
  interpretations must derive only from visible observations.
- Contextual action surfaces must support the commands relevant to a selected
  facility, payer, competitor, policy process, or affiliation partner; expose
  AP/cash/political-capital costs, delays, constraints, and uncertainty; allow
  batch revision/removal; and show canonical command previews.
- The pending-effects timeline must cover recruitment, capital/technology
  work, annual policy events, contract and regulatory milestones, affiliation
  stages, delayed reports, and prior commitments when present.
- Monthly resolution must sequence submitted actions, visible responses,
  process advancement, operating results, resource and outcome changes, newly
  visible information, and updated pending processes. It must be skippable,
  pausable, reviewable, reduced-motion compatible, and replayable without a
  state transition.
- Causal overlays must begin with direct committed effects and documented
  presentation formulas for operating drivers, access, workforce, capacity,
  projects, and other supported outcomes. Replay/debrief must preserve what was
  knowable at decision time and may expose hashes, action/observation history,
  consequence chains, advisor comparison, and strategy summaries.

#### Visual and motion language (`Done for generated bounded vocabulary`)

- Use a serious, inviting, contemporary institutional style: information-rich
  without becoming a generic card dashboard or retro city-builder imitation.
- Give each health system a consistent emblem/icon, restrained color identity,
  facility markers, and cross-screen identity. Never rely on color alone.
- Represent stable, watch, constrained, critical, improving, uncertain,
  delayed, and revised states with text plus icon, shape, or pattern.
- Use animation only to explain committed visible changes such as recruitment,
  project progress, demand/capacity movement, review stages, affiliations, month
  transitions, and changed causal contributors. Keep it brief and skippable.

#### Presentation and action boundary (`Done`)

- Establish stable serializable, actor-visible DTOs or equivalent adapter
  contracts for campaign summary, regional map, institutions, facilities,
  briefing, action catalog/preview, pending processes, monthly resolution,
  causal attribution, debrief, and audio presentation events.
- Keep client navigation, selection, draft action batches, animation, audio,
  and local settings non-authoritative. The core or existing host boundary owns
  command legality, stochastic resolution, transitions, history, and hashes.
- Validation rejection must leave simulation state unchanged. Presentation
  changes, animation, and audio must leave commands, replay artifacts, histories,
  outcomes, and golden hashes unchanged.
- Missing, delayed, uncertain, revised, or hidden information must be explicit;
  the client must not guess, query private state, duplicate formulas, create
  GUI-only rules, or resolve randomness.
- The technology stack remains a Phase 0 decision. Do not introduce deployment,
  browser-hosting, networking, or generalized GUI platform conventions before
  the first slice proves their need.

#### Audio system (`Done for optional generated presentation`)

- Provide independently controlled music, interface/notification effects, and
  ambience/event effects with master, per-channel, mute, unfocused-mute,
  reduced-notification, and persistent-setting controls.
- Start browser audio only after user interaction and keep complete play
  possible when muted. Every audio-signaled event needs a visual/textual
  equivalent; spoken or broadcast content needs labels or subtitles.
- Begin with loopable menu, stable-operations, pressure, and debrief music.
  Later visible-state mappings may distinguish workforce strain, regulatory
  scrutiny, competition, and affiliation. Crossfades and classifications must
  derive deterministically from visible conditions or campaign stage.
- Provide restrained UI cues for confirm/reject, add/remove action, submit,
  month advance, report receipt, save, and useful focus changes; and event cues
  for project, staffing, operating, payer, regulatory, rival, community,
  affiliation, and revised-information events supported by visible committed
  history.
- Optional ambience must avoid sensational clinical distress, alarms,
  resuscitation, or sirens as entertainment. Playback paths, volume, and assets
  stay outside the simulation; replay may regenerate cues from committed visible
  history without recording playback in simulation history.

#### Assets, licensing, and accessibility (`Done for generated provenance and accessibility contract`)

- Prefer CC0/public-domain, manageable CC BY, or individually reviewed
  permissive game-asset licenses. Reject unclear, personal-use-only,
  noncommercial-only, redistribution-hostile, or copyright-claim-prone assets.
- Maintain a machine-readable registry with stable ID, release path, type,
  title, creator, source, retrieval date, license and URL, modifications, and
  original/release hashes. Generate or support `ASSET_CREDITS.md`, in-game
  credits, audit, and replacement. Keep originals outside the release tree or
  in an explicitly adopted large-file store; keep optimized release assets and
  provenance text under documented paths.
- Establish coherent original art direction through license-compatible
  recoloring, cropping, simplification, line weight, perspective, and resolution
  normalization rather than accumulating visually inconsistent assets.
- From the first slice, support sufficient contrast, readable scaling/zoom,
  labels plus icons, keyboard navigation, semantic labels, color-independent
  status, reduced motion, no essential hover-only content, complete mute,
  independent audio channels, and non-spatial/non-pitch-only cues.
- Keep terminology consistent with canonical docs; explain game units, costs,
  delays, and uncertainty; separate current decisions from retrospective
  explanation; and allow skipped resolution to be reviewed.

#### Evidence-gated development sequence (`Done for bounded technical phases 0–13`)

| Phase | Bounded output | Promotion/exit gate |
| --- | --- | --- |
| 0. Product and architecture alignment | Interface boundary, one-month experience spec, DTO inventory, wireframes, audio catalogs, asset policy, stack/ADR decisions | No client-owned simulation state; every first-slice action is canonical; every value and audio cue has a visible source |
| 1. Static executive desktop | Navigable injected-data desktop, responsive layout, design tokens, entity/status language, initial icons | AI review profiles locate finance/workforce/capacity/access/rival information without raw JSON; hidden-state and viewport checks pass |
| 2. Live read-only integration | Typed live/recorded adapter, observations, entity detail, pending/history/hash views, replay prototype, loading/error/empty states | CLI/MCP visible-fact parity, no duplicated formulas, stable fixtures, and explicit missingness |
| 3. Contextual action submission | Action forms/batch builder, command preview, validation/retry, one graphical competitive month | Generated commands are equivalent, costs/delays are visible, rejection is non-mutating, and no stochastic certainty is implied |
| 4. Resolution and causal feedback (`Done`) | One committed month, typed sequencing, operating breakdown, source-labeled direct effects, skip/pause/review/historical read | Principal drivers are traceable to committed effects; textual results are immediate; historical reads are non-mutating |
| 5. Foundational audio (`Done`) | Four music states, bounded UI/event cues, controls, generated-audio registry/credits, deterministic cue mapping | Audio leaves state/hash/replay unchanged, muted play is complete, music leaks no hidden state, provenance is complete, repeated cues are restrained |
| 6. Persistent regional world (`Done`) | Actor-visible schematic map, demand/access overlays, identities, lagged public rival signals, navigation, owned facilities/processes, and explicit missingness | Host/browser contracts pass; map supports decisions/explanations, respects rival observation lag, and decorative complexity does not obscure state |
| 7. Campaign coverage | Tutorial-oriented stabilization flow and affiliation partner/fit/commitment/review/integration flow with shared plus campaign-specific visuals/audio | Components are reused without flattening campaign semantics or requiring GUI-driven simulation changes |
| 8. AI-agent testplay readiness | Onboarding, settings, accessibility/error recovery, AI roles/tasks, UI/event/cue/replay capture, structured diagnostics | Agents complete declared tasks and exercise mute, reduced-motion, keyboard, rejection, and recovery paths; claim classes remain separate |
| 9. AI-agent evaluation and revision | Reproducible multi-role/seed/mode findings, prioritized revisions, product decision log | Decisions cite captured traces; interpretation mismatches are hypotheses; human usability, engagement, lived accessibility, learning, and expert validity remain unclaimed |
| 10. Accessibility and visual-language hardening | Keyboard landmarks, non-color status vocabulary, local text scaling, and optional cue-explanation control | Static semantic, settings, responsive, reduced-motion, and boundary checks pass without changing host state or claiming lived access |
| 11. First-session launch/load boundary | Host-authoritative competitive session start/load handoff into the existing first-month presentation | Start/load calls map to the existing host session contract, malformed/failed responses recover, and no transition or local simulation is introduced |
| 12. Visual identity and marker provenance | Generated system identities, facility/metric/process markers, explicit generic fallback, and machine-readable visual registry | Known and unknown visible entities render stable semantic tokens, provenance is complete, and no host/simulation boundary changes |
| 13. First-month continuity | Local text-first path rail and adapter-driven launch-to-refresh handoff evidence for one competitive month | Stage order is deterministic, two-draft review is visible, confirmed host handoffs reach continue, and failures do not advance or mutate state |

Phase 7 is closed only for the bounded stabilization and affiliation coverage
slice; broad campaign, map, and asset production remain explicit non-goals. The
audit at
[`docs/history/initiatives/visual-audio/visual-audio-first-month-contract-v0.12.30.md`](docs/history/initiatives/visual-audio/visual-audio-first-month-contract-v0.12.30.md)
closes the technical Phase 0–13 sequence with source/test evidence. Human and
educational evaluation remain separately gated and are not implied by this
closure.

#### First competitive vertical slice (`Done for technical/interface-task evidence`)

The first polished implementation is exactly one month of
`competitive-regional-v1`:

1. Start or load a campaign and inspect the regional market, Riverside, and its
   facilities.
2. Identify one actor-visible workforce or capacity bottleneck and inspect
   recent payer/rival information.
3. Choose at least two contextual actions; review canonical commands, costs,
   constraints, uncertainty, and delays; revise if needed; then submit.
4. Watch or skip resolution and inspect updated volume, unmet demand, revenue,
   cost, margin, pending processes, and direct causal attribution.
5. Receive restrained music/event cues with complete visual equivalents and
   continue to the next actor-visible observation.

Initial assets are limited to three system identities; facility, demand,
capacity, project, staffing, payer/policy, and timeline markers; a schematic
map; status/severity language; four music tracks; eight UI sounds; eight event
sounds; and at most two optional ambience loops. The current implementation
uses project-generated glyphs/CSS and generated Web Audio recipes with explicit
registry/credits; no third-party release assets are required for this bounded
closure.

#### Verification and AI testplay (`Done for technical/proxy evidence; human evaluation deferred`)

- Architecture: presentation DTO use, hidden-field exclusion, canonical action
  mapping, rejection atomicity, visible-only cue/mood derivation, and unchanged
  golden hashes/replays.
- Rendering: static contracts cover normal, empty, missing, uncertain, delayed,
  revised, long-text, and reduced-motion states; real viewport rendering and
  contrast measurement remain unresolved browser/human questions.
- Audio: event/cue and visible-state/music mappings, mute and independent
  channels, focus behavior, reduced notifications, repetition throttling, and
  missing-asset fallback through a recording sink or equivalent.
- Accessibility: keyboard paths, semantic structure, color-independent status,
  reduced motion, text scaling, complete muted play, and textual cue
  equivalence have static/Node coverage; contrast, screen-reader behavior, and
  lived access remain unresolved.
- AI-agent testplay: Phase 8/9 covers declared roles, tasks, seeds, settings,
  recovery, visible events, commands, histories, hashes, and deterministic
  artifact diagnostics. Browser automation, screenshots, model/network
  orchestration, and human interpretation remain outside this closure.
- Classify evidence separately as technical correctness, interface-task proxy,
  strategic trace, document-grounded domain consistency, or unresolved human
  question. AI testplays do not prove human usability, engagement, accessibility
  lived experience, learning, classroom effectiveness, domain-expert validity,
  calibration, balance, or policy validity.

#### Contributor boundaries and risk controls

- Product/UX owns information architecture, wireframes, onboarding, action
  flow, and resolution pacing; visual design owns maps, icons, identity, motion,
  and visual accessibility; front-end work owns client state, adapter use,
  rendering, settings, audio playback, and UI tests.
- Rust/interface work owns only justified actor-visible projections, DTO/adapter
  contracts, canonical validation integration, and replay/debrief access. Audio
  work owns cue taxonomy, selection, normalization, mixing, and playback rules;
  asset governance owns license review, registry, credits, source retention, and
  release optimization; AI-testplay work owns roles, protocols, capture,
  comparison, triage, and evidence classification.
- Prevent a parallel engine with hidden-field exclusion, command-equivalence,
  rejection-atomicity, and unchanged-hash tests. Prevent dashboard-only polish
  by promoting causal overlays and process timelines before decorative assets.
- Prevent city-builder scope by requiring each map element to support a decision
  or explanation. Prevent fatigue and hidden-state leakage with visible-only
  mappings, throttling, independent controls, and repeated-session tests.
- Prevent license and accessibility debt by making registry completeness and
  first-slice accessibility checks phase gates. Prevent campaign flattening by
  sharing primitives without sharing incompatible semantics.

#### Track-level success and stop rules

The track may be considered technically successful when intended players can
act without command syntax in the designed interface; major pressures, pending
effects, monthly consequences, and visible causal chains have explicit homes;
graphical commands remain canonical; audio remains optional and restrained;
observation/replay boundaries hold; and diverse AI-agent profiles complete and
replay declared tasks across seeds and accessibility modes with reproducible
artifacts.

Rendering alone, passing automation alone, one successful AI profile, polish,
or subjective AI commentary is insufficient. Stop or narrow the phase when it
requires simulation changes solely for presentation, exposes hidden state,
duplicates formulas, lacks asset rights, makes audio essential, or cannot be
verified without claiming human experience.

#### Deferred / Non-goals

- No simulation rewrite, browser-owned state, GUI-only command or rule, hidden
  outcome calculation, real-time core, network multiplayer, city/patient or
  hospital-interior simulation, individual-worker placement, general visual
  scenario editor, or production deployment platform.
- No initial mobile requirement, dynamic music composition, broad inferred
  causal graph, detailed geography, large asset pipeline, or forced common
  screen metaphor across campaigns.
- Instructor/analytic true-state views must remain a later, separately
  authorized mode and must never weaken standard-player historical information
  boundaries.
- Human usability, engagement, lived accessibility, domain-expert review, and
  educational evaluation are deferred until separately funded; AI testplay is
  the development validation method, not a substitute claim.

The v0.11.0 operating loop, v0.11.2 explainability audit, v0.11.3
month-specific debrief linkage, v0.11.4 post-fix validation, and v0.11.5
operating-outcome use audit are the current gameplay-maturity baseline.
Before adding actors, commands, service lines, or platform layers, validate it
with AI strategy archetypes across seeds and rival
configurations. Required diagnostics
are effect attribution, monthly bottlenecks, unused or dominated actions,
trajectory diversity, low-influence state variables, stable marginal effects,
and threshold cliffs. Runtime changes require a concrete unexplained gap.

Shared contested mechanics remain gated. Contested hiring, demand diversion,
scarce shared resources, coalition conflicts, or multi-party negotiations must
first introduce a three-stage resolver: evaluate intentions against one prior
snapshot, centrally resolve conflicts, then apply effects. Existing
permutation-invariance tests remain mandatory but are not by themselves proof
for future shared mutations.

Routine project governance should update the four canonical layers—product
thesis, architecture/invariants, current mechanics, and evidence/validation—at
coherent feature boundaries. Dated findings and ADRs remain historical records;
they do not each require a new runtime release or synchronized ceremony.

### Promotion rules

Before any Future item moves into `Present`, the new Present entry must name:

- the roadmap phase or gate it satisfies;
- the evidence source, proposal review, AI-agent testplay finding, domain QA note, or
  release need that justifies promotion;
- the narrow artifact or runtime behavior being changed;
- verification criteria needed before the slice can close; and
- explicit non-goals that keep adjacent Future tracks out of scope.

Major architecture, scenario-generalization, documentation-taxonomy, GUI, MCP,
or release-automation work remains frozen by default. Permit it only when a
AI-agent testplay, authoring, QA, debrief, audience-access, or release-readiness finding
names a concrete need that current structures cannot meet.

### Ranked next-development queue

1. The bounded visual/audio technical sequence is complete at v0.12.30 and its
   local competitive transport gap is repaired at v0.12.31. Do not
  promote another presentation runtime item without a new source-backed gap;
  use the contract audit as the reopening gate.
2. Human usability, lived accessibility, learning, engagement, calibration,
  balance, policy validity, and domain-expert evaluation remain separately
  gated Future work.
