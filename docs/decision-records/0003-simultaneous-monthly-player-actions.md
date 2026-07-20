# ADR-0003: Simultaneous Monthly Player Actions

**Status:** Accepted  
**Date:** 2026-06-24  
**Deciders:** Project contributors

## Context

The competitive regional market campaign (`competitive-regional-v1`) requires
multiple health-system players to act each month. Real institutions make monthly
decisions without observing same-month rival choices, but the CLI must collect
human input sequentially.

The stabilization demo uses sequential player-then-NPC turns. The competitive
campaign needs a documented resolution contract that preserves simultaneous-move
semantics and ADR-0001 determinism.

## Decision

1. **Semantic simultaneity.** All player command batches for month `t` are
   treated as simultaneous strategic choices. UX order does not imply
   first-mover advantage.

2. **Ordered input, simultaneous resolve.** The human enters commands during the
   decision phase. AI batches are computed from pre-resolution observations for
   month `t` before aggregation. Human does not see AI same-month choices before
   submitting.

3. **Aggregation layer.** A new `SimultaneousActionResolver` (design:
   `sim/resolve.rs`) validates each batch, then produces
   `AggregatedMonthlyActions` passed to `transition()`.

4. **Deterministic sub-step order.** When aggregated actions interact (e.g.,
   competing recruitment from shared labor pool), apply sub-effects in ascending
   `system_id` order. Document order in transition tests.

5. **Public action log.** After resolution, public commands append to
   `public_action_log` for month `t`. Observations at month `t+1` include log
   entries from `t` per observability rules in mechanism design.

## Consequences

### Positive

- Matches institutional simultaneity without real-time multiplayer infrastructure
- Deterministic replay: store all batches + aggregated record in history
- Human CLI remains turn-based and teachable

### Negative / tradeoffs

- AI cannot react to human same-month commands (by design)
- Sub-step ordering is a modeling simplification; must be documented for debrief
- Resolver adds complexity before competitive runtime exists

### Follow-ups

- Implement `sim/resolve.rs` in slice I5
- Golden tests for tie-order sensitivity
- Revisit commit-reveal for async classroom play if needed

## Alternatives Considered

| Alternative | Why not chosen |
| --- | --- |
| Strict alternating moves | Grants first-mover advantage; conflicts with sketch |
| Real-time simultaneous input | Out of scope for CLI-first MVP |
| AI moves after human each month | Violates simultaneity; teaches wrong incentives |
| RNG resolution of conflicts | Breaks ADR-0001; use deterministic system_id order |

## Verification

- Mechanism design and core-loop-spec document the sequence
- Future tests: same batches permuted UX order → identical final state
- Code review blocks first-mover logic in competitive transition path

## Related Documents

- [ADR-0001](0001-deterministic-transition-and-stochastic-input-boundary.md)
- [`core-loop-spec.md`](../design/core-loop-spec.md)
- [`gameplay-competitive-sketch.md`](../design/gameplay-competitive-sketch.md)
