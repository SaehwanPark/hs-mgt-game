# Mechanism Design — Forecast Uncertainty Preview Slice

## Goal and Roadmap Phase

Phase 5 §5.4 hardening: add bounded uncertainty preview before interactive turns
without probabilistic forecast objects or new stochastic mechanisms.

## Slice Boundary

- **In:** Pure CLI helper using player observation, prior state cash/policy
  pressure, and ruleset spend bounds per turn; pre-turn display in interactive
  mode; observation note on starting dashboard.
- **Out:** Probabilistic forecasts, new random streams, transition changes, new
  turns, resolved-input leakage beyond existing observation boundary.

## Information Boundary

Preview may use only:

- `WorldState` fields already shown in executive briefing (cash, policy pressure)
- `Observation` fields (reported access, policy briefing, revisions, market
  context briefing)
- `Ruleset` validation spend ceilings for the upcoming turn

Preview must not reveal actor decision outcomes or raw resolved input draws not
already represented in observation.

## Debrief Hooks

No debrief changes. Preview language explicitly disclaims actor-response
forecasting.

## Determinism

No changes to `transition()` or hash semantics. Golden seed-42 trajectory
unchanged.

## Tests

- Observation-only content; no actor outcome keywords
- Turn-specific spend bounds from ruleset
- Market briefing without rival decision labels
