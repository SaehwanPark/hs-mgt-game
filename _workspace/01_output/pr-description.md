## Summary

- Add a deterministic read-only v0.11.6 strategy-comparison use audit.
- Reuse the frozen v0.11.4 capture and compose the v0.11.5 operating-outcome
  contract.
- Group command trajectories and operating-signal responses by profile, seed,
  and difficulty.
- Confirm 60 complete runs, 1,440 committed months, 1,380 prior-month matches,
  1,440 debrief matches, 441 response opportunities, and 28 terminal signals.
- Preserve runtime, MCP, ruleset, replay, state-hash, balance, and difficulty
  behavior.

## Evidence result

No structural strategy-comparison, traceability, or debrief-use gap was
identified. Runtime promotion remains deferred.

## Evidence limits

This is deterministic simulated-policy traceability evidence. Trajectory and
signal-to-command differences do not establish causal response, strategy
quality, dominance, human comprehension, learning, enjoyment, balance,
winnability, calibration, or policy validity.

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
