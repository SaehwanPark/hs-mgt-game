# Final Handoff - Rival Information Pressure Design

## Summary

Implemented the `v0.10.36` rival information pressure design slice. The change
adds a Phase 7 design note that defines information delay, monitor value, and
public disclosure as the bounded difficulty pressure surfaces to test before
any runtime tuning.

This is a documentation and project-state slice. It does not change runtime
mechanics, command legality, scenario schemas, MCP DTOs, replay formats, state
hashes, ruleset values, difficulty values, scoring, balance, GUI code, M&A
design, release automation, or asset files.

## Changed Files

- `docs/playtest-findings-v0.10.36.md`: adds the rival information pressure
  design note.
- `docs/mcp-playtesting-guide.md`: adds a `v0.10.36` routing checkpoint.
- `SPEC.md`: records the completed `v0.10.36` slice and updates the Past
  rollup.
- `CHANGELOG.md`, `Cargo.toml`, and `Cargo.lock`: record `v0.10.36` project
  state and package metadata.
- `_workspace/00_input/request-summary.md`, `_workspace/03_domain_qa.md`, and
  `_workspace/final/handoff.md`: record repo-local handoff bookkeeping.

## Verification

- `python3 -m json.tool _workspace/experiments/v0.9.8-difficulty-sweep/results.json`
- `python3 -m json.tool _workspace/experiments/v0.9.9-difficulty-adaptive/results.json`
- `python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
- `python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- `git diff --check`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test -- --test-threads=1`

## PR Handoff

- PR: https://github.com/SaehwanPark/hs-mgt-game/pull/115
- Branch: `feat/rival-info-pressure-design-v0.10.36`
- Review loop: 3 independent local review passes completed.
- Review findings: no Critical, High, Medium, or Low actionable findings.
- PR replies: none required; no actionable PR review comments were present.
- CI: GitHub `check` passed.
- Merge-ready: yes.

## Known Limits

- The tier shape is a design hypothesis, not an implemented ruleset.
- The note uses simulated-agent, deterministic-policy, reviewer-policy, and
  operator-authored evidence, not human classroom observation.
- Expert clearability remains unvalidated until a future evidence slice shows
  at least one severe but clearable path.
- Runtime changes to information delay, monitor value, public disclosure,
  difficulty values, command costs, AP budgets, scoring, or balance remain
  deferred until a future artifact identifies a concrete mechanics gap.
