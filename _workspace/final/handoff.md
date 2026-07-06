# Final Handoff - Agent Playtest Synthesis After Service-Line Expansion

## Summary

Recorded a Phase 7 scripted AI-agent playtest synthesis for the current
post-ASC prototype and bumped the package version to `0.9.4`. This slice is
documentation and evidence only; it does not change simulation behavior,
command grammar, scenario schemas, MCP DTOs, state hashes, or balance values.

## Changed Files

- `docs/playtest-findings-v0.9.4.md`: new findings report for the scripted MCP
  batch.
- `SPEC.md`: completed v0.9.4 slice and Past rollup row.
- `CHANGELOG.md`: v0.9.4 release note.
- `Cargo.toml` and `Cargo.lock`: package metadata version bump.
- `_workspace/00_input/request-summary.md`: current request framing.
- `_workspace/final/handoff.md`: this handoff.

## Evidence Summary

The scripted MCP batch completed 24 sessions: 12 stabilization sessions and 12
competitive sessions across four profiles and seeds `42`, `43`, and `44`.
No validation failures, crashes, or hangs were observed.

Key metric ranges:

- Stabilization: cash `15-70`, access `73-93`, workforce trust `64-68`,
  community trust `57-75`, policy pressure `35-59`.
- Competitive: cash `5-60`, access `70-73`, staffed beds `118-123`,
  workforce trust `30-60`, community trust `64-66`, political capital `15`.

## Verification

- `python3 scripts/run_automated_playtests.py` completed all scripted sessions.
- `cargo fmt --check` passed.
- `cargo clippy --all-targets -- -D warnings` passed.
- `cargo test` passed 282 tests.

## Known Limits

- The findings are simulated-agent evidence, not human learning evidence.
- The run matrix supports smoke-style gameplay and explanation checks, not
  empirical calibration or balance conclusions.
- No raw transcript artifact was committed because the existing harness prints
  summary tables and the findings document captures the relevant evidence.

## Next Phase Dependency

Future runtime, balance, or actor expansion should cite a concrete playtest,
authoring, debrief, or domain-review finding before broadening the model.
