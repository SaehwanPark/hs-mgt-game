# Implementation Plan — Phase 3.1 general-hospital base v0.12.43

## Objective

Prove one reusable fictional general-hospital base component with the complete
Phase 3.1 per-component layer contract.

## Scope

- Add source/release SVG derivatives using a shared 8px grid and system color
  variables.
- Define base, identity, capacity, project, pressure, selection, and
  uncertainty layers with visible sources and written equivalents.
- Add registry hashes, accessible labels, generic facility fallback, fixture
  proof, tests, and SDD bookkeeping.
- Keep the component outside live board rendering and host/session behavior.

## Acceptance criteria

- Source/release assets are accessible, external-reference-free, deterministic,
  and usable in monochrome and at small size.
- Layer patterns communicate visible categories without color alone or hidden
  facility state.
- Unknown facility kinds resolve to generic fallback without guessing.
- Version and SDD bookkeeping align to v0.12.43.

## Verification

- `python3 -m unittest tests.test_general_hospital_base`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
