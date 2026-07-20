# Workforce Capacity Observation Design — v0.12.5

## Decision

The v0.12.4 all-tier artifact identifies a candidate workforce-capacity
pressure signal, but the current MCP observation does not expose all of the
safe typed context needed to interpret it numerically. An observation-only
follow-up is justified; difficulty and balance changes are not.

## Existing visible context

The current competitive observation already exposes workforce trust,
nursing-vacancy wording, prior operations, labor-market delay/cost guidance,
state-conditioned consultant options, and retrospective staffing attribution.

## Omitted typed context

`PlayerObservation` owns Riverside's current:

- staffing counts: nurses, physicians, and admins;
- physical capacities: staffed beds, outpatient, emergency, ICU, obstetrics,
  psychiatric, cardiology, oncology, infusion, neurology, and ASC.

The MCP formatter currently omits these fields. The gap is at the projection
boundary, not in the deterministic transition mechanism.

## Proposed next slice

Render two lines from `PlayerObservation`:

```text
Staffing: nurses <n>, physicians <n>, admins <n>
Physical capacity: staffed beds <n>, outpatient <n>, emergency <n>, ICU <n>, obstetrics <n>, psychiatric <n>, cardiology <n>, oncology <n>, infusion <n>, neurology <n>, ASC <n>
```

The implementation must not calculate or expose role targets, effective
allocations, pending hire outcomes, rival private workforce state, or future
actor responses. Focused MCP session tests and an unchanged v0.12.4-compatible
history/state-hash matrix are required before the interface gap can be marked
closed.

## Evidence limits

This design does not establish human comprehension, educational effectiveness,
causality, balance, calibration, or general Expert winnability. It is a
presentation-boundary proposal only.
