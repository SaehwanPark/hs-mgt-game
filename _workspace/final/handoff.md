# Handoff — Competitive Campaign Runtime I5 (v0.1.32)

## Summary

Implemented simultaneous monthly action resolution per ADR-0003: batch aggregation
in `sim/resolve.rs`, `transition_competitive()` with public action log and pending
effect enqueue, `observe_for_human()` with 1-month lag rival intel and monitor
depth support, CLI month-1 resolution demo with month-2 executive report preview,
and competitive golden test. Stabilization demo unchanged.

## Changed files

### New

- `src/model/competitive_batch.rs`, `src/model/competitive_history.rs`, `src/model/competitive_hash.rs`
- `src/sim/resolve.rs`, `src/sim/transition_competitive.rs`, `src/sim/observe_competitive.rs`
- `src/competitive/resolution.rs`
- `tests/golden_competitive_seed42.rs`

### Updated

- `src/model/mod.rs`, `src/model/resources.rs`
- `src/sim/mod.rs`, `src/cli/campaign.rs`, `src/competitive/mod.rs`
- `SPEC.md`, `CHANGELOG.md`, `ARCHITECTURE.md`, `README.md`, `Cargo.toml`
- `docs/phase5-scope-register.md`, `docs/core-loop-spec.md`

## Verification

- `cargo fmt --check`
- `cargo test` (171 lib + 2 golden; stabilization hash `6fb1ebbea564274f` unchanged)
- Competitive month-1 golden hash `05a422b51a2c24e8` at Normal difficulty

## Known limits

- Preset batches only; no AI decision logic (I6)
- Effect queue enqueues but does not apply delayed resolutions (I7)
- No interactive monthly command entry (I8)
- Competitive replay artifact format not yet versioned

## Recommended next slice

**I6:** `feat/competitive-ai-players` — bounded game-theory AI players with
inspectable rationales.

**Then I7:** random events, delayed effect queue application, annual policy tick.

**Then I8:** Stata-like CLI (can parallelize after I6 batch generation stabilizes).

## Phase dependencies

- I6 AI players require I5 batch shapes and resolver (complete)
- I7 events/delays require I5 effect queue and transition_competitive (complete)
- I8 Stata CLI requires stable command batch API from I5 (complete)
