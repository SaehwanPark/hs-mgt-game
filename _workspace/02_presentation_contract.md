# Presentation Contract — Phase 3.2 parcel-system v0.12.58

## Goal and Authorization

Define deterministic symbolic parcel tokens for facility, map, report, and
consequence surfaces while preserving the completed map-grid, road-token,
district-token, and generic fallback contracts.

## Player Questions and Consequences

- Which visible parcel type is involved?
- Which non-color pattern helps distinguish the parcel?
- Can a facility placement slot be shown without claiming ownership or status?
- What appears when a parcel token is unavailable?

## Actor-Visible Source Ledger

| Surface | Visible source | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| Facility parcel | Fixture-only symbolic parcel vocabulary | Ownership, availability, operational status, or facility outcome | Parcel type and placement-slot labels |
| Undeveloped parcel | Token-defined dashed boundary and open-area mark | Development potential, ownership, land value, zoning, or future use | Written type and pattern equivalent |
| Missing parcel | Missing/unknown parcel token | Guessed parcel type | Generic parcel fallback |

## Visual, Motion, and Audio Semantics

- Parcel tokens use a stable 144x120 viewBox, 24px grid, and 6x5-cell
  footprint.
- Tokens organize symbolic placement; they do not establish real-world
  ownership, availability, development potential, land value, zoning,
  geography, or future use.
- Each pattern varies visible structure, not hidden state.
- Selection is local presentation state; uncertainty remains explicitly stale
  or missing rather than being resolved by the client.

## Accessibility and Fallbacks

- Tokens carry written parcel-type and non-color-pattern equivalents plus a
  symbolic-placement disclaimer.
- Unknown or unavailable parcel IDs use `parcel-generic` rather than being
  inferred by the client.

## Authority, History, and Replay Boundaries

The parcel catalog and proof consume only local fixture IDs and labels. They do
not load host DTOs, infer rival information, submit commands, create session
state, or alter transitions, history, hashes, replay, audio state, or debriefs.

## Asset Provenance and Release Requirements

The parcel catalog remains registry-backed with a current hash, project
provenance, accessible equivalents, visible sources, approval, and no
third-party or external references.

## Verification and Evidence Limits

Focused tests cover all parcel types, the shared fallback, non-color patterns,
asset boundary, and syntax. These are technical checks, not human design,
contrast, accessibility, learning, or policy evidence.

## Non-Goals and Open Questions

Do not promote the catalog into live board rendering, infer private facility or
parcel state, or claim human design, accessibility, learning, or policy
evidence in this slice.
