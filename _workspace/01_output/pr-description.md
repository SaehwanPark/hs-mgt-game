## Summary

- Add a deterministic v0.11.1 operating-loop AI validation matrix.
- Capture five policy lanes across seeds 42–44 and Easy/Normal/Hard/Expert.
- Audit 1,440 player-owned operating months and decision-to-debrief traces.
- Preserve runtime, MCP, ruleset, replay, and state-hash behavior.

## Evidence limits

The artifact is simulated-policy gameplay evidence. It does not establish
causal marginal effects, dominance, balance, calibration, human learning,
enjoyment, winnability, or policy validity. Runtime promotion remains deferred.

## Verification

```text
python3 -m unittest tests/test_operating_loop_ai_validation.py
python3 _workspace/experiments/v0.11.1-operating-loop-ai-validation/run_sessions.py
python3 _workspace/experiments/v0.11.1-operating-loop-ai-validation/run_audit.py
python3 -m unittest discover -s tests -p 'test_*.py'
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
git diff --check
```
