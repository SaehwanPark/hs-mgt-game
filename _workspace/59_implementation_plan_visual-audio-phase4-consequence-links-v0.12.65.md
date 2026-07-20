# Implementation Plan — Visual/audio Phase 4.2 consequence linkage v0.12.65

## Target slice

Complete the Phase 4.2 visible consequence linkage checklist over existing
regional-world and resolution envelopes.

## Plan

1. Read canonical docs and existing regional/resolution contracts.
2. Implement pure deterministic links for public signals, visible processes,
   host-committed effects, targetless effects, and replay turn/hash entries.
3. Integrate bidirectional report/entity/consequence focus without animation or
   host mutation.
4. Add focused tests and provenance, complete SDD/roadmap bookkeeping.
5. Run focused/full verification, perform one light reviewer pass, fix findings,
   push the PR, and merge to `main` before the next slice.

## Boundaries

- The host remains authoritative for targets, effects, timing, history, hashes,
  replay, and rival observability.
- Text matching may attach only an explicitly visible institution name; effects
  without host targets remain targetless.
- Local focus never asserts geography, causality, severity, private action, or
  future outcome.

## Acceptance evidence

- `tests/test_consequence_links.py` covers public timing/boundaries, stable
  effects, targetless behavior, replay sequence preservation, and GUI controls.
- Existing resolution, first-month, regional, asset, metadata, documentation,
  full Python/Rust, formatting, presentation-contract, and diff checks remain
  green.
