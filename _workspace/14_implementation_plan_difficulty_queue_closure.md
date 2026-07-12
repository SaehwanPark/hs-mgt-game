# Implementation Plan — Difficulty Queue Closure v0.12.9

## Target slice

Close the difficulty-depth and winnability Future item using the v0.12.4
pressure/clearability review plus the v0.12.6 observation-only validation.

## Files

- `_workspace/experiments/v0.12.9-difficulty-queue-closure/`: rerunnable
  evidence closure artifact.
- `tests/test_difficulty_queue_closure.py`: focused evidence-limit and
  reopening-condition tests.
- `docs/difficulty-depth-queue-closure-v0.12.9.md`: durable decision.
- `SPEC.md`, canonical docs, and `LESSONS.md`: remove the completed queue item.

## Non-goals

No difficulty values, resource scaling, balance pass, scoring change, rival AI
change, winnability claim, hidden omniscience, or transition change.

## Acceptance criteria

- v0.12.4 evidence remains 75 runs/1,800 transitions with the pinned candidate
  signal and 15-run Expert clearability overlap.
- v0.12.6 observation controls remain exact and hidden markers remain absent.
- The Future item is removed with explicit limits and a reopening condition.
- Full repository checks pass.
