# Competitive Debrief Comparison Surface v0.10.29

## Summary

Adds a Phase 7 debrief comparison surface for `competitive-regional-v1`. The
new findings note helps instructors and reviewers compare decision quality,
outcome quality, cash runway, durable follow-through, rival pressure, and
debrief traceability across repeated competitive runs while keeping runtime
mechanics and balance unchanged.

## Changes

- Added `docs/playtest-findings-v0.10.29.md`.
- Updated `docs/mcp-playtesting-guide.md` with the `v0.10.29` routing
  checkpoint.
- Updated `SPEC.md`, `CHANGELOG.md`, `Cargo.toml`, and `Cargo.lock` for
  `0.10.29`.
- Refreshed `_workspace/00_input/request-summary.md`,
  `_workspace/03_domain_qa.md`, and `_workspace/final/handoff.md`.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json >/dev/null
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.29-live-diagnostics.md
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.29-access-diagnostics.md
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
git diff --check
```

## Non-Goals

- No runtime simulation, command validation, scenario schema, stochastic input,
  replay artifact, state hash, MCP DTO, Python wrapper, diagnostic parser, or
  command-surface change.
- No access-pledge cooldown, effect tuning, command-cost change, difficulty
  adjustment, scoring redesign, balance change, hidden strategy taxonomy,
  empirical calibration claim, policy-validity claim, human-learning claim, or
  validated learner archetype.
