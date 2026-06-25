# Mechanism Design — Competitive Regional Market Campaign

## Goal and Roadmap Phase

Design the **competitive regional market campaign** as a parallel track to the
existing five-turn stabilization demo (v0.1.27). This artifact supports Phase 3
(core loop specification) and Phase 6.0 (competitive campaign design) without
runtime implementation.

**Campaign id:** `competitive-regional-v1`

## Slice Boundary

### In scope

- Monthly turn calendar with annual policy tick
- 1 human + K AI health-system players on shared market model
- Simultaneous monthly action resolution with partial rival observability
- Action-point economy with cash and political capital costs
- Executive one-page report with consultant recommendations
- Stata-like command CLI (design only)
- Random monthly events and delayed effect queues
- Difficulty profiles scaling K, CPU budgets, and AI ability

### Out of scope

- Refactoring stabilization demo commands or turn structure
- Medicare/Medicaid strategic actors
- Service-line portfolio modeling
- Global equilibrium or multi-human hot-seat play
- Runtime implementation in this design slice
- Empirical calibration

## Actors and Authority

### Player entities (K+1 health systems)

| Entity | Type | Authority |
| --- | --- | --- |
| Player 0 | Human CEO | Issues commands for nonprofit health system H0 within monthly AP/cash/political limits |
| Players 1..K | AI CEOs | Same command vocabulary and limits; decisions via bounded game-theory heuristics |

Each health system has: `system_id`, `cash`, `staffed_beds`, `access_index`,
`quality_index`, `workforce_trust`, `community_trust`, `commercial_rate`,
`policy_pressure`, `in_flight_projects[]`.

### NPC institution actors (shared market)

Unchanged from stabilization slice; operate on aggregated market state after
player actions resolve:

- Commercial insurers (payer negotiations)
- State policy officials
- Nursing workforce representatives
- Regional provider coalition liaisons

NPCs are **not** counted in K. The turn-5 rival NPC in the stabilization demo
becomes unnecessary in competitive mode because rival systems are AI players.

### Difficulty profiles

| Tier | K | Human AP/mo | CPU AP/mo | CPU ability | Notes |
| --- | --- | --- | --- | --- | --- |
| Easy | 1 | 4 | 2 | Low | One weaker rival; teaching mode |
| Normal | 2 | 3 | 3 | Medium | Two rivals with mixed styles |
| Hard | 3 | 3 | 3 | High | Three capable rivals |
| Expert | 4 | 2 | 4 | High | Tight human budget; strong field |

Style weights per AI: `growth`, `margin`, `access`, `political` (sum to 1.0).

## State, Beliefs, and Observations

### True state (simulator)

- `CompetitiveWorldState`: shared market fields + `systems: Vec<HealthSystemState>`
- `EffectQueue`: pending delayed effects
- `PolicyCalendar`: `current_month`, `current_year`, `last_annual_tick`
- `turn` (month index from campaign start)

### Observations (per player)

Each player receives `PlayerObservation`:

- Own system reported metrics (may include noise via resolved inputs)
- Public rival commitments and announced investments (lagged 1 month)
- Policy briefing and market summary
- Consultant recommendation block (advisory only)
- Intelligence gaps list
- In-flight project status for own system

`monitor` actions may attach `RivalIntel` observations at t+1 with depth
proportional to spend.

### Beliefs

AI players maintain `AiBeliefs`: last observed rival moves, estimated rival
cash runway (noisy), style hypotheses updated from public actions. Beliefs are
inputs to decision procedure only; not hidden state mutation inside
`transition()`.

## Commands, Events, and Effects

### Command shape

```
PlayerCommand {
  system_id,
  verb,
  args: Vec<Arg>,
}
```

Monthly batch: `Vec<PlayerCommand>` per player, subject to AP/cash/political
validation.

### Initial action catalog (MVP)

See `docs/action-catalog-draft.md` for full table. Core verbs:

- `recruit`, `invest`, `monitor`, `negotiate`, `commit`, `project`, `hold`

`hold` costs 0 AP; explicit pass for teaching and AI satisficing.

### Validation failures vs modeled outcomes

- **Invalid:** insufficient AP, cash, or political capital; unknown verb/args;
  project already in flight for same domain.
- **Modeled unfavorable:** payer rejection, workforce action, rival market share
  loss despite valid commands.

### Events

- `MonthlyEvent`: narrative + bounded shock at month start (`monthly_events` stream)
- `AnnualPolicyEvent`: insurance renewal / state policy shift (`annual_policy` stream, month % 12 == 0)

### Effect queue

```
PendingEffect {
  id,
  system_id,
  source_command,
  enqueue_month,
  resolve_month,
  attributed_effects: Vec<Effect>,
}
```

Example: `project ehr epic 50` enqueues resolve at month+12 with cash draw spread
across months per ruleset.

## Strategic Interaction

### Monthly turn sequence

1. **Environment tick** — advance calendar; resolve monthly/annual events into
   `ResolvedInputs`
2. **Observation generation** — per-player executive report data
3. **Decision phase** — human enters command batch via Stata-like CLI; AI
   computes batches from observations and beliefs (human does not see AI choices)
4. **Simultaneous resolution** — aggregate all batches; deterministic sub-step
   order by `system_id` ascending
5. **NPC institution phase** — insurer/state/labor/coalition respond to post-player
   market state (may be simplified in MVP competitive slice)
6. **Transition** — apply effects, enqueue delayed effects, commit history
7. **Reporting** — turn summary; update public rival action log for next month

### Partial observability of rival actions

- **Public log:** `commit`, announced `invest`, `project` groundbreaking
- **Private until disclosed:** `negotiate` outcomes, deep `monitor` results
- **Lag:** public log entries appear in human report at month t+1 for actions
  taken in month t

### AI decision procedure

1. Filter feasible commands given AP/cash/political capital
2. Score candidates with style-weighted utility over expected metric deltas
   (bounded lookahead 1 month)
3. Level-1 response: overweight responses to last month's observed rival public
   actions in same service domain
4. Satisficing: if no candidate beats `hold` by threshold, pass
5. Tie-break via `ai_player_{id}` stream

Rationale string documents top two candidates and chosen action.

## Assumptions and Parameters

- Campaign length default: 24 months
- Starting conditions: scenario-authored per system (may be asymmetric)
- AP refresh: full monthly budget; no banking across months in MVP
- Political capital: base 10, +2 refresh/month, cap 15; advocacy spends consume
- Cash runway signal in report: "comfortable" / "watch" / "strained" from months
  of negative operating margin proxy (design abstraction)

All numeric values are balancing abstractions labeled in scenario format.

- Consultant recommendations generated deterministically from scenario templates +
  state conditions (2–4 options; labeled advisory; no single optimal path).

### Consultant recommendation generation

1. Load scenario-authored template variants per month band (e.g., months 1–6 growth
   focus, months 7–12 policy focus).
2. Filter templates by state triggers (cash runway, rival public moves, policy
   pressure thresholds).
3. Cap at four options; label section "Advisory — not binding."
4. Options map to plausible command batches but player may choose any valid batch.

## Educational Debrief Hooks

- Compare human choices to consultant recommendations (advisory vs actual)
- Show rival rationales for AI systems alongside human decisions
- Attribute market share / access changes to simultaneous rival moves
- Cite resolved `MonthlyEvent` shocks where they materially affected outcomes
- Counterfactual prompt: "What if you had monitored rival R2 in month 4?"
- Distinguish good decisions under uncertainty from fortunate monthly outcomes
- Annual policy year-in-review section at month 12, 24

## Determinism and Replay Notes

- ADR-0001 preserved: `transition()` receives `AggregatedMonthlyActions` +
  `ResolvedInputs`; no RNG inside core
- New streams: `monthly_events`, `annual_policy`, `ai_player_{id}` for each AI
- Replay artifact version bump required when competitive runtime ships
- Human command text log stored for classroom review (CLI layer only)

## Open Questions

- Simplify NPC institution phase in MVP competitive slice vs full institution set?
  **Recommendation:** start with payer + state only; add labor/coalition in I7.
- Fork `transition_competitive()` vs extend existing transition?
  **Recommendation:** extend with `CampaignKind` dispatch; fork only if merge
  proves unsafe during I4.

## Related Documents

- `docs/gameplay-competitive-sketch.md`
- `docs/core-loop-spec.md`
- `docs/competitive-scenario-brief.md`
- `docs/action-catalog-draft.md`
- `docs/executive-report-format.md`
- `docs/cli-command-grammar-draft.md`
- ADRs 0003–0006
