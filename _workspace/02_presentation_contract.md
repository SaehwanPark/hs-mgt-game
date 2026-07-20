# Presentation Contract — Phase 3.2 relationship-lines v0.12.59

## Goal and Authorization

Define deterministic symbolic relationship-line styles for facility, map,
report, and consequence surfaces while preserving the completed map-grid,
road-token, district-token, parcel-system, and generic fallback contracts.

## Player Questions and Consequences

- Which visible relationship category is involved?
- Which non-color pattern helps distinguish that category?
- Is the relationship uncertain or stale?
- What appears when a relationship style is unavailable?

## Actor-Visible Source Ledger

| Surface | Visible source | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| Peer line | Fixture-only symbolic relationship-line vocabulary | Hidden intent, causality, strength, direction, distance, or future outcome | Peer label and solid-line pattern |
| Service line | Token-defined paired-line style | Operational dependency, volume, or capacity not supplied by the host | Service label and paired-line pattern |
| Policy line | Token-defined dash-dot style | Authority, influence, or policy outcome not supplied by the host | Policy label and dash-dot pattern |
| Uncertain line | Token-defined dotted style | Resolution of stale or missing information | Uncertain label and dotted pattern |
| Missing relationship | Missing/unknown relationship style | Guessed relationship category | Generic relationship fallback |

## Visual, Motion, and Audio Semantics

- Styles use deterministic line patterns, a stable 2px width, round caps, and
  no arrowheads.
- Directionality is not encoded by the style catalog; a relationship instance
  may only expose direction if the actor-visible source explicitly supplies it.
- Patterns organize symbolic relationships and attention; they do not infer
  hidden intent, causality, strength, direction, distance, or future outcome.
- Selection is local presentation state; uncertainty remains explicitly stale
  or missing rather than being resolved by the client.

## Accessibility and Fallbacks

- Styles carry written relationship-type and non-color-pattern equivalents plus
  an information-boundary disclaimer.
- Unknown or unavailable style IDs use `relationship-generic` rather than
  being inferred by the client.

## Authority, History, and Replay Boundaries

The relationship-style catalog and proof consume only local fixture IDs and
labels. They do not load host DTOs, infer rival information, submit commands,
create session state, or alter transitions, history, hashes, replay, audio
state, or debriefs.

## Asset Provenance and Release Requirements

The relationship-style catalog remains registry-backed with a current hash,
project provenance, accessible equivalents, visible sources, approval, and no
third-party or external references.

## Verification and Evidence Limits

Focused tests cover all relationship categories, non-directional defaults, the
shared fallback, non-color patterns, asset boundary, and syntax. These are
technical checks, not human design, contrast, accessibility, learning, or
policy evidence.

## Non-Goals and Open Questions

Do not promote the catalog into live board rendering, infer private or hidden
relationships, or claim human design, accessibility, learning, or policy
evidence in this slice.
