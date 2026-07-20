# Implementation Plan — Phase 3.1 research-education-building v0.12.52

## Objective

Extend the reusable facility layer contract to a distinct fictional research
and education building without creating a second rendering path or outcome
claim.

## Scope

- Add research-education-building source/release SVG derivatives using the
  shared 8px grid and system color variables.
- Provide base, identity, capacity, project, pressure, selection, and
  uncertainty layers with visible sources and written equivalents.
- Extend the shared facility catalog/proof selector, registry hashes,
  accessible labels, generic fallback, tests, and SDD bookkeeping.
- Keep the component outside live board rendering and host/session behavior.

## Acceptance criteria

- Research and education building is visually distinct from existing components
  while using the same layer IDs and fallback contract.
- Source/release assets are external-reference-free, deterministic, and usable
  in monochrome and at small size.
- The wing-and-tower type cue does not imply research or education outcome,
  ownership, or hidden capacity.
- Version and SDD bookkeeping align to v0.12.52.

## Verification

- `python3 -m unittest tests.test_research_education_building tests.test_utility_plant tests.test_parking_structure tests.test_administrative_headquarters tests.test_rural_clinic tests.test_specialty_center tests.test_ambulatory_center tests.test_emergency_department tests.test_patient_tower tests.test_general_hospital_base`
- Full Python, Rust, Clippy, formatting, Node, asset/credits, metadata,
  documentation-link, and diff checks before PR handoff.
