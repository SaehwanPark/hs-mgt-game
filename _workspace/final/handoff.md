# Final Handoff - Competitive Playtest Policy Coverage

## Summary

Extended Phase 7 scripted competitive MCP playtest policies beyond month 3 and
bumped the package version to `0.9.6`. The automated playtest runner now covers
more of the 24-month competitive command space, including newer service-line
investments, public payers, staffing, monitoring, and commitments.

This slice does not change simulation behavior, command grammar, scenario
schemas, MCP DTOs, replay formats, state hashes, or balance values.

## Changed Files

- `scripts/run_automated_playtests.py`: extended competitive scripted policies
  across the 24-month campaign.
- `docs/playtest-findings-v0.9.6.md`: new playtest-policy coverage findings.
- `docs/mcp-playtesting-guide.md`: updated automated-playtest artifact example
  and coverage description.
- `LESSONS.md`: recorded long-run scripted-policy budgeting lesson.
- `SPEC.md`: completed v0.9.6 slice and Past rollup row.
- `CHANGELOG.md`: v0.9.6 release note.
- `Cargo.toml` and `Cargo.lock`: package metadata version bump.
- `_workspace/00_input/request-summary.md`: current request framing.
- `_workspace/final/handoff.md`: this handoff.

## Evidence Summary

The scripted MCP batch completed 24 sessions: 12 stabilization sessions and 12
competitive sessions across four profiles and seeds `42`, `43`, and `44`.
No validation failures, crashes, hangs, or incomplete sessions were observed.

Competitive action coverage improved from hold-heavy month-3 scripts to
profile schedules with 45-75 action commands over three seeds. The findings are
still simulated-agent coverage evidence, not runtime balance, calibration, or
human-learning evidence.

## Verification

- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/run_automated_playtests.py --json-output _workspace/experiments/v0.9.6-playtest-policy-coverage/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.6-playtest-policy-coverage/results.json --output _workspace/experiments/v0.9.6-playtest-policy-coverage/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## Known Limits

- Batch diagnostics use MCP transition summaries and debriefs, not full replay
  artifacts.
- The findings are simulated-agent evidence, not human learning evidence.
- No raw transcript artifact is committed.
- Project-command coverage remains intentionally limited because active monthly
  draws can invalidate low-cash scripted policies late in the campaign.

## Next Phase Dependency

Future playtest-policy work should target only specific under-exercised command
families or scenario questions. Runtime or balance changes should require
stronger repeated-run, scenario-specific, or domain-review evidence.
