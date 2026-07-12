# Affiliation Runtime Boundary Proposal — v0.12.7

- **Decision:** existing bounded runtime satisfies the proposal contract
- **New runtime changes authorized:** no
- **Runtime promotion:** deferred

The opt-in `regional-affiliation-v1` runtime already implements the minimum contract required by the affiliation-first design gate. This version reconciles the proposal, source boundaries, and committed evidence; it does not add another affiliation mechanism.

## Contract coverage

| Contract | Status |
| --- | --- |
| True State | supported |
| Actor Observation | supported |
| Resolved Inputs | supported |
| Deterministic Core | supported |
| History And Replay | supported |
| Debrief | supported |

## Evidence

- Source artifact: `_workspace/experiments/v0.12.2-affiliation-observation-context/results.json` (code version `0.12.2`).
- Complete runs: 9/9.
- Committed stages: 54.
- Observations with typed commitments, alternatives, and assumptions: 54.
- Source-marker audit: all required state, observation, input, transition, replay, MCP, scenario, and debrief markers supported.

## Boundary decision

- The runtime remains an opt-in `regional-affiliation-v1` scenario and does not alter `competitive-regional-v1`.
- Stochastic outcomes are resolved before deterministic transition evaluation and retained in append-only transitions.
- The debrief distinguishes Riverside outcomes, actor responses, actor utility, social welfare, and decision quality.
- Direct acquisition, deal finance, national markets, legal forecasts, and generic actor-framework expansion remain deferred.

## Evidence limits

- This is a source-boundary and deterministic trace review, not human-learning, classroom, calibration, legal-validity, or policy-forecast evidence.
- The 9-run/54-stage artifact supports contract coverage for named policies and seeds; it does not establish general balance, winnability, or social-welfare validity.
- Affiliation response and review outcomes are stylized game abstractions and must not be read as legal or antitrust predictions.
