# Evidence Map

## Scope

Test whether the current post-difficulty code preserves bounded clearability,
strategy-trace variation, operating accounting, and decision-to-debrief
inspectability across the existing competitive all-tier matrix.

## Sources Reviewed

- `SPEC.md`, especially the Phase 7 validation gate and ranked queue.
- `docs/roadmap.md`, `docs/design_principles.md`, and the active agent-playtest
  protocol.
- The v0.11.1 five-profile all-tier runner and operating audit.
- The v0.11.9 post-change Expert validation artifact.
- The v0.11.10 source-contract synthesis and findings.

## Mechanisms and Institutions

- Difficulty changes rival count, action budgets, starting rival resources, and
  AI risk posture through existing competitive setup and actor logic.
- The player remains evaluated through actor-visible observations and submitted
  commands; committed history and debriefs provide retrospective explanation.
- Operating effects are validated through demand, treated volume, unmet demand,
  revenue, cost, and cash-margin identities.

## Actor Incentives and Information

- Policy profiles are deterministic simulated-player lanes, not learner types,
  validated strategy classes, or utility functions.
- Rival actions and rationales in committed history are engine evidence; they
  must not be treated as information the player possessed unless exposed in the
  actor-visible observation.
- Player and rival operating outcomes remain separate evidence boundaries.

## Assumptions

- The five existing profiles, three seeds, four difficulty tiers, 24-month
  campaign, ruleset, and state-hash schema remain the active validation surface.
- The seed-42 Normal hold-control hash is the compatibility control.
- Current-code all-tier results may differ from historical policy trajectories;
  those differences are descriptive and not cross-version causal comparisons.

## Unresolved Questions

- Whether the tested profiles represent broad player strategy space remains
  unresolved.
- Whether completion or endpoint variation establishes balance, winnability,
  strategy quality, or causal value remains unresolved.
- Human comprehension, classroom learning, calibration, and policy validity
  require separate evidence.

## Design Implications

- Reuse the existing versioned artifact shape rather than creating a generalized
  evidence schema.
- Keep runtime promotion deferred and route any discovered gap to a separate
  proposal or implementation slice.
- Report action frequencies, trajectory counts, endpoint ranges, bottlenecks,
  and threshold candidates as diagnostic signals only.

## Risks

- A failed or partial coordinate can be hidden by aggregate summaries; the
  validator must require exact coordinate coverage and preserve failures.
- Hidden engine state can leak into interpretation; findings must label true
  history separately from actor-visible decision context.
- Reusing historical artifacts could mask post-change behavior; this slice must
  launch current-code sessions rather than compare old endpoint hashes.
