# Final Handoff - Difficulty-Tier Playtest Synthesis

## Summary

Added a targeted Phase 7 automated MCP playtest mode for competitive difficulty-
tier coverage and bumped the package version to `0.9.8`. The harness runs
baseline scripted profiles at Easy and Hard difficulty across seeds `42`, `43`,
and `44`. Batch diagnostics now report outcomes grouped by difficulty and by
profile-by-difficulty cross-tab.

This slice does not change simulation behavior, command grammar, scenario
schemas, MCP DTOs, replay formats, state hashes, or balance values.

## Changed Files

- `scripts/run_automated_playtests.py`: added `--target difficulty-sweep`.
- `scripts/diagnose_runs.py`: added per-difficulty batch reporting.
- `docs/playtest-findings-v0.9.8.md`: new targeted difficulty-tier findings.
- `docs/mcp-playtesting-guide.md`: documented the difficulty-sweep target.
- `SPEC.md`: completed v0.9.8 slice and Past rollup row.
- `CHANGELOG.md`: v0.9.8 release note.
- `Cargo.toml` and `Cargo.lock`: package metadata version bump.
- `_workspace/00_input/request-summary.md`: current request framing.
- `_workspace/final/handoff.md`: this handoff.

## Evidence Summary

The targeted MCP batch completed 36 sessions: 12 stabilization sessions and 24
competitive sessions across Easy and Hard difficulty, four baseline profiles,
and seeds `42`, `43`, and `44`. No validation failures, crashes, hangs, or
incomplete sessions were observed.

Easy and Hard runs produce different committed state hashes because rival
composition differs by difficulty tier, but the fixed scripted profiles produce
identical final player tradeoff metrics for the same seed and profile across
tiers. The findings are simulated-agent validation evidence, not balance,
calibration, or human-learning evidence.

## Verification

- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/run_automated_playtests.py --target difficulty-sweep --json-output _workspace/experiments/v0.9.8-difficulty-sweep/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.8-difficulty-sweep/results.json --output _workspace/experiments/v0.9.8-difficulty-sweep/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## Known Limits

- Batch diagnostics use MCP transition summaries and debriefs, not full replay
  artifacts.
- Scripted policies do not adapt to difficulty-tier rival counts or CPU budgets.
- Identical player endpoints across Easy/Hard do not prove difficulty is
  ineffective; they show static scripted commands mask rival-pressure differences
  in player-facing debrief metrics.
- No raw transcript artifact is committed.

## Next Phase Dependency

Future difficulty-aware playtest work should use rival-adaptive scripted
policies or free-form agent profiles when testing whether difficulty tiers
change strategic outcomes. Runtime or balance changes should require stronger
repeated-run, scenario-specific, or domain-review evidence.
