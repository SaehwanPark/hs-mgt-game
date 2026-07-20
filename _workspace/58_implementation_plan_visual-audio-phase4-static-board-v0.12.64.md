# Implementation Plan — Visual/audio Phase 4.1 static regional board v0.12.64

## Target slice

Complete the Phase 4.1 static regional-board integration checklist while
preserving the existing typed host boundary and semantic GUI fallback.

## Plan

1. Read the canonical project/design/roadmap and presentation contracts.
2. Implement a pure adapter from `competitive-regional-world-v1` DTO values to
   deterministic scene entities, facilities, overlays, sources, statuses, and
   explicit missingness.
3. Integrate the SVG renderer into the existing GUI and route board/report
   focus through the existing local selection/detail path.
4. Add a fixture-only proof page, static SVG snapshot fixture, registry/credits
   provenance, and focused tests.
5. Run focused and full verification, perform one light code-review pass, fix
   any findings, push the PR, and merge to `main` before selecting the next
   roadmap slice.

## Assumptions and boundaries

- Existing `RegionalWorldEnvelope` and `RegionalWorldEntity` fields are the
  authority; no Rust DTO or simulation change is needed.
- Layout slots organize attention only; they are not geography, distance,
  ownership, importance, or performance.
- SVG and DOM selection are local presentation state. The semantic map/detail
  surface remains the fallback when SVG or color is unavailable.

## Acceptance evidence

- `tests/test_regional_board.py` covers DTO ordering, missingness, generic
  fallback, deterministic SVG snapshot, integration markers, and proof syntax.
- Existing GUI and SVG tests remain green.
- Asset registry/credits and v0.12.64 metadata remain current.
