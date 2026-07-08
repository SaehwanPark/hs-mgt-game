# Final Handoff - Live Retry Visibility Checkpoint

## Summary

Implemented the `v0.10.20` Phase 7 evidence-routing checkpoint. The current live
retry visibility gate is now documented as complete for live-capture
classification: structured MCP validation fields are emitted, preserved by the
Python wrapper, and preferred by diagnostics while retaining legacy fallback.

This is a documentation and project-state slice. It does not change Rust runtime
mechanics, MCP DTOs, Python wrapper logic, diagnostic parser logic, command
legality, scenario schemas, replay hashes, state hash logic, action costs,
ruleset values, or balance.

## Changed Files

- `docs/playtest-findings-v0.10.20.md`: checkpoint findings, evidence limits,
  and follow-up routing.
- `docs/mcp-playtesting-guide.md`: v0.10.20 retry-visibility routing note.
- `SPEC.md`, `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`: `v0.10.20`
  project-state and version metadata.
- `_workspace/00_input/request-summary.md`: scoped request summary for this
  continuation slice.

## Verification

- `python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.20-diagnostics.md`
- `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test -- --test-threads=1`

Note: an initial parallel `cargo test` run failed once in
`cli::persistence::tests::competitive_persistence_write_load_delete_round_trip`
while reading `~/.config/hs-mgt-game/competitive_session.save`. The serial
rerun passed the full suite and this slice did not touch persistence code.

## PR Handoff

- Branch: `feat/live-retry-visibility-checkpoint`
- Base: `main`
- PR: Pending

## Review Summary

- Pass 1: Pending after PR creation.
- Pass 2: Pending after PR creation.
- Pass 3: Pending after PR creation.
- Critical/High findings: Pending after review.
- Medium/Low disposition: Pending after review.
- Follow-up review after Critical/High fixes: Pending if needed.
- CI/comment triage: Pending after PR creation.
- Merge-ready: No, pending verification, PR creation, and review loop.

## Known Limits

- This checkpoint relies on simulated-agent and operator-authored evidence, not
  human play or empirical calibration.
- The strongest live retry signal still comes from the `v0.10.15` seed `42`
  exemplar.
- Runtime tuning remains deferred until a later evidence slice identifies a
  concrete mechanic problem beyond retry classification.
