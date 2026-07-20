# Teachability-Gate Synthesis v0.10.49

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-11
- **Code version:** 0.10.49
- **Campaign:** `competitive-regional-v1`
- **Source artifacts:** v0.10.45 instructor debrief-use, v0.10.46 Expert
  clearability, v0.10.47 command-to-effect explainability, and v0.10.48
  strategy diversity
- **Audit artifact:**
  `_workspace/experiments/v0.10.49-teachability-gate-synthesis/results.json`

This deterministic read-only synthesis checks continuity across the existing
Phase 7 evidence chain. It does not launch new sessions or change runtime
behavior.

## Result

All four source artifacts were supported. The v0.10.46–v0.10.48 Expert
profile/seed matrix remained continuous across all 12 expected members. The
source chain covers instructor debrief-use fields, Expert completion,
command-to-effect traceability, and descriptive strategy variation.

## Interpretation and Routing

No concrete unexplained player-facing, instructor-facing, or domain-review gap
was identified. Runtime promotion remains deferred. Traceability, completion,
distinct trajectories, and endpoint tradeoffs do not establish causality,
strategy value, balance, winnability, or educational effectiveness.

The next runtime or interface slice requires a new finding that current
observations, histories, diagnostics, and debriefs cannot explain.

## Evidence Limits

- The policies are deterministic simulated policies, not human or classroom
  evidence.
- The source artifacts use different trace shapes; this synthesis checks their
  declared evidence boundaries rather than creating a generalized schema.
- Endpoint differences and command-family variation are descriptive only.
- The audit does not establish calibration, policy validity, or measured
  learning.

## Verification

```bash
python3 -m py_compile _workspace/experiments/v0.10.49-teachability-gate-synthesis/run_audit.py
python3 -m unittest tests/test_teachability_gate_synthesis.py
python3 _workspace/experiments/v0.10.49-teachability-gate-synthesis/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.49-teachability-gate-synthesis/results.json
```
