# Handoff — Competitive Multi-Month Loop (v0.1.36)

## Summary

Implemented a bounded three-month competitive campaign loop in the CLI preview.
The loop reuses the existing deterministic monthly resolver, AI batches,
event/delay tick, institution phase, executive report renderer, and Stata-like
command parser over one evolving `CompetitiveWorldState`.

## Changed files

### Updated runtime

- `src/cli/campaign.rs`
- `src/competitive/month_loop.rs`

### Updated project state

- `Cargo.toml`, `Cargo.lock`, `CHANGELOG.md`
- `README.md`, `SPEC.md`, `ARCHITECTURE.md`
- `_workspace/00_input/request-summary.md`
- `_workspace/final/handoff.md`

## Verification

- `cargo fmt`
- `cargo test` (193 unit tests plus integration tests)
- Competitive seed-42 golden hash unchanged (`88d07f9e1bbd6f04`)
- Stabilization seed-42 golden hash unchanged (`6fb1ebbea564274f`)

## Known limits

- Competitive preview remains bounded to three months, not the full 24-month
  campaign.
- Competitive autosave, replay artifact export, syntax highlighting,
  autocomplete, and scenario loading remain deferred.
