# Request Summary

## Scope

- Continue the v0.11.0 operating-loop checkpoint as a Phase 7 validation slice.
- Capture five deterministic policy hypotheses across seeds 42–44 and Easy,
  Normal, Hard, and Expert competitive configurations.
- Audit player-owned operating attribution, bottlenecks, trajectories,
  threshold candidates, and decision-to-debrief trace coverage.
- Prepare the v0.11.1 branch and PR handoff.

## Non-goals

- No new actors, commands, service lines, scenarios, GUI, runtime mechanics,
  balance tuning, calibration, or human-learning claim.
- No MCP schema, replay format, ruleset, or state-hash change.
- No causal dominance or marginal-effect claim from observational traces.

## Sources

- v0.11.0 final handoff and current SPEC Future queue.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, and the harness team specification.
- Existing MCP wrapper, transition summaries, operating-loop tests, and ADR-0009.

## Expected Files

- `_workspace/experiments/v0.11.1-operating-loop-ai-validation/`.
- `tests/test_operating_loop_ai_validation.py`.
- Version, findings, playtest guidance, SPEC, changelog, lessons, and required
  workspace handoffs.

## Validation Target

- 60 complete competitive runs and 1,440 committed operating months.
- Player-owned demand, treated volume, unmet demand, revenue, cost, margin, and
  cash identities pass for every audited month.
- Actor-visible observations, commands, transition summaries, hashes, and
  debrief traces are preserved for every run.
- The separate seed-42 Normal hold-control retains hash `61357596d8800592`.
- Generated JSON and Markdown artifacts are deterministic.

## Global Skills

- `preferred-workflow`, `simple-code-writer`, `spec-driven-developer`, and
  `code-reviewer`.
