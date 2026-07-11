# Mechanism Design - Consultant Advice Validation Evidence

## Goal and Roadmap Phase

Phase 7 validation of the v0.10.39 advice-only baseline without changing game
mechanics.

## Slice Boundary

- Reuse Fiscal Caution, Capacity Growth, Balanced Strategy, and Naive First-Time
  policies.
- Capture seeds 42-44 at Normal and Hard difficulty.
- Record actor-visible observations, submitted commands, accepted transition
  summaries, validation failures, and end-session debriefs.
- Produce machine-readable results and a human-readable diagnostic report.

## Actors and Authority

The MCP wrapper is the capture boundary. The human-system observation remains
the only source for consultant options. Existing scripted policies remain the
decision source; no new actor or AI decision rule is introduced.

## State, Beliefs, and Observations

The runner parses only visible option lines and visible context categories:
cash runway, workforce trust, community trust, and intelligence gaps. It never
reads hidden rival state or recomputes outcomes.

## Commands, Events, and Effects

No commands, events, effects, ruleset values, or transition behavior change.
Submitted commands are retained only to place observed advice beside the
corresponding debrief month.

## Educational Debrief Hooks

The artifact verifies that each month has exact retained option titles and an
advisory comparison line. It deliberately does not score whether a policy
followed an option or label one option as correct.

## Determinism and Replay Notes

The runner reuses the existing seeded MCP server and deterministic policies. It
fails closed on incomplete histories, validation failures, missing A-D options,
missing tradeoffs, missing debrief records, or absent visible variation.

## Open Questions

This slice cannot establish advice quality, learning value, calibration, or
whether a differentiated advisor market would improve the baseline.
