# Final Handoff - Project-Command Playtest Diagnostics

## Summary

Added a targeted Phase 7 automated MCP playtest mode for competitive
capital-project command coverage and bumped the package version to `0.9.7`.
The diagnostic script now reports project-command counts, project kinds, final
active projects, and final monthly project draws for automated batch artifacts.

This slice does not change simulation behavior, command grammar, scenario
schemas, MCP DTOs, replay formats, state hashes, or balance values.

## Changed Files

- `scripts/run_automated_playtests.py`: added `--target project-coverage`.
- `scripts/diagnose_runs.py`: added project-command and project-kind reporting.
- `docs/playtest-findings-v0.9.7.md`: new targeted project-command findings.
- `docs/mcp-playtesting-guide.md`: documented the target command.
- `LESSONS.md`: recorded project-command concurrency lesson.
- `SPEC.md`: completed v0.9.7 slice and Past rollup row.
- `CHANGELOG.md`: v0.9.7 release note.
- `Cargo.toml` and `Cargo.lock`: package metadata version bump.
- `_workspace/00_input/request-summary.md`: current request framing.
- `_workspace/final/handoff.md`: this handoff.

## Evidence Summary

The targeted MCP batch completed 6 sessions: 3 stabilization sessions and 3
competitive sessions across the Project Coverage profile and seeds `42`, `43`,
and `44`. No validation failures, crashes, hangs, or incomplete sessions were
observed in the successful v0.9.7 run.

The competitive target exercised five project kinds across three seeds:
EmergencyPavilion, ClinicNetwork, AscUnit, NeurologyUnit, and InfusionCenter.
The findings are simulated-agent command-path coverage evidence, not runtime
balance, calibration, or human-learning evidence.

## Verification

- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `python3 scripts/run_automated_playtests.py --target project-coverage --json-output _workspace/experiments/v0.9.7-project-command-coverage/results.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.7-project-command-coverage/results.json --output _workspace/experiments/v0.9.7-project-command-coverage/diagnostics.md`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## Known Limits

- Batch diagnostics use MCP transition summaries and debriefs, not full replay
  artifacts.
- The findings are simulated-agent evidence, not human learning evidence.
- No raw transcript artifact is committed.
- Project-command coverage remains intentionally limited because active monthly
  draws and scenario-driven delays can invalidate project-heavy policies late in
  the campaign.

## Next Phase Dependency

Future playtest-policy work should target only specific under-exercised command
families or scenario questions. Runtime or balance changes should require
stronger repeated-run, scenario-specific, or domain-review evidence.
