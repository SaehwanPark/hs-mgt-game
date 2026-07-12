# v0.11.11-phase7-post-change-all-tier-validation

- Code version: `0.11.11`
- Campaign: `competitive-regional-v1`
- Runs: 60/60 complete
- Operating months audited: 1440
- Distinct command trajectories: 10
- Decision-to-debrief trace coverage: 60/60 runs
- Runtime promotion: deferred

## Matrix

Seeds: 42, 43, 44
Difficulties: easy, normal, hard, expert
Profiles: Access First, Commercial Focus, Workforce Resilience, Capital Modernization, Coalition/Legitimacy

## Operating evidence

| Metric | Count | Range | Unique values | Stable observed effect |
| --- | ---: | ---: | ---: | --- |
| cash_delta | 1440 | -8–14 | 23 | no |
| cost | 1440 | 34–40 | 7 | no |
| demand | 1440 | 18–34 | 17 | no |
| margin | 1440 | -8–14 | 23 | no |
| revenue | 1440 | 29–48 | 20 | no |
| treated | 1440 | 18–27 | 10 | no |
| unmet | 1440 | 0–7 | 8 | no |

## Final outcome ranges

| Metric | Range | Unique values |
| --- | ---: | ---: |
| access | 68–93 | 4 |
| cash | -33–330 | 30 |
| community_trust | 64–69 | 3 |
| market_share | 24–34 | 2 |
| quality | 72–87 | 5 |
| workforce_trust | 34–60 | 9 |

### Bottlenecks

- `capacity_or_demand`: 140 operating months
- `operating_loss`: 268 operating months
- `workforce_capacity`: 205 operating months

### Candidate signals

- Low-variation operating variables: none.
- Candidate common first-month actions: none.
- Candidate near-dominance first-month actions: none.
- Threshold-crossing candidates: 78.
- No dominance, causal marginal-effect, calibration, or balance claim is made.

## Evidence limits

- These are deterministic simulated-policy traces, not human or classroom evidence.
- Observed effect stability and common actions are not causal marginal effects or dominance proof.
- Integer operating quantities are gameplay abstractions, not calibrated financial or clinical units.
- The matrix does not establish enjoyment, learning, winnability, or policy validity.

## Strategy comparison

Profile and difficulty groupings below are descriptive simulated-policy diagnostics, not validated strategy classes or causal comparisons.

| Profile | Runs | Distinct trajectories | Action families |
| --- | ---: | ---: | --- |
| Access First | 12 | 2 | commit, hold, invest, monitor, recruit |
| Capital Modernization | 12 | 2 | hold, invest |
| Coalition/Legitimacy | 12 | 1 | commit, monitor, negotiate |
| Commercial Focus | 12 | 1 | hold, monitor, negotiate |
| Workforce Resilience | 12 | 4 | commit, hold, recruit |

| Difficulty | Runs | Distinct trajectories | Cash range | Access range | Workforce trust range |
| --- | ---: | ---: | ---: | ---: | ---: |
| easy | 15 | 6 | 9–330 | 68–93 | 34–60 |
| normal | 15 | 9 | -33–251 | 68–93 | 34–60 |
| hard | 15 | 9 | -31–251 | 68–93 | 34–60 |
| expert | 15 | 9 | -33–251 | 68–93 | 34–60 |
