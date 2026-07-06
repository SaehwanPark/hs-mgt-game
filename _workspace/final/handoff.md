# Final Handoff - Free-Form Hard Competitive Playtest Synthesis

## Summary

Collected bounded free-form MCP competitive sessions at Hard difficulty on the
full 24-month campaign and bumped the package version to `0.10.0`. Three
observation-driven profiles (Fiscal Steward, Access Expansion Advocate,
First-Time Executive) completed seed-42 Hard runs with zero validation failures.
Findings compare free-form endpoints against v0.9.9 difficulty-adaptive scripted
Hard baselines.

This slice does not change simulation behavior, command grammar, scenario
schemas, MCP DTOs, replay formats, state hashes, or balance values.

## Changed Files

- `docs/playtest-findings-v0.10.0.md`: new free-form Hard competitive findings.
- `docs/mcp-playtesting-guide.md`: documented free-form Hard competitive procedure.
- `SPEC.md`: completed v0.10.0 slice and Past rollup row.
- `CHANGELOG.md`: v0.10.0 release note.
- `Cargo.toml` and `Cargo.lock`: package metadata version bump.
- `_workspace/00_input/request-summary.md`: current request framing.
- `_workspace/final/handoff.md`: this handoff.

## Evidence Summary

Three Hard competitive sessions at seed 42 completed 24 months each with zero
validation failures. Free-form endpoints diverged materially from v0.9.9
adaptive scripted Hard baselines: cash 38–60 versus 7–20, access 84–100 versus
72–75, community trust 72–100 versus 66–67. All three free-form final hashes
differ from each other and from scripted Hard seed-42 hashes.

The findings are simulated-agent validation evidence, not balance, calibration,
or human-learning evidence.

## Verification

- Operator capture: `python3 _workspace/experiments/v0.10.0-free-form-hard/run_sessions.py`
- `python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## Known Limits

- Operator policies are deterministic observation heuristics, not LLM or human play.
- Only seed 42 was exercised in this slice.
- Access Expansion Advocate and First-Time Executive entered repetitive
  commitment loops under persistent scrutiny cues.
- Operator script and JSON artifact live under `_workspace/experiments/` and are
  not required for CI.

## Next Phase Dependency

Extend free-form Hard evidence to seeds 43 and 44 before broader
strategy-diversity claims. Runtime or balance changes should require stronger
repeated-run, scenario-specific, or domain-review evidence.
