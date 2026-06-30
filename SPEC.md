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


### Recent slices

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
player guidance, SDD cleanup, deferred-item triage, and the AI-agent playtest
validation pivot are complete.

## Future

### Prioritized / gated tracks

- Track: AI-agent playtest synthesis
  Phase / Gate: Phase 7 prep; use `docs/agent-playtest-protocol.md`,
  `docs/mcp-playtesting-guide.md`, and the v0.1.42 automated findings as
  baseline evidence.

  Next actionable slice:
  Run a versioned AI-agent playtest batch for current `stabilization-v1` and
  `competitive-regional-v1` preview flows, then add a findings document that
  separates command comprehension, strategic tension, winnability, exploit
  discovery, pacing proxies, and educational debrief coherence.

  Verification target:
  Findings cite session counts, campaign(s), seeds, difficulty, agent profiles
  or prompts, actor-visible observations, submitted commands, validation
  failures, histories, debriefs, evidence limits, and prioritized follow-up
  recommendations. No runtime change is required unless findings identify a
  narrow blocking defect.

  Deferred / Non-Goals:
  No external human recruitment gate, formal human-subjects research process,
  measured human learning claim, empirical calibration claim, scoring redesign,
  or broad balance pass.

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
  Extend scenario loading in the smallest useful direction, such as additional
  stabilization fixture validation, authoring diagnostics, or a design-only
  competitive scenario-loading plan before runtime support.

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
  Create or extend a parameter/evidence ledger for one bounded mechanism,
  linking model assumptions to sources, plausible ranges, uncertainty, and
  unresolved normative choices before changing formulas.

  Verification target:
  The ledger distinguishes empirical claims, design abstractions, balancing
  choices, and social-welfare assumptions. Any later runtime formula change must
  cite the ledger and include deterministic regression tests.

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
  rationale tests.

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
