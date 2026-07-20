# Visual/audio Phase 3.2 — Service-area overlays contract

## Result

Implemented v0.12.60 as a deterministic, fixture-only symbolic service-area
overlay catalog for the shared map vocabulary.

## Scope completed

Added `SERVICE_AREA_SET` with primary, shared, and coordinated overlays,
symbolic contour/fill patterns, written equivalents, metric-free and
non-directional defaults, and a generic fallback. The module does not load
host state, infer hidden state, or promote the catalog into live board
rendering.

Added registry/hash/credits provenance and deterministic tests. The contract
explicitly says service-area overlays organize actor-visible service
relationships; they do not establish real-world catchment, distance, travel
time, population, access, jurisdiction, or performance.

The Phase 3.2 service-area overlays checklist item is complete. Uncertainty
overlays, event markers, and interaction behavior remain separate bounded
slices.

## Verification

- Focused service-area, fallback, registry, and syntax tests passed.
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks are required before handoff.

## Evidence limits

This is symbolic presentation infrastructure, not human art-direction,
contrast, lived-accessibility, learning, or policy evidence.
