# Implementation Plan — Phase 2.1 Summit identity kit v0.12.41

## Objective

Complete the fictional Summit identity lane using the established Riverside
and Northlake surface contract and close Phase 2.1.

## Scope

- Add Summit source/release SVG variants for all required identity surfaces.
- Add the Summit identity catalog entry and audio motif recipe.
- Extend the shared proof page with Summit selection and generic fallback.
- Add registry, hashes, credits, accessibility, and authority tests.
- Check Summit's 13 per-system roadmap items and close the Phase 2.1 exit.

## Acceptance criteria

- Summit, Riverside, and Northlake remain visually distinct while sharing one
  surface vocabulary and fallback contract.
- Source/release SVGs contain accessible labels and no external references.
- Summit's identity and motif remain visible-only fixture semantics.
- Version and SDD bookkeeping align to v0.12.41.

## Verification

- `python3 -m unittest tests.test_summit_identity tests.test_northlake_identity tests.test_riverside_identity tests.test_audio_direction`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
