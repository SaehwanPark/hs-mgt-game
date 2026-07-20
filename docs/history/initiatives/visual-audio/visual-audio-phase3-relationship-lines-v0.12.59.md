# Visual/audio Phase 3.2 — Relationship-line styles contract

## Result

Implemented v0.12.59 as a deterministic, fixture-only symbolic
relationship-line style catalog for the shared map vocabulary.

## Scope completed

Added `RELATIONSHIP_LINE_SET` with peer, service, policy, and uncertain styles,
non-color patterns, written equivalents, no-arrowhead defaults, and a generic
fallback. The module does not load host state, infer hidden state, or promote
the catalog into live board rendering.

Added registry/hash/credits provenance and deterministic tests. The contract
explicitly says relationship-line styles organize actor-visible relationships;
they do not infer hidden intent, causality, strength, direction, distance, or
future outcome.

The Phase 3.2 relationship-line styles checklist item is complete. Service-area
overlays, uncertainty overlays, event markers, and interaction behavior remain
separate bounded slices.

## Verification

- Focused relationship-style, fallback, registry, and syntax tests passed.
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks are required before handoff.

## Evidence limits

This is symbolic presentation infrastructure, not human art-direction,
contrast, lived-accessibility, learning, or policy evidence.
