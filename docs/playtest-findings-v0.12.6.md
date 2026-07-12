# Workforce Capacity Observation Findings — v0.12.6

## Finding

The safe typed workforce and physical-capacity fields are now visible in every
competitive MCP decision-time observation through two deterministic lines:

- `Staffing: nurses <n>, physicians <n>, admins <n>`
- `Physical capacity: staffed beds <n>, outpatient <n>, emergency <n>, ICU <n>, obstetrics <n>, psychiatric <n>, cardiology <n>, oncology <n>, infusion <n>, neurology <n>, ASC <n>`

The projection uses existing `PlayerObservation` values only. It does not
expose role targets, effective allocations, pending hire outcomes, rival
private workforce state, or future actor responses.

## Evidence

- Campaign: `competitive-regional-v1`
- Matrix: five profiles, seeds 42–44, Easy/Normal/Hard/Expert, plus the
  standalone Expert overlap used by the v0.12.4 compatibility review.
- Runs: 75 complete.
- Transitions: 1,800.
- Projection coverage: 1,800 staffing lines and 1,800 physical-capacity lines.
- Source comparison: 60 all-tier histories and 15 Expert histories match
  exactly; all state-hash sequences match exactly.
- Seed-42 Normal hold control hash: `61357596d8800592`.
- Excluded hidden-marker occurrences: 0.

## Interpretation and limits

This supports an observation-only interface change and closes the bounded
typed-vs-rendered gap identified by v0.12.5. It does not establish causal
difficulty, balance, winnability, comprehension, human learning, or calibrated
workforce meaning. Runtime difficulty and balance promotion remain deferred.
