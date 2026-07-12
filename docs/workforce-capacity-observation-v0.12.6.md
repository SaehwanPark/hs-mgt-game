# Workforce Capacity Observation Context — v0.12.6

## Scope

Render safe, already-typed `PlayerObservation` staffing and physical-capacity
context at the competitive MCP boundary. Keep the deterministic transition
core, command legality, history, state hashes, replay behavior, and debrief
semantics unchanged.

## Projection contract

The formatter renders exactly:

```text
Staffing: nurses <n>, physicians <n>, admins <n>
Physical capacity: staffed beds <n>, outpatient <n>, emergency <n>, ICU <n>, obstetrics <n>, psychiatric <n>, cardiology <n>, oncology <n>, infusion <n>, neurology <n>, ASC <n>
```

The source is the actor-visible `PlayerObservation`, not hidden world state or
derived effective-capacity calculations.

## Verification contract

- Focused session-boundary test asserts the exact seed-42 starting values.
- The v0.12.4-compatible matrix contains 75 complete runs and 1,800
  transitions.
- All 1,800 observations include both projection lines.
- All 60 all-tier source histories and all 15 standalone Expert source
  histories match exactly, including state-hash sequences.
- Runtime difficulty, balance, scoring, winnability, and human-learning
  promotion remain deferred.
