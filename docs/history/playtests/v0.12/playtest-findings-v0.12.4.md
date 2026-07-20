# Difficulty Depth Evidence Findings — v0.12.4

## Validation contract

- Evidence type: deterministic read-only audit of committed simulated-policy
  artifacts
- Sources: v0.11.11 post-change all-tier validation and v0.11.9 standalone
  Expert validation
- Coverage: 75 complete runs and 1,800 committed transitions
- Source artifact: `_workspace/experiments/v0.12.4-difficulty-depth-evidence/results.json`

## Findings

The all-tier source preserves complete matrix, observation, command,
history/hash, operating-accounting, and debrief coverage across five profiles,
three seeds, and four difficulty tiers. The standalone Expert source preserves
the same five profiles and three seeds with 15/15 complete runs and zero
validation failures.

The audit recomputes a candidate `workforce_capacity` pressure signal: 0 Easy,
15 Normal, 30 Hard, and 160 Expert operating months. Normal, Hard, and Expert
retain identical aggregate scripted action counts in the all-tier artifact, so
the signal is routed as an operating-pressure observation rather than a claim
that players experience the tiers differently.

## Promotion decision

The result supports a later bounded difficulty design gate focused on
workforce-capacity pressure. It does not authorize runtime tuning, scoring
changes, balance promotion, or a general Expert winnability claim. Runtime
promotion remains deferred.

## Evidence limits

This is deterministic simulated-policy evidence, not human or classroom
evidence. Bottleneck counts, action trajectories, endpoint ranges, and Expert
completion are descriptive signals and bounded clearability proxies for named
profiles and seeds. The sources were produced at different code versions, so
their endpoint values are not a causal comparison. Integer operating quantities
are gameplay abstractions, not calibrated financial, clinical, legal, or policy
units.
