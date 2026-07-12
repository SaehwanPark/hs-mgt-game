# v0.12.6-workforce-capacity-observation

- Code version: `0.12.6`
- Campaign: `competitive-regional-v1`
- Runs: 75/75 complete
- Transitions: 1800
- Exact history match: yes
- Exact state-hash match: yes
- Runtime promotion: `deferred`

## Observation projection

- Staffing line: `Staffing: nurses <n>, physicians <n>, admins <n>`
- Capacity line: `Physical capacity: staffed beds <n>, outpatient <n>, emergency <n>, ICU <n>, obstetrics <n>, psychiatric <n>, cardiology <n>, oncology <n>, infusion <n>, neurology <n>, ASC <n>`
- Trace entries: 1800
- Staffing lines observed: 1800
- Physical-capacity lines observed: 1800
- Excluded hidden-marker occurrences: 0

## Source comparison

| Source | Runs | Transitions | Exact histories | Exact state hashes | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| all_tiers | 60 | 1440 | 60 | 60 | supported |
| expert | 15 | 360 | 15 | 15 | supported |

## Interpretation

The two lines are rendered from existing typed `PlayerObservation` fields. Exact transition histories and state hashes match the earlier immutable controls, supporting an observation-only change classification. Runtime difficulty, balance, scoring, and winnability promotion remain deferred.

## Evidence limits

- This is deterministic simulated-policy evidence, not human or classroom evidence.
- Exact history and state-hash equality supports an observation-only change claim; it does not establish causal difficulty, balance, winnability, or comprehension.
- The source artifacts were produced at earlier code versions and are used only as immutable transition controls.
- Integer staffing and capacity quantities are gameplay abstractions, not calibrated clinical, financial, or workforce estimates.
