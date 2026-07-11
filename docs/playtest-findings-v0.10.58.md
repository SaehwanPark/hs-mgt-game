# Debrief-Coherence Audit v0.10.58

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-11
- **Code version:** 0.10.58
- **Campaign:** `competitive-regional-v1`
- **Source artifacts:** v0.10.43, v0.10.50, v0.10.51, and v0.10.54–v0.10.56

## Evidence question

Do existing competitive traces connect actor-visible decision context and
submitted responses to accepted transitions, delayed or partial information,
realized outcomes, and retrospective debrief framing that separates decision
quality from outcome quality?

## Result

All six source artifacts and 39 completed runs report supported decision
context, action response, transition follow-through, outcome context, and
debrief explanation coverage. Rival-information traces support partial-context
coverage, and project-recovery traces support visible pending-project context.
The v0.10.54 to v0.10.55 and v0.10.55 to v0.10.56 project-recovery hash
comparisons match for seeds 42, 43, and 44.

The v0.10.51 resource-probe source uses its declared pre-submit observation
record for expected failures; it does not silently treat missing
`observation_after_failure` fields as a successful recovery claim.

## Interpretation and routing

The audit closes the current decision-to-debrief traceability question. It does
not establish that a person would find the debrief clear, that a decision was
good or bad, or that any mechanism is causally valid. Runtime and interface
promotion remain deferred.

## Evidence limits

- This is deterministic simulated-policy traceability evidence, not human or
  classroom evidence.
- Supported decision-versus-outcome text does not establish decision quality,
  learning, strategy value, balance, winnability, calibration, or policy
  validity.
- Project ceilings, rival behavior, delayed effects, and all numerical
  thresholds remain gameplay abstractions.

## Verification

```bash
python3 _workspace/experiments/v0.10.58-debrief-coherence-audit/run_audit.py
python3 -m unittest tests/test_debrief_coherence_audit.py
python3 -m json.tool _workspace/experiments/v0.10.58-debrief-coherence-audit/results.json
```
