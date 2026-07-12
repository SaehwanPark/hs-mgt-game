# Final Handoff - Expert Difficulty Validation v0.11.9

## Result

- Added a reproducible Expert difficulty validation artifact after the v0.11.7
  risk-posture and v0.11.8 rival resource-scaling changes.
- Ran five deterministic policy lanes across seeds 42, 43, and 44 at Expert
  difficulty.
- Confirmed 15/15 runs completed the full 24-month competitive campaign with
  zero validation failures.
- Preserved actor-visible observations, legal command hints, submitted commands,
  validation failures, histories, state hashes, final observations, and debriefs.
- Recorded findings in `docs/playtest-findings-v0.11.9.md` and updated MCP
  playtesting guidance, SPEC, changelog, lessons, README, and package metadata.

## Evidence

- Artifact:
  `_workspace/experiments/v0.11.9-expert-difficulty-validation/results.json`
- Diagnostics:
  `_workspace/experiments/v0.11.9-expert-difficulty-validation/diagnostics.md`
- Normal seed-42 hold-control hash remains `61357596d8800592`.
- Python tests: 142/142 passed.
- Rust tests: `cargo test --all -- --test-threads=1` passed.
- `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`,
  `python3 scripts/run_automated_playtests.py`, JSON validation, and diff
  checks pass.
- Completion is bounded simulated-policy clearability evidence only.

## Version Boundaries

- Package: `0.11.9`
- Competitive ruleset: `competitive-ruleset-0.2.0`
- Competitive state hash: `competitive-state-hash-v9`

## PR Handoff

- Base branch: `main`
- Working branch: `feat/expert-difficulty-validation-v0.11.9`
- Runtime mechanics, difficulty values, scoring, balance, scenario behavior,
  replay formats, MCP schema, and state-hash logic remain unchanged.
