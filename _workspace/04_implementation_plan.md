# Coding Implementation Plan - Active Projects Detailed Observation

## Task restatement
Enhance the competitive campaign dashboard's `In-flight` project display by formatting detailed active project states (kind, remaining months, and monthly cash draw) instead of a simple count.

## Current understanding
- `PlayerObservation::in_flight_projects` is a string currently populated by calling `in_flight_projects_label(human.resources.active_projects)` in `src/sim/observe_competitive.rs`.
- `in_flight_projects_label` currently just takes a count `active_projects` and formats it as `"none"` or `"{active_projects} active project(s)"`.
- The actual list of active projects is contained in `world.effect_queue` (where `effect.system_id == human.system_id` and the effect has a `project_draw` value).
- `PendingEffectKind` variants (`BedsCapacity`, `OutpatientCapacity`, `TechnologyQuality`) store the `project_draw` as `Option<i32>`.

## Assumptions
- `project_draw` values are only `Some(draw)` for actual active projects started via the `project` command.
- The state values in `human.resources.active_projects` and `human.resources.active_project_monthly_draws` remain correct and do not need to change.
- Replay/save compatibility is not broken since the observation struct's fields do not change types (only `in_flight_projects` string content is enriched).

## Minimal implementation plan
1. **Refactor `in_flight_projects_label`:**
   - Change signature in `src/sim/observe_competitive.rs` to take `world: &CompetitiveWorldState` and `human_id: u32`.
   - Scan `world.effect_queue`.
   - Filter effects where `effect.system_id == human_id` and `effect.kind` is a project.
   - Map them to project details:
     - `PendingEffectKind::BedsCapacity { project_draw: Some(draw), .. }` -> `"Tower"`
     - `PendingEffectKind::OutpatientCapacity { project_draw: Some(draw), .. }` -> `"ClinicNetwork"`
     - `PendingEffectKind::TechnologyQuality { project_draw: Some(draw), .. }` -> if `effect.summary.contains("EhrCerner")` { `"EhrCerner"` } else { `"EhrEpic"` }
     - Calculate remaining months: `effect.resolve_month.saturating_sub(world.policy_calendar.month_index)`.
     - Format: `"{label} ({remaining} mos left, ${draw}k/mo draw)"`.
   - Join with `", "`. If none, return `"none"`.
2. **Update observation call:**
   - Update `in_flight_projects` population in `observe_for_human`:
     ```rust
     in_flight_projects: in_flight_projects_label(world, human.system_id),
     ```
3. **Verify & Test:**
   - Add a unit test in `src/sim/observe_competitive.rs` verifying observation formatting with one or two active projects in `effect_queue`.
   - Run `cargo test` to ensure all tests pass.
   - Update version to `0.5.9` in `Cargo.toml`.
   - Document changes in `CHANGELOG.md` and `SPEC.md`.

## Files and functions likely to change
- `src/sim/observe_competitive.rs`: `in_flight_projects_label`, `observe_for_human`, and unit tests.
- `Cargo.toml`: version bump.
- `CHANGELOG.md`: Record new version and additions.
- `SPEC.md`: Move feature track to Done / Present.

## Tests and checks
- `cargo test` (ensuring 260+ tests pass successfully).

## Acceptance criteria
- Starting a project shows its name, remaining duration, and monthly draw on the turn dashboard.
- Multiple active projects are listed simultaneously.
- Completed projects disappear.
- All tests pass cleanly.

## Non-goals
- No changes to stabilization campaign loop rules.
- No changes to competitive transition engine rules.

## Stop conditions
- Stop and review if any core state serialization schema must change.

## Review checklist
- Only requested changes are implemented.
- Covered by unit tests.
- Version bumped by 0.0.1.
