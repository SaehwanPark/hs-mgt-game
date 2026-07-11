# Mechanism Design

## Goal and Roadmap Phase

Phase 7 AI-agent gameplay validation of the v0.11.0 monthly operating loop.

## Slice Boundary

- Competitive campaign only.
- Five external scripted policy lanes × three seeds × four difficulty levels.
- One 24-month run per matrix coordinate.
- No transition, command, actor, scenario, MCP, or replay changes.

## Actors and Authority

The existing Riverside player system and existing AI rival systems remain the
only actors. The five policy lanes are test-client behavior, not runtime actor
definitions.

## State, Beliefs, and Observations

The audit uses actor-visible observations, legal-resource hints, submitted
commands, transition summaries, attributed effects, state hashes, and debriefs.
It does not infer rival private operating state.

## Commands, Events, and Effects

The runner submits existing commands only. Each operating month must expose:
demand, treated volume, unmet demand, revenue, cost, and cash-margin effect, plus
the Riverside operations event. Invalid commands are not expected-policy evidence.

## Strategic Interaction

The lanes vary priorities among access, commercial negotiation, workforce,
capital modernization, and coalition/legitimacy. Difficulty changes only the
existing rival configuration and resource rules.

## Assumptions and Parameters

- `demand = treated + unmet`.
- `margin = revenue - cost`.
- Operating cash effect equals margin.
- Observed effect ranges and threshold crossings are descriptive only.

## Educational Debrief Hooks

The artifact preserves month-level observation, action, transition, operating
effect, hash, and debrief continuity so reviewers can inspect what was visible
and what followed. It does not score decisions or learning.

## Determinism and Replay Notes

The runner builds the local MCP binary, uses fixed seeds and policy order, writes
timestamp-free sorted JSON, and separately checks the known seed-42 Normal
hold-control hash.

## Open Questions

Loss and bottleneck patterns need a future controlled evidence slice before any
runtime or balance change is considered.
