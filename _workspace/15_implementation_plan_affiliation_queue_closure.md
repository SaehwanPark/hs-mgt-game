# Implementation Plan — Affiliation Queue Closure v0.12.10

## Target slice

Synchronize the SPEC affiliation/acquisition queue entry with the already
merged v0.12.7 runtime-boundary proposal.

## Files

- `_workspace/experiments/v0.12.10-affiliation-queue-closure/`: rerunnable
  proposal/marker closure artifact.
- `tests/test_affiliation_queue_closure.py`: focused closure tests.
- `docs/affiliation-queue-closure-v0.12.10.md`: durable scope and reopening
  decision.
- `SPEC.md`, canonical docs, and `LESSONS.md`: remove the completed queue item.

## Non-goals

No new affiliation mechanism, acquisition branch, deal finance, legal forecast,
generic actor framework, or competitive-campaign change.

## Acceptance criteria

- Six proposal contracts and all source markers are supported.
- Existing evidence remains 9/9 runs, 54 stages, and 54 observations.
- Broader acquisition scope remains explicitly deferred.
- Full repository checks pass.
