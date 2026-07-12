# Implementation Plan - Operating-Outcome Use Audit v0.11.5

## Summary

Audit the frozen v0.11.4 competitive capture for prior-month operating
observation alignment, signal-to-next-command continuity, exact committed
debrief linkage, and actor-boundary preservation.

## Implementation

- Add focused audit-contract tests first.
- Reuse the existing operating-transition parser through its established audit
  boundary; do not create a generalized evidence framework.
- Validate 60 runs, 1,440 traces, 1,380 prior-month matches, 1,440 hash matches,
  1,440 debrief matches, 441 response opportunities, and 28 terminal signals.
- Record descriptive signal-to-command distributions without causal claims.
- Update v0.11.5 findings, version records, lessons, and workspace handoffs.

## Verification

```text
python3 -m unittest tests/test_operating_outcome_use_audit.py
python3 _workspace/experiments/v0.11.5-operating-outcome-use-audit/run_audit.py
python3 -m json.tool _workspace/experiments/v0.11.5-operating-outcome-use-audit/results.json
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

Push `feat/competitive-operating-outcome-use-v0.11.5`, open a PR against
`main`, run exactly three independent code-reviewer passes, fix or explicitly
defer findings, reply to actionable feedback, and record Domain QA and the PR
URL in the final handoff.
