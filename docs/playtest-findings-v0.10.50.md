# Teachability Observation Capture v0.10.50

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-11
- **Code version:** 0.10.50
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** Hard
- **Profiles:** Fiscal Steward, Access Expansion Advocate, First-Time Executive
- **Seeds:** 42, 43, 44
- **Capture artifact:** `_workspace/experiments/v0.10.50-teachability-observation-capture/results.json`
- **Diagnostics:** `_workspace/experiments/v0.10.50-teachability-observation-capture/diagnostics.md`

This wrapper-boundary capture tests whether deterministic policies that read only
actor-visible observations, legal command hints, and turn number can produce
distinct, complete Hard campaign traces. It does not change runtime behavior.

## Result

All nine runs completed the full 24-month campaign. Every run recorded 24
transitions, state hashes, actor-visible turn traces, final observations, and
debrief output. No run produced a validation failure or safe retry.

The Access Expansion Advocate produced the most action-heavy trace, with ten
action commands and 22 holds per seed. Fiscal Steward produced five action
commands and First-Time Executive produced seven; both otherwise relied on
monitoring and holds. These are descriptive policy differences, not validated
strategy classes or causal comparisons. Endpoint metrics were stable across the
three seeds for each deterministic policy, while final hashes remained
seed-specific.

## Interpretation and Routing

The capture confirms that the existing MCP observation boundary supports
reproducible observation-driven policies and complete history/debrief capture.
It identifies no concrete unexplained player-facing, instructor-facing, or
domain-review gap that current observations, histories, diagnostics, and
debriefs cannot explain. Runtime promotion remains deferred.

The next runtime or interface slice requires a new finding that names a concrete
gap and explains why the current observation, command, history, or debrief
surface cannot account for it.

## Evidence Limits

- These are deterministic simulated-policy runs, not human or classroom
  sessions.
- Zero validation failures and zero retries show compatibility with the current
  command surface, not human comprehension or educational effectiveness.
- Profile action frequencies and endpoint metrics do not establish causality,
  strategy value, balance, winnability, calibration, or policy validity.
- Three profiles, three seeds, one campaign, and one difficulty do not support a
  general difficulty or balance claim.

## Verification

```bash
python3 -m unittest tests/test_teachability_observation_capture.py
python3 _workspace/experiments/v0.10.50-teachability-observation-capture/run_sessions.py
python3 scripts/diagnose_runs.py \
  _workspace/experiments/v0.10.50-teachability-observation-capture/results.json \
  --output _workspace/experiments/v0.10.50-teachability-observation-capture/diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.50-teachability-observation-capture/results.json
```
