# Handoff — Competitive Campaign Runtime I7 (v0.1.34)

## Summary

Implemented competitive environment tick, delayed effect application, institution
NPC phase, and multi-month resolution loop. Month start applies `monthly_events`
and `annual_policy` streams plus due `PendingEffect` entries before player
decisions. CLI previews months 2–3 after month-1 resolution.

## Changed files

### New

- `src/model/competitive_resolved.rs`
- `src/inputs/resolve_competitive.rs`
- `src/sim/effects_competitive.rs`
- `src/competitive/month_loop.rs`

### Updated

- `src/model/competitive_world.rs` (`PendingEffectKind`)
- `src/sim/transition_competitive.rs`, `src/sim/mod.rs`
- `src/competitive/resolution.rs`, `src/competitive/mod.rs`
- `src/cli/campaign.rs`, `tests/golden_competitive_seed42.rs`
- `Cargo.toml`, `CHANGELOG.md`

## Verification

- `cargo fmt --check`, `cargo test` (185 tests)
- Competitive golden hash `88d07f9e1bbd6f04` at seed 42
- Stabilization hash unchanged

## Recommended next slice

**I8:** `feat/competitive-stata-cli` — Stata-like parser and interactive human monthly entry.
