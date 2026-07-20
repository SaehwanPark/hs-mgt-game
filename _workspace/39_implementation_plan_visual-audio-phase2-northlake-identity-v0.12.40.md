# Implementation Plan — Phase 2.1 Northlake identity kit v0.12.40

## Objective

Complete the fictional Northlake identity lane using the tested Riverside
surface contract and shared selector proof.

## Scope

- Add Northlake source/release SVG variants for all required identity surfaces.
- Add the Northlake identity catalog entry and audio motif recipe.
- Extend the shared proof page with Northlake selection and generic fallback.
- Add registry, hashes, credits, accessibility, and authority tests.
- Check Northlake's 13 per-system roadmap items while Summit remains unchecked.

## Acceptance criteria

- Northlake and Riverside remain visually distinct and use the same surface
  vocabulary and fallback contract.
- Source/release assets contain accessible labels and no external references.
- Northlake's identity and motif remain visible-only fixture semantics.
- Version and SDD bookkeeping align to v0.12.40.

## Verification

- `python3 -m unittest tests.test_northlake_identity tests.test_riverside_identity`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
