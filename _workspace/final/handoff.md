# Final Handoff - Static-vs-Adaptive Live Capture

## Summary

Implemented the `v0.10.13` Phase 7 static-vs-adaptive live-capture slice. The
existing MCP wrapper and diagnostics path now have one artifact comparing static
deterministic profile policies against the existing difficulty-adaptive wrapper
across four automated playtest profiles, seeds `42`, `43`, and `44`, and
Normal/Hard competitive difficulty tiers.

This is evidence/reporting-only. It does not change transition logic,
validation, command grammar, scenario schemas, MCP DTOs, replay hashes, state
hashes, or balance values.

## Changed Files

- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py`:
  deterministic static/adaptive matrix runner.
- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`:
  48-session live-capture artifact.
- `_workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md`:
  generated diagnostic report.
- `docs/playtest-findings-v0.10.13.md`: findings and evidence limits.
- `docs/mcp-playtesting-guide.md`: diagnostic command.
- `_workspace/00_input/request-summary.md`, `_workspace/01_evidence_map.md`,
  `_workspace/03_domain_qa.md`: harness handoff artifacts.
- `SPEC.md`, `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`: `v0.10.13` record and
  package metadata.
- `LESSONS.md`: workflow lesson on using artifact metadata before expanding
  diagnostics.

## Verification

- `python3 -m py_compile scripts/play_game.py`
- `python3 -m py_compile scripts/run_automated_playtests.py`
- `python3 -m py_compile _workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py`
- `python3 _workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json --output _workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md`
- `python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
- `python3 -m py_compile scripts/diagnose_runs.py`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## PR Handoff

- Branch: `feat/live-static-adaptive-capture`
- Base: `main`
- PR: https://github.com/SaehwanPark/hs-mgt-game/pull/94

## Review Summary

- Pass 1: Low handoff-bookkeeping finding: PR/review status still said pending
  after PR #94 was opened. Fixed in this handoff.
- Pass 2: No additional actionable findings; artifact shape, run counts,
  validation totals, static/adaptive labels, and generated findings matched the
  captured results.
- Pass 3: No additional actionable findings; version metadata, evidence-limit
  language, no-runtime-change claims, and handoff artifacts matched scope.
- Critical/High findings: none.
- Medium/Low disposition: one Low documentation finding fixed.
- Follow-up review after Critical/High fixes: not required.
- CI/comment triage: pending
- Merge-ready: pending

## Known Limits

- The runs are simulated-agent evidence, not human play, classroom learning, or
  empirical calibration.
- Final metric extraction depends on current debrief text format.
- Static/adaptive differences are mediated by the existing policy wrapper, so
  this does not prove difficulty balance or strategic richness.
