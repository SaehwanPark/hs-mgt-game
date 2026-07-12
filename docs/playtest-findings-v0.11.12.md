# Current-Code Teachability Evidence v0.11.12

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-12
- **Code version:** 0.11.12
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** Hard
- **Profiles:** Fiscal Steward, Access Expansion Advocate, First-Time Executive
- **Seeds:** 42, 43, and 44
- **Evidence artifact:**
  `_workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/results.json`

## Evidence question

Does the current code preserve actor-visible observation capture, command
acceptance and retry traceability, temporal action-load signals, and debrief
continuity for three observation-driven profiles after the v0.11.7 and v0.11.8
difficulty changes?

## Result

- 9/9 runs completed all 24 months with zero validation failures or retries.
- The artifact covers 216 committed months and 216 player operating-month
  records.
- Action cadence was preserved as a descriptive signal: Fiscal Steward used
  15 non-hold commands, Access Expansion Advocate used 30, and First-Time
  Executive used 21 across the three-seed repeats.
- No structural matrix, history/hash, trace, or debrief gap was identified.
- The Normal seed-42 hold-control hash remains `61357596d8800592`.
- Runtime promotion remains deferred.

## Interpretation and routing

The current-code capture preserves the expected observation, command, history,
hash, and debrief contracts for this focused Hard-difficulty matrix. The
profiles and action counts are deterministic simulated-policy diagnostics, not
validated learner types, strategy classes, causal comparisons, or balance
evidence. No unexplained player-facing, instructor-facing, or domain-review
gap was identified that requires a runtime change.

## Evidence limits

- These are deterministic simulated-policy traces, not human or classroom
  sessions.
- Action cadence and retry counts are pacing and friction proxies, not
  cognitive-load or comprehension measurements.
- The three profiles and three seeds do not cover all strategies, stochastic
  conditions, or player skill levels.
- The artifact does not establish enjoyment, learning, calibration, general
  winnability, balance, or policy validity.

## Verification

```bash
python3 -m py_compile _workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/*.py
python3 -m unittest tests/test_phase7_current_code_teachability_capture.py
python3 _workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/run_sessions.py
python3 _workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/run_audit.py
python3 -m json.tool _workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/results.json
```
