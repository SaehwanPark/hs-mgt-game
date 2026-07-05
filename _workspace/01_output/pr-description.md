# Pull Request Description: Implement Exemplary Competitive Scenario & Timeline Events

## Summary
This PR implements the `competitive-exemplary-v1` scenario, including its timeline events, delayed consequences, and the labor strike and Certificate of Need (CON) legal objection mechanics.

## Changes Included
- **Scenario setup file:** Added [scenarios/competitive-exemplary-v1.toml](file:///Users/saehwan/repos/hs-mgt-game/scenarios/competitive-exemplary-v1.toml) specifying initial assets and capacities for Riverside Community Health, Northlake Health, and Summit Care.
- **Dynamic event tracking:** Added `scenario_id` and `event_metadata` tracking to the competitive world state, allowing the engine to dynamically record mid-run scenario state variables.
- **Workforce Wage Settlement Pledge:** Added `PledgeType::Workforce` to represent wage agreement commitments, allowing the player to commit 1 AP, 0 cash, and 1 PC to settle labor disputes. Added parser, autocomplete, help description, and AI scoring support.
- **Timeline rules (`src/sim/effects_competitive.rs` and `src/sim/transition_competitive.rs`):**
  - **Month 8 Burnout:** Drops Riverside workforce trust by 15% and warns the player of a nurse strike if the nurse staffing ratio is under 80%.
  - **Month 10 Active Strike:** Activates a 2-month strike if wages were not settled, halving effective bed/outpatient capacities, postponing capital projects, and costing $30k/month for travel nurses.
  - **Month 10 CON legal challenge:** Automatically handles clinic network project objections using 3 PC or $100k cash if available, or delays project completion by 3 months.
  - **Month 12 Blue Shield Contract Renewal:** Drops commercial patient volume by 40% (reflected in `market_share_index`) if negotiations were not performed.
  - **Month 18 EHR & Strike Consequences:** Deducts $20k/month for data system lag if EHR migration was underfunded by Month 15, and drops community trust by 20% / market share by 10% if a strike occurred.
- **Documentation & versioning:** Bumped version to `0.5.6` in `Cargo.toml`. Documented changes in `CHANGELOG.md`, `SPEC.md`, and added learnings to `LESSONS.md`.

## Verification Target
- Executed `cargo test` verifying all 260 unit and integration tests compile and pass successfully.
- Added comprehensive colocated tests in `src/sim/transition_competitive.rs` asserting burnout, wage commitments, active strike delays, CON legal challenges, and out-of-network/EHR lag penalties.
- Added integration test in `tests/scenario_selection_tests.rs` verifying successful TOML parsing and scenario validation.

## Outstanding Issues
- None. All requirements have been implemented and verified.
