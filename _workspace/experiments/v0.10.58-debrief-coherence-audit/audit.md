# Debrief-Coherence Audit v0.10.58

- **Batch id:** v0.10.58-debrief-coherence-audit
- **Campaign:** `competitive-regional-v1`
- **Source artifacts:** 6
- **Runs reviewed:** 39 of 39

This deterministic read-only audit joins decision-time observations, commands, accepted transitions, delayed or partial context, outcomes, and retrospective debrief markers.

## Coverage

| Source artifact | Lane | Decision context | Action response | Transition follow-through | Delayed/partial context | Outcome context | Debrief explanation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `v0.10.43-rival-info-follow-through` | rival-pressure | supported | supported | supported | supported | supported | supported |
| `v0.10.50-teachability-observation-capture` | strategy-tradeoff | supported | supported | supported | not_applicable | supported | supported |
| `v0.10.51-adversarial-resource-probe` | resource-retry | supported | supported | supported | not_applicable | supported | supported |
| `v0.10.54-project-limit-recovery` | project-recovery | supported | supported | supported | supported | supported | supported |
| `v0.10.55-asc-project-observation` | project-recovery | supported | supported | supported | supported | supported | supported |
| `v0.10.56-project-recovery-use` | project-recovery | supported | supported | supported | supported | supported | supported |

## Hash continuity

- `v0.10.54-project-limit-recovery` → `v0.10.55-asc-project-observation`: supported (3 seeds; mismatches: none).
- `v0.10.55-asc-project-observation` → `v0.10.56-project-recovery-use`: supported (3 seeds; mismatches: none).

## Promotion decision

Runtime promotion: deferred.

This audit measures decision-to-debrief trace coherence in existing artifacts. Runtime or interface promotion requires separate player-facing, instructor-facing, or domain-review evidence of an unexplained problem.

Decision-versus-outcome separation is a traceability marker, not a quality judgment.

## Evidence gaps

None identified in the reviewed source shapes.

## Evidence limits

- Coverage is traceability evidence, not causal evidence.
- The source policies are deterministic simulated policies, not human or classroom sessions.
- The audit does not measure debrief clarity, learning, strategy quality, balance, or calibration.
- Decision-versus-outcome separation in text does not establish that a decision was good or bad.
- Project ceilings, rival behavior, and delayed effects remain gameplay abstractions.
