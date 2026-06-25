# Handoff — Competitive Campaign Runtime I6 (v0.1.33)

## Summary

Implemented bounded game-theory AI players per gameplay sketch §9: per-system
observation (`sim/observe_ai.rs`), `compute_ai_batch` with style-weighted scoring,
satisficing, level-1 best response, and `ai_player_{id}` tie-break stream;
`SystemMonthlyBatch.rationale`; AI-generated rival batches in month-1 resolution;
CLI seed wiring and rationale display. Stabilization demo unchanged.

## Changed files

### New

- `src/actors/ai_player.rs`
- `src/sim/observe_ai.rs`

### Updated

- `src/model/competitive_batch.rs`, `src/inputs/streams.rs`, `src/inputs/mod.rs`
- `src/actors/mod.rs`, `src/sim/mod.rs`
- `src/competitive/resolution.rs`, `src/competitive/mod.rs`, `src/cli/campaign.rs`
- `tests/golden_competitive_seed42.rs`
- `SPEC.md`, `CHANGELOG.md`, `ARCHITECTURE.md`, `README.md`, `Cargo.toml`
- `docs/phase5-scope-register.md`, `docs/gameplay-competitive-sketch.md`

## Verification

- `cargo fmt --check`
- `cargo test` (178 lib + 2 golden; stabilization hash `6fb1ebbea564274f` unchanged)
- Competitive month-1 golden hash `e68f683da77d7c2f` at Normal difficulty, seed 42

## Known limits

- Human month-1 batch still preset (I8 interactive CLI)
- Effect queue enqueues but does not apply delayed resolutions (I7)
- No multi-month competitive loop yet (I7)
- Competitive replay artifact format not yet versioned

## Recommended next slice

**I7:** `feat/competitive-events-delays` — random events, delayed effect queue
application, annual policy tick, 2–3 month demo loop.

**Then I8:** Stata-like CLI for human monthly command entry.

## Phase dependencies

- I7 events/delays require I5 effect queue and I6 stable monthly resolution (complete)
- I8 Stata CLI requires stable command batch API from I5–I6 (complete)
