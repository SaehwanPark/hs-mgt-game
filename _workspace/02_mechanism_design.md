# Mechanism Design - Expert Clearability Evidence

## Goal and Roadmap Phase

Phase 7 difficulty and winnability evidence: test whether the existing Expert
campaign can be completed by multiple bounded simulated policies before any
difficulty or balance promotion.

## Slice Boundary

- Inputs: existing MCP wrapper and four existing policy functions.
- Output: deterministic 12-run JSON matrix, diagnostics, and findings.
- Included: observations, legal hints, commands, failures, histories, hashes,
  and debriefs.
- Excluded: runtime mechanics, difficulty parameters, scoring, balance, and
  new simulation behavior.

## Actors and Information

- Policies act only through the actor-visible MCP observation and legal hints.
- Retrospective history and debrief output are not treated as decision-time
  knowledge.
- Existing rival and payer behavior remains unchanged.

## Clearability Proxy

An eligible run is complete when it records all 24 competitive transitions with
zero validation failures. A failed or incomplete run is retained and reported;
it is not silently excluded from the matrix.

## Determinism and Replay Notes

The runner uses the existing seeded MCP session boundary and does not alter
transition inputs, state hashes, replay formats, or stochastic resolution.
Repeated generation must produce identical JSON and Markdown output.

## Educational and Domain Limits

The artifact supports inspectability of Expert completion paths only. It does
not measure learning, establish strategy quality, prove balance, or validate
real health-policy outcomes.
