# Difficulty Depth Evidence Review v0.12.4

- **Status:** supported
- **Source artifacts:** 2
- **Runs reviewed:** 75 of 75
- **Committed transitions reviewed:** 1,800
- **Runtime promotion:** deferred

This deterministic read-only audit checks whether the existing difficulty artifacts expose a visible pressure signal and whether Expert completion remains a bounded clearability proxy.

## Source coverage

| Source | Code version | Runs | Transitions | Supported | Status |
| --- | --- | ---: | ---: | ---: | --- |
| all-tier post-change | 0.11.11 | 60 | 1440 | 60 | supported |
| standalone Expert | 0.11.9 | 15 | 360 | 15 | supported |

## Difficulty pressure summary

| Difficulty | Runs | Workforce capacity | Operating loss | Capacity/demand | Trajectories |
| --- | ---: | ---: | ---: | ---: | ---: |
| easy | 15 | 0 | 26 | 35 | 6 |
| normal | 15 | 15 | 81 | 35 | 9 |
| hard | 15 | 30 | 81 | 35 | 9 |
| expert | 15 | 160 | 80 | 35 | 9 |

## Finding

The all-tier artifact exposes a candidate `workforce_capacity` pressure signal: counts rise 0 → 15 → 30 → 160 from Easy through Expert. Normal, Hard, and Expert retain identical aggregate scripted action counts in this matrix, so the signal is routed as operating-pressure evidence rather than a claim about player-perceived difficulty.

The all-tier Expert subset and standalone Expert artifact each complete 15/15 named profile/seed runs. This is a bounded clearability proxy, not general Expert winnability.

## Evidence limits

- This is deterministic simulated-policy evidence, not human or classroom evidence.
- Bottleneck counts, action trajectories, and endpoint ranges are descriptive signals, not causal marginal effects, validated strategy classes, balance proof, or equilibrium outcomes.
- Expert completion is a bounded clearability proxy for the named profiles and seeds, not general winnability.
- The all-tier and Expert sources were produced at different code versions, so their endpoint values are not treated as a causal comparison.
- Integer operating quantities are gameplay abstractions, not calibrated financial, clinical, legal, or policy units.
