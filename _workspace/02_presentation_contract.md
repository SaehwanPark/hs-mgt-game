# Presentation Contract — Phase 3.2 uncertainty-overlays v0.12.61

## Goal and Authorization

Define deterministic symbolic uncertainty-overlay tokens for facility, map,
report, and consequence surfaces while preserving the completed map-grid,
road-token, district-token, parcel-system, relationship-line, service-area,
and generic fallback contracts.

## Player Questions and Consequences

- Is the visible information stale, missing, or revised?
- Which non-color pattern helps distinguish that status?
- Can reduced motion preserve the same meaning?
- What appears when an uncertainty token is unavailable?

## Actor-Visible Source Ledger

| Surface | Visible source | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| Stale status | Fixture-only symbolic uncertainty vocabulary | Hidden risk, severity, probability, truth, or future outcome | Stale label and dash-dot/hatch pattern |
| Missing status | Token-defined dashed/crosshatch style | Cause, magnitude, or resolution of missing information | Missing label and dashed/crosshatch pattern |
| Revised status | Token-defined solid/sparse-hatch style | Proof of truth, correction quality, or future outcome | Revised label and solid/sparse-hatch pattern |
| Missing overlay | Missing/unknown uncertainty token | Guessed information status | Generic uncertainty fallback |

## Visual, Motion, and Audio Semantics

- Overlays use deterministic non-color boundary/fill patterns.
- Severity encoding is always `none` in this catalog.
- Motion is always `none`; reduced-motion presentation therefore preserves the
  same static semantic pattern.
- Patterns identify explicit visible information status; they do not quantify
  hidden risk, severity, probability, truth, or future outcome.
- Selection is local presentation state; uncertainty remains explicitly stale,
  missing, or revised rather than being resolved by the client.

## Accessibility and Fallbacks

- Overlays carry written information-status and non-color-pattern equivalents,
  explicit reduced-motion behavior, and an information-boundary disclaimer.
- Unknown or unavailable overlay IDs use `uncertainty-generic` rather than
  being inferred by the client.

## Authority, History, and Replay Boundaries

The uncertainty catalog and proof consume only local fixture IDs and labels.
They do not load host DTOs, infer rival information, submit commands, create
session state, or alter transitions, history, hashes, replay, audio state, or
debriefs.

## Asset Provenance and Release Requirements

The uncertainty catalog remains registry-backed with a current hash, project
provenance, accessible equivalents, visible sources, approval, and no
third-party or external references.

## Verification and Evidence Limits

Focused tests cover all uncertainty categories, no-severity and reduced-motion
defaults, the shared fallback, non-color patterns, asset boundary, and syntax.
These are technical checks, not human design, contrast, accessibility,
learning, or policy evidence.

## Non-Goals and Open Questions

Do not promote the catalog into live board rendering, infer private or hidden
risk, or claim human design, accessibility, learning, or policy evidence in
this slice.
