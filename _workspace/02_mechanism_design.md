# Mechanism Design

## Goal and Roadmap Phase

Phase 7 validation of whether the v0.11.1 operating consequence loop is
inspectable from decision-time context through debrief evidence.

## Slice Boundary

- Read the existing v0.11.1 artifact only.
- Audit 60 runs and 1,440 committed months.
- Classify capacity/demand, operating-loss, and workforce-capacity signals.
- Make no transition, command, actor, scenario, MCP, replay, or hash change.

## Actors and Authority

Riverside remains the player-owned system. Existing rivals remain background
actors in source history, but rival-private operating results are excluded from
the new audit output.

## State, Beliefs, and Observations

For each categorized signal, record whether the trace contains cash, prior
operations, workforce, project, and labor-market context; a submitted command;
and a player-owned operating transition with a committed hash.

## Debrief Contract

Count month-level `Player:` decision links separately from month-level operating
outcome lines. Count global attributed-mechanism summaries separately and never
promote them to month-level explanation evidence.

## Determinism and Evidence Limits

The audit uses fixed source JSON, stable sorting, no wall-clock data, and no new
randomness. It reports traceability only; it does not score decisions or claim
causal explanation, balance, or learning.

## Open Question

Whether a future debrief should expose month-specific operating outcomes remains
deferred to a separate bounded design or runtime slice.
