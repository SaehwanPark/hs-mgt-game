# Evidence Map - Strategy-Diversity Evidence

## Scope

Audit descriptive strategy variation in the existing Expert traces without
changing runtime behavior or treating endpoint differences as causal evidence.

## Sources Reviewed

- Canonical project documents and Phase 7 evidence gates.
- `docs/playtest-findings-v0.10.44.md` through `docs/playtest-findings-v0.10.47.md`.
- The v0.10.46 Expert capture artifact and competitive debrief output contract.

## Evidence Matrix

- Campaign: `competitive-regional-v1`.
- Source: v0.10.46 Expert artifact.
- Profiles: Fiscal Caution, Capacity Growth, Balanced Strategy, and Naive
  First-Time.
- Seeds: `42`, `43`, and `44`.
- Runs reviewed: 12.

## Mechanisms and Institutions

- The audit observes player command choices, action families, repeated
  trajectories, and final debrief tradeoff records.
- It does not add or reinterpret a health-policy mechanism.

## Actor Incentives and Information

- Profiles are deterministic scripted policies using actor-visible observations
  and legal command hints.
- The source debrief records support retrospective inspection; they do not
  reveal information unavailable at decision time.

## Assumptions

- Command-family normalization is a descriptive grouping, not a strategy
  taxonomy or utility function.
- Final tradeoff values are endpoint descriptions, not treatment outcomes.

## Unresolved Questions

- Whether human players would perceive these profiles as meaningfully distinct.
- Whether repeated play produces strategically interesting choices beyond these
  four deterministic policies.

## Design Implications

- The current evidence supports keeping runtime and balance unchanged.
- A future runtime change still requires a concrete player-facing, instructor-
  facing, or domain-review gap that existing traces cannot explain.

## Risks

- Deterministic profile and seed coverage cannot establish general strategy
  diversity, balance, winnability, or educational effectiveness.
- Common actions must not be described as dominant or optimal without stronger
  evidence.

## Interpretation Limits

- Deterministic policies are not human players or classroom learners.
- Endpoint tradeoffs cannot prove that a command caused an outcome.
- Strategy signatures cannot establish optimality, balance, learning, or policy
  validity.
- Runtime promotion remains deferred because this artifact identifies no
  concrete unexplained runtime gap.
