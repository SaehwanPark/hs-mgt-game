# Final Handoff - Difficulty-Adaptive Playtest Policies

## Summary

Added a targeted Phase 7 automated MCP playtest mode for difficulty-adaptive
competitive policies and bumped the package version to `0.9.9`. The harness runs
baseline scripted profiles at Easy and Hard difficulty with rival-aware command
adjustments on Hard (reduced aggressive invests, added monitors/holds, workforce-
commit preference when trust is low). Batch diagnostics now include an adaptive
action-frequency comparison section.

This slice does not change simulation behavior, command grammar, scenario
schemas, MCP DTOs, replay formats, state hashes, or balance values.

## Changed Files

- `scripts/run_automated_playtests.py`: added `--target difficulty-adaptive`,
  `adapt_command`, and `with_difficulty` policy wrapper.
- `scripts/diagnose_runs.py`: added difficulty-adaptive action comparison notes.
- `docs/playtest-findings-v0.9.9.md`: new targeted difficulty-adaptive findings.
- `docs/mcp-playtesting-guide.md`: documented the difficulty-adaptive target.
- `SPEC.md`: completed v0.9.9 slice and Past rollup row.
- `CHANGELOG.md`: v0.9.9 release note.
- `Cargo.toml` and `Cargo.lock`: package metadata version bump.
- `_workspace/00_input/request-summary.md`: current request framing.
- `_workspace/final/handoff.md`: this handoff.

## Evidence Summary

The targeted MCP batch completed 36 sessions: 12 stabilization sessions and 24
competitive sessions across Easy and Hard difficulty, four baseline profiles,
and seeds `42`, `43`, `44`. No validation failures, crashes, hangs, or
incomplete sessions were observed.

Hard adaptive policies increased monitor commands (147 vs 84 pooled) and
differentiated Capacity Growth and Balanced Strategy endpoints across tiers.
Naive First-Time remained unchanged because hold-heavy static commands bypass
most adaptation rules. The findings are simulated-agent validation evidence,
not balance, calibration, or human-learning evidence.

## Verification

- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/run_automated_playtests.py --target difficulty-adaptive --json-output _workspace/experiments/v0.9.9-difficulty-adaptive/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.9-difficulty-adaptive/results.json --output _workspace/experiments/v0.9.9-difficulty-adaptive/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## Known Limits

- Batch diagnostics use MCP transition summaries and debriefs, not full replay
  artifacts.
- Adaptation rules are deterministic heuristics over observation text, not
  LLM or best-response play.
- Hold-heavy profiles can still mask difficulty-tier differences in player-facing
  debrief metrics.
- No raw transcript artifact is committed.

## Next Phase Dependency

Future difficulty-aware playtest work should use free-form agent profiles at
Hard difficulty when scripted heuristics are insufficient. Runtime or balance
changes should require stronger repeated-run, scenario-specific, or domain-review
evidence.
