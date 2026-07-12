# Request Summary

## Scope

- Continue the merged v0.11.5 Phase 7 checkpoint as a bounded v0.11.6
  strategy-comparison use audit.
- Reuse the frozen v0.11.4 capture without launching new sessions.
- Group existing command trajectories and operating-signal responses by
  profile, seed, and difficulty while preserving observation and debrief
  contracts.
- Complete the feature branch, verification, PR handoff, and review loop.

## Non-goals

- No new actors, commands, service lines, scenarios, transition mechanics,
  active-observation changes, balance, difficulty, calibration, or learning
  claim.
- No MCP request/response schema, replay format, ruleset, state-hash, or
  generalized evidence-schema change.
- Do not infer causality, strategy quality, dominance, human comprehension, or
  runtime promotion from trajectory or response differences.

## Sources

- `SPEC.md` and the ranked Phase 7 teachability queue.
- `docs/roadmap.md`, Phase 7 validation and educational artifact gates.
- `docs/playtest-findings-v0.11.5.md` and the v0.11.4 capture.
- The v0.11.5 operating-outcome audit parser and focused tests.
- `README.md`, `docs/proposal.md`, `docs/design_principles.md`, and the harness
  team specification.

## Expected files

- New v0.11.6 audit script, generated JSON/diagnostics, findings, and focused
  Python tests.
- Version, changelog, SPEC, roadmap, lessons, and workspace handoffs.
- No `src/**` changes.

## Validation target

- 60 complete runs and 1,440 committed months.
- 1,380 prior-month observation matches and 1,440 exact debrief matches.
- 441 non-terminal signal-to-next-command opportunities and 28 terminal
  signals.
- Profile and difficulty summaries with no unexplained structural gaps.
- Seed-42 Normal hold-control hash remains unchanged.

## Skills

- `preferred-workflow`, `plan-designer`, `simple-code-writer`,
  `code-reviewer`, and `hs-mgt-game-orchestrator`.
