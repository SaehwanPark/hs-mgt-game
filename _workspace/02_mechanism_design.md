# Mechanism Design - Regional Affiliation Observation Context v0.12.2

## Goal and Roadmap Phase

Phase 7.6 educational artifact/debrief review follow-up to the v0.12.1
observation-context finding. This is an interface projection slice, not a new
simulation mechanism.

## Slice Boundary

- Setting: existing `regional-affiliation-v1` six-stage scenario.
- Player view: MCP `SessionEnvelope.observation` only.
- New lines: commitment values/total, current alternatives, and stylized
  assumptions already produced by `observe_affiliation`.
- Verification: focused Rust session tests plus the unchanged 9-coordinate
  post-fix capture.
- Excluded: true-state expansion, transition changes, actor-response changes,
  balance, GUI, legal modeling, and generic observation abstractions.

## Actors and Authority

Riverside sees its own commitments and the scenario's declared alternatives and
assumptions. Partner condition, actor utility, review/labor/payer/community
responses, and future realized effects remain outside the new rendered lines.

## State, Beliefs, and Observations

The formatter will consume `AffiliationObservation` without reading
`AffiliationWorldState` directly. It will render:

- `Commitments: community <n>, workforce <n>, continuity <n>, total <n>`;
- one `Alternative: <text>` line per typed alternative; and
- one `Assumption: <text>` line per typed assumption.

This preserves the typed observation boundary and makes the debrief's
alternative-comparison prompt inspectable at decision time.

## Commands, Events, and Effects

No command, event, effect, transition, resolved input, or state-hash behavior
changes. The existing commands and legal hints remain authoritative.

## Strategic Interaction

No strategic decision procedure changes. The post-fix capture reuses the
independent, deferred, and maximum-commitment pursuit probes from v0.12.1 to
test interface continuity across all staged states.

## Assumptions and Parameters

- `AffiliationCommitments::total()` is the source for the rendered total.
- Existing typed alternative and assumption strings are rendered verbatim.
- No new numeric parameter or dependency is introduced.

## Educational Debrief Hooks

- A player can see the alternatives before choosing posture.
- A player can see the commitments currently carried by the run.
- The stylized/legal boundary assumptions are visible before decisions and can
  be compared with the debrief's actor-response explanation.

## Determinism and Replay Notes

The change is presentation-only. It does not enter transition evaluation,
history, replay artifacts, or state hashing. The post-fix artifact excludes
session IDs and validates the same state hashes as v0.12.1.

## Open Questions

- Human comprehension and educational effectiveness require evidence outside
  this deterministic simulated-policy slice.
- Future observation fields require a separate review against hidden-state and
  actor-authority boundaries.
