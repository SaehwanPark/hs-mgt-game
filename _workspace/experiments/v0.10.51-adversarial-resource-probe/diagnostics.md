# Adversarial Resource-Probe Diagnostics v0.10.51

- **Batch id:** v0.10.51-adversarial-resource-probe
- **Code version:** 0.10.51
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** `hard`
- **Control:** `_workspace/experiments/v0.10.50-teachability-observation-capture/results.json` / First-Time Executive
- **Evidence type:** deterministic simulated-policy resource and retry probe

## Run Summary

| Profile | Seed | Status | Transitions | Expected failures | Retries | Final hash |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| Adversarial Resource Probe / hard / seed 42 | 42 | complete | 24 | 5 | 5 | 46c48f42b8ba6030 |
| Adversarial Resource Probe / hard / seed 43 | 43 | complete | 24 | 5 | 5 | d595f7419fd37b52 |
| Adversarial Resource Probe / hard / seed 44 | 44 | complete | 24 | 5 | 5 | b6b49ca7ee57142d |

## Probe Results

| Seed | Month | Probe | Expected code | Observed code | Accepted | Retry turn |
| ---: | ---: | --- | --- | --- | --- | ---: |
| 42 | 1 | initial_cash_overrun | insufficient_cash | insufficient_cash | no | 1 |
| 42 | 2 | action_budget_overrun | ap_budget_exceeded | ap_budget_exceeded | no | 2 |
| 42 | 3 | accepted_beds_investment | accepted | accepted | yes | — |
| 42 | 4 | accepted_clinic_project | accepted | accepted | yes | — |
| 42 | 5 | active_draw_cash_overrun | insufficient_cash | insufficient_cash | no | 5 |
| 42 | 6 | accepted_asc_project | accepted | accepted | yes | — |
| 42 | 7 | concurrent_project_overrun | too_many_concurrent_projects | too_many_concurrent_projects | no | 7 |
| 42 | 12 | late_cash_overrun | insufficient_cash | insufficient_cash | no | 12 |
| 43 | 1 | initial_cash_overrun | insufficient_cash | insufficient_cash | no | 1 |
| 43 | 2 | action_budget_overrun | ap_budget_exceeded | ap_budget_exceeded | no | 2 |
| 43 | 3 | accepted_beds_investment | accepted | accepted | yes | — |
| 43 | 4 | accepted_clinic_project | accepted | accepted | yes | — |
| 43 | 5 | active_draw_cash_overrun | insufficient_cash | insufficient_cash | no | 5 |
| 43 | 6 | accepted_asc_project | accepted | accepted | yes | — |
| 43 | 7 | concurrent_project_overrun | too_many_concurrent_projects | too_many_concurrent_projects | no | 7 |
| 43 | 12 | late_cash_overrun | insufficient_cash | insufficient_cash | no | 12 |
| 44 | 1 | initial_cash_overrun | insufficient_cash | insufficient_cash | no | 1 |
| 44 | 2 | action_budget_overrun | ap_budget_exceeded | ap_budget_exceeded | no | 2 |
| 44 | 3 | accepted_beds_investment | accepted | accepted | yes | — |
| 44 | 4 | accepted_clinic_project | accepted | accepted | yes | — |
| 44 | 5 | active_draw_cash_overrun | insufficient_cash | insufficient_cash | no | 5 |
| 44 | 6 | accepted_asc_project | accepted | accepted | yes | — |
| 44 | 7 | concurrent_project_overrun | too_many_concurrent_projects | too_many_concurrent_projects | no | 7 |
| 44 | 12 | late_cash_overrun | insufficient_cash | insufficient_cash | no | 12 |

## Interpretation

- Expected validation failures are probes, not final replay failures.
- A rejected command must leave the session turn unchanged; the safe `hold` retry must advance it once.
- This artifact tests wrapper traceability and resource-guard compatibility, not human comprehension, exploit value, balance, winnability, or learning.
- A concrete unexplained gap would require a separate runtime or interface plan.
