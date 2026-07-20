# Workforce Capacity Difficulty Design Findings — v0.12.5

## Validation contract

- Evidence type: deterministic observation-contract and domain design review
- Input evidence: v0.12.4 difficulty-depth artifact plus current typed
  observation, MCP formatter, transition, and debrief source
- Design artifact: `_workspace/experiments/v0.12.5-workforce-capacity-design/design.json`
- Runtime difficulty change: not authorized

## Findings

The v0.12.4 workforce-capacity signal is grounded in accepted operating
records. The current MCP view already exposes workforce trust, nursing-vacancy
wording, prior operations, labor-market delay/cost guidance, state-conditioned
consultant options, and later debrief attribution.

The typed `PlayerObservation` also owns Riverside's current staffing counts and
physical-capacity fields, but `format_competitive_observation` does not render
those numeric fields. This is a bounded decision-time observation-context gap:
the player can see that staffing strain exists but cannot inspect the current
numeric staffing/capacity context that frames the pressure.

## Routing decision

An observation-only follow-up is justified. The next implementation should add
`Staffing:` and `Physical capacity:` lines from existing typed fields, add MCP
boundary tests, and rerun the unchanged v0.12.4-compatible evidence matrix.

No difficulty values, transition formulas, balance, scoring, hidden targets,
effective allocations, future hire outcomes, rival private state, or winnability
claim is promoted by this design gate.

## Evidence limits

The design does not establish human comprehension, educational effectiveness,
calibration, causality, balance, or general Expert winnability. Safe typed-field
projection is an interface decision; it does not make the underlying gameplay
mechanics empirically validated.
