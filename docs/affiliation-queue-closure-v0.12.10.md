# Affiliation/Acquisition Queue Closure — v0.12.10

## Decision

The affiliation/acquisition Future item is complete for the bounded scope
already implemented. The v0.12.7 proposal confirms that the opt-in
`regional-affiliation-v1` runtime satisfies the six minimum contracts: true
state, actor observation, resolved inputs, deterministic transition,
history/replay, and debrief.

This closes the queue entry and authorizes no broader acquisition mechanism.

## Evidence

- Proposal artifact: v0.12.7 affiliation runtime-boundary proposal.
- Source markers: ADR, model, observation, input resolution, transition,
  replay, MCP, scenario, and debrief boundaries supported.
- Existing affiliation evidence: 9/9 complete runs, 54 stages, and 54 typed
  decision-time observations.

## Deferred scope

Direct acquisition, national consolidation, private-equity rollups, detailed
transaction finance, calibrated legal or antitrust forecasts, generic actor
framework expansion, and changes to `competitive-regional-v1` remain deferred.

## Reopening condition

Reopen only when new evidence identifies a concrete affiliation strategy,
traceability, or educational gap that the existing boundary cannot address.
