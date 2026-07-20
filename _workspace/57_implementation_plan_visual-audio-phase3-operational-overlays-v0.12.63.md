# Implementation Plan — Visual/audio Phase 3.3 operational overlays v0.12.63

## Acceptance criteria

- `gui/operational-overlays.mjs` contains all twelve roadmap overlay categories
  with the full semantic/source/accessibility/fallback contract.
- Deterministic display priority, ID tie-breaking, bounded collision layout,
  and overflow text are pure local functions.
- `gui/operational-overlay-proof.html` renders every category plus a
  simultaneous-overlay collision example with text and source labels.
- Focused Python tests verify every repeated checklist field, fallback, layout,
  simultaneous ordering, registry hash, credits, and syntax.
- Phase 3.3 is marked complete in the roadmap and SDD records; live board
  integration remains explicitly deferred to Phase 4.

## Verification plan

1. Run focused operational-overlay tests and Node syntax checks.
2. Run asset validation and credits checks.
3. Run full Python/Rust, metadata, documentation-link, and diff checks.
4. Complete presentation QA and one light code-review pass on the PR diff.
