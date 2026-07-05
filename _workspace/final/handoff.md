# Final Handoff - PR Review Polish: Emergency Department Service Line

## Summary of Changes
1. **Added Serde Defaults:**
   - Modified `src/model/competitive_world.rs` to add `#[serde(default)]` to the `emergency_capacity` field in the `HealthSystemState` struct, ensuring backward compatibility when resuming legacy autosaves/replays.
2. **Suspended ED Pavilion Projects during RNA Strikes:**
   - Updated the strike delay match block in `src/sim/effects_competitive.rs` to include `PendingEffectKind::EmergencyCapacity`, ensuring active Emergency Department Pavilion projects and their monthly cash draws are properly suspended during active RNA strikes.
3. **Corrected Admin Staffing Target:**
   - Corrected the formula for calculating target admins in `src/sim/transition_competitive.rs` and `src/actors/ai_player.rs` to be `(system.staffed_beds + system.outpatient_capacity + 19) / 20 + (system.emergency_capacity + 9) / 10`, aligning with the documented ratio in `SPEC.md` (existing target + `ceil(emergency_capacity / 10)`).
   - Updated the nurse target warning check in `src/sim/effects_competitive.rs` to include the `emergency_capacity` nurse target.
4. **Updated Test Cases:**
   - Refactored assertions in `test_emergency_department_mechanics` in `src/sim/transition_competitive.rs` to account for the corrected target admin calculations and their impact on workforce trust drops.
5. **Tracked Lockfile Updates:**
   - Refreshed and updated `Cargo.lock` to reflect version `0.6.0` bump.

## Verification Results
- Ran `cargo fmt` and `cargo test`.
- All 272 tests passed successfully.
