# Final Handoff - Difficulty Resource Scaling v0.11.8

## Result

- Scaled starting cash and political capital for rivals based on difficulty in the genesis world creator:
  - **Easy**: Rivals start with 40 cash and 5 political capital (PC), with a conservative posture.
  - **Normal**: Rivals start with 60 cash and 8 PC, with a moderate posture (default baseline).
  - **Hard**: Rivals start with 80 cash and 12 PC, with an aggressive posture.
  - **Expert**: Rivals start with 100 cash and 15 PC, with an aggressive posture.
- Kept the player's starting resources (Riverside) invariant across all difficulties (default 60 cash and 8 PC).
- Updated CLI difficulty selection menu descriptions in `src/cli/display/prompt.rs` to show the starting resource and risk posture pressures for each difficulty tier.
- Added focused unit tests in `src/competitive/genesis_tests.rs` verifying starting resource scaling across all difficulties.

## Evidence

- Rust Tests: 293/293 passed (including the new `genesis_rivals_resources_scale_by_difficulty` test).
- Python Tests: 138/138 passed.
- Formatting and Clippy checks pass cleanly.
- State-hash Invariance: Seed-42 Normal hold-control hash remains unchanged (state hashes are invariant).
- Backward compatibility for session serialization is preserved.

## Version Boundaries

- Package: `0.11.8`
- Competitive ruleset: `competitive-ruleset-0.2.0`
- Competitive state hash: `competitive-state-hash-v9`

## PR Handoff

- Base branch: `main`
- Working branch: `feat/difficulty-resource-scaling-v0.11.8`
- Verification: formatting, clippy, Rust and Python test suites pass cleanly.
