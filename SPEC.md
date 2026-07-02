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


### Recent slices

- Feature: Free-form agent playtest evidence
  Status: Complete
  Started: 2026-07-02
  Version: 0.1.54

  Summary:
  Run one bounded free-form `Free-Form First-Time Executive` profile through the
  existing MCP interface for both current campaigns, then record observations,
  legal-command hints, submitted commands, histories, debriefs, causal
  explanation, evidence limits, and follow-up recommendations.

  Done:
  - `docs/playtest-findings-v0.1.54.md` records one stabilization and one
    competitive free-form session at seed 42 with zero validation failures
  - The free-form stabilization run produced final cash 45, access 84,
    workforce trust 64, community trust 70, and hash `5beed26a91f1b739`
  - The free-form competitive run produced final cash 30, access 71, staffed
    beds 124, workforce trust 57, community trust 65, political capital 11, and
    hash `10c3060949fa8aa1`
  - `docs/mcp-playtesting-guide.md` documents the operator-run free-form
    evidence procedure
  - Package version bumped to `0.1.54`

  Deferred / Non-Goals:
  - No LLM runner, new playtest orchestration framework, transition behavior,
    ruleset, scenario schema, replay format, MCP DTO, campaign length, active
    observation surface, golden hash, balance tuning, or diagnostics platform
    changed
  - No human learning claim, empirical calibration claim, policy forecast claim,
    or formula tuning from one free-form simulated-agent profile

  Verification:
  - Free-form MCP profile completed both current campaigns at seed 42 without
    validation failures
  - Rust checks, scripted MCP regression batch, and diff checks completed for
    the slice

- Feature: Campaign test fallback fix
  Status: Complete
  Started: 2026-07-02
  Version: 0.1.53

  Summary:
  Fix competitive campaign tests so PTY-backed test runs use fallback input
  instead of blocking on interactive prompts.

  Done:
  - CLI stdin fallback detection treats unit tests like non-TTY input for the
    competitive preview loop
  - Package version bumped to `0.1.53`

  Deferred / Non-Goals:
  - No simulation behavior, scenario files, MCP contract, replay format, or
    golden hash changed

  Verification:
  - `cargo test` and `cargo fmt --check` pass on `main`

- Feature: Naive-profile playtest evidence
  Status: Complete
  Started: 2026-07-01
  Version: 0.1.52

  Summary:
  Extend the scripted MCP Phase 7 playtest batch with a deliberately simple
  `Naive First-Time` profile to test whether current command hints and
  observations support legal low-complexity completion beyond the three
  optimized scripted strategies.

  Done:
  - Automated playtest runner now executes Fiscal Caution, Capacity Growth,
    Balanced Strategy, and Naive First-Time profiles for both current campaigns
    across seeds 42, 43, and 44
  - `docs/playtest-findings-v0.1.52.md` records 24 completed scripted MCP
    sessions, naive-profile command choices, outcome comparisons, evidence
    limits, and follow-up recommendations
  - The naive profile completed all sessions without validation failures while
    preserving cash and underusing some access, community-trust, and competitive
    action-space opportunities
  - Package version bumped to `0.1.52`

  Deferred / Non-Goals:
  - No transition behavior, rulesets, scenario schemas, replay formats, MCP DTO
    shapes, active observation surfaces, campaign length, golden hashes,
    free-form agent orchestration, balance tuning, or diagnostics platform
    changed
  - No human learning claim, empirical calibration claim, policy forecast claim,
    formula tuning, or command-surface change from this scripted naive profile

  Verification:
  - Automated MCP naive-profile batch completed 24 sessions without validation
    failures
  - Rust checks and diff checks completed for the slice

- Feature: Seed-variation playtest evidence
  Status: Complete
  Started: 2026-07-01
  Version: 0.1.51

  Summary:
  Extend the scripted MCP Phase 7 playtest batch from the seed-42 baseline to a
  fixed seed matrix using the v0.1.50 competitive final metric debrief surface.

  Done:
  - Automated playtest runner now executes Fiscal Caution, Capacity Growth, and
    Balanced Strategy profiles for both current campaigns across seeds 42, 43,
    and 44
  - Script output now prints per-seed comparison rows and compact metric ranges
    for stabilization and competitive preview outcomes
  - `docs/playtest-findings-v0.1.51.md` records 18 completed scripted MCP
    sessions, seed-sensitivity observations, evidence limits, and follow-up
    recommendations
  - Package version bumped to `0.1.51`

  Deferred / Non-Goals:
  - No transition behavior, rulesets, scenario schemas, replay formats, MCP DTO
    shapes, active observation surfaces, campaign length, golden hashes, free-
    form agent profile, naive profile, balance tuning, or diagnostics platform
    changed
  - No human learning claim, empirical calibration claim, policy forecast claim,
    or formula tuning from this scripted seed matrix

  Verification:
  - Automated MCP seed-variation batch completed 18 sessions without validation
    failures
  - Full Rust checks and diff checks completed for the slice

- Feature: Competitive final debrief metrics
  Status: Complete
  Started: 2026-07-01
  Version: 0.1.50

  Summary:
  Close the v0.1.49 competitive evidence gap by adding bounded final player
  tradeoff and resource metrics to the competitive MCP `end_session` debrief.

  Done:
  - Competitive MCP debrief now reports final human-system cash, access,
    quality, workforce trust, community trust, market share, political capital,
    active projects, active project monthly draws, and staffed beds from
    committed history
  - Automated playtest summaries now parse competitive final metrics from the
    MCP end-session debrief
  - Focused MCP session tests cover completed-session metric reporting and keep
    rival organization names out of the final metric lines
  - MCP playtesting and interface docs describe the end-session metric surface
  - Package version bumped to `0.1.50`

  Deferred / Non-Goals:
  - No transition behavior, rulesets, scenario schemas, replay formats, MCP DTO
    shapes, active observation surfaces, campaign length, golden hashes, or
    gameplay formulas changed
  - No seed-variation batch, free-form agent profile, human learning claim,
    empirical calibration claim, policy forecast claim, balance tuning, or
    diagnostics platform

  Verification:
  - MCP session tests cover the new competitive final debrief metrics
  - Full Rust checks and diff checks completed for the slice

- Feature: AI-agent playtest evidence
  Status: Complete
  Started: 2026-06-30
  Version: 0.1.49

  Summary:
  Fix the automated MCP playtest harness enough to complete the active Phase 7
  default scripted-policy batch, then record versioned findings for the current
  stabilization and competitive preview campaigns.

  Done:
  - Automated playtest policies now keep stabilization command selection on the
    stabilization legal-command surface after Turn 1
  - MCP Python client now launches the built stdio server by default, uses
    byte-level response reads, and reports scripted validation failures instead
    of looping silently
  - `docs/playtest-findings-v0.1.49.md` records six completed seed-42 sessions,
    gameplay-hypothesis results, rubric scores, evidence limits, and prioritized
    follow-up
  - Package version bumped to `0.1.49`

  Deferred / Non-Goals:
  - No runtime transition behavior, rulesets, scenario schemas, replay formats,
    MCP DTO shapes, campaign length, golden hashes, or gameplay formulas changed
  - No human learning claim, empirical calibration claim, policy forecast claim,
    balance tuning, or broad diagnostics platform

  Verification:
  - Automated MCP playtest batch completed for three profiles across both
    current campaigns
  - Rust checks and diff checks completed for the harness and docs slice

- Feature: Feedback-aligned future planning
  Status: Complete
  Started: 2026-06-30
  Version: 0.1.48

  Summary:
  Review external project feedback and translate it into docs-only future plans
  that prioritize gameplay validation, strategy-space diagnostics, debrief
  quality, one exemplary scenario, and model-confidence annotations before
  broad new architecture.

  Done:
  - Future tracks now foreground falsifiable gameplay hypotheses, diagnostic
    evidence, debrief QA, canonical scenario quality, evidence/confidence
    labeling, and abstraction-freeze gates
  - Agent-playtest protocol now asks findings to test explicit gameplay
    validity hypotheses and strategy-space diagnostics when relevant
  - Roadmap and architecture planning language now makes validation evidence the
    gate for broader scenario tooling, calibration, and platform expansion
  - Package version bumped to `0.1.48`

  Deferred / Non-Goals:
  - No runtime behavior, scenario schemas, rulesets, replay artifacts, MCP DTOs,
    golden hashes, or transition semantics changed
  - No strategy-space diagnostic implementation, new scenario loader,
    calibration pass, human learning claim, or policy-forecasting claim

  Verification:
  - Rust checks, markdown diff checks, stale-claim scan, and domain QA completed
    for the docs-only planning refresh

- Feature: AI-agent playtest validation pivot
  Status: Complete
  Started: 2026-06-30
  Version: 0.1.47

  Summary:
  Replace planned external human playtest recruitment with AI-agent and
  sub-agent playtests as the active Phase 7 validation path.

  Done:
  - Added `docs/agent-playtest-protocol.md` with required MCP evidence,
    profile matrix, rubric, synthesis template, and evidence limits
  - Added ADR-0009 accepting AI-agent playtests as the active validation path
  - Superseded the external human playtest protocol in active planning language
  - Package version bumped to `0.1.47`

  Deferred / Non-Goals:
  - No runtime behavior, scenario schemas, rulesets, replay artifacts, MCP DTOs,
    or golden hashes changed
  - No claim of measured human learning, empirical calibration, or policy
    forecasting validity from agent runs

  Verification:
  - MCP one-turn smoke test, Rust checks, markdown diff checks,
    stale-language scans, and domain QA completed for the docs-only pivot
  - Full `scripts/run_automated_playtests.py` was attempted twice and hung on
    the first stabilization batch `submit_turn`; script debugging remains
    outside this docs-only slice

- Feature: Deferred item triage
  Status: Complete
  Started: 2026-06-30
  Version: 0.1.46

  Summary:
  Review deferred items from completed Past records and archived slice history,
  then preserve still-worthy follow-up work in Future without carrying forward
  items that are complete, obsolete, or permanent non-goals.

  Done:
  - Future tracks now explicitly cover evidence and parameter-ledger work,
    instructor analysis and replay/export capabilities, competitive command
    ergonomics, and broader simulation breadth gates
  - Completed deferred items such as per-turn command entry, module split,
    CI baseline, replay artifact export, and competitive runtime I1-I8 were not
    re-added as Future work
  - Package version bumped to `0.1.46`

  Deferred / Non-Goals:
  - No runtime behavior, scenario schemas, rulesets, replay artifacts, MCP DTOs,
    or golden hashes changed
  - No Future track was promoted into `Present`

  Verification:
  - Deferred-item scan reviewed `SPEC.md` and `docs/spec-past-archive.md`
  - `cargo fmt --check` and markdown whitespace checks pass

- Feature: SDD next-development cleanup
  Status: Complete
  Started: 2026-06-30
  Version: 0.1.45

  Summary:
  Refresh the spec-driven-development index so the next development tracks are
  specific, gated, and verification-oriented while companion docs reflect the
  current bounded competitive preview, scenario-loader, and MCP interface state.

  Done:
  - `SPEC.md` Future now names actionable next slices with gates,
    verification targets, and deferred work
  - README status text summarizes current capabilities without repeating the
    full release history
  - Architecture, core-loop, roadmap, system-boundary, competitive-sketch, and
    CLI grammar docs no longer describe completed competitive runtime slices as
    only planned or design-only
  - Package version bumped to `0.1.45`

  Deferred / Non-Goals:
  - No runtime behavior, scenario files, schemas, replay artifacts, golden
    hashes, MCP DTOs, or test expectations changed
  - No active Future slice was promoted into `Present`

  Verification:
  - `cargo fmt --check` and `cargo test` pass
  - Stale status scan leaves only historical release/archive references

- Feature: Automated MCP playtest findings
  Status: Complete
  Started: 2026-06-28
  Version: 0.1.43

  Summary:
  Run automated MCP sessions across stabilization and competitive-preview
  campaigns and record findings for strategy diversity, winnability, tension,
  and entertainment value.

  Done:
  - `docs/playtest-findings-v0.1.42.md` summarizes three strategy runs across
    both current campaigns
  - `scripts/play_game.py` and `scripts/run_automated_playtests.py` support
    bounded MCP playtest sessions
  - Package version bumped to `0.1.43`

  Deferred / Non-Goals:
  - No transition, scenario, MCP tool-contract, or campaign-length changes
  - No claim of external validation or empirical calibration

  Verification:
  - Automated MCP sessions completed for fiscal, growth, and balanced strategies
  - `cargo fmt --check` and `cargo test` pass

- Feature: Playtest-guided player guidance
  Status: Complete
  Started: 2026-06-29
  Branch: feat/playtest-guidance-fixes
  Version: 0.1.44

  Summary:
  Clarify player-facing guidance for commercial payer leverage and competitive
  recruitment timing based on the v0.1.42 automated playtest findings.

  Done:
  - Stabilization Turn 1 help explains that above-target commercial rate bids
    need visible leverage from reported access, capacity, or quality context
  - Beginner-mode Turn 1 option copy surfaces payer-leverage risk without
    exposing exact outcomes
  - Competitive observation and MCP debrief text explain that recruitment spends
    cash immediately, resolves after role-specific delays, and can strain
    workforce trust
  - `docs/how-to-play.md` records the same player-facing strategy notes
  - Package version bumped to `0.1.44`

  Deferred / Non-Goals:
  - No changes to transition logic, validation thresholds, scenario files, MCP
    DTO schemas, replay artifacts, or golden hashes
  - No competitive campaign length expansion or competitive scenario loading

  Verification:
  - `cargo fmt --check` and `cargo test </dev/null>` pass

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

- Feature: CLI arbitrary scenario path selection
  Status: Complete
  Started: 2026-06-27
  Branch: feat/cli-scenario-loading
  Version: 0.1.42

  Summary:
  Add CLI support for `--scenario <PATH>` / `-s <PATH>` flags to load and play
  arbitrary scenario TOML files, bypassing campaign selection and resume prompts
  when a custom scenario is loaded.

  Done:
  - Parse CLI arguments in `src/main.rs`
  - Update `run()`, `read_stabilization_run_config()`, and `read_stabilization_run_setup()` in `src/cli/session.rs`
  - Add integration tests in `tests/scenario_selection_tests.rs`
  - Package version bumped to `0.1.42`

  Deferred / Non-Goals:
  - No competitive scenario loading from TOML (remains deferred)
  - No changes to transition logic, state hashes, or session save format

  Verification:
  - Golden hashes (`6fb1ebbea564274f` and `88d07f9e1bbd6f04`) are unchanged
  - All 219 tests pass successfully

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

## Present

No active slice. Competitive runtime I1-I8, the bounded three-month loop,
competitive command-prompt ergonomics, external playtest protocol refresh, the
minimal stabilization scenario loader, bounded MCP agent-play support, CLI
scenario file path selection, automated MCP playtest findings, playtest-guided
player guidance, SDD cleanup, deferred-item triage, the AI-agent playtest
validation pivot, feedback-aligned future planning refresh, the v0.1.49
AI-agent playtest evidence batch, and the v0.1.50 competitive final debrief
metrics slice, the v0.1.51 scripted seed-variation playtest batch, and the
v0.1.52 naive-profile playtest batch, the v0.1.53 campaign test fallback fix,
and the v0.1.54 free-form agent playtest evidence slice are complete.

## Future

### Prioritized / gated tracks

- Track: AI-agent playtest synthesis
  Phase / Gate: Phase 7 prep; use `docs/agent-playtest-protocol.md`,
  `docs/mcp-playtesting-guide.md`, the v0.1.42 automated findings, and
  `docs/playtest-findings-v0.1.49.md` as baseline evidence.

  Next actionable slice:
  Run at least two additional free-form profiles with different strategic
  priorities before stronger command-comprehension or passive-competitive-play
  conclusions. If repeated free-form runs underuse commitments or negotiations,
  review monthly report guidance and command help before considering balance
  changes.

  Verification target:
  Any follow-up findings cite session counts, campaign(s), seeds, difficulty,
  agent profiles or prompts, actor-visible observations, submitted commands,
  validation failures, histories, debriefs, diagnostic summaries, evidence
  limits, and prioritized recommendations. Competitive findings may use the
  v0.1.50 end-session player metrics, but should still label evidence as
  scripted-agent or free-form-agent evidence rather than human validation.

  Deferred / Non-Goals:
  No external human recruitment gate, formal human-subjects research process,
  measured human learning claim, empirical calibration claim, scoring redesign,
  or broad balance pass.

- Track: Strategy-space diagnostics
  Phase / Gate: Phase 7; start with analysis artifacts only, and implement
  tooling only when manual or scripted findings show repeated diagnostic needs.

  Next actionable slice:
  For one current campaign and seed matrix, summarize action frequencies,
  outcome distributions, strategy clusters, stochastic sensitivity, and any
  dominance or near-dominance findings from committed histories and debriefs.

  Verification target:
  The diagnostic report links claims to captured runs, separates simulated-player
  behavior from interpretation, and names which findings should affect guidance,
  debriefing, balance, or future tooling. No formula tuning should happen from a
  single profile, seed, or campaign.

  Deferred / Non-Goals:
  No analytics platform, policy forecast validation, automated optimization
  framework, or runtime export change unless a later slice proves the need.

- Track: Debrief quality as product surface
  Phase / Gate: Phase 6.4/7.6; proceed when playtest evidence shows a specific
  gap in causal explanation, decision-quality review, or uncertainty framing.

  Next actionable slice:
  Improve or evaluate one debrief surface so it answers: what happened, why it
  happened, what the player knew, which assumptions mattered, what alternatives
  were available, and whether a poor outcome reflected decision quality or
  unfavorable realization.

  Verification target:
  Debrief tests or findings prove the output is derived from committed history,
  distinguishes actor-visible observations from true state, and labels
  uncertainty without revealing hidden mechanisms too early in play.

  Deferred / Non-Goals:
  No grading system, LMS integration, full counterfactual engine, or omniscient
  player-facing report during active play.

- Track: Competitive campaign hardening
  Phase / Gate: Phase 6/7; start only after playtest findings identify concrete
  comprehension, pacing, exploit, or command-entry issues.

  Next actionable slice:
  Pick one bounded issue from playtest evidence, such as month-summary clarity,
  command help coverage, argument-key or enum-value autocomplete, AI rationale
  visibility, or a three-month pacing problem, and address it without expanding
  campaign length.

  Verification target:
  Focused CLI/parser/simulation tests cover the changed behavior, competitive
  seed-42 golden hash is unchanged unless transition semantics intentionally
  change, and player-facing docs explain any new guidance.

  Deferred / Non-Goals:
  Full 24-month campaign loop, competitive autosave, competitive replay export,
  competitive scenario loading, multiplayer, and new strategic actor classes.

- Track: Instructor analysis and replay exports
  Phase / Gate: Phase 6.4/8; proceed when playtest or instructional use shows a
  concrete need beyond the current end-of-run debrief and stabilization replay
  artifact export.

  Next actionable slice:
  Add one bounded analysis capability, such as competitive replay export,
  instructor-visible run summary, decision-quality review, counterfactual rerun
  notes, or a debrief extension tied to committed history.

  Verification target:
  Export or debrief tests round-trip the relevant data, preserve append-only
  history, and prove that actor-visible observations are not replaced by
  omniscient true-state reporting in player-facing output.

  Deferred / Non-Goals:
  Cryptographic integrity guarantees, a general analytics platform, LMS
  integration, and policy-forecasting or grading claims.

- Track: Scenario data loading expansion
  Phase / Gate: Phase 6.2; proceed only with authoring or playtest evidence that
  the current stabilization-only TOML boundary is limiting iteration.

  Next actionable slice:
  Develop one exemplary scenario brief or fixture plan before broadening runtime
  tooling. The scenario should include financial pressure, one workforce
  conflict, one payer interaction, one competitive response, one policy or
  regulatory process, delayed consequences, and at least two defensible
  strategic directions. Extend loading only after authoring friction is concrete.

  Verification target:
  Scenario parser/validator tests cover valid input, unsupported campaign or
  format, missing required content, and CLI error reporting. Existing
  `scenario-toml-0.1.40` stabilization files remain valid.

  Deferred / Non-Goals:
  No unrestricted rules language, no migration framework without a concrete
  versioning need, no competitive loader until the state boundary and campaign
  length are explicitly accepted.

- Track: Evidence, parameters, and calibration groundwork
  Phase / Gate: Phase 1/7; proceed when a mechanism needs stronger grounding
  than the current visibly labeled prototype abstractions.

  Next actionable slice:
  Create or extend a parameter/evidence ledger for one bounded mechanism, and
  assign model-confidence labels that distinguish empirically calibrated,
  literature-grounded, expert-informed, stylized abstraction, and
  gameplay-driven mechanics before changing formulas.

  Verification target:
  The ledger distinguishes empirical claims, design abstractions, balancing
  choices, social-welfare assumptions, and confidence labels. Any later runtime
  formula change must cite the ledger and include deterministic regression
  tests.

  Deferred / Non-Goals:
  External data ingestion pipeline, empirical calibration across the whole
  model, real-world policy forecast validation, or authoritative numerical
  claims.

- Track: MCP agent interface expansion
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

- Track: Medicare/Medicaid strategic actors
  Phase / Gate: Phase 5.1/6.1; blocked until actor-card and scenario briefs
  define authority, information, objectives, and learning purpose for the actor.

  Next actionable slice:
  Draft or update actor cards and a scenario brief section before adding runtime
  behavior. Choose one institution and one localized interaction rather than a
  general public-payer framework.

  Verification target:
  Domain docs distinguish actor utility from social welfare, define observation
  boundaries, and label evidence-backed mechanisms versus design abstractions.
  Runtime implementation, if later approved, must include deterministic actor
  rationale tests. Actor decisions should favor explicit institutional
  heuristics, constraints, routines, aspiration levels, and attention limits over
  cleaner but less realistic global optimization.

  Deferred / Non-Goals:
  National policy simulation, federal budget modeling, full Medicaid eligibility
  rules, Medicare payment reproduction, and authoritative policy forecasting.

- Track: Broader simulation breadth
  Phase / Gate: Phase 6.1; proceed only after playtest or instructor feedback
  shows that current campaign limits block meaningful strategy or learning.

  Next actionable slice:
  Add one bounded breadth element, such as one service-line decision, one patient
  or distributional outcome category, one capital-allocation tradeoff, one
  market-area concept, or one additional strategic interaction.

  Verification target:
  The new mechanism has a documented actor/observation boundary, deterministic
  tests, debrief attribution, and clear player-facing tradeoffs. Existing
  stabilization and competitive golden hashes remain stable unless the slice
  intentionally changes transition semantics.

  Deferred / Non-Goals:
  Full US health-system model, individual patient simulation, broad federal
  policy lifecycle framework, global equilibrium AI, and speculative generalized
  frameworks.

- Track: Architecture and documentation discipline
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

- Track: Clippy CI / release automation
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
