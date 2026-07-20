# Implementation Plan — Phase 3.2 district-tiles v0.12.57

## Objective

Define the deterministic symbolic district vocabulary needed by later regional
map/environment slices without implying real-world land use or geography.

## Scope

- Add commercial, residential, employer-center, and government district tokens
  on the shared 24px grid.
- Provide non-color patterns, type labels, and a generic district fallback.
- Add registry hash/provenance, accessible equivalents, focused tests, and SDD
  bookkeeping.
- Keep intersections, parcels, overlays, live rendering, and host/session
  behavior out of scope.

## Acceptance criteria

- District tile definitions are deterministic and dimensionally consistent.
- Unknown district IDs use an explicit generic fallback.
- Written contract says the tokens do not assert real-world land use,
  population, ownership, zoning, travel time, or jurisdiction.
- Version and SDD bookkeeping align to v0.12.57.

## Verification

- `python3 -m unittest tests.test_district_tiles`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
