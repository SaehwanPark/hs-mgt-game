# Visual/audio Phase 3.2 — Parcel-system contract

## Result

Implemented v0.12.58 as a deterministic, fixture-only symbolic parcel
vocabulary on the shared 24px map grid.

## Scope completed

Added `PARCEL_SET` with facility and undeveloped-land tokens, explicit
non-color patterns, written equivalents, and a generic fallback. The module
does not load host state, infer hidden state, or promote the catalog into live
board rendering.

Added registry/hash/credits provenance and deterministic tests. The contract
explicitly says parcel tokens organize symbolic placement; they do not
establish real-world ownership, availability, development potential, land
value, zoning, geography, or future use.

The Phase 3.2 parcel-system checklist item is complete. Relationship lines,
service-area overlays, uncertainty overlays, event markers, and interaction
behavior remain separate bounded slices.

## Verification

- Focused parcel-token, fallback, registry, and syntax tests passed.
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks are required before handoff.

## Evidence limits

This is symbolic presentation infrastructure, not human art-direction,
contrast, lived-accessibility, learning, or policy evidence.
