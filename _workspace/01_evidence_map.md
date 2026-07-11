# Evidence Map - Expert Clearability Evidence

## Scope

Capture bounded Expert completion evidence for the current competitive campaign
using existing simulated-policy profiles and no runtime changes.

## Sources Reviewed

- Canonical project documents and Phase 7 evidence gates.
- `docs/playtest-findings-v0.10.35.md` through `docs/playtest-findings-v0.10.45.md`.
- `scripts/play_game.py` and existing policy functions in
  `scripts/run_automated_playtests.py`.

## Evidence Matrix

- Campaign: `competitive-regional-v1`.
- Difficulty: Expert.
- Profiles: Fiscal Caution, Capacity Growth, Balanced Strategy, and Naive
  First-Time.
- Seeds: `42`, `43`, and `44`.
- Expected runs: 12.

## Evidence Boundary

- Completion means 24 recorded transitions without validation failure.
- Actor-visible observations and legal hints are the decision-time evidence.
- Histories, hashes, and debriefs support retrospective explanation only.
- Completion is a bounded clearability proxy, not a win condition or broad
  winnability result.

## Interpretation Limits

- Deterministic policies are not human players or classroom learners.
- Profile and seed coverage cannot establish all strategies, skills, or
  stochastic conditions.
- Endpoint differences are descriptive and non-causal.
- Runtime promotion remains deferred without a concrete unexplained gap.
