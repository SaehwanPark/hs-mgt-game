# Evidence Map - Command-to-Effect Explainability Evidence

## Scope

Audit whether the existing Expert traces connect submitted commands to
action-specific transition evidence and preserved debrief records, with no
runtime changes.

## Sources Reviewed

- Canonical project documents and Phase 7 evidence gates.
- `docs/playtest-findings-v0.10.44.md` through `docs/playtest-findings-v0.10.46.md`.
- The v0.10.46 Expert capture artifact and competitive debrief output contract.

## Evidence Matrix

- Campaign: `competitive-regional-v1`.
- Source: v0.10.46 Expert artifact.
- Profiles: Fiscal Caution, Capacity Growth, Balanced Strategy, and Naive
  First-Time.
- Seeds: `42`, `43`, and `44`.
- Runs reviewed: 12.

## Evidence Boundary

- A supported command has action-specific event/effect evidence and a monthly
  `Player:` debrief record.
- `hold` is explicitly neutral and does not require an effect.
- Deferred matches record trace continuity only; they are not causal claims.
- Actor-visible observations remain decision-time evidence; histories and
  debriefs support retrospective explanation.

## Interpretation Limits

- Deterministic policies are not human players or classroom learners.
- Aggregated effects cannot prove that a command caused an endpoint metric.
- Trace coverage cannot establish debrief clarity, decision quality, balance,
  learning, or policy validity.
- Runtime promotion remains deferred because all reviewed commands were
  traceable and no concrete explainability gap was found.
