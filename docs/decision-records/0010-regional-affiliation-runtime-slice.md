# ADR-0010: Regional Affiliation Runtime Slice

**Status:** Proposed
**Date:** 2026-07-12
**Deciders:** Project maintainer and implementation agent

## Context

The v0.11.13 affiliation-first design gate identified a credible regional
nonprofit partnership mechanism but intentionally stopped before runtime work.
The next slice needs a narrow scenario boundary and explicit contracts without
changing the existing `competitive-regional-v1` campaign or its golden replay.

## Decision

Propose an opt-in `regional-affiliation-v1` scenario that reuses competitive
transition, observation, history, replay, and debrief primitives. The scenario
is six monthly stages with one human-led Riverside system and one localized
nonprofit partner actor. It is not a second full campaign engine and does not
add AI rivals.

The stages are:

1. assess partner condition and fit;
2. choose independence, deferral, or affiliation pursuit;
3. negotiate community, workforce, and service-continuity commitments;
4. submit the package for institutional review;
5. resolve approval, conditions, delay, or rejection; and
6. begin or decline early integration and record its initial consequences.

The future runtime proposal must define:

- true affiliation state: partner condition, status, commitments, review state,
  integration progress, and existing Riverside organizational metrics;
- Riverside observations: reported partner signals, public labor/community/payer
  signals, review status and uncertainty, obligations, and alternatives;
- explicit resolved inputs for partner response, review response, labor response,
  payer response, community response, and integration drag or continuity shock;
- validated actions, modeled unfavorable outcomes, attributed effects, and
  append-only retention of decision-time observations and resolved inputs; and
- debrief output separating actor utility, organizational outcomes, community
  and social-welfare effects, and decision quality from outcome quality.

All stochastic results must be resolved before deterministic transition
evaluation. Direct acquisition, national consolidation, detailed transaction
finance, legal prediction, and changes to the default competitive campaign are
deferred.

## Consequences

### Positive

- Preserves the existing competitive campaign and seed-42 golden trajectory.
- Provides a concrete implementation target without introducing a generalized
  actor framework.
- Keeps partner, regulator, labor, payer, and community authority distinct.
- Makes replay and educational debrief requirements explicit before code work.

### Negative / tradeoffs

- A later implementation may require a new scenario identifier, command surface,
  ruleset values, replay fields, and state-hash schema version.
- The six-stage abstraction will omit broader deal-market and post-integration
  dynamics.
- Regulatory and community outcomes remain stylized design abstractions.

## Follow-ups

- A separate implementation PR must choose concrete Rust types, scenario fields,
  command syntax, numeric bounds, and replay/hash compatibility policy.
- Domain QA must approve the implementation before runtime promotion.
- Any new shared contested interaction must use prior-snapshot intent evaluation,
  central conflict resolution, and effect application.

## Alternatives Considered

| Alternative | Reason not chosen |
| --- | --- |
| Add the affiliation arc to `competitive-regional-v1` | Would change the default campaign and expand its golden/replay contract prematurely |
| Create a separate campaign engine | Duplicates transition and interface architecture before a slice proves value |
| Implement full acquisition mechanics | Exceeds the current Phase 7/9 bounded-slice gate |

## Verification

- Domain QA confirms the proposal preserves scope, determinism, observation
  boundaries, utility/welfare separation, and debriefability.
- Existing Rust, Python, formatting, clippy, golden, and diff checks remain
  green because this ADR changes no runtime code.

## Related Documents

- [`docs/expansion-proposal-review.md`](../expansion-proposal-review.md)
- [`docs/system-boundary.md`](../system-boundary.md)
- [`docs/scenario-format-draft.md`](../scenario-format-draft.md)
- [`docs/roadmap.md`](../roadmap.md)
