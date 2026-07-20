# Implementation Plan — Phase 3.2 parcel-system v0.12.58

## Objective

Define the deterministic symbolic parcel vocabulary needed by later regional
map/environment slices without implying real-world ownership or future use.

## Scope

- Add facility-parcel and undeveloped-land-parcel tokens on the shared 24px
  grid.
- Provide non-color patterns, type labels, and a generic parcel fallback.
- Add registry hash/provenance, accessible equivalents, focused tests, and SDD
  bookkeeping.
- Keep relationship lines, overlays, live rendering, and host/session behavior
  out of scope.

## Acceptance criteria

- Parcel definitions are deterministic and dimensionally consistent.
- Unknown parcel IDs use an explicit generic fallback.
- Written contract says the tokens do not assert ownership, availability,
  development potential, land value, zoning, geography, or future use.
- Version and SDD bookkeeping align to v0.12.58.

## Verification

- `python3 -m unittest tests.test_parcels`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
