# Implementation Plan — Phase 3.2 relationship-lines v0.12.59

## Objective

Define deterministic symbolic relationship-line styles needed by later
regional map/environment slices without leaking hidden relationships or
causality.

## Scope

- Add peer, service, policy, and uncertain line styles.
- Provide non-color patterns, non-directional defaults, written labels, and a
  generic relationship fallback.
- Add registry hash/provenance, accessible equivalents, focused tests, and SDD
  bookkeeping.
- Keep relationship instances, overlays, live rendering, and host/session
  behavior out of scope.

## Acceptance criteria

- Line styles are deterministic and distinguishable without color.
- Arrowheads and directionality remain absent unless a later actor-visible
  instance contract supplies them.
- Unknown relationship IDs use an explicit generic fallback.
- Written contract says the styles do not infer hidden intent, causality,
  strength, direction, distance, or future outcome.
- Version and SDD bookkeeping align to v0.12.59.

## Verification

- `python3 -m unittest tests.test_relationship_lines`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
