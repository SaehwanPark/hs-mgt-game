# Live-Capture Diagnostics v0.10.10

- **Status:** Phase 7 strategy-space diagnostics
- **Date:** 2026-07-07
- **Code version:** 0.10.10
- **Source artifact:** `_workspace/experiments/v0.10.9-live-mcp-capture/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md`

This slice extends the existing diagnostics script so it can read the live MCP
capture artifact shape introduced in v0.10.9. It is a reporting/tooling slice,
not a new playtest batch and not a runtime mechanics change.

## Findings

1. `scripts/diagnose_runs.py` now parses live-capture artifacts and reports each
   profile's completed months, final metrics parsed from debrief text,
   validation failures, access pledges, final hash, and action frequencies.
2. The v0.10.9 live-capture artifact remains conservative: all three profiles
   completed 24 months with zero validation failures, and only Access Operations
   made an access pledge.
3. The report is useful for strategy-space review because it converts the large
   observation-by-observation JSON into compact profile and action-frequency
   tables.

## Evidence Limits

- This is derived from three deterministic persona policies, one seed, one
  difficulty, and one campaign.
- The diagnostic parses debrief text for final metrics; it does not expose hidden
  active-play state or change MCP DTOs.
- Do not use this report to justify access-pledge cooldowns, pledge-effect
  tuning, balance changes, empirical calibration, policy-validity claims, or
  human-learning claims.

## Verification

```bash
python3 -m py_compile scripts/diagnose_runs.py
python3 scripts/diagnose_runs.py tests/fixtures/mock_replay.json
python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.9-live-mcp-capture/results.json --output _workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.9-live-mcp-capture/results.json >/dev/null
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
