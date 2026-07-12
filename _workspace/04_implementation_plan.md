# Implementation Plan - Post-v0.11.3 Operating-Outcome Validation

## Summary

Capture and audit the existing 60-run competitive policy matrix against the
v0.11.3 monthly operating-result debrief surface. Preserve all runtime and
replay behavior.

## Implementation

- Add focused audit-contract tests first.
- Capture five existing profiles across seeds 42/43/44 and four difficulties.
- Validate 60 complete runs, 1,440 committed months, 1,440 player result lines,
  and 469/469 categorized signal-month links.
- Reject trace/hash mismatches, validation failures, malformed month sections,
  duplicate matrix coordinates, and rival-owned result lines.
- Update v0.11.4 project records and workspace handoffs.

## Verification

```text
python3 -m unittest tests/test_operating_outcome_debrief_validation.py
python3 _workspace/experiments/v0.11.4-operating-outcome-debrief-validation/run_sessions.py
python3 _workspace/experiments/v0.11.4-operating-outcome-debrief-validation/run_audit.py \
  --source _workspace/experiments/v0.11.4-operating-outcome-debrief-validation/capture.json
python3 -m unittest discover -s tests -p 'test_*.py'
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
git diff --check
```

## Non-goals

No runtime, MCP schema, scenario, replay, ruleset, state-hash, balance,
difficulty, calibration, or learning change.

## Handoff

Commit, push, open the GitHub PR against `main`, run exactly three independent
`code-reviewer` passes, fix Critical/High findings, reply to actionable review
feedback, and record domain QA as `Pass` before reporting merge readiness.
