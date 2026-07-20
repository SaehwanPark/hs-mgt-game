# Presentation Contract — Phase 3.1 emergency-department v0.12.45

## Goal and Authorization

Make a fictional emergency department reusable across facility, map, report,
and consequence surfaces while preserving the completed identity and generic
fallback contracts.

## Player Questions and Consequences

- Which recurring public system is involved?
- Which visible facility kind is involved?
- Which visible layer explains the facility presentation?
- Can the component remain recognizable in monochrome and at small size?
- What appears when a public identity is unavailable?

## Actor-Visible Source Ledger

| Surface | Visible source | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| Facility base | Visible facility kind | Unobserved facility condition | Facility label and base silhouette |
| Identity layer | Visible owning-system identity | Hidden ownership or intent | Identity badge and written label |
| Capacity/project/pressure layers | Visible status fields | Hidden metric or outcome | Layer pattern and written label |
| Selection layer | Local selected-facility presentation state | Host selection fact | Focus outline and selected label |
| Uncertainty layer | Visible freshness/missingness | Guessed current state | Stale/uncertain pattern and text |
| Missing facility | Missing/unknown visible kind | Guessed facility type | Generic facility fallback |

## Visual, Motion, and Audio Semantics

- The entrance-wing silhouette uses a shared 8px grid, system color variables,
  and a stable viewBox distinct from the general-hospital base and patient
  tower.
- Each layer varies visible structure and pattern, not hidden state.
- Selection is local presentation state; uncertainty remains explicitly stale
  or missing rather than being resolved by the client.

## Accessibility and Fallbacks

- Source/release SVGs carry title/description, system-ui labels, and a written
  layer equivalent.
- Shared proof controls are native keyboard buttons and retain visible labels.
- Unknown facility kinds use `generic-facility`; unavailable assets leave the
  facility label and written equivalent.

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
