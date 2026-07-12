# Request Summary — Workforce Capacity Observation Context v0.12.6

## Decision

Implement the bounded v0.12.5 follow-up: render safe typed staffing and
physical-capacity values in the competitive MCP observation.

## Target slice

- Add exactly two observation lines from `PlayerObservation`.
- Add a focused session-boundary test.
- Rerun the compatible matrix and compare complete histories and state hashes.

## Explicit non-goals

No difficulty values, balance, transitions, command legality, hidden state,
effective capacity, future hires, rival private workforce state, scoring,
winnability, or human-learning claims.
