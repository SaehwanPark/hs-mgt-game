# ADR-0005: Action Economy and Monthly Budget

**Status:** Accepted  
**Date:** 2026-06-24  
**Deciders:** Project contributors

## Context

The competitive sketch requires each action to have a cost and a monthly limit on
player capacity, with CPU budgets varying by difficulty. The stabilization demo
uses per-field spend caps but does not enforce cash feasibility or a unified
action-point budget.

Roadmap §3.1 lists management attention, capital, and political capital as
strategic limits.

## Decision

1. **Three cost channels.** Each competitive command declares:
   - `action_points` (AP) — monthly management attention budget
   - `cash_cost` — liquid resources
   - `political_capital` (optional) — advocacy and negotiation capacity

2. **Monthly AP budget.** Each player receives `ap_budget` per month from
   difficulty profile. Unspent AP does not bank in MVP. Sum of AP in a monthly
   batch ≤ budget.

3. **Cash feasibility.** Validation rejects commands that would drive cash below
   ruleset minimum (typically 0) when costs apply. Project commands may schedule
   future draws; all draws must pass feasibility at enqueue time.

4. **Political capital.** Base stock scenario-defined; partial monthly refresh
   (+2/month, cap 15 in default ruleset). PC costs on `negotiate` and `commit`.

5. **Difficulty scaling.** CPU `ap_budget` and `ability_tier` vary by tier; human
   AP floors documented in competitive scenario brief (minimum 2 Expert).

6. **Catalog as source of truth.** Costs defined in
   [`action-catalog-draft.md`](../action-catalog-draft.md); ruleset may scale by
   scenario without changing verb semantics.

7. **Stabilization unchanged.** Five-turn demo keeps existing per-field caps;
   cash feasibility may be added later as separate slice.

## Consequences

### Positive

- Teaches scarcity across attention, cash, and political channels
- Difficulty tuning without changing market physics
- Clear validation errors separate from unfavorable negotiations

### Negative / tradeoffs

- More player tracking (AP, PC) in UI
- Balancing numbers are abstractions requiring playtest iteration
- Project spread costs complicate feasibility checks

### Follow-ups

- Implement validation in `sim/validate.rs` competitive path (slice I3)
- Executive report shows AP and PC remaining (slice I2)
- Playtest AP budgets after first competitive prototype

## Alternatives Considered

| Alternative | Why not chosen |
| --- | --- |
| Cash only (no AP) | Does not limit command count; encourages spam |
| Single combined "energy" | Loses political vs operational tradeoff |
| Unlimited AP with escalating costs | Harder to teach; obscures monthly pacing |
| Real-time regeneration | Conflicts with monthly turn unit |

## Verification

- Action catalog lists AP/Cash/PC per verb
- Future tests: batch exceeding AP fails validation; insufficient cash fails
- Debrief cites resource constraints when commands rejected

## Related Documents

- [ADR-0004](0004-multi-system-player-state.md)
- [`action-catalog-draft.md`](../action-catalog-draft.md)
- [`executive-report-format.md`](../executive-report-format.md)
