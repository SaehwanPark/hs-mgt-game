# Request Summary - Month-Summary Clarity (Phase 6 - Track 1)

## Scope
Enhance the month resolution summary in the competitive campaign CLI to display the player's resolved commands, detailed logged rival public actions, resolved attributed effects, and starting resources for the next month.

## Non-Goals
- No changes to stabilization campaign resolution rules.
- No changes to core simulation transition logic or scenario TOML schemas.
- No new dependencies or third-party crates.

## Sources
- `src/competitive/resolution.rs`
- `src/cli/campaign.rs`

## Expected Files
- `src/competitive/resolution.rs` (Modified)
- `Cargo.toml` (Modified)
- `CHANGELOG.md` (Modified)
- `SPEC.md` (Modified)

## Validation Target
- All cargo tests pass cleanly (242+ tests).
- `cargo clippy --all-targets -- -D warnings` compiles without warnings.
- `cargo fmt --check` passes cleanly.
