# Handoff — Competitive Campaign Runtime I4 (v0.1.31)

## Summary

Implemented competitive multi-system player state per ADR-0004: typed
`CompetitiveWorldState`, difficulty-scoped genesis fixtures for Riverside plus
K named AI rivals, genesis-derived human observation metrics, and a roster
display in the competitive campaign preview. Stabilization demo unchanged.

Also reconciled `SPEC.md` with `docs/spec-past-archive.md` (slice on
`refactor/spec-cleanup`).

## Changed files

### New

- `docs/spec-past-archive.md`
- `src/model/competitive_world.rs`
- `src/competitive/genesis.rs`, `src/competitive/genesis_tests.rs`

### Updated

- `SPEC.md`, `docs/phase5-scope-register.md`
- `src/model/mod.rs`, `src/competitive/mod.rs`, `src/competitive/fixtures.rs`
- `src/cli/campaign.rs`
- `CHANGELOG.md`, `ARCHITECTURE.md`, `README.md`, `Cargo.toml`

## Verification

- `cargo fmt --check`
- `cargo test` (153 lib + 1 golden; golden hash `6fb1ebbea564274f` unchanged)

## Known limits

- Genesis only; no `transition_competitive()` or monthly loop
- Market/policy narrative bullets in executive report remain partly fixture text
- Autosave resume applies to stabilization interactive runs only

## Recommended next slice

**I5:** `feat/competitive-simultaneous-resolver` — simultaneous monthly action
resolver and partial rival observability per ADR-0003.

**Then I6:** bounded game-theory AI players with rationales.

## Phase dependencies

- I5 resolver before I6 AI players and I7 events/delays
- I8 Stata CLI can parallelize after I5 command batch shapes stabilize
