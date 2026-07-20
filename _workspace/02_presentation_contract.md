# Presentation Contract — Phase 3.2 map-grid v0.12.55

## Goal and Authorization

Define a deterministic symbolic regional map coordinate contract for facility,
map, report, and consequence surfaces while preserving the completed identity
and generic fallback contracts.

## Player Questions and Consequences

- Which recurring public system is involved?
- Which visible entity or facility is involved?
- Which named coordinate organizes the visible relationship?
- Can the layout remain understandable when geography is symbolic?
- What appears when a coordinate or entity is unavailable?

## Actor-Visible Source Ledger

| Surface | Visible source | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| Map coordinate | Fixture-only symbolic layout coordinate | Real-world distance or geography | Named column/row coordinate |
| Entity placement | Visible entity/facility ID | Hidden location or relationship | Visible label and coordinate equivalent |
| Missing coordinate | Missing/unknown layout coordinate | Guessed position | Explicit unavailable coordinate |

## Visual, Motion, and Audio Semantics

- The regional map uses a stable 960x600 viewport and deterministic 24px cells.
- Grid coordinates organize symbolic relationships and attention; they do not
  establish real-world distance, travel time, jurisdiction, or geography.
- Each layer varies visible structure and pattern, not hidden state.
- Selection is local presentation state; uncertainty remains explicitly stale
  or missing rather than being resolved by the client.

## Accessibility and Fallbacks

- The contract carries a written symbolic-geography disclaimer and named
  coordinate equivalent.
- Unknown or unavailable coordinates remain explicitly unavailable rather than
  being inferred by the client.

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
