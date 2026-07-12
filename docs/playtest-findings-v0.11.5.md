# Operating-Outcome Use Audit v0.11.5

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-12
- **Code version:** 0.11.5
- **Source artifact:** `v0.11.4-operating-outcome-debrief-validation`

## Evidence question

Do the existing competitive traces connect actor-visible prior-month operating
outcomes to the next submitted command, the committed transition, and the
player-owned monthly debrief result without crossing rival-information
boundaries?

## Result

- 60/60 runs and 1,440/1,440 committed months were audited.
- 60 initial zero baselines and 1,380/1,380 prior-month observation matches
  were confirmed.
- 1,440/1,440 trace state hashes matched committed history.
- 1,440/1,440 player-owned monthly debrief results matched committed operating
  transitions exactly.
- The v0.11.4 matrix contained 469 categorized signals; 441 non-terminal
  signal-to-next-command opportunities were linked and 28 terminal signals were
  correctly treated as having no later command.
- Signal counts were 128 capacity/demand, 253 operating-loss, and 60
  workforce-capacity observations.
- Rival-owned operating-result lines counted as player evidence: 0.

## Interpretation and routing

The existing artifact supports descriptive operating-outcome use and response
traceability. Signal-to-command distributions are not evidence that a command
caused an outcome, that a strategy is good, or that a human understood the
interface. No runtime or interface gap is promoted by this audit. Any future
runtime change still requires a separate concrete player-facing,
instructor-facing, or domain-review finding.

## Evidence limits

- This is deterministic simulated-policy traceability evidence, not human or
  classroom evidence.
- It does not establish comprehension, learning, enjoyment, balance,
  winnability, calibration, causal marginal effects, or policy validity.
- Operating quantities remain visible integer game abstractions.

## Verification

```bash
python3 -m unittest tests/test_operating_outcome_use_audit.py
python3 _workspace/experiments/v0.11.5-operating-outcome-use-audit/run_audit.py
python3 -m json.tool _workspace/experiments/v0.11.5-operating-outcome-use-audit/results.json
```
