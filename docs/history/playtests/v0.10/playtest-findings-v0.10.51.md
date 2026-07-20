# Adversarial Resource-Probe Evidence v0.10.51

- **Status:** Phase 7 competitive validation evidence
- **Date:** 2026-07-11
- **Code version:** 0.10.51
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** Hard
- **Profile:** Adversarial Resource Probe
- **Seeds:** 42, 43, 44
- **Capture artifact:** `_workspace/experiments/v0.10.51-adversarial-resource-probe/results.json`
- **Diagnostics:** `_workspace/experiments/v0.10.51-adversarial-resource-probe/diagnostics.md`
- **Control:** v0.10.50 First-Time Executive traces for the same seeds

This wrapper-boundary capture probes existing resource validation and retry
behavior without changing simulation code. The fixed policy submits cash,
action-point, and concurrent-project boundary commands, then retries rejected
commands with `hold`.

## Result

All three runs completed 24 months. Each run produced five expected validation
failures and five safe retries:

- three `insufficient_cash` probes;
- one `ap_budget_exceeded` probe; and
- one `too_many_concurrent_projects` probe.

Every rejected command left the session at the same turn, and every `hold`
retry advanced the campaign exactly once. Cash and action-point failures
included structured resource limits and actionable hints. The concurrent-
project failure preserved its stable error code but did not expose a resource
hint.

## Interpretation and Routing

The existing validation boundary behaved as expected for all tested probes. The
artifact identifies no unexplained runtime, command-surface, or debrief gap.
Runtime promotion remains deferred.

The absence of a resource hint for `too_many_concurrent_projects` is recorded as
a trace fact, not a defect: the probe did not establish that the player needs a
new interface or that current guidance is inadequate. A separate evidence
finding would be required before changing that behavior.

## Evidence Limits

- These are deterministic simulated-policy runs, not human or classroom
  sessions.
- Intentional validation failures test guard compatibility and trace capture;
  they do not establish exploit value, balance, winnability, or comprehension.
- Three seeds, one campaign, one difficulty, and one adversarial policy do not
  support general difficulty, calibration, learning, or policy-validity claims.
- Endpoint hashes and outcomes are descriptive and are not causal strategy
  comparisons.

## Verification

```bash
python3 -m unittest tests/test_adversarial_resource_probe.py
python3 _workspace/experiments/v0.10.51-adversarial-resource-probe/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.51-adversarial-resource-probe/results.json
```
