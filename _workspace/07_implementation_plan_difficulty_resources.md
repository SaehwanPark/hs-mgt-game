# Operational Coding Plan - Difficulty Resource Scaling v0.11.8

## Task restatement

Scale rival starting cash and political capital at genesis according to the chosen difficulty level, and display these resource details in the difficulty selection menu. Maintain full backwards compatibility, state-hash invariance for `Normal` difficulty, and player starting resource invariance.

## Current understanding

- Starting resources for systems are initialized in `src/competitive/genesis.rs` inside `genesis_competitive_world_with_ruleset`.
- Riverside (the human player) uses `PlayerResources::genesis(difficulty, ruleset)`.
- Rivals currently use `PlayerResources::genesis(difficulty, ruleset)`, which sets their cash to `ruleset.starting_cash` (60) and PC to `ruleset.starting_political_capital` (15).
- We want to adjust rivals' starting cash and PC based on `difficulty` while keeping Normal difficulty unchanged.
- The CLI menu displaying difficulty choices is defined in `src/cli/display/prompt.rs` in `difficulty_menu_lines`.

## Minimal implementation plan

1. **Update Genesis Resource Setup**:
   - In `src/competitive/genesis.rs`, inside `genesis_competitive_world_with_ruleset`:
     - Modify the rival initialization loop so that each rival's resources are scaled based on the active `difficulty`:
       - `Difficulty::Easy` -> cash = 40, political_capital = 10
       - `Difficulty::Normal` -> cash = 60, political_capital = 15 (unchanged)
       - `Difficulty::Hard` -> cash = 80, political_capital = 20
       - `Difficulty::Expert` -> cash = 100, political_capital = 25
2. **Update CLI Difficulty Menu**:
   - In `src/cli/display/prompt.rs`, update `difficulty_menu_lines` to describe the starting resources and posture of rivals:
     - Easy: `style::option_line("1", "Easy", "1 AI rival · 4 AP/month (Rivals: 40 cash / 10 PC, Conservative)")`
     - Normal: `style::option_line("2", "Normal", "2 AI rivals · 3 AP/month (Rivals: 60 cash / 15 PC, Moderate) (default)")`
     - Hard: `style::option_line("3", "Hard", "3 AI rivals · 3 AP/month (Rivals: 80 cash / 20 PC, Aggressive)")`
     - Expert: `style::option_line("4", "Expert", "4 AI rivals · 2 AP/month (Rivals: 100 cash / 25 PC, Aggressive)")`
3. **Verify and Update Tests**:
   - Add unit tests in `src/competitive/genesis_tests.rs` verifying that starting resources of rivals are scaled correctly by difficulty.
   - Verify that all Rust and Python tests pass.
4. **Governance Updates**:
   - Bump package version to `0.11.8` in `Cargo.toml`.
   - Update `CHANGELOG.md` and `SPEC.md`.

## Files and functions likely to change

- `src/competitive/genesis.rs`: Modify rival resource assignment in `genesis_competitive_world_with_ruleset`.
- `src/cli/display/prompt.rs`: Update `difficulty_menu_lines`.
- `src/competitive/genesis_tests.rs`: Add unit tests for resource scaling.
- `Cargo.toml`: Bump version to `0.11.8`.
- `CHANGELOG.md`: Document changes under `[0.11.8]`.
- `SPEC.md`: Update `Present` and `Future` section and version entries.

## Non-goals

- No change to player (Riverside) starting resources (always 60 cash / 15 PC).
- No modification to ruleset structs or scenario loading files.
- No changes to state-hash schemas.

## Verification

Run the test suite sequentially:
- `cargo test --all -- --test-threads=1`
- `python3 -m unittest discover -s tests -p "test_*.py"`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
