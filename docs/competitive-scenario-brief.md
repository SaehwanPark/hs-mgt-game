# Competitive Scenario Brief

**Status:** Phase 6.0 design artifact  
**Audience:** Contributors, domain reviewers, playtest designers  
**Campaign id:** `competitive-regional-v1`

Parallel to [`first-scenario-brief.md`](first-scenario-brief.md) for the
stabilization demo. This brief defines the first **competitive** regional market
campaign without changing the stabilization executable.

## Scenario concept

Two to five nonprofit and community health systems compete in a fictional
mid-size regional US market (1 human + K AI rivals, K=1–4 by difficulty). The human player leads **Riverside Community
Health**, a safety-net-leaning system facing rivals with different growth
strategies, payer mixes, and community relationships.

The scenario tests whether players can balance competitive positioning with
nonprofit obligations: access, workforce stability, and policy legitimacy — not
mere market share maximization.

## Player role

- Human: CEO of Riverside Community Health (player 0)
- AI: CEOs of K rival systems (names and styles scenario-defined)
- NPC institutions: commercial payers, state policy officials (MVP); labor and
  coalition expanded in later implementation slices

## Scenario duration

- **24 months** (24 turns) for MVP competitive campaign
- 1 turn = 1 calendar month
- Annual policy review at months 12 and 24

## Difficulty and K

| Tier | K rivals | Human AP/mo | CPU AP/mo | Rival systems (example) |
| --- | --- | --- | --- | --- |
| Easy | 1 | 4 | 2 | Northlake Health (growth) |
| Normal | 2 | 3 | 3 | Northlake + Summit Care (margin) |
| Hard | 3 | 3 | 3 | Northlake + Summit + Valley Regional (access) |
| Expert | 4 | 2 | 4 | Above + Metro Academic (political) |

Future difficulty expansion should preserve the table as the visible baseline
while adding explainable pressure dimensions only after validation: rival
resource access, information delay, monitoring depth, and risk/aggression
posture. Expert should be documented and playtested as difficult but winnable,
not as an impossible challenge tier.

## Learning objectives

Players should practice:

- Reading executive reports under partial rival observability
- Allocating monthly action points across competing priorities
- Evaluating consultant advice without treating it as optimal policy
- Anticipating simultaneous rival moves in capacity and workforce markets
- Managing delayed projects (EHR, expansion) against short-term pressures
- Responding to annual insurance and policy shifts
- Distinguishing decision quality from monthly luck and rival behavior

## Included interactions

- Monthly executive report with four deterministic consultant recommendations
  derived from the actor-visible observation
- Simultaneous multi-system command resolution
- Action-point, cash, and political capital economy
- Public vs private rival action observability
- `monitor` intelligence gathering
- Random monthly events (versioned deck)
- Multi-month `project` pipelines including EHR migration
- Annual policy and insurance renewal tick
- Stata-like command entry (competitive CLI)
- End-of-run debrief with AI rationales and month-by-month advisory comparison

## Excluded interactions (competitive v1)

- Medicare/Medicaid as strategic actors
- Service-line portfolio optimization
- Individual patient simulation
- Federal legislative process
- Hot-seat classroom multiplayer (Phase 9)
- Empirical calibration or forecasting claims
- Refactoring or replacing stabilization demo
- Regional merger/acquisition mechanics in the default campaign. The separate
  `regional-affiliation-v1` proposal is opt-in and not implemented.
- GUI-specific scenario behavior; future graphical clients must reuse the same
  scenario and core data.
- Advisor-market, payroll, candidate-pool, or hire/fire mechanics until the
  reviewed advisor proposal is promoted into a bounded runtime slice.

## Initial strategic tensions

- Capacity investment defends share but consumes cash before payer rate relief
- Workforce recruitment helps access but rivals may poach with higher spend
- Public access pledges reduce policy pressure but signal strategy to rivals
- EHR projects improve long-run quality but bind AP and cash for months
- Monitoring rivals delays action but reduces blind investment risk
- Annual payer renewal concentrates bargaining power in specific months

## Observations and uncertainty

- Human sees own reported metrics (noise and delay via resolved inputs)
- Rival **public** actions appear with 1-month lag
- Consultant options highlight tradeoffs; ignoring advice remains viable
- Intelligence gaps explicitly list unobserved rival activity
- Random events inject exogenous shocks without railroading a single path

## Assessment framing

- No single normative winner or market-share score; discussion focuses on
  access, trust, workforce, and policy legitimacy tradeoffs.
- `evaluation_profile` in scenario format may supply reflection prompts only.
- Instructor debrief emphasizes nonprofit obligations vs competitive positioning.

## Debrief hooks

- Month-by-month comparison of human actions and retained consultant options
- Rival AI rationales for key competitive months
- Effect attribution for simultaneous moves (share, access, trust)
- Cite resolved monthly event shocks where material
- Year 1 and Year 2 policy review summaries
- Reflection: "Which rival move surprised you given observability rules?"

## Relationship to stabilization demo

| Aspect | Stabilization (`stabilization-v1`) | Competitive (`competitive-regional-v1`) |
| --- | --- | --- |
| Turns | 5 abstract points | 24 months |
| Players | 1 CEO | 1 human + K AI systems |
| Commands | Turn-locked five types | Open verb catalog per month |
| CLI | Numeric prompts | Stata-like grammar |
| Rival | Turn-5 NPC actor | K AI peer systems |
| Status | Implemented | Implemented (24-month campaign loop, autosave, scenario loading, and replay export) |

Both campaigns coexist through the implemented campaign router.

## Related documents

- [`first-scenario-brief.md`](first-scenario-brief.md)
- [`gameplay-competitive-sketch.md`](gameplay-competitive-sketch.md)
- [`core-loop-spec.md`](core-loop-spec.md)
- [`executive-report-format.md`](executive-report-format.md)
- [`action-catalog-draft.md`](action-catalog-draft.md)
- [`scenario-format-draft.md`](scenario-format-draft.md)
