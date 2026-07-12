# Final Handoff - Regional Affiliation Runtime Proposal v0.11.14

## Result

- Defined an opt-in six-stage `regional-affiliation-v1` scenario proposal for
  one human-led Riverside system and one localized nonprofit partner.
- Defined minimum true-state, actor-observation, resolved-input, history,
  replay, state-hash, and educational-debrief contracts.
- Preserved the default `competitive-regional-v1` campaign and seed-42 golden
  path; no runtime files were changed.
- Added proposed ADR-0010 and synchronized canonical and workspace handoffs.
- Updated the evidence registry and lessons document with the proposal boundary.

## Version boundaries

- Package: `0.11.14`
- Competitive ruleset: unchanged
- Competitive state hash: unchanged
- Runtime mechanics, commands, scenarios, replay formats, MCP behavior, and
  state-hash logic remain unchanged.

## Branch and PR handoff

- Base branch: `main`
- Working branch: `feat/regional-affiliation-runtime-proposal-v0.11.14`
- PR: https://github.com/SaehwanPark/hs-mgt-game/pull/152
- Domain QA: Pass.
- Review passes: pending three independent review passes.

## Verification

- `cargo fmt --check`: passed.
- `cargo clippy --all-targets -- -D warnings`: passed.
- `cargo test --all -- --test-threads=1`: passed, 293 Rust tests.
- `cargo test --test golden_competitive_seed42 -- --test-threads=1`: passed,
  2 competitive golden tests.
- `python3 -m unittest discover -s tests -p 'test_*.py'`: passed, 163 tests.
- `git diff --check`: passed before commit.

## Next dependency

A separate implementation PR must choose concrete Rust types, scenario fields,
command syntax, numeric ruleset bounds, and replay/state-hash compatibility.
That PR requires fresh domain QA and focused runtime tests before promotion.
