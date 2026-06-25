# ADR-0004: Multi-System Player State

**Status:** Accepted  
**Date:** 2026-06-24  
**Deciders:** Project contributors

## Context

The competitive campaign requires 1 human and K AI health systems operating in
one regional market. The stabilization demo models a single health system in
`WorldState` with a turn-5 rival NPC actor — not peer players with independent
action budgets.

Contributors need a recorded model for shared market state, per-system metrics,
and controller assignment without breaking the stabilization demo.

## Decision

1. `CampaignKind` distinguishes `Stabilization` vs `Competitive`, mapped to
   `campaign_id` values `stabilization-v1` and `competitive-regional-v1`.
   Stabilization retains current `WorldState` shape and transition path unchanged.

2. **Competitive world state.** `CompetitiveWorldState` contains:
   - `market: SharedMarketFields` (payer landscape, policy pressure, demand signals)
   - `systems: Vec<HealthSystemState>` length K+1
   - `players: Vec<PlayerSlot>` with `system_id` and `controller: Human | Ai(profile)`
   - `public_action_log`, `effect_queue`, `policy_calendar`

3. **Shared model.** All systems read/write the same competitive world instance
   during a month. No duplicate shadow simulations per player.

4. **NPC institutions remain separate.** Insurer, state, labor, and coalition
   actors are not `PlayerSlot` entries. They respond after player aggregation
   per core-loop-spec.

5. **AI players ≠ rival NPC.** The stabilization `competitor` actor is not used
   in competitive mode; rivalry is entirely among `PlayerSlot` AI controllers.

6. **Transition dispatch.** Competitive months call
   `transition_competitive(prior, aggregated_actions, resolved_inputs, ruleset)`
   initially; merge into unified `transition()` only if stabilization and
   competitive paths share sufficient structure without regression risk.

## Consequences

### Positive

- Clear entity model for K+1 peer systems
- Stabilization demo isolated from competitive expansion
- Replay can serialize full `systems` vector and player batches

### Negative / tradeoffs

- Two world state shapes until/unless unified
- Replay artifact version bump required for competitive runs
- Scenario authoring must define K+1 starting conditions

### Follow-ups

- `model/players.rs` in slice I4
- Scenario format fields: `k_competitors`, `difficulty`, per-system genesis
- Competitive golden test `tests/golden_competitive_seed42.rs`

## Alternatives Considered

| Alternative | Why not chosen |
| --- | --- |
| Single system + K NPC rivals | NPCs lack peer action economy; conflicts with sketch |
| Extend stabilization WorldState in place | High regression risk for golden hash |
| Separate binary / crate | Premature; campaign router sufficient |

## Verification

- `docs/competitive-scenario-brief.md` and mechanism design align
- Stabilization `cargo test` golden hash unchanged until competitive code lands
- Future: competitive genesis + 1-month replay test

## Related Documents

- [ADR-0003](0003-simultaneous-monthly-player-actions.md)
- [`system-boundary.md`](../system-boundary.md)
- [`actor-cards.md`](../actor-cards.md) (AI player card)
