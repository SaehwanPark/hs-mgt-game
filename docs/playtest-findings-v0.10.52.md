# Decision-Load and Pacing Proxy Evidence v0.10.52

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-11
- **Audit version:** 0.10.52
- **Campaign:** `competitive-regional-v1`
- **Source artifact:** `_workspace/experiments/v0.10.50-teachability-observation-capture/results.json`
- **Source runs:** Fiscal Steward, Access Expansion Advocate, and First-Time Executive across seeds 42, 43, and 44 at Hard difficulty

This read-only audit adds turn-level decision-load signals to the existing
observation-driven traces. It does not launch new sessions or change runtime
behavior.

## Result

All nine source runs completed 24 months with zero validation failures and zero
retries. The profile metrics were stable across seeds:

| Profile | Action commands | Active months | Holds | Multi-action months | Maximum actions/month |
| --- | ---: | ---: | ---: | ---: | ---: |
| Fiscal Steward | 5 | 5 | 24 | 0 | 1 |
| Access Expansion Advocate | 10 | 8 | 22 | 2 | 2 |
| First-Time Executive | 7 | 7 | 24 | 0 | 1 |

The audit exposes temporal command concentration that aggregate action totals
did not show. This is a descriptive pacing and action-overload proxy only.

## Interpretation and routing

The source artifact supports turn-level decision-load reporting. It does not
identify a concrete player-facing, instructor-facing, or domain-review gap that
requires runtime, interface, command-help, or debrief changes. Runtime
promotion remains deferred.

## Evidence limits

- These are deterministic simulated-policy traces, not human or classroom
  evidence.
- Action concentration and active-month cadence do not measure cognitive load,
  comprehension, or educational effectiveness.
- Profile differences and endpoint metrics do not establish causal strategy
  value, balance, winnability, optimality, calibration, or policy validity.
- The audit covers one campaign, one difficulty, three profiles, and three
  seeds.

## Verification

```bash
python3 -m unittest tests/test_decision_load_evidence.py
python3 _workspace/experiments/v0.10.52-decision-load-evidence/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.52-decision-load-evidence/results.json
```
