# Workforce Capacity Difficulty Design Gate v0.12.5

- **Decision:** observation-context follow-up required
- **Runtime difficulty change authorized:** no
- **Runtime promotion:** deferred

The v0.12.4 artifact identifies a workforce-capacity pressure signal, but the current MCP formatter omits safe typed staffing and physical-capacity fields from the decision-time observation.

## Candidate signal

- Dimension: `workforce_capacity`
- All-tier bottleneck counts: Easy 0, Normal 15, Hard 30, Expert 160.
- Interpretation: descriptive operating-pressure signal, not causal difficulty, balance, or winnability evidence.

## Proposed next projection

- Source: `PlayerObservation`
- `Staffing: nurses <n>, physicians <n>, admins <n>`
- `Physical capacity: staffed beds <n>, outpatient <n>, emergency <n>, ICU <n>, obstetrics <n>, psychiatric <n>, cardiology <n>, oncology <n>, infusion <n>, neurology <n>, ASC <n>`

These lines use only existing typed Riverside observation fields. They do not expose role targets, effective allocations, pending hire outcomes, rival private workforce state, or future actor responses.

## Verification gate

- focused MCP session-boundary test for exact safe labels and values
- rerun the v0.12.4 75-run/1800-transition compatible evidence matrix
- compare pre/post history and state hashes exactly
- keep runtime difficulty, balance, scoring, and winnability promotion deferred

## Evidence limits

- This is a design and observation-contract review, not human-learning evidence.
- The v0.12.4 signal is deterministic simulated-policy evidence, not causal balance or winnability evidence.
- Current typed fields are safe to project but their presence does not establish comprehension or educational effectiveness.
