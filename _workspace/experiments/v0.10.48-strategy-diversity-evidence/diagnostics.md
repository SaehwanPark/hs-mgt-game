# Strategy-Diversity Evidence Audit v0.10.48

- **Batch id:** v0.10.48-strategy-diversity-evidence
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** `expert`
- **Source artifact:** `_workspace/experiments/v0.10.46-expert-clearability-evidence/results.json`
- **Runs reviewed:** 12 of 12

This deterministic read-only audit compares command-family trajectories and
descriptive tradeoff records across existing simulated-policy runs. It does
not infer causality, optimal strategy, or human learning.

## Profile summary

| Profile | Seeds | Distinct trajectories | Action families | First-turn families |
| --- | --- | ---: | ---: | --- |
| Balanced Strategy | 42, 43, 44 | 1 | 14 | monitor:northlake, recruit:nurse |
| Capacity Growth | 42, 43, 44 | 1 | 14 | invest:beds |
| Fiscal Caution | 42, 43, 44 | 1 | 14 | hold, monitor:northlake |
| Naive First-Time | 42, 43, 44 | 1 | 13 | hold, monitor:northlake |

## Run summary

| Profile | Seed | Status | Commands | Non-hold | Hold rate | Tradeoff record |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| Fiscal Caution | 42 | supported | 43 | 19 | 0.5581 | present |
| Fiscal Caution | 43 | supported | 43 | 19 | 0.5581 | present |
| Fiscal Caution | 44 | supported | 43 | 19 | 0.5581 | present |
| Capacity Growth | 42 | supported | 44 | 23 | 0.4773 | present |
| Capacity Growth | 43 | supported | 44 | 23 | 0.4773 | present |
| Capacity Growth | 44 | supported | 44 | 23 | 0.4773 | present |
| Balanced Strategy | 42 | supported | 47 | 25 | 0.4681 | present |
| Balanced Strategy | 43 | supported | 47 | 25 | 0.4681 | present |
| Balanced Strategy | 44 | supported | 47 | 25 | 0.4681 | present |
| Naive First-Time | 42 | supported | 39 | 15 | 0.6154 | present |
| Naive First-Time | 43 | supported | 39 | 15 | 0.6154 | present |
| Naive First-Time | 44 | supported | 39 | 15 | 0.6154 | present |

## Common first-turn action screen

The following families appeared in every profile's first-turn family set:

- None.

This is a candidate common-action signal only. It is not evidence that an
action dominates, improves outcomes, or should be made mandatory.

## Evidence limits

- This is descriptive strategy-trace evidence, not a causal comparison.
- The source contains deterministic simulated-policy traces, not human or classroom sessions.
- A common action is a candidate dominance signal only; it is not proof of an optimal strategy.
- The tested profiles, seeds, and difficulty do not establish general balance, learning, or policy validity.
