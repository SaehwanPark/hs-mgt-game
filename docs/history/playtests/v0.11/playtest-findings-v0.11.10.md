# Phase 7 Difficulty Evidence Synthesis v0.11.10

- **Status:** Phase 7 competitive teachability and difficulty evidence synthesis
- **Date:** 2026-07-12
- **Code version:** 0.11.10
- **Campaign:** `competitive-regional-v1`
- **Source artifacts:**
  `v0.11.6-strategy-comparison-use-audit` and
  `v0.11.9-expert-difficulty-validation`
- **Evidence artifact:**
  `_workspace/experiments/v0.11.10-phase7-difficulty-synthesis/results.json`

## Evidence Question

Does the post-change Expert validation artifact preserve the existing
all-tier strategy-comparison, observation, history, hash, and debrief evidence
contracts across the overlapping policy profiles and seeds?

## Result

- The v0.11.6 source covers 60 runs, five profiles, three seeds, four
  difficulty tiers, and 1,440 committed months.
- The v0.11.9 source covers 15 complete Expert runs, the same five profiles and
  three seeds, and 360 committed months.
- All 15 profile/seed coordinates overlap between the source artifacts.
- Both artifacts retain their source-specific trace contracts; no generalized
  raw evidence schema was introduced.
- No structural evidence gap was identified.

## Interpretation and Routing

The synthesis supports continuity of the existing deterministic evidence
surfaces after the difficulty changes. It does not compare endpoint outcomes
causally because the source artifacts were produced at different code
versions. Runtime promotion remains deferred until a concrete unexplained
player-facing, instructor-facing, or domain-review gap appears.

## Evidence Limits

- These are deterministic simulated-policy traces, not human or classroom
  sessions.
- Contract continuity does not establish strategy quality, causal value,
  balance, general Expert winnability, learning, or policy validity.
- Operating quantities remain visible integer game abstractions rather than
  calibrated financial or clinical units.

## Verification

```bash
python3 -m py_compile _workspace/experiments/v0.11.10-phase7-difficulty-synthesis/run_audit.py
python3 -m unittest tests/test_phase7_difficulty_synthesis.py
python3 _workspace/experiments/v0.11.10-phase7-difficulty-synthesis/run_audit.py
python3 -m json.tool _workspace/experiments/v0.11.10-phase7-difficulty-synthesis/results.json
```
