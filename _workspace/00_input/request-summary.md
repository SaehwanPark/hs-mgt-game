# Request Summary - Difficulty Resource Scaling v0.11.8

## Scope

- Scale rival starting cash and political capital based on difficulty in the genesis world creator:
  - **Easy**: Rivals start with 40 cash and 10 political capital (PC), with a conservative posture.
  - **Normal**: Rivals start with 60 cash and 15 PC, with a moderate posture (default baseline).
  - **Hard**: Rivals start with 80 cash and 20 PC, with an aggressive posture.
  - **Expert**: Rivals start with 100 cash and 25 PC, with an aggressive posture.
- Keep the player's starting resources (Riverside) invariant across all difficulties (default 60 cash and 15 PC).
- Update CLI difficulty selection menu descriptions in `src/cli/display/prompt.rs` to show the starting resource and risk posture pressures for each difficulty tier.
- Ensure Normal difficulty seed-42 hold-control hash remains completely invariant.
- Update the package version to `0.11.8`.
- Complete the feature branch setup, verification, PR handoff, and review loop.

## Non-goals

- No change to the player's starting resources.
- No changes to state-hash schemas.
- No changes to scenario files or general ruleset files.

## Sources

- `docs/expansion-proposal-review.md` (Proposal 1: Difficulty Expansion)
- `SPEC.md` (Ranked next-development queue - Track 2: Difficulty depth and winnability)
- `docs/roadmap.md` (Phase 7 validation and educational gates)

## Expected files

- Updated `src/competitive/genesis.rs` (setting rival starting cash/PC based on difficulty).
- Updated `src/cli/display/prompt.rs` (updating difficulty menu text).
- Updated `Cargo.toml`, `CHANGELOG.md`, `SPEC.md`, and workspace files.

## Validation target

- All 292 Rust tests and 138 Python tests pass.
- Verification of seed-42 Normal state-hash invariance.
