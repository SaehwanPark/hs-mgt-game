## Summary

- Add the v0.10.42 synthesis of consultant-advice evidence from v0.10.39–v0.10.41.
- Close the generic advice promotion gate while keeping advisor-market runtime
  work deferred.
- Update project-state, version, playtesting, QA, and handoff documentation.

## Scope

This is a documentation and evidence-synthesis change. It adds no runtime
mechanics, commands, actors, scenarios, replay fields, state-hash fields, MCP
schema changes, balance changes, or new playtest matrix.

## Verification

- JSON artifact validation for v0.10.40 and v0.10.41
- Stable v0.10.41 artifact regeneration
- Python unit tests
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1`
- Automated MCP playtests
- `git diff --check`
