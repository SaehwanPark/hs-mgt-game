# Implementation Plan - Monthly Operating-Outcome Debrief Linkage

## Summary

Add a small debrief formatter that renders committed player operating outcomes
next to each competitive month’s player command. Preserve all transition,
observation, replay, ruleset, and hash behavior.

## Implementation

- Add focused report and MCP tests first.
- Read the human system from `CompetitiveTransition.next`.
- Render demand, treated volume, unmet demand, revenue, cost, and signed margin.
- Keep the formatter in `src/debrief/report.rs` so CLI and MCP remain aligned.
- Update v0.11.3 project records and workspace handoffs.

## Verification

```text
cargo test debrief::report_tests::competitive_debrief_includes_player_owned_monthly_operating_results -- --test-threads=1
cargo test mcp::session::tests::competitive_debrief_includes_monthly_operating_result -- --test-threads=1
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

## Non-goals

No new simulation mechanics, actors, commands, schema fields, scenario files,
replay migration, balance tuning, or new Phase 7 matrix.

## Handoff

Commit, push, open the GitHub PR against `main`, run three independent
`code-reviewer` passes, fix all Critical/High findings, and record domain QA
as `pass` before reporting merge readiness.
