# Evidence Map — Competitive Regional Market Campaign

## Scope

Map evidence and design precedents to support the competitive gameplay sketch:
monthly turns, 1 human + K AI health-system players, simultaneous monthly
actions with partial rival observability, action economy, executive-report
briefings, Stata-like CLI, delayed effects, yearly policy cadence, and random
events. This map supports design artifacts only; it does not calibrate formulas
or approve runtime schemas.

## Sources Reviewed

- User competitive gameplay sketch (2026-06-24)
- Canonical project docs: deterministic transitions, observation separation,
  local game theory, educational debriefing, narrow vertical slices
- `docs/phase1-lit-review.md` and `docs/phase1-implications-memo.md`
- `docs/proposal.md` §10 (quarterly first slice) and §14 (long-term multiplayer)
- `docs/roadmap.md` §3.1 (limited resources), §6.3 (bounded decision models)
- `docs/design_principles.md` §5 (game theory as decision framework)
- Current v0.1.27 stabilization demo: five abstract turns, one CEO, NPC actors,
  turn-5 rival as reactive institution (not peer player)
- Business simulation precedent: *Capitalism* (difficulty-scaled CPU competitors,
  asymmetric ability and style)
- ADR-0001 stochastic input boundary

## Boundary Evidence

- A **parallel campaign** preserves the stabilization demo as regression anchor
  while the competitive track introduces monthly calendar, K peer systems, and
  generalized action vocabulary.
- Monthly turns are appropriate for executive strategy pacing in a regional market
  campaign; the stabilization demo may keep abstract turns until voluntarily
  migrated.
- K AI health systems are **peer players** with action budgets; insurer, state,
  labor, and coalition remain **NPC institution actors** on the shared market.
- All players share one market `CompetitiveWorldState`; they differ only in which system's
  commands they issue and what they can observe about rivals.
- Consultant recommendations are advisory content in the executive report; player
  agency requires that ignoring advice remains viable.

## Mechanisms and Institutions

### Capitalism-style difficulty scaling

- Difficulty sets K (number of AI health systems), CPU monthly action-point
  budget, ability tier (forecast accuracy, spend efficiency), and style weights.
- Easy: K=1, generous human AP, weaker CPU. Hard: K=3–4, tighter budgets, mixed
  aggressive and margin-focused rivals.
- Evidence: established genre convention; aligns with `design_principles.md`
  difficulty-from-tradeoffs rather than arbitrary punishment.

### Simultaneous move games

- Real health systems make monthly decisions without observing same-month rival
  choices; the model should treat all player actions for month t as simultaneous.
- Implementation pattern: **ordered input, simultaneous resolve** — human enters
  commands during the month; AI choices computed from pre-resolution
  observations; all batches aggregated before `transition()` (ADR-0003).
- Partial observability: rival **public** actions (investments announced,
  access pledges) appear in month t+1 briefing; **monitor** actions may reduce
  lag; private negotiations stay hidden until disclosed.
- Alternative commit-reveal rejected for CLI UX complexity in v1 competitive
  slice; may revisit for classroom async play.

### Action economy

- Roadmap §3.1 lists capital, management attention, political capital, trust,
  time, and implementation capacity as strategic limits.
- Competitive campaign maps **management attention** to monthly **action points
  (AP)**; capital to cash costs; political capital to advocacy/negotiation verbs.
- Each command declares `cash_cost`, `action_points`, optional `political_capital`.
- Cash feasibility must be validated before resolution (closes current prototype
  gap where spend can drive cash negative without rejection).

### Delayed effects

- EHR migration and major capital projects require multi-month pipelines, not
  same-turn metric deltas.
- Pattern: `PendingEffect { enqueue_turn, resolve_turn, source_command, deltas }`
  applied deterministically when due; visible in executive report as "in-flight
  projects."
- Evidence: `design_principles.md` delayed consequences principle; real health
  system IT and construction timelines.

### Yearly policy and insurance cadence

- Insurance contract cycles and major state policy shifts often operate on annual
  rhythms; month 12, 24, … triggers `annual_policy` stream resolution.
- Monthly `policy_signal` stream continues for shorter-horizon movements.
- Keeps deterministic boundary: annual shocks are resolved inputs, not RNG inside
  `transition()`.

### Random events

- Exogenous shocks (workforce shortage spike, surprise audit, payer policy memo)
  enter via `monthly_events` named stream at month start.
- Events produce narrative text + bounded numeric shock; logged in history for
  debrief. Not a hidden optimal-path railroad.

### Stata-like CLI

- Stata models command + arguments with syntax highlighting, autocomplete, and
  `help`; suitable for CLI-first reproducible logs.
- Parser is presentation/I/O layer only; typed commands feed validation and
  transition (ADR-0006). Overrides `LESSONS.md` parser deferral for competitive
  track only.

### Game-theory AI for computer players

- Global equilibrium rejected per `phase1-implications-memo.md`.
- Bounded procedures: satisficing → level-1 best response to observed rival moves
  → style-weighted utility; stochastic tie-break via `ai_player_{id}` stream.
- Rationale output required for debrief (reuse `ActorDecisionRecord` pattern).

## Actor Incentives and Information

- Human health system: nonprofit regional CEO balancing access, margin, trust,
  workforce, and competitive position.
- AI health systems: same action vocabulary and market rules; utility weights
  vary by style profile (growth, margin, access leader, political operator).
- NPC institutions: unchanged incentive structure from stabilization slice;
  respond to aggregated market state after player resolution.
- Human observes: own system metrics, public rival moves (lagged), policy
  briefings, consultant advice, intelligence gaps.
- AI observes: own metrics + same public rival intel as human (no omniscience
  unless ability tier grants forecast noise reduction on own forecasts only).

## Assumptions

- Competitive campaign length 12–36 months for MVP; parameterized in scenario.
- One human player per run; hot-seat multiplayer deferred to Phase 9 classroom
  roles (distinct from K AI systems).
- Stabilization demo golden hash `6fb1ebbea564274f` remains unchanged.
- New competitive golden trajectory will be added when runtime ships (slice I1+).
- Consultant recommendations generated deterministically from scenario + state
  (not LLM); 2–4 options per month with explicit tradeoff text.

## Unresolved Questions

| Question | Owner | Notes |
| --- | --- | --- |
| Default K and AP by difficulty tier? | Mechanism design / balancing | Easy K=1 AP=4, Normal K=2 AP=3, Hard K=3 AP=3, Expert K=4 AP=2 human / 4 CPU |
| Human input order before or after AI compute? | ADR-0003 | Recommend human-first UX; AI uses pre-month observations only |
| Same `transition()` or `transition_competitive()`? | Architecture | Prefer shared core with aggregated action batch; fork only if needed |
| How many verbs in MVP action catalog? | Scenario brief | Start with 6–8 verbs; expand after playtest |
| Consultant advice: scenario-authored or rules-generated? | Educational design | Hybrid: scenario templates + state-conditional variants |
| Event deck: fixed scenario list or procedural? | Scenario format | Fixed versioned deck per scenario for reproducibility |
| Rival action observability lag: 1 or 2 months default? | Mechanism design | 1 month public lag; `monitor` can reveal month t rival private intel at t+1 |
| Political capital replenishment rate? | Action economy | Monthly partial refresh + annual policy events |

## Design Implications

- Preserve ADR-0001: all randomness in `inputs/resolve.rs`; competitive streams
  added with stable indices (`monthly_events`, `annual_policy`, `ai_player_{id}`).
- Campaign router selects stabilization vs competitive without merging code paths
  prematurely.
- Executive report schema documented before `briefing.rs` rewrite (slice I2).
- AI player cards distinct from NPC institution cards in `docs/actor-cards.md`.
- Scenario format gains `campaign_id`, `turn_unit: month`, `k_competitors`,
  `difficulty`, `action_catalog_ref`, `event_schedule`.

## Risks

- **Scope expansion:** competitive track is Phase 6-scale; design package must
  not imply imminent full implementation.
- **False precision:** monthly cash/AP numbers are balancing abstractions.
- **Strategic opacity:** AI must expose rationales; simultaneous resolve order
  must be documented and deterministic.
- **Educational opacity:** consultant advice must not imply single optimal path.
- **Replay complexity:** multi-player action batches must serialize in replay
  artifacts with version bump.
- **Parser creep:** Stata CLI limited to competitive campaign entry until
  stabilization path needs it.
