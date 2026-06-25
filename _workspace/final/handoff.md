# Handoff — Competitive Campaign Runtime I1+I2 (v0.1.29)

## Summary

Implemented CLI campaign router and month-1 executive report preview for
`competitive-regional-v1`. Stabilization demo unchanged.

## Changed files

### New

- `src/model/campaign.rs`, `src/model/campaign_tests.rs`
- `src/cli/campaign.rs`
- `src/cli/display/executive_report.rs`, `src/cli/display/executive_report_tests.rs`
- `src/competitive/mod.rs`, `src/competitive/fixtures.rs`

### Updated

- `src/cli/session.rs`, `src/cli/io.rs`, `src/cli/io_tests.rs`
- `src/cli/display/prompt.rs`, `src/cli/display/mod.rs`
- `src/cli/guidance.rs`, `src/cli/error.rs`, `src/cli/mod.rs`
- `src/model/mod.rs`, `src/model/session.rs`, `src/main.rs`, `src/lib.rs`
- `SPEC.md`, `CHANGELOG.md`, `ARCHITECTURE.md`, `README.md`, `Cargo.toml`
- `docs/core-loop-spec.md`, `docs/phase5-scope-register.md`

## Verification

- `cargo fmt --check`
- `cargo test` (129 lib + 1 golden; golden hash `6fb1ebbea564274f` unchanged)

## Known limits

- Competitive path is preview-only: no command entry or monthly loop
- Report uses mock `PlayerObservation` fixtures, not live simulation state
- Autosave resume applies to stabilization interactive runs only

## Recommended next slice

**I3:** `feat/competitive-action-economy` — AP/cash/political capital validation
before simultaneous resolver (I5) and multi-system state (I4 can parallelize with
care; ADR-0004 lists I4 before I5).

## Phase dependencies

- I4 multi-system state before I5 simultaneous resolver
- I3 action economy before competitive CLI command validation
- I8 Stata CLI after I3 and typed command shapes exist
