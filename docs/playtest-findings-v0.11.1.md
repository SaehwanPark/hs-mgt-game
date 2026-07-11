# Playtest Findings v0.11.1

**Status:** Phase 7 competitive operating-loop validation evidence
**Batch:** `v0.11.1-operating-loop-ai-validation`
**Date:** 2026-07-11

## Matrix

- Campaign: `competitive-regional-v1`
- Profiles: Access First, Commercial Focus, Workforce Resilience, Capital Modernization, Coalition/Legitimacy
- Seeds: `42`, `43`, `44`
- Difficulties: Easy, Normal, Hard, Expert
- Runs: 60 complete runs, 1,440 committed months
- Decision-to-debrief trace coverage: 60/60 runs

The five profiles are deterministic scripted policies. They are evidence lanes,
not runtime AI classes or validated player archetypes.

## Observed results

- Ten distinct command trajectories appeared across the matrix; no common-action
  or near-dominance candidate was identified by the bounded audit.
- Player-owned operating traces preserved demand, treated volume, unmet demand,
  revenue, cost, margin, cash effect, events, and attributed effects for every
  committed month.
- Observed operating ranges were demand 18–34, treated volume 18–27, unmet
  demand 0–7, revenue 29–48, cost 34–40, and margin/cash effect -8–14.
- Final outcome ranges were cash -33–330, access 68–93, quality 72–87,
  workforce trust 34–60, community trust 64–69, and market share 24–34.
- The audit recorded 140 capacity/demand bottleneck months, 269 operating-loss
  months, 60 workforce-capacity months, and 76 threshold-crossing candidates.
- No rival private operating event was present in the player-owned traces.
- The seed-42 Normal hold-control retained the known month-one hash
  `61357596d8800592`; new policy trajectories intentionally have different
  hashes because they submit different commands.

## Interpretation limits

These are reproducible simulated-policy diagnostics. They do not establish
causal marginal effects, action dominance, balance, calibration, winnability,
human comprehension, enjoyment, learning, classroom effectiveness, or policy
validity. The operating quantities remain visible integer game abstractions.

## Follow-up routing

Runtime promotion remains deferred. The bottleneck, loss, and threshold patterns
are candidates for a later controlled evidence or design review, not reasons to
tune formulas in this PR. Any runtime, difficulty, balance, or interface change
must be proposed as a separate bounded slice with focused tests and domain QA.
