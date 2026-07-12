# Post-Change All-Tier Difficulty Validation v0.11.11

- **Status:** Phase 7 competitive teachability and difficulty evidence
- **Date:** 2026-07-12
- **Code version:** 0.11.11
- **Campaign:** `competitive-regional-v1`
- **Matrix:** Access First, Commercial Focus, Workforce Resilience, Capital
  Modernization, and Coalition/Legitimacy across seeds 42, 43, and 44 at Easy,
  Normal, Hard, and Expert difficulty
- **Evidence artifact:**
  `_workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/results.json`

## Evidence Question

Does the current post-v0.11.7/v0.11.8 code preserve bounded clearability,
strategy-trace variation, operating accounting, and decision-to-debrief
inspectability across the full competitive difficulty matrix?

## Result

- 60/60 runs completed all 24 months with zero validation failures.
- The artifact audits 1,440 committed operating months and 60/60 complete
  decision-to-debrief traces.
- Ten distinct command trajectories were observed across the matrix.
- No common first-month action or candidate near-dominant action was found.
- Operating evidence includes 140 capacity/demand bottleneck months, 268
  operating-loss months, 205 workforce-capacity months, and 78 threshold
  crossings.
- Final tradeoff ranges remain varied across cash, access, quality, workforce
  trust, community trust, and market share.
- The Normal seed-42 hold-control hash remains `61357596d8800592`.

## Interpretation and Routing

The current matrix preserves the expected trace, accounting, and completion
contracts after the difficulty changes. The profile and difficulty summaries are
descriptive simulated-policy diagnostics; they do not establish that one policy
is better, that a command caused an outcome, or that Expert is generally
winnable. Runtime promotion remains deferred because this artifact identifies no
unexplained player-facing, instructor-facing, or domain-review gap that cannot
be described by the current observations, history, diagnostics, and debriefs.

## Evidence Limits

- These are deterministic simulated-policy traces, not human or classroom
  sessions.
- Full completion is a bounded clearability proxy for the tested policies and
  seeds, not a general winnability or balance claim.
- Trajectory differences, endpoint ranges, bottlenecks, and threshold signals
  are not causal marginal effects, equilibrium results, or validated strategy
  classes.
- Operating quantities remain visible integer game abstractions rather than
  calibrated financial or clinical units.
- The artifact does not establish enjoyment, learning, calibration, or policy
  validity.

## Verification

```bash
python3 -m py_compile _workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/*.py
python3 -m unittest tests/test_phase7_post_change_all_tier_validation.py
python3 _workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/run_sessions.py
python3 _workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/run_audit.py
python3 -m json.tool _workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/results.json
```
