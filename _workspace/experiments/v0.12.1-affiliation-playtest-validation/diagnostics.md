# Regional Affiliation Playtest Validation — `v0.12.1-affiliation-playtest-validation`

- Code version: `0.12.1`
- Campaign: `regional-affiliation-v1`
- Matrix: independent, deferred, and pursuit × seeds `42`, `43`, `44`
- Evidence type: deterministic simulated-policy MCP trace and debrief audit
- Status: `supported_with_gap`
- Runtime promotion: `deferred`

## Coverage

| Measure | Count |
| --- | ---: |
| Complete runs | 9 / 9 |
| Committed stages | 54 |
| Pre-command observations | 54 |
| Debrief stage lines | 54 |
| Unexpected validation failures | 0 |

## Final statuses

- `Deferred`: 3
- `Independent`: 3
- `Integrated`: 3

## Actor-response coverage

- `partner`: `Accepted`, `Conditioned`, `NotEngaged`
- `review`: `Approved`, `NotEngaged`
- `labor`: `Concern`, `NotEngaged`, `Support`
- `payer`: `NotEngaged`, `Support`
- `community`: `NotEngaged`, `Support`

## Concrete gap

- **decision-time context** (`alternatives, assumptions, commitments`): The typed AffiliationObservation exposes alternatives, assumptions, and commitments, but the MCP-rendered observation omits them across all nine captured runs. The debrief later asks the player to compare alternatives, so this is a bounded observation-context gap rather than evidence for balance or transition tuning.

Next bounded candidate: Expose typed affiliation observation context in the MCP surface, then rerun this audit.

## Evidence limits

- This is deterministic simulated-policy evidence, not human-learning or classroom-effectiveness evidence.
- The nine-run matrix does not establish general winnability, balance, calibration, legal validity, or policy forecasting.
- The observation-context gap supports an interface follow-up only; it does not justify runtime transition or ruleset tuning.
