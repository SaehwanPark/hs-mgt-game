# Mechanism Design

## Goal and Roadmap Phase

Add Phase 5 replay artifact export and internal playtest findings for the
current fictional regional US market prototype while preserving the existing
deterministic transition core unchanged.

## Slice Boundary

Included:

- Versioned `replay-artifact-0.1.15` text format.
- Serialize, deserialize, and verify helpers over committed history.
- Optional post-run CLI export prompt with empty-input skip behavior.
- Internal playtest findings for preset path 1 and interactive defaults at seed
  `42`.

Excluded:

- New commands, actors, state fields, or random streams.
- Mid-run save/load.
- Scenario or ruleset file loader.
- Cryptographic integrity guarantees.
- Module split or CI workflow.

## Documentation Changes

- `docs/playtest-findings-v0.1.15.md` records comprehensibility, strategic
  tension, debrief usefulness, and recommended next slice.
- `ARCHITECTURE.md` documents the artifact boundary under Interface and open
  architectural decisions.
- `SPEC.md` records the interactive slice as complete and this replay export
  slice as active.

## Determinism and Replay Notes

- Artifact verification replays committed commands and resolved inputs through
  the existing `replay()` path and fails on hash drift.
- Resolved inputs remain explicit in the artifact so verification does not
  re-derive RNG streams differently.
- `transition()` and hash semantics are unchanged.

## Open Questions

- Whether future artifacts should embed debrief text or instructor notes.
- Whether module extraction should happen before the next actor expansion.
