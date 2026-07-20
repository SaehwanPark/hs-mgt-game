# Visual/audio Phase 3.2 — Uncertainty overlays contract

## Result

Implemented v0.12.61 as a deterministic, fixture-only symbolic
uncertainty-overlay catalog for the shared map vocabulary.

## Scope completed

Added `UNCERTAINTY_SET` with stale, missing, and revised visible-information
overlays, non-color patterns, written equivalents, no-severity and static
reduced-motion defaults, and a generic fallback. The module does not load host
state, infer hidden state, or promote the catalog into live board rendering.

Added registry/hash/credits provenance and deterministic tests. The contract
explicitly says uncertainty overlays identify explicit visible information
status; they do not quantify hidden risk, severity, probability, truth, or
future outcome.

The Phase 3.2 uncertainty overlays checklist item is complete. Event markers
and interaction behavior remain separate bounded slices.

## Verification

- Focused uncertainty-overlay, fallback, registry, and syntax tests passed.
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks are required before handoff.

## Evidence limits

This is symbolic presentation infrastructure, not human art-direction,
contrast, lived-accessibility, learning, or policy evidence.
