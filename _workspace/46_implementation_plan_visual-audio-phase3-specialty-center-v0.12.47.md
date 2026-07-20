# Implementation Plan — Phase 3.1 specialty-center v0.12.47

## Objective

Extend the reusable facility layer contract to a distinct fictional specialty
center without creating a second rendering path.

## Scope

- Add specialty-center source/release SVG derivatives using the shared 8px
  grid and system color variables.
- Provide base, identity, capacity, project, pressure, selection, and
  uncertainty layers with visible sources and written equivalents.
- Extend the shared facility catalog/proof selector, registry hashes,
  accessible labels, generic fallback, tests, and SDD bookkeeping.
- Keep the component outside live board rendering and host/session behavior.

## Acceptance criteria

- Specialty center is visually distinct from existing components while using
  the same layer IDs and fallback contract.
- Source/release assets are external-reference-free, deterministic, and usable
  in monochrome and at small size.
- The peaked-canopy type cue does not imply clinical scope, capacity, ownership,
  or hidden outcome.
- Version and SDD bookkeeping align to v0.12.47.

## Verification

- `python3 -m unittest tests.test_specialty_center tests.test_ambulatory_center tests.test_emergency_department tests.test_patient_tower tests.test_general_hospital_base`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
