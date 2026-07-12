## Summary

- Add a deterministic read-only v0.11.5 audit of operating-outcome use.
- Reuse the v0.11.4 capture to verify prior-month observation alignment,
  signal-to-next-command continuity, exact debrief linkage, and actor
  boundaries.
- Confirm 60 complete runs, 1,440 traces, 1,380 prior-month matches, 1,440
  debrief matches, 441 response opportunities, and 28 terminal signals.
- Preserve runtime, MCP, ruleset, replay, state-hash, balance, and difficulty
  behavior.

## Evidence limits

This is deterministic simulated-policy traceability evidence. Signal-to-command
counts do not establish causal response, strategy quality, human comprehension,
learning, enjoyment, balance, winnability, calibration, or policy validity.
Runtime promotion remains deferred.

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
