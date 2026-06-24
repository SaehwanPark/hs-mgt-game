# Mechanism Design — Competitor Capacity Slice

## Goal and Roadmap Phase

Phase 5 world-slice expansion: add one competitive capacity interaction as
roadmap §3.3 third strategic form. Fifth executive turn after coalition turn.

## Slice Boundary

- **In:** One rival nonprofit health system, capacity-expansion threat, player
  defensive response command, competitor deterministic decision, fifth-turn replay,
  debrief, preset paths, golden test update.
- **Out:** Market-entry relocation, Medicare/Medicaid, scenario loader, forecast UI.

## Actors and Authority

- **Player CEO:** Allocates defensive capital and access posture; cannot control
  competitor expansion directly.
- **Rival regional health system (`competitor_health_system`):** Responds to
  player credibility with accelerate, hold, or partial retreat.

## State, Beliefs, and Observations

- True state unchanged structurally; competitor signal enters via resolved input
  `competitor_market_signal` when `prior.turn >= 4` (fifth decision).
- CEO briefing adds `market_competition_briefing` on turn 5 from observation.

## Commands, Events, and Effects

- `RespondToCompetitorCapacityMove { defensive_capital_commitment, access_posture }`
- Validation: non-negative capital within max; positive access posture within max.
- Player effects: cash spend, access gain, modest bed addition from capital.
- Competitor effects: access/trust/rate pressure (accelerate) vs relief (retreat).

## Strategic Interaction

- **Form:** Competitive capacity expansion response (not market entry).
- **Procedure:** Threshold-based credible/strong offer evaluation using
  `competitor_market_signal` as exogenous pressure.
- **Outcomes:** `AccelerateExpansion`, `HoldPosition`, `PartialRetreat`.

## Debrief Hooks

- Competitive tradeoff: defensive spend vs market share and community trust.
- Decision quality separate from competitor realization under market signal.

## Determinism

- `competitor_market_signal` from named stream `STREAM_COMPETITOR` at turn 5 only
  (zero on turns 1–4 to preserve golden trajectory for first four transitions).

## Tests

- Validation failures, decision branches, five-transition replay, golden hash,
  preset path 1–4 regression, artifact round-trip.
