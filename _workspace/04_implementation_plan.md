# Implementation Plan - Strategy-Comparison Use Audit v0.11.6

## Summary

Audit the frozen v0.11.4 competitive capture for profile-, seed-, and
difficulty-level strategy trace comparison while preserving the v0.11.5
operating-outcome use contract.

## Implementation

- Add focused audit-contract tests first.
- Compose the existing v0.11.5 operating-outcome parser; do not create a
  generalized evidence framework.
- Normalize ordered command families and summarize trajectories, action-family
  coverage, hold rates, and signal-to-next-command responses by profile and
  difficulty.
- Validate 60 runs, 1,440 months, 1,380 prior-observation matches, 1,440
  debrief matches, 441 response opportunities, and 28 terminal signals.
- Record no unexplained structural gap and keep runtime promotion deferred.

## Verification

```text
python3 -m unittest tests/test_strategy_comparison_use_audit.py
python3 _workspace/experiments/v0.11.6-strategy-comparison-use-audit/run_audit.py
python3 -m json.tool _workspace/experiments/v0.11.6-strategy-comparison-use-audit/results.json
python3 -m unittest discover -s tests -p 'test_*.py'
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
cargo test --test golden_competitive_seed42 -- --test-threads=1
git diff --check
```

## Non-goals

No runtime, MCP schema, scenario, replay, ruleset, state-hash, balance,
difficulty, calibration, winnability, causal, human-learning, or policy-validity
change.

## Handoff

Push `feat/competitive-strategy-comparison-use-v0.11.6`, open a PR against
`main`, run exactly three independent code-reviewer passes, fix or explicitly
defer findings, reply to actionable feedback, and record Domain QA and the PR
URL in the final handoff.
