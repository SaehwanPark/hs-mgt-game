# Strategy-Comparison Use Audit v0.11.6

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-12
- **Code version:** 0.11.6
- **Source artifact:** `v0.11.4-operating-outcome-debrief-validation`

## Evidence question

Does the latest frozen competitive evidence support profile-, seed-, and
difficulty-level comparison of player strategy traces while preserving the
existing observation, committed-transition, state-hash, and player-owned
debrief contracts?

## Result

- 60/60 runs and 1,440/1,440 committed months were represented.
- All 60 runs retained complete observation, command, transition, hash, and
  player-owned monthly debrief linkage.
- The matrix contained 2 profile trajectories for Access First, 2 for Capital
  Modernization, 1 for Coalition/Legitimacy, 1 for Commercial Focus, and 4 for
  Workforce Resilience across the tested seed and difficulty coordinates.
- Profile summaries preserved action-family coverage, first-month actions,
  hold rates, operating-signal response counts, and evidence-support status.
- No structural strategy-comparison, traceability, or debrief-use gap was
  identified.

## Interpretation and routing

The artifact supports descriptive comparison of the existing scripted policy
traces. It does not show that one profile is better, that an action dominates,
that a command caused an outcome, or that a person understood the interface.
Runtime, interface, difficulty, balance, and scoring changes remain deferred.

## Evidence limits

- These are deterministic simulated-policy traces, not human or classroom
  sessions.
- Five profiles, three seeds, four difficulty tiers, and one campaign do not
  establish general strategy diversity, balance, or winnability.
- Command trajectories and signal-to-command counts are descriptive groupings,
  not validated strategy classes or utility functions.
- Operating quantities remain visible integer game abstractions rather than
  calibrated financial or clinical units.

## Verification

```bash
python3 -m unittest tests/test_strategy_comparison_use_audit.py
python3 _workspace/experiments/v0.11.6-strategy-comparison-use-audit/run_audit.py
python3 -m json.tool _workspace/experiments/v0.11.6-strategy-comparison-use-audit/results.json
```
