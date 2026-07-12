# Evidence Map — Workforce Capacity Observation Context v0.12.6

| Question | Evidence | Result | Limit |
| --- | --- | --- | --- |
| Are safe fields typed? | `PlayerObservation` staffing/capacity fields | supported | Typed ownership does not imply visibility. |
| Are the fields now rendered? | 75-run MCP trace artifact | 1,800/1,800 observations contain both lines | Simulated trace evidence only. |
| Did transitions change? | v0.11.11 all-tier and v0.11.9 Expert controls | 75/75 exact history matches | Controls are from earlier versions. |
| Did hashes change? | Per-transition state-hash comparison | 75/75 exact sequence matches | Hash equality is not a learning claim. |
| Did hidden fields leak? | Excluded-marker scan | 0 occurrences | Marker scan is contract evidence, not a formal privacy proof. |

## Source controls

- `_workspace/experiments/v0.11.11-phase7-post-change-all-tier-validation/results.json`
- `_workspace/experiments/v0.11.9-expert-difficulty-validation/results.json`
- `_workspace/experiments/v0.12.6-workforce-capacity-observation/results.json`

Runtime promotion remains deferred.
