# Presentation Contract — Phase 3.2 service-area-overlays v0.12.60

## Goal and Authorization

Define deterministic symbolic service-area overlay tokens for facility, map,
report, and consequence surfaces while preserving the completed map-grid,
road-token, district-token, parcel-system, relationship-line, and generic
fallback contracts.

## Player Questions and Consequences

- Which visible service-area category is involved?
- Which contour and fill patterns help distinguish it without color?
- Is the overlay a primary, shared, or coordinated visible relationship?
- What appears when a service-area token is unavailable?

## Actor-Visible Source Ledger

| Surface | Visible source | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| Primary area | Fixture-only symbolic service-area vocabulary | Real-world catchment, distance, travel time, population, access, jurisdiction, or performance | Primary label and solid/hatch pattern |
| Shared area | Token-defined paired contour and crosshatch | Shared capacity, demand, or operational outcome | Shared label and paired/crosshatch pattern |
| Coordinated area | Token-defined dash-dot contour and sparse hatch | Coordination success, authority, or future outcome | Coordinated label and dash-dot/hatch pattern |
| Missing area | Missing/unknown service-area token | Guessed scope or metric | Generic service-area fallback |

## Visual, Motion, and Audio Semantics

- Overlays use deterministic contour/fill patterns without metric encoding.
- Directionality is not encoded by the overlay catalog; a later actor-visible
  instance may only expose direction if its source explicitly supplies it.
- Patterns organize symbolic service relationships and attention; they do not
  establish real-world catchment, distance, travel time, population, access,
  jurisdiction, or performance.
- Selection is local presentation state; uncertainty remains explicitly stale
  or missing rather than being resolved by the client.

## Accessibility and Fallbacks

- Overlays carry written category and contour/fill pattern equivalents plus an
  information-boundary disclaimer.
- Unknown or unavailable overlay IDs use `service-area-generic` rather than
  being inferred by the client.

## Authority, History, and Replay Boundaries

The service-area catalog and proof consume only local fixture IDs and labels.
They do not load host DTOs, infer rival information, submit commands, create
session state, or alter transitions, history, hashes, replay, audio state, or
debriefs.

## Asset Provenance and Release Requirements

The service-area catalog remains registry-backed with a current hash, project
provenance, accessible equivalents, visible sources, approval, and no
third-party or external references.

## Verification and Evidence Limits

Focused tests cover all service-area categories, symbolic-only geometry,
metric-free defaults, the shared fallback, non-color patterns, asset boundary,
and syntax. These are technical checks, not human design, contrast,
accessibility, learning, or policy evidence.

## Non-Goals and Open Questions

Do not promote the catalog into live board rendering, infer private or hidden
service relationships, or claim human design, accessibility, learning, or
policy evidence in this slice.
