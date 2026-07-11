## Summary

- Expose accepted `AscUnit` projects in the actor-visible `In-flight projects`
  observation.
- Add deterministic v0.10.55 Hard-seed evidence across seeds 42–44.
- Preserve the existing third-project rejection, same-turn state, safe retry,
  debrief explanation, and v0.10.54 state hashes.

## Scope

This is a bounded Phase 7 observability correction. It changes one existing
observation formatter and adds focused tests/evidence. It does not change
project limits, validation hints, transition rules, commands, scenarios,
replay formats, MCP schemas, difficulty, scoring, balance, or debrief wording.

## Verification

- Five focused ASC observation evidence tests
- Deterministic JSON and Markdown artifact regeneration
- Full Python unit-test suite
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- Automated MCP playtests
- `git diff --check`
