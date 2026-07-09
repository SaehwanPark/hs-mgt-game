# Competitive Strategy-Space Synthesis v0.10.28

## Summary

Adds a Phase 7 strategy-space synthesis for `competitive-regional-v1`. The new
findings note compares finance-first, access-heavy, workforce-protective, and
growth-oriented signals across existing competitive evidence while keeping
runtime mechanics and balance unchanged.

## Changes

- Added `docs/playtest-findings-v0.10.28.md`.
- Updated `docs/mcp-playtesting-guide.md` with the `v0.10.28` routing
  checkpoint.
- Updated `SPEC.md`, `CHANGELOG.md`, `Cargo.toml`, and `Cargo.lock` for
  `0.10.28`.
- Refreshed `_workspace/00_input/request-summary.md`,
  `_workspace/03_domain_qa.md`, and `_workspace/final/handoff.md`.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json >/dev/null
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.28-live-diagnostics.md
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.28-access-diagnostics.md
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
  adjustment, scoring redesign, balance change, empirical calibration claim,
  policy-validity claim, human-learning claim, or validated learner archetype.
