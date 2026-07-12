# Affiliation Runtime Boundary — v0.12.7

## Decision

The existing opt-in `regional-affiliation-v1` runtime already satisfies the
minimum runtime-proposal contract from the affiliation-first design gate. This
cycle documents and verifies that boundary; it does not add a new mechanism or
authorize another runtime change.

## Contract coverage

- True state: staged affiliation status, Riverside metrics, partner condition
  and fit, commitments, review state, integration progress, and actor response
  state.
- Actor observation: reported partner condition, Riverside metrics, commitments,
  review/labor/payer/community signals, alternatives, and explicit assumptions.
- Resolved inputs: report noise, partner/review/labor/payer/community responses,
  integration drag, and continuity shock.
- Deterministic core: validate the stage-specific command, apply resolved inputs
  through one transition, record attributed effects, and compute the versioned
  state hash.
- History/replay: retain prior state, command, observation, resolved inputs,
  actor decisions, effects, next state, and hash; replay verifies each boundary.
- Debrief: distinguish Riverside outcomes, actor responses, actor utility,
  social welfare, and decision quality, while inviting comparison of
  independence and deferral.

## Evidence

- Source-marker audit: all required model, observation, input-resolution,
  transition, replay, MCP, scenario, and debrief markers supported.
- Existing post-observation-context artifact: 9/9 complete runs and 54/54
  committed stages with typed commitments, alternatives, and assumptions in
  every decision-time observation.
- Runtime remains isolated to `regional-affiliation-v1`; the competitive
  campaign and its golden path are unchanged.

## Deferred scope

Direct acquisition, national consolidation, private-equity rollups, detailed
transaction finance, calibrated legal or antitrust forecasts, a generic actor
framework, and changes to `competitive-regional-v1` remain deferred. A future
runtime change requires a new concrete evidence gap and a separate proposal.

## Evidence limits

This is a deterministic source-boundary and trace review, not human-learning,
classroom, calibration, legal-validity, policy-forecast, balance, winnability,
or social-welfare evidence. Affiliation responses and review outcomes are
stylized game abstractions.
