# Implementation Plan — Phase 2.2 actor-family identity language v0.12.42

## Objective

Create one shared, fixture-only identity language for the eight recurring
actor families in Phase 2.2.

## Scope

- Finalize payer, regulator, labor, employer, community, board, policy
  coalition, and independent-provider records.
- Provide stable glyphs, report-frame patterns, notification styles, optional
  identity-only sonic tags, visible sources, written equivalents, and generic
  fallback.
- Add a keyboard-reachable proof page, registry provenance, tests, and SDD
  bookkeeping.
- Keep the catalog outside live GUI and host/session behavior.

## Acceptance criteria

- Every family uses the same catalog/proof contract and remains recognizable
  without color or optional audio.
- Unknown IDs resolve to a generic actor fallback without guessing.
- No family record encodes private intent, urgency, outcome, or true state.
- Version and SDD bookkeeping align to v0.12.42.

## Verification

- `python3 -m unittest tests.test_actor_families`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
