# Implementation Plan — Phase 3.2 uncertainty-overlays v0.12.61

## Objective

Define deterministic symbolic uncertainty-overlay vocabulary needed by later
regional map/environment slices without leaking hidden risk or severity.

## Scope

- Add stale, missing, and revised visible-information overlay tokens.
- Provide non-color patterns, no-severity defaults, reduced-motion behavior,
  written labels, and a generic overlay fallback.
- Add registry hash/provenance, accessible equivalents, focused tests, and SDD
  bookkeeping.
- Keep live rendering, host/session behavior, and hidden-risk inference out of
  scope.

## Acceptance criteria

- Overlay definitions are deterministic and distinguishable without color.
- Severity encoding is absent and reduced motion preserves static semantics.
- Unknown uncertainty IDs use an explicit generic fallback.
- Written contract says the overlays do not quantify hidden risk, severity,
  probability, truth, or future outcome.
- Version and SDD bookkeeping align to v0.12.61.

## Verification

- `python3 -m unittest tests.test_uncertainty_overlays`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
