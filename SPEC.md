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
  - Extended `docs/expansion-proposal-review.md` with evidence limits, fixture
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
  - Added `docs/playtest-findings-v0.10.37.md` and updated the MCP playtesting
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
  - Added `docs/playtest-findings-v0.10.36.md` with the design intent, tier
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
  - Added `docs/playtest-findings-v0.10.35.md` with the current difficulty
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
  - Added `docs/playtest-findings-v0.10.34.md` with a facilitation sequence,
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
  - Added `docs/playtest-findings-v0.10.33.md` with growth/capacity signals,
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
  - Added `docs/expansion-proposal-review.md` with proposal-review posture,
    source links, recommended gates, design implications, risks, and promotion
    rules.
  - Updated `docs/roadmap.md` with a Phase 7 expansion proposal review gate and
    Phase 9 routing for difficulty depth, regional consolidation, and GUI
    thin-client work.
  - Propagated future-boundary guidance into `ARCHITECTURE.md`,
    `docs/design_principles.md`, `docs/competitive-scenario-brief.md`,
    `docs/system-boundary.md`, `docs/scenario-format-draft.md`, and
    `docs/evidence-registry.md`.
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
  - Added `docs/playtest-findings-v0.10.30.md` with workforce-protective
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
  - Added `docs/playtest-findings-v0.10.29.md` with a compact comparison table,
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
  - Added `docs/playtest-findings-v0.10.28.md` with cross-run strategy-space
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
  - Added `docs/playtest-findings-v0.10.27.md` with prompts for public
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
  - Added `docs/playtest-findings-v0.10.26.md` comparing the recent live
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
  - Added `docs/playtest-findings-v0.10.25.md` summarizing the live-capture
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
    `docs/playtest-findings-v0.10.24.md`.
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
  - Added `docs/playtest-findings-v0.10.22.md` comparing the Live Access
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
  - Added `docs/playtest-findings-v0.10.21.md` summarizing the live evidence
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
  - Added `docs/playtest-findings-v0.10.20.md` summarizing the v0.10.17-v0.10.19
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
  - Added `docs/playtest-findings-v0.10.19.md` and updated the MCP playtesting
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
  - Added `docs/playtest-findings-v0.10.18.md` and updated MCP docs.
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
  - Added `docs/playtest-findings-v0.10.17.md` and updated
    `docs/mcp-playtesting-guide.md`.
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
  - Added `docs/playtest-findings-v0.10.16.md`.
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
  - Added `docs/playtest-findings-v0.10.15.md` and updated the MCP playtesting
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
  - Added `docs/playtest-findings-v0.10.14.md` and updated the MCP playtesting
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
  - Added `docs/playtest-findings-v0.10.13.md` and updated the MCP playtesting
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
  - Added `docs/playtest-findings-v0.10.12.md` and updated the MCP playtesting
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
  - Added `docs/playtest-findings-v0.10.11.md` and updated the MCP playtesting
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
  - Added `docs/playtest-findings-v0.10.10.md` and updated the MCP playtesting
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
  - Added `docs/playtest-findings-v0.10.9.md` and replay artifacts under
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
  - Added `docs/playtest-findings-v0.10.7.md` and replay artifacts under
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
  - Added `docs/playtest-findings-v0.10.5.md` with source matrix, synthesis
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
  - Added `docs/playtest-findings-v0.10.4.md` with command totals, endpoint
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
  - Added `docs/playtest-findings-v0.10.2.md` with variant definitions, command
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
  - Added `docs/playtest-findings-v0.10.1.md` with session matrix, outcome
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
  - Added `docs/playtest-findings-v0.10.0.md` with session matrix, outcome
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
  - Added `docs/playtest-findings-v0.9.9.md` documenting the completed targeted
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
  - Added `docs/playtest-findings-v0.9.8.md` documenting the completed targeted
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
  - Added `docs/playtest-findings-v0.9.7.md` documenting the completed targeted
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
  - Added `docs/playtest-findings-v0.9.6.md` documenting the completed batch,
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
  - Added `docs/playtest-findings-v0.9.5.md` documenting strategy-space
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
  - Added `docs/playtest-findings-v0.9.4.md` with session matrix, metric
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


## Present

None. All scheduled features are complete.


## Future

### Promotion rules

Before any Future item moves into `Present`, the new Present entry must name:

- the roadmap phase or gate it satisfies;
- the evidence source, proposal review, playtest finding, domain QA note, or
  release need that justifies promotion;
- the narrow artifact or runtime behavior being changed;
- verification criteria needed before the slice can close; and
- explicit non-goals that keep adjacent Future tracks out of scope.

Major architecture, scenario-generalization, documentation-taxonomy, GUI, MCP,
or release-automation work remains frozen by default. Permit it only when a
playtest, authoring, QA, debrief, audience-access, or release-readiness finding
names a concrete need that current structures cannot meet.

### Ranked next-development queue

The first runnable prototype is complete enough that the next risk is not
engine proof. The next risk is whether repeated play remains explainable,
teachable, and strategically interesting before the project expands mechanics,
strategic actors, or platform architecture.

1. Track: Competitive teachability and validation loop
  Phase / Gate: Phase 7; proceed when existing or newly captured playtest
  evidence identifies one concrete comprehension, pacing, traceability, strategy
  comparison, or debrief-use issue.

  Next actionable slice:
  Preserve the evidence-only posture until a new artifact identifies a concrete
  comprehension, pacing, traceability, strategy-comparison, or debrief-use gap
  that the current observations, history, diagnostics, and debriefs cannot
  explain. Do not promote runtime work from the v0.10.44 synthesis alone.

  Verification target:
  Findings cite campaigns, seeds, difficulty, profiles/prompts, actor-visible
  observations, submitted commands, validation failures or retries, histories,
  debriefs, diagnostic summaries, evidence limits, and prioritized
  recommendations. Runtime or interface changes require focused tests, and the
  competitive seed-42 golden hash remains unchanged unless transition semantics
  intentionally change.

  Deferred / Non-Goals:
  No external human recruitment gate, formal human-subjects research process,
  measured human-learning claim, empirical calibration claim, scoring redesign,
  broad balance pass, multiplayer, new strategic actor class, or platform
  architecture expansion.

2. Track: Difficulty depth and winnability
  Phase / Gate: Phase 7/9; proceed only after the expansion proposal review and
  difficulty evidence identify one pressure dimension current tiers do not
  express.

  Next actionable slice:
  Design or test one visible difficulty dimension, such as rival resource
  access, information delay, monitoring depth, implementation capacity, or
  risk/aggression posture. Validate Expert difficulty as severe but winnable
  before changing default balance.

  Verification target:
  Findings cite seeds, profiles, difficulty tiers, validation failures or
  retries, final tradeoff metrics, rival pressure, and debrief traceability.
  Expert should show at least one clearable path without hidden omniscience or
  one locked optimal strategy.

  Deferred / Non-Goals:
  No broad balance pass, hidden rival omniscience, punitive player-resource cut,
  scoring redesign, runtime tuning from a single run, or difficulty claim from
  one profile/seed/campaign.

3. Track: Regional affiliation/acquisition slice
  Phase / Gate: Phase 7/9; proceed only after proposal review and domain QA
  approve one bounded US regional affiliation or acquisition scenario.

  Next actionable slice:
  Draft one regional affiliation/acquisition scenario design covering partner
  fit, regulatory review, community-benefit commitments, payer leverage, labor
  response, integration drag, capital access, service continuity, and
  access/quality consequences.

  Verification target:
  The design distinguishes organizational utility, actor incentives, social
  welfare, community effects, and educational evaluation. Legal/regulatory
  outcomes are labeled abstractions unless separately grounded.

  Deferred / Non-Goals:
  No national consolidation simulator, private-equity rollup model, detailed
  deal-financing system, calibrated antitrust forecast, multi-transaction
  strategy framework, or scenario-schema/runtime implementation before the
  design slice closes.

4. Track: GUI thin-client proof
  Phase / Gate: Phase 8/9; proceed only after audience-access, playtest, or
  review evidence shows a graphical surface would improve usability without
  weakening core inspectability.

  Next actionable slice:
  Prototype one GUI surface that consumes existing observations, command
  validation, history/replay, and debrief outputs. Complete an asset-license
  audit before distributing any downloaded pixel assets.

  Verification target:
  GUI work preserves CLI/MCP behavior, does not duplicate simulation state, and
  keeps rendering, input, assets, layout, and packaging outside the deterministic
  core. Asset manifests record source and license before distribution.

  Deferred / Non-Goals:
  No GUI-only scenario behavior, runtime semantics fork, release packaging
  commitment, non-audited assets, replacement of CLI/MCP, HTTP multiplayer,
  auth, or durable session persistence.

5. Track: Broader simulation breadth and strategic actors
  Phase / Gate: Phase 6/9; proceed only after playtest, instructor, scenario, or
  domain-review evidence shows current campaign limits block meaningful strategy
  or learning.

  Next actionable slice:
  Add one bounded breadth element, such as one service-line decision, one patient
  or distributional outcome category, one capital-allocation tradeoff, one
  market-area concept, one additional strategic interaction, or one localized
  Medicare/Medicaid actor interaction. A differentiated in-house advisor market
  is a gated candidate only after repaired state-conditioned advice proves
  insufficient for the desired decision-support and debrief value.

  Verification target:
  The new mechanism has a documented actor/observation boundary, deterministic
  tests, debrief attribution, and clear player-facing tradeoffs. Public-payer
  work must distinguish actor utility from social welfare and label
  evidence-backed mechanisms versus design abstractions. Advisor work must also
  show viable recurring-cost sensitivity across supported scenario cash scales,
  symmetric human/AI information and roster rules, and explicit arrivals and
  contested-hire inputs.

  Deferred / Non-Goals:
  Full US health-system model, individual patient simulation, broad federal
  policy lifecycle framework, national policy simulation, federal budget
  modeling, full Medicaid eligibility rules, Medicare payment reproduction,
  global equilibrium AI, speculative generalized frameworks, and broad
  scenario-authoring infrastructure.

6. Track: Release automation and contributor readiness
  Phase / Gate: Phase 0/8; proceed when contributor-readiness or release
  preparation becomes the active priority.

  Next actionable slice:
  Add one lightweight quality or release check with documented local command
  usage, starting with non-invasive checks before release packaging.

  Verification target:
  Local command passes, CI documentation is updated, and the change does not
  alter simulation behavior or require release conventions beyond
  `docs/versioning-policy.md`.

  Deferred / Non-Goals:
  No public release packaging, publication automation, data/licensing
  finalization, or broad repository restructuring.
