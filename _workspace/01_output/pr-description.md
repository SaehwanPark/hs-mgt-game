## Summary

- Add the v0.10.54 project-limit recovery capture across Hard seeds 42–44.
- Preserve the third-project rejection, unchanged actor-visible turn,
  structured response shape, safe retry, transition history, and debrief.
- Keep validation-hint and runtime promotion deferred because no unexplained
  recovery failure was identified.

## Scope

This is a bounded Phase 7 evidence change. It adds no runtime mechanics,
commands, actors, scenarios, replay fields, state-hash fields, MCP schema
changes, difficulty changes, scoring changes, balance changes, or debrief
behavior changes.

## Verification

- Eight focused project-limit tests
- Stable JSON and Markdown artifact regeneration
- Full Python unit-test suite
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- Automated MCP playtests
- `git diff --check`
