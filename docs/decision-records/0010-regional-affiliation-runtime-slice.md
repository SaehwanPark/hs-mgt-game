# ADR-0010: Regional Affiliation Runtime Slice

**Status:** Implemented in v0.12.0
**Date:** 2026-07-12
**Deciders:** Project maintainer and implementation agent

## Context

The v0.11.13 affiliation-first design gate identified a credible regional
nonprofit partnership mechanism but intentionally stopped before runtime work.
The next slice needs a narrow scenario boundary and explicit contracts without
changing the existing `competitive-regional-v1` campaign or its golden replay.

## Decision

Implement an opt-in `regional-affiliation-v1` scenario that reuses competitive
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

## Implementation

- `src/model/affiliation.rs` owns typed state, commands, ruleset, observations,
  resolved inputs, immutable history, and replay records.
- `src/affiliation/` provides genesis, observation, validation, deterministic
  transition, and replay functions; `src/inputs/resolve_affiliation.rs` resolves
  stochastic outcomes before transition evaluation.
- The six-stage CLI/MCP command surface is `assess`, `posture`, `commit`,
  `submit_review`, `await_review`, `integrate`, and `hold`.
- Affiliation uses ruleset `regional-affiliation-ruleset-0.1.0`, state-hash
  schema `regional-affiliation-state-hash-v1`, and replay artifact
  `regional-affiliation-replay-v1`; competitive hashes remain unchanged.

## Follow-ups

- Domain QA should validate educational balance and interpretation before broader
  scenario expansion.
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
- Rust, Python, formatting, clippy, golden, replay, MCP, and diff checks pass.

## Related Documents

- [`docs/expansion-proposal-review.md`](../expansion-proposal-review.md)
- [`docs/system-boundary.md`](../system-boundary.md)
- [`docs/scenario-format-draft.md`](../scenario-format-draft.md)
- [`docs/roadmap.md`](../roadmap.md)
