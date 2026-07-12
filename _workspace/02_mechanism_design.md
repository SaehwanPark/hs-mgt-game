# Mechanism Design

## Goal and Roadmap Phase

Phase 7 validation of the existing competitive debrief surface. This slice
adds no actor, policy, scenario, or transition mechanism.

## Evidence Contract

- Reuse the five existing deterministic policy lanes, seeds 42/43/44, and
  Easy/Normal/Hard/Expert difficulties.
- Audit the player-owned transition operating fields and the matching monthly
  debrief section.
- Count one player `Operating result:` line per committed month and require a
  result line for each categorized capacity/demand, operating-loss, or
  workforce-capacity signal-month.
- Keep global attribution summaries separate from month-level linkage.

## Boundaries

- Capture only through the existing MCP wrapper boundary.
- Preserve actor-visible observations, rival-private state, ruleset,
  state-hash schema, replay formats, and transition semantics.
- Do not modify historical v0.11.1 or v0.11.2 artifacts.
- Treat the output as structural traceability evidence, not causal, balance,
  winnability, calibration, human-learning, or policy-validity evidence.

## Validation

- Matrix coordinates are complete and unique: 60 runs.
- Every run has 24 committed transitions and matching trace hashes.
- The post-v0.11.3 debrief contains 1,440 player result lines and 469/469
  categorized signal-month links.
- The audit is deterministic and rejects missing, duplicate, malformed, or
  rival-owned result records.
