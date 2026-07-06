# Final Handoff - Strategy-Space Diagnostics Artifact

## Summary

Added a Phase 7 strategy-space diagnostics artifact path and bumped the package
version to `0.9.5`. The automated MCP playtest runner can now optionally write
a compact JSON batch artifact, and the diagnostics script can read that artifact
while preserving its existing competitive replay JSON support.

This slice does not change simulation behavior, command grammar, scenario
schemas, MCP DTOs, replay formats, state hashes, or balance values.

## Changed Files

- `scripts/run_automated_playtests.py`: optional `--json-output` batch artifact.
- `scripts/diagnose_runs.py`: automated playtest batch JSON diagnostics.
- `docs/playtest-findings-v0.9.5.md`: new diagnostic findings report.
- `docs/mcp-playtesting-guide.md`: documented the JSON artifact workflow.
- `SPEC.md`: completed v0.9.5 slice and Past rollup row.
- `CHANGELOG.md`: v0.9.5 release note.
- `Cargo.toml` and `Cargo.lock`: package metadata version bump.
- `_workspace/00_input/request-summary.md`: current request framing.
- `_workspace/final/handoff.md`: this handoff.

## Evidence Summary

The scripted MCP batch completed 24 sessions: 12 stabilization sessions and 12
competitive sessions across four profiles and seeds `42`, `43`, and `44`.
No validation failures, crashes, hangs, or incomplete sessions were observed.

The diagnostic output highlights that current competitive scripted policies act
mostly in the first three months and then hold through month 24. That is a
playtest-coverage finding, not a runtime balance finding.

## Verification

- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/run_automated_playtests.py --json-output _workspace/experiments/v0.9.5-playtest-batch/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.5-playtest-batch/results.json --output _workspace/experiments/v0.9.5-playtest-batch/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## Known Limits

- Batch diagnostics use MCP transition summaries and debriefs, not full replay
  artifacts.
- The findings are simulated-agent evidence, not human learning evidence.
- No raw transcript artifact is committed.

## Next Phase Dependency

Future playtest-policy work should extend competitive scripted profiles beyond
month 3 and directly exercise newer service-line commands before runtime or
balance changes are considered.
