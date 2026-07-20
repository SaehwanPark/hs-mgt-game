# Implementation Plan — Phase 3.2 service-area-overlays v0.12.60

## Objective

Define deterministic symbolic service-area overlay vocabulary needed by later
regional map/environment slices without implying geographic catchment or
operational performance.

## Scope

- Add primary, shared, and coordinated service-area overlay tokens.
- Provide contour/fill non-color patterns, metric-free defaults, written labels,
  and a generic overlay fallback.
- Add registry hash/provenance, accessible equivalents, focused tests, and SDD
  bookkeeping.
- Keep overlay instances, uncertainty overlays, live rendering, and
  host/session behavior out of scope.

## Acceptance criteria

- Overlay definitions are deterministic and distinguishable without color.
- Geometry is explicitly symbolic, with no metric or direction encoding.
- Unknown service-area IDs use an explicit generic fallback.
- Written contract says the overlays do not establish catchment, distance,
  travel time, population, access, jurisdiction, or performance.
- Version and SDD bookkeeping align to v0.12.60.

## Verification

- `python3 -m unittest tests.test_service_area_overlays`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
