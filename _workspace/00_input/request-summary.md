# Request Summary - Address PR Review Comments for Emergency Department Service Line

## Phase / Gate
Phase 6.1: Simulation Breadth (Track 5) - PR Review Polish

## Scope
Address 4 specific reviewer comments on PR #67:
1. Add `#[serde(default)]` to the `emergency_capacity` field in the `HealthSystemState` struct in `src/model/competitive_world.rs` to maintain backward-compatibility with older save files.
2. Update the RNA strike delay loop in `src/sim/effects_competitive.rs` to include `PendingEffectKind::EmergencyCapacity` so ED Pavilion projects are properly suspended during active RNA strikes.
3. Fix the admin staffing target formula in `src/sim/transition_competitive.rs` and `src/actors/ai_player.rs` to properly calculate target admins as `(system.staffed_beds + system.outpatient_capacity + 19) / 20 + (system.emergency_capacity + 9) / 10`, aligning with the documented ratio (existing target + `ceil(emergency_capacity / 10)`).
4. Update the test assertions in `src/sim/transition_competitive.rs` to reflect the updated admin target calculation.
5. Compile and run cargo to update and track `Cargo.lock` with the package version `0.6.0` bump.

## Non-Goals
- No changes to stabilization campaign loops or other service lines.

## Expected Files to Change
- `src/model/competitive_world.rs`
- `src/sim/effects_competitive.rs`
- `src/sim/transition_competitive.rs`
- `src/actors/ai_player.rs`
- `Cargo.lock`
