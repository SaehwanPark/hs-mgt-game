# Core Game Loop Specification

**Status:** Phase 3 deliverable  
**Audience:** Contributors, instructors, playtest designers  
**Supersedes:** Informal loop descriptions scattered in roadmap §3.1 only

This document defines the high-level turn cycle for both campaigns in the
repository.

## Campaigns

| Campaign id | Name | Turn unit | Player model | Status |
| --- | --- | --- | --- | --- |
| `stabilization-v1` | Regional stabilization demo | Abstract (5 points) | 1 human CEO + per-turn NPC actors | Implemented v0.1.27 |
| `competitive-regional-v1` | Competitive regional market | 1 month | 1 human + K AI health systems + NPC institutions | Stub: campaign select + month-1 report preview (v0.1.29) |

## Shared principles

Both campaigns preserve:

- Deterministic `transition()` core (ADR-0001)
- True state vs actor observations
- Invalid operations vs unfavorable modeled outcomes
- Append-only history with replay verification
- Educational end-of-run debrief from committed history

## Stabilization campaign loop

Current executable loop (`stabilization-v1`):

```
FOR turn IN 1..5:
  1. Resolve stochastic inputs for turn (seeded streams)
  2. Generate CEO observation (reported metrics, briefings)
  3. Optional uncertainty preview (interactive mode)
  4. Executive briefing (turn-scoped)
  5. Player selects turn-locked command (interactive, preset, or beginner)
  6. Validate command against ruleset
  7. Dispatch NPC actor for turn (insurer, state, labor, coalition, competitor)
  8. transition(prior, command, inputs, ruleset) -> next state, events, effects
  9. Commit transition to history with state hash
  10. Turn resolution summary
END
11. Replay verification
12. Educational debrief
```

**Limited resources (current):** per-field spend caps in ruleset; cash debited
but not feasibility-checked.

**Calendar:** none; turns are executive decision points.

## Competitive campaign loop

Designed loop (`competitive-regional-v1`):

```
FOR month IN 1..campaign_length:
  1. Environment tick
     - Advance PolicyCalendar (Year Y, Month M)
     - Resolve monthly_events stream
     - IF month % 12 == 0: resolve annual_policy stream
     - Apply due PendingEffects from queue

  2. Observation generation
     - Per-player PlayerObservation
     - Executive report (6 sections; see executive-report-format.md)
     - Consultant recommendations (advisory)
     - Rival intel from public action log (lagged)

  3. Decision phase
     - Human: Stata-like CLI command batch entry until submit or hold
     - AI: compute batches from observations + beliefs (not shown to human)

  4. Simultaneous resolution (ADR-0003)
     - Validate all batches (AP, cash, political capital)
     - Aggregate AggregatedMonthlyActions
     - Deterministic resolve order by system_id ascending

  5. NPC institution phase (simplified in MVP)
     - Payer and state actors respond to post-player market (expand later)

  6. transition(prior, aggregated_actions, inputs, ruleset)
     - Dispatch via `CampaignKind`; may use `transition_competitive()` until
       unified merge is proven safe (ADR-0004)
     - Enqueue new PendingEffects
     - Update public rival action log for next month observability

  7. Commit transition to history with state hash

  8. Monthly resolution summary
END
9. Replay verification
10. Educational debrief (includes consultant comparison, AI rationales, annual review)
```

## Limited resources (competitive)

| Resource | Role | Refresh |
| --- | --- | --- |
| Cash | Capital spends, recruitment, projects | Operating flows per transition |
| Action points (AP) | Monthly command capacity | Full budget each month (no banking in MVP) |
| Political capital | Advocacy, negotiation posture | Partial monthly refresh, cap 15 |
| Trust metrics | Workforce and community legitimacy | Modified by commits and outcomes |
| Implementation capacity | Concurrent projects | Max 2 in-flight projects per system in MVP |

Difficulty scales K, CPU AP, and AI ability — not human AP below documented floors.

## Paper-playable manual prototype

Instructors can run the competitive loop on paper:

1. Distribute executive report printout per month (template in executive-report-format.md).
2. Each AI seat uses style card + last month's public log.
3. Collect command slips face-down; reveal simultaneously.
4. Apply action catalog costs; resolve with spreadsheet ruleset.
5. Update public log for next month.

**Exit criterion (roadmap §3):** loop supports multiple defensible strategies without
hidden optimal path.

## Reporting and explanation

| Stage | Stabilization | Competitive |
| --- | --- | --- |
| Pre-decision | Turn briefing + forecast preview | Executive report + consultant advice |
| Post-decision | Actor rationale + state hash | All player rationales + monthly summary |
| End of run | Debrief from history | Debrief + advisory comparison + year reviews |

## Related documents

- [`gameplay-competitive-sketch.md`](gameplay-competitive-sketch.md)
- [`executive-report-format.md`](executive-report-format.md)
- [`competitive-scenario-brief.md`](competitive-scenario-brief.md)
- [`system-boundary.md`](system-boundary.md)
- ADR-0001, ADR-0003, ADR-0004, ADR-0005, ADR-0006
