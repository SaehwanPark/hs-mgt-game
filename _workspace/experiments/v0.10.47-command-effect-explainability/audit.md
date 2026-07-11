# Command-to-Effect Explainability Audit v0.10.47

- **Batch id:** v0.10.47-command-effect-explainability
- **Campaign:** `competitive-regional-v1`
- **Source artifact:** `_workspace/experiments/v0.10.46-expert-clearability-evidence/results.json`
- **Runs reviewed:** 12 of 12

This deterministic read-only audit checks whether submitted player commands
are retained in the debrief and linked to action-specific transition evidence.
It does not infer causality or decision quality.

## Coverage

| Profile | Seed | Completion | Commands | Supported | Unmatched | Missing debrief | Status |
| --- | ---: | --- | ---: | ---: | ---: | ---: | --- |
| Fiscal Caution | 42 | complete | 43 | 43 | 0 | 0 | supported |
| Fiscal Caution | 43 | complete | 43 | 43 | 0 | 0 | supported |
| Fiscal Caution | 44 | complete | 43 | 43 | 0 | 0 | supported |
| Capacity Growth | 42 | complete | 44 | 44 | 0 | 0 | supported |
| Capacity Growth | 43 | complete | 44 | 44 | 0 | 0 | supported |
| Capacity Growth | 44 | complete | 44 | 44 | 0 | 0 | supported |
| Balanced Strategy | 42 | complete | 47 | 47 | 0 | 0 | supported |
| Balanced Strategy | 43 | complete | 47 | 47 | 0 | 0 | supported |
| Balanced Strategy | 44 | complete | 47 | 47 | 0 | 0 | supported |
| Naive First-Time | 42 | complete | 39 | 39 | 0 | 0 | supported |
| Naive First-Time | 43 | complete | 39 | 39 | 0 | 0 | supported |
| Naive First-Time | 44 | complete | 39 | 39 | 0 | 0 | supported |

## Unmatched commands

No unmatched commands were found in the reviewed traces.

## Missing debrief command records

No missing monthly player command records were found.

## Interpretation

Supported means that the trace contains an action-specific event/effect and a monthly `Player:` debrief record.
A deferred match records later trace continuity; it does not establish that the command caused the later outcome.

## Evidence limits

- Coverage is traceability evidence, not causal evidence.
- The source contains deterministic simulated-policy traces, not human or classroom sessions.
- Aggregated transition effects do not prove that a command caused an endpoint metric.
- A supported trace does not establish decision quality, balance, learning, or policy validity.
