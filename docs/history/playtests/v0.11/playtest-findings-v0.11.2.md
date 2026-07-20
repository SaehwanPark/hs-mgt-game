# Playtest Findings v0.11.2

**Status:** Phase 7 read-only operating explainability audit
**Source batch:** `v0.11.1-operating-loop-ai-validation`
**Date:** 2026-07-11

## Question

Do player-owned operating-loss and bottleneck signals retain decision-time
context, transition attribution, and month-level debrief linkage?

This slice reuses the existing v0.11.1 artifact. It launches no new sessions
and changes no runtime, MCP, scenario, replay, ruleset, or debrief behavior.

## Source coverage

- Campaign: `competitive-regional-v1`
- Runs: 60
- Committed months: 1,440
- Seeds: `42`, `43`, `44`
- Difficulties: Easy, Normal, Hard, Expert
- Policy lanes: five deterministic operating hypotheses

## Findings

- 140 capacity/demand signal-months were identified.
- 269 operating-loss signal-months were identified.
- 60 workforce-capacity signal-months were identified.
- All 469 categorized signal-months retained actor-visible decision context,
  player-owned transition attribution, and a month-level player decision link.
- No categorized signal-month had a month-specific operating-outcome line in
  the debrief.
- All 60 runs retained a global attributed-mechanisms summary. That summary is
  reported separately and is not treated as month-level explanation evidence.
- No rival operating event was accepted as player-owned evidence.

## Interpretation limits

These results establish traceability properties of deterministic simulated
policy artifacts. They do not establish causal marginal effects, action
dominance, balance, calibration, winnability, human comprehension, enjoyment,
learning, classroom effectiveness, or policy validity. A missing month-level
debrief marker is a product-evidence gap, not proof that a decision was poor.

## Follow-up routing

Runtime promotion remains deferred. A future bounded debrief-design slice may
test whether month-specific operating outcomes should be rendered or linked in
the debrief. Any such change requires its own focused tests and domain QA.
