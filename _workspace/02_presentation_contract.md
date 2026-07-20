# Presentation Contract — Phase 3.2 district-tiles v0.12.57

## Goal and Authorization

Define deterministic symbolic district tokens for facility, map, report, and
consequence surfaces while preserving the completed map-grid, road-token, and
generic fallback contracts.

## Player Questions and Consequences

- Which visible district type is involved?
- Which non-color pattern helps distinguish the district?
- Can the layout remain understandable when geography is symbolic?
- What appears when a district token is unavailable?

## Actor-Visible Source Ledger

| Surface | Visible source | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| District token | Fixture-only symbolic district vocabulary | Real-world land use, population, ownership, zoning, travel time, or jurisdiction | District type and non-color pattern labels |
| District pattern | Token-defined block, campus, or civic mark | Hidden demand, workforce, capacity, or performance | Written pattern equivalent |
| Missing district | Missing/unknown district token | Guessed district type | Generic district fallback |

## Visual, Motion, and Audio Semantics

- District tokens use a stable 192x144 viewBox, 24px grid, and 8x6-cell
  footprint.
- Tokens organize symbolic relationships and attention; they do not establish
  real-world land use, population, ownership, zoning, travel time, or
  jurisdiction.
- Each pattern varies visible structure, not hidden state.
- Selection is local presentation state; uncertainty remains explicitly stale
  or missing rather than being resolved by the client.

## Accessibility and Fallbacks

- Tokens carry written district-type and non-color-pattern equivalents plus a
  symbolic-geography disclaimer.
- Unknown or unavailable district IDs use `district-generic` rather than being
  inferred by the client.

## Authority, History, and Replay Boundaries

The district catalog and proof consume only local fixture IDs and labels. They
do not load host DTOs, infer rival information, submit commands, create session
state, or alter transitions, history, hashes, replay, audio state, or debriefs.

## Asset Provenance and Release Requirements

The district catalog remains registry-backed with a current hash, project
provenance, accessible equivalents, visible sources, approval, and no
third-party or external references.

## Verification and Evidence Limits

Focused tests cover all district types, the shared fallback, non-color
patterns, asset boundary, and syntax. These are technical checks, not human
design, contrast, accessibility, learning, or policy evidence.

## Non-Goals and Open Questions

Do not promote the catalog into live board rendering, infer private facility or
district state, or claim human design, accessibility, learning, or policy
evidence in this slice.
