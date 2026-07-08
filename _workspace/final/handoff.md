# Final Handoff - Live Retry Cash-Pressure Diagnostics

## Summary

Implemented the `v0.10.17` Phase 7 diagnostic visibility slice. The live-capture
diagnostic now reports optional live validation retry metadata and separates
cash-overrun retries from final replay validation failures.

This is evidence/reporting-only. It does not change transition logic,
validation, command grammar, scenario schemas, MCP DTOs, replay hashes, state
hash logic, or balance values.

## Changed Files

- `scripts/diagnose_runs.py`: live retry table and cash-overrun retry
  classification for live-capture artifacts.
- `tests/fixtures/live_capture_batch.json`: fixture retry metadata for focused
  diagnostic verification.
- `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`:
  regenerated with live retry signals.
- `docs/playtest-findings-v0.10.17.md` and `docs/mcp-playtesting-guide.md`:
  diagnostic findings and usage note.
- `SPEC.md`, `CHANGELOG.md`, `Cargo.toml`, `Cargo.lock`: `v0.10.17` record and
  package metadata.
- `_workspace/00_input/request-summary.md`, `_workspace/03_domain_qa.md`: harness
  handoff artifacts.

## Verification

- `python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json`
- `python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`
- `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test`

## PR Handoff

- Branch: `feat/live-retry-cash-pressure-diagnostics`
- Base: `main`
- PR: https://github.com/SaehwanPark/hs-mgt-game/pull/98

## Review Summary

- Pass 1: No script, fixture, generated diagnostic, or findings-note issues.
- Pass 2: Low handoff-bookkeeping finding: the handoff still said PR pending
  after PR #98 was opened. Fixed.
- Pass 3: No additional workflow, versioning, diagnostic, or scope findings.
- Critical/High findings: none.
- Medium/Low disposition: one Low documentation finding fixed.
- Follow-up review after Critical/High fixes: not required.
- CI/comment triage: GitHub Actions `check` passed on PR #98; no PR comments
  or reviews were present during triage.
- Merge-ready: yes.

## Known Limits

- The inputs are simulated-agent/operator-authored evidence, not human play,
  classroom learning, or empirical calibration.
- Retry metadata is optional and older artifacts may not contain it.
- Cash-overrun retry classification currently uses validation error text.
- Final metric extraction depends on current debrief text format.
