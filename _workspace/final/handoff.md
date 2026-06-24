# Handoff

## Summary

Shipped ADR 0001 and scenario format design draft at v0.1.24. No runtime changes.

## Changed Files

- `docs/decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md`
- `docs/scenario-format-draft.md`
- `docs/decision-records/README.md`
- `ARCHITECTURE.md`, `SPEC.md`, `README.md`, `CHANGELOG.md`, `Cargo.toml`

## Verification

- `cargo fmt --check` passed
- `cargo test` passed: 82 tests
- Golden hash unchanged

## Next Slice

`feat/forecast-uncertainty-preview` — observation-only CLI forecast preview.
