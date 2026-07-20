# Phase 7 Post-Fix Findings — Regional Affiliation Observation Context v0.12.2

## Validation contract

- Campaign: `regional-affiliation-v1`
- Matrix: independent, deferred, and pursuit policies × seeds 42, 43, and 44
- Evidence type: deterministic simulated-policy MCP post-fix audit
- Runtime code version: `0.12.2`
- Source artifact: `_workspace/experiments/v0.12.2-affiliation-observation-context/results.json`

The post-fix capture reuses the v0.12.1 observation-driven policies and exact
seed matrix. It preserves the historical v0.12.1 artifact rather than
rewriting it.

## Findings

- 9/9 runs completed all six stages.
- 54/54 committed stages retained the same transition/state-hash/debrief
  linkage contract.
- All 54 pre-command MCP observations include a `Commitments:` line, at least
  two `Alternative:` lines, and two `Assumption:` lines sourced from the typed
  affiliation observation.
- No validation failures occurred.
- The v0.12.1 missing-context count is now zero at the MCP projection boundary.

## Boundary review

The new lines render only Riverside commitments, the scenario's staged
alternatives, and explicit abstraction assumptions. They do not expose hidden
partner condition, actor utility, future resolved responses, or realized
outcomes. No transition, ruleset, state-hash, replay, command, or competitive
golden behavior changed.

## Next validation posture

This structural gap is closed. Continue the evidence-only posture: do not tune
balance or transition mechanics without a new concrete player-facing,
instructor-facing, or domain-review gap.

## Evidence limits

This is deterministic simulated-policy traceability evidence. It does not
measure human comprehension, classroom effectiveness, cognitive load, general
winnability, balance, calibration, legal validity, or policy forecasting.
