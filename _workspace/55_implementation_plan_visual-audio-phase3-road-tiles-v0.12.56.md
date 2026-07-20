# Implementation Plan — Phase 3.2 road-tiles v0.12.56

## Objective

Define the deterministic symbolic road-segment vocabulary needed by later
regional map/environment slices without implying real-world road geometry.

## Scope

- Add fixture-only horizontal, vertical, and quarter-curve road tokens on a
  24px grid.
- Provide path-role labels, orientation labels, and a generic road fallback.
- Add registry hash/provenance, accessible equivalents, focused tests, and SDD
  bookkeeping.
- Keep intersections, districts, live rendering, and host/session behavior out
  of scope.

## Acceptance criteria

- Road tile definitions are deterministic and dimensionally consistent.
- Unknown road IDs use an explicit generic fallback.
- Written contract says the tokens do not assert real-world road geometry,
  travel time, jurisdiction, or geography.
- Version and SDD bookkeeping align to v0.12.56.

## Verification

- `python3 -m unittest tests.test_road_tiles`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
