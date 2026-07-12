# Phase 7 Playtest Findings — Regional Affiliation Validation v0.12.1

## Capture contract

- Campaign: `regional-affiliation-v1`
- Matrix: independent, deferred, and pursuit policies × seeds 42, 43, and 44
- Evidence type: deterministic simulated-policy MCP traces and debrief audit
- Runtime code version: `0.12.1`
- Source artifact: `_workspace/experiments/v0.12.1-affiliation-playtest-validation/results.json`

The policies used only actor-visible MCP observations and legal command hints.
Independent and deferred policies assessed the partner, selected their posture,
and held. The pursuit policy assessed the partner, submitted the maximum legal
commitment package, submitted review when offered, awaited review when offered,
and began integration when the legal surface allowed it.

## Findings

- 9/9 runs completed all six stages.
- 54/54 committed stages had a pre-command observation, accepted command,
  transition summary, and state hash.
- 54/54 debrief stage lines linked stage-level partner, review, labor, payer,
  and community response labels to the committed run.
- The final status split was 3 `Independent`, 3 `Deferred`, and 3 `Integrated`.
- The capture exposed partner `Accepted` and `Conditioned`, review `Approved`,
  labor `Support` and `Concern`, payer `Support`, and community `Support`
  responses across the pursuit runs.
- No unexpected validation failures occurred.

## Concrete decision-time gap

The typed `AffiliationObservation` exposes `alternatives`, `assumptions`, and
`commitments`, but the MCP observation formatter does not render those fields in
any of the nine runs. The debrief later asks the player what independence or
deferral would have preserved, so the current interface cannot show all of the
decision context that the debrief expects the player to use.

This is a bounded observation-context issue. It is not evidence that the
affiliation transition, commitment thresholds, or ruleset are incorrectly
balanced, and it does not justify a legal, financial, winnability, or learning
claim.

## Next bounded candidate

Implement the v0.12.2 MCP observation-context slice: decide the minimal safe
rendering for alternatives, assumptions, and commitments, add focused tests,
rerun this exact matrix, and preserve the affiliation replay/hash contract and
the competitive seed-42 golden path.

## Evidence limits

This is deterministic simulated-policy traceability evidence. It does not
measure human comprehension, classroom effectiveness, cognitive load, general
winnability, balance, calibration, legal validity, or policy forecasting.
