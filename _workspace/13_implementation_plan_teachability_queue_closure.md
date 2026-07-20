# Implementation Plan — Teachability Queue Closure v0.12.8

## Target slice

Convert the already-supported v0.12.3 teachability review into an explicit
queue-closure artifact and remove the completed item from `SPEC.md` Future.

## Files

- `_workspace/experiments/v0.12.8-teachability-queue-closure/`: rerunnable
  source-audit and closure artifact.
- `tests/test_teachability_queue_closure.py`: focused closure-contract tests.
- `docs/history/milestones/teachability-validation-queue-closure-v0.12.8.md`: durable decision and
  reopening condition.
- `SPEC.md`, canonical docs, and `LESSONS.md`: record the completed queue item.

## Non-goals

No new observation, command, transition, ruleset, difficulty, balance, GUI,
human-learning, or classroom-evaluation behavior.

## Acceptance criteria

- The pinned v0.12.3 audit reports 18 complete runs, 270 transitions, and zero
  structural gaps.
- All source-specific review steps remain supported.
- The Future queue entry is removed while its limits and reopening condition
  remain documented.
- Full repository checks pass.
