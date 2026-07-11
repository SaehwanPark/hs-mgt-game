# Project-Limit Recovery Diagnostics v0.10.54

- **Batch id:** v0.10.54-project-limit-recovery
- **Code version:** 0.10.54
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** `hard`
- **Source:** `_workspace/experiments/v0.10.51-adversarial-resource-probe/results.json` / v0.10.51-adversarial-resource-probe
- **Evidence type:** deterministic actor-visible project-limit recovery capture

## Run Summary

| Profile | Seed | Status | Transitions | Expected failures | Retries | Final hash |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| Project-Limit Recovery / hard / seed 42 | 42 | complete | 24 | 1 | 1 | 09a3b81bb5eec4b3 |
| Project-Limit Recovery / hard / seed 43 | 43 | complete | 24 | 1 | 1 | ec30c132f4d92155 |
| Project-Limit Recovery / hard / seed 44 | 44 | complete | 24 | 1 | 1 | b62f7b549e4f0bf6 |

## Probe Results

| Seed | Month | Probe | Expected code | Observed code | Accepted | Retry turn | Structured hint | Resource limit |
| ---: | ---: | --- | --- | --- | --- | ---: | --- | --- |
| 42 | 4 | accepted_clinic_project | accepted | accepted | yes | — | no | no |
| 42 | 6 | accepted_asc_project | accepted | accepted | yes | — | no | no |
| 42 | 7 | concurrent_project_limit | too_many_concurrent_projects | too_many_concurrent_projects | no | 7 | no | no |
| 43 | 4 | accepted_clinic_project | accepted | accepted | yes | — | no | no |
| 43 | 6 | accepted_asc_project | accepted | accepted | yes | — | no | no |
| 43 | 7 | concurrent_project_limit | too_many_concurrent_projects | too_many_concurrent_projects | no | 7 | no | no |
| 44 | 4 | accepted_clinic_project | accepted | accepted | yes | — | no | no |
| 44 | 6 | accepted_asc_project | accepted | accepted | yes | — | no | no |
| 44 | 7 | concurrent_project_limit | too_many_concurrent_projects | too_many_concurrent_projects | no | 7 | no | no |

## Recovery Surface

- Stable `too_many_concurrent_projects` codes: 3/3.
- Structured hint fields: 0/3.
- Resource-limit fields: 0/3.
- Same-turn recoveries: 3/3.
- Safe `hold` retries: 3/3.
- Debriefs explaining the two-project ceiling: 3/3.

## Interpretation

- The current response exposes a stable code and plain-language limit, while structured hint and resource-limit fields are absent.
- Rejected commands preserve the actor-visible turn and observation; one safe `hold` retry advances each run exactly once.
- The debrief retains the two-project ceiling for retrospective review.
- These facts support recovery traceability. They do not establish human comprehension or justify a validation-hint change by themselves.

## Evidence Limits

- The project ceiling is a game abstraction, not an empirical health-system constraint.
- A stable error code and safe retry show traceability, not human comprehension or learning.
- The three-seed Hard matrix does not establish balance, winnability, strategy quality, calibration, or policy validity.
- This evidence gate does not promote a validation-hint or runtime change.
