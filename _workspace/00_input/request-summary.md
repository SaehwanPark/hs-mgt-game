# Request Summary - Exemplary Competitive Scenario & Timeline Events

## Scope
Implement the `competitive-exemplary-v1` scenario, including its timeline events, delayed consequences, and the RNA strike / CON challenge mechanics.

Specifically:
- Create `scenarios/competitive-exemplary-v1.toml` TOML file with the setup parameters from `docs/exemplary-scenario-brief.md`.
- Add `scenario_id` and `event_metadata` fields to `CompetitiveWorldState` to identify and track events for the exemplary campaign.
- Extend `PledgeType` with `Workforce` to support wage increase commitments.
- Implement conditional timeline checks and effects in `src/sim/effects_competitive.rs` and `src/sim/transition_competitive.rs` for Month 8, 10, 12, and 18 events.

## Non-Goals
- No changes to stabilization campaign loop rules.
- No network multiplayer capabilities.
- No database integration.

## Sources
- `docs/exemplary-scenario-brief.md`
- `src/model/competitive_world.rs`
- `src/scenario/mod.rs`
- `src/sim/effects_competitive.rs`
- `src/sim/transition_competitive.rs`

## Expected Files
- `scenarios/competitive-exemplary-v1.toml`
- `src/model/competitive_world.rs`
- `src/model/competitive_command.rs`
- `src/cli/competitive_parse.rs`
- `src/cli/repl.rs`
- `src/sim/effects_competitive.rs`
- `src/sim/transition_competitive.rs`
- `SPEC.md`
- `CHANGELOG.md`
