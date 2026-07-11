# Strategy-Diversity Evidence v0.10.48

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-11
- **Code version:** 0.10.48
- **Campaign:** `competitive-regional-v1`
- **Source artifact:** `_workspace/experiments/v0.10.46-expert-clearability-evidence/results.json`
- **Audit artifact:** `_workspace/experiments/v0.10.48-strategy-diversity-evidence/results.json`

This read-only audit compares normalized command-family trajectories and
descriptive final tradeoff records across the existing four-policy, three-seed
Expert matrix. It does not launch new sessions or change runtime behavior.

## Result

All 12 source runs were represented and supported. The four profiles produced
four distinct command trajectories across the tested matrix, with different
action-family coverage and no common first-turn action family across every
profile. Every run retained a final tradeoff record.

## Interpretation and Routing

The artifact provides bounded evidence that the existing scripted profiles are
observably different in their command choices. It does not show that any profile
is better, that an action dominates, or that endpoint differences were caused by
the command trajectory. Keep runtime mechanics, difficulty, scoring, balance,
and debrief behavior unchanged.

Future runtime work still requires a concrete player-facing, instructor-facing,
or domain-review gap that current observations, histories, diagnostics, and
debriefs cannot explain.

## Evidence Limits

- The policies are deterministic simulated policies, not human or classroom
  sessions.
- Four profiles, three seeds, one campaign, and one difficulty do not establish
  general strategy diversity, balance, or winnability.
- Command-family signatures are descriptive groupings, not validated strategy
  classes or utility functions.
- Final tradeoff records are endpoint descriptions, not causal comparisons.
- The audit does not establish learning, calibration, or policy validity.

## Verification

```bash
python3 -m py_compile _workspace/experiments/v0.10.48-strategy-diversity-evidence/run_audit.py
python3 -m unittest tests/test_strategy_diversity_evidence.py
python3 _workspace/experiments/v0.10.48-strategy-diversity-evidence/run_audit.py
python3 -m json.tool _workspace/experiments/v0.10.48-strategy-diversity-evidence/results.json
```
