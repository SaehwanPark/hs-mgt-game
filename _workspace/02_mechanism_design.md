# Mechanism Design — Workforce Capacity Observation Context v0.12.6

This slice adds no mechanism. It projects existing actor-visible typed values at
the MCP boundary:

```text
Staffing: nurses <n>, physicians <n>, admins <n>
Physical capacity: staffed beds <n>, outpatient <n>, emergency <n>, ICU <n>, obstetrics <n>, psychiatric <n>, cardiology <n>, oncology <n>, infusion <n>, neurology <n>, ASC <n>
```

The deterministic transition core remains the sole owner of state mutation.
The formatter consumes `PlayerObservation`; it does not read hidden targets,
effective allocations, pending outcomes, rival private state, or future actor
responses.

## Acceptance

- Exact boundary test.
- 75 complete runs / 1,800 transitions.
- Exact histories and state hashes against prior controls.
- Runtime difficulty and balance promotion deferred.
