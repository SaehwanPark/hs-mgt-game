# Request Summary

## Scope

- Continue the merged v0.11.3 Phase 7 checkpoint as a bounded v0.11.4
  post-debrief validation slice.
- Re-run the existing competitive five-profile matrix across seeds 42/43/44
  and Easy/Normal/Hard/Expert.
- Verify one player-owned monthly operating-result line per committed month and
  469/469 categorized signal-month outcome links.
- Complete the feature branch, verification, PR handoff, and review loop.

## Non-goals

- No new actors, commands, service lines, scenarios, transition mechanics,
  active-observation changes, balance, difficulty, calibration, or learning
  claim.
- No MCP request/response schema, replay format, ruleset, state-hash, or
  historical v0.11.1/v0.11.2 evidence-artifact change.
- Do not expose rival-private operating values or promote runtime work from
  structural traceability evidence alone.

## Sources

- `docs/playtest-findings-v0.11.1.md`, the 60-run operating-loop matrix.
- `docs/playtest-findings-v0.11.2.md`, identifying the prior 0/469 monthly
  outcome-link gap.
- The merged v0.11.3 debrief tests and shared CLI/MCP report output.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, and the harness team specification.

## Expected files

- New v0.11.4 capture/audit scripts, generated JSON/diagnostics, findings, and
  focused Python tests.
- Version, changelog, SPEC, roadmap, MCP playtesting guide, lessons, and
  workspace handoffs.
- No `src/**` changes.

## Validation target

- 60 complete runs and 1,440 committed months.
- One player-owned `Operating result:` line per committed month.
- 469/469 categorized signal-month outcome links.
- Zero validation failures, trace/hash mismatches, or rival-result leaks.
- Seed-42 Normal hold-control hash remains `61357596d8800592`.
- Focused and full Rust/Python checks, domain QA, CI, and three review passes
  complete before merge readiness.

## Global and repo-local skills

- `preferred-workflow`, `simple-code-writer`, `spec-driven-developer`,
  `code-reviewer`, `hs-policy-evidence-mapper`, and `hs-policy-domain-qa`.
