# Implementation Plan — Simulation Breadth and Strategic Actors Queue Closure v0.12.12

## Target slice

Audit the existing competitive campaign against the Future queue's bounded
breadth candidates and close the queue item only if the committed evidence
shows no concrete unexplained strategy or learning gap. The artifact must
distinguish implemented breadth from deferred actor expansion and individual
patient modeling.

## Evidence and files

- `_workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/`: 60
  complete competitive runs, trajectory diversity, and operating tradeoffs.
- `_workspace/experiments/v0.11.12-phase7-current-code-teachability-capture/`:
  current-code observation and debrief continuity.
- `_workspace/experiments/v0.12.3-phase7-teachability-review/`: cross-campaign
  structural-gap review.
- `src/model/competitive_command.rs`, `src/model/competitive_world.rs`,
  `src/sim/observe_competitive.rs`, `src/debrief/report.rs`: runtime boundary
  markers for capacity, outcomes, actors, observations, and debriefs.
- `docs/breadth-strategic-actor-queue-closure-v0.12.12.md` and the reproducible
  closure artifact: decision, limits, and reopening condition.
- `tests/test_breadth_queue_closure.py`: deterministic source/evidence contract
  checks.
- `SPEC.md`, `ARCHITECTURE.md`, `docs/roadmap.md`, `README.md`, `CHANGELOG.md`,
  and `LESSONS.md`: canonical status and version updates.

## Decision gate

No new simulation state, command, transition, actor class, payer utility
model, or individual-patient model is authorized unless the evidence audit
finds a concrete gap. Existing breadth is sufficient for the current bounded
strategy and debrief scope, so the queue item will be removed while preserving
explicit reopening criteria.

## Non-goals

- No full US health-system model or national market.
- No individual patient simulation or distributional equity claim.
- No new Medicare/Medicaid strategic actor behavior or payment reproduction.
- No generalized actor framework, portfolio optimizer, balance tuning, or
  scenario-authoring platform.
- No human-learning, classroom-effectiveness, causal calibration, or policy
  validity claim.

## Acceptance criteria

- The closure artifact inventories service-line/capacity, operating outcome,
  capital, market/monitoring, public-payer, and strategic-rival surfaces.
- True state, player observation, private rival information, and debrief
  boundaries are explicit.
- Existing evidence is summarized with source versions and limitations.
- Source markers and closure tests pass; no runtime source changes are made.
- The breadth Future item is removed, its deferred scope remains visible, and a
  new unexplained gap is required to reopen it.
- Package metadata is bumped to `0.12.12`.
