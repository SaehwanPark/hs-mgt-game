# Final Handoff - Access-Loop Diagnostic

## Summary

Compared the v0.10.1 free-form Hard baseline policies against bounded
access-pledge cooldown and reported-access-threshold variants, then bumped the
package version to `0.10.2`. Three observation-driven profiles completed all 27
24-month Hard runs across seeds `42`, `43`, and `44` with zero validation
failures.

This slice does not change simulation behavior, command grammar, scenario
schemas, MCP DTOs, replay formats, state hashes, or balance values.

## Changed Files

- `docs/playtest-findings-v0.10.2.md`: new access-loop diagnostic findings.
- `docs/mcp-playtesting-guide.md`: documented the diagnostic procedure.
- `_workspace/experiments/v0.10.2-access-loop-diagnostic/run_sessions.py`: operator capture script.
- `_workspace/experiments/v0.10.2-access-loop-diagnostic/results.json`: captured session artifact.
- `SPEC.md`: completed v0.10.2 slice and Past rollup row.
- `CHANGELOG.md`: v0.10.2 release note.
- `Cargo.toml` and `Cargo.lock`: package metadata version bump.
- `LESSONS.md`: access-loop diagnostic lesson.
- `_workspace/00_input/request-summary.md`: current request framing.
- `_workspace/03_domain_qa.md`: current domain QA note.
- `_workspace/final/handoff.md`: this handoff.

## Evidence Summary

Baseline sessions repeated 162 access pledges across nine runs. Cooldown reduced
that to 72 and threshold reduced it to 60 while preserving full completion and
zero validation failures. The reduced-pledge variants also reduced access and/or
community-trust endpoints for access-heavy profiles, so the evidence supports a
guidance/operator-policy diagnostic rather than a runtime balance change.

## Verification

- Operator capture: `python3 _workspace/experiments/v0.10.2-access-loop-diagnostic/run_sessions.py`
- JSON validity: `python3 -m json.tool _workspace/experiments/v0.10.2-access-loop-diagnostic/results.json >/dev/null`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## Known Limits

- Operator policies are deterministic observation heuristics, not LLM or human play.
- Only seeds 42, 43, and 44 were exercised.
- Cooldown and threshold fallback choices are diagnostic controls, not
  recommended player strategy.
- Operator script and JSON artifact live under `_workspace/experiments/` and are
  not required for CI.

## Next Phase Dependency

Treat repetitive access pledges as a guidance and operator-policy diagnostic
unless future human or LLM evidence shows the loop persists under richer play.
Runtime or balance changes should require stronger scenario-specific,
human-learning, or domain-review evidence.
