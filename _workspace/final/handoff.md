# Final Handoff - Active Projects Display Hardening (Track 1)

## Summary of Changes
1. **Created Working Branch:** Switched to branch `feat/active-projects-display-details`.
2. **Handoff Artifacts Created/Updated:**
   - `_workspace/00_input/request-summary.md`: Scoped request to detail active project kind, duration, and cash draws.
   - `_workspace/02_mechanism_design.md`: Map pending project effects to descriptive labels and remaining durations in the observation step.
   - `_workspace/03_domain_qa.md`: Domain QA review (status: `pass`) validating transparency and determinism.
   - `_workspace/04_implementation_plan.md`: Step-by-step code change list and validation checks.
3. **Implementation details:**
   - Refactored `in_flight_projects_label` in [src/sim/observe_competitive.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/observe_competitive.rs) to scan `world.effect_queue` for matching system project effects, calculate remaining months, and extract project names and cash draws.
   - Updated `observe_for_human` call site to pass `world` and `human.system_id`.
   - Added unit test `test_active_projects_observation` covering formatting.
4. **Project tracking updated:**
   - Version bumped to `0.5.9` in [Cargo.toml](file:///Users/saehwan/repos/hs-mgt-game/Cargo.toml).
   - Documented changes in [CHANGELOG.md](file:///Users/saehwan/repos/hs-mgt-game/CHANGELOG.md) and [SPEC.md](file:///Users/saehwan/repos/hs-mgt-game/SPEC.md) (archived `Medicare` and `Active Projects` detailed entries under `Past`).
   - Bookkept new lesson in [LESSONS.md](file:///Users/saehwan/repos/hs-mgt-game/LESSONS.md).

## Verification Results
- Runs `cargo fmt` and `cargo test` sequentially.
- All 271 tests pass successfully.
