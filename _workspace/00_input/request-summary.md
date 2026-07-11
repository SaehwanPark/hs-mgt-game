# Request Summary

## Scope

- Continue the v0.11.1 operating-loop checkpoint as a Phase 7 read-only
  explainability audit.
- Reuse the existing 60-run, 1,440-month artifact without launching sessions.
- Separate decision-time context, transition attribution, month-level debrief
  outcome linkage, and global debrief attribution.
- Prepare the v0.11.2 branch and PR handoff.

## Non-goals

- No new actors, commands, service lines, scenarios, GUI, runtime mechanics,
  balance tuning, calibration, or human-learning claim.
- No MCP schema, replay format, ruleset, state-hash, or debrief wording change.
- No causal dominance or marginal-effect claim from observational traces.

## Sources

- The v0.11.1 operating-loop validation artifact and audit.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, and the harness team specification.
- Existing MCP observations, transition summaries, debriefs, and operating-loop
  tests.

## Expected Files

- `_workspace/experiments/v0.11.2-operating-loss-explainability/`.
- `tests/test_operating_loss_explainability.py`.
- Version, findings, playtest guidance, SPEC, changelog, lessons, and current
  workspace handoffs.

## Validation Target

- 60 source runs and 1,440 source transitions validate unchanged.
- 469 categorized signal-months reproduce the v0.11.1 counts.
- Decision context, player-owned transition attribution, and month-level
  decision links remain complete.
- Month-level operating-outcome linkage is reported separately from global
  debrief attribution.
- Generated JSON and Markdown artifacts are deterministic.

## Global Skills

- `preferred-workflow`, `simple-code-writer`, and `code-reviewer`.
