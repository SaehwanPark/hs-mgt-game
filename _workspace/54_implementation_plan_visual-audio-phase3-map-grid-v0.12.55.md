# Implementation Plan — Phase 3.2 map-grid v0.12.55

## Objective

Define the deterministic symbolic coordinate contract needed by later regional
map/environment slices without implying real-world geography.

## Scope

- Add a fixture-only 960x600 regional map grid with deterministic 24px cells.
- Expose named origin, dimensions, symbolic-geography boundary, and a pure
  coordinate conversion helper.
- Add registry hash/provenance, accessible coordinate equivalent, focused tests,
  and SDD bookkeeping.
- Keep map rendering, live host integration, and scenario state out of scope.

## Acceptance criteria

- Grid dimensions are internally consistent and deterministic.
- Coordinate conversion is pure, rejects inputs outside the declared grid, and
  is side-effect free.
- Written contract says the grid does not assert real-world distance or
  geography.
- Version and SDD bookkeeping align to v0.12.55.

## Verification

- `python3 -m unittest tests.test_map_grid`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
