# Presentation Contract — Phase 3.2 road-tiles v0.12.56

## Goal and Authorization

Define deterministic symbolic road-segment tokens for facility, map, report,
and consequence surfaces while preserving the completed identity and generic
fallback contracts.

## Player Questions and Consequences

- Which recurring public system is involved?
- Which visible entity or facility is involved?
- Which visible road orientation is involved?
- Which path role explains the road token?
- Can the layout remain understandable when geography is symbolic?
- What appears when a road token is unavailable?

## Actor-Visible Source Ledger

| Surface | Visible source | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| Road token | Fixture-only symbolic road-segment vocabulary | Real-world geometry or travel time | Orientation and path-role labels |
| Path role | Token-defined surface/centerline role | Hidden traffic or capacity fact | Written path-role equivalent |
| Missing road | Missing/unknown road token | Guessed segment | Generic road fallback |

## Visual, Motion, and Audio Semantics

- Road tokens use a stable 96x96 viewBox and deterministic 24px grid.
- Segments organize symbolic relationships and attention; they do not establish
  real-world road geometry, travel time, jurisdiction, or geography.
- Each layer varies visible structure and pattern, not hidden state.
- Selection is local presentation state; uncertainty remains explicitly stale
  or missing rather than being resolved by the client.

## Accessibility and Fallbacks

- Tokens carry written orientation/path-role equivalents and a symbolic-
  geography disclaimer.
- Unknown or unavailable road IDs use `road-generic` rather than being inferred
  by the client.

## Authority, History, and Replay Boundaries

The facility catalog and proof consume only local fixture IDs and labels. They
do not load host DTOs, infer rival information, submit commands, create session
state, or alter transitions, history, hashes, replay, audio state, or debriefs.

## Asset Provenance and Release Requirements

The generated family catalog remains registry-backed with a current hash,
project provenance, accessible equivalents, visible sources, approval, and no
third-party or external references.

## Verification and Evidence Limits

Focused tests cover all facility layers, shared fallback, non-color patterns,
asset boundary, and syntax. These are technical checks, not human design,
contrast, accessibility, learning, or policy evidence.

## Non-Goals and Open Questions

Do not promote the component into live board rendering, infer private facility
state, or claim human design, accessibility, learning, or policy evidence in
this slice.
