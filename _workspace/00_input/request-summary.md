# Request Summary

## Scope

- Continue the merged v0.11.2 Phase 7 checkpoint as a bounded v0.11.3 runtime
  debrief slice.
- Add one player-owned monthly operating-result line to each valid competitive
  end-of-run debrief month section.
- Complete the feature branch, verification, PR handoff, and review loop.

## Non-goals

- No new actors, commands, service lines, scenarios, transition mechanics,
  active-observation changes, balance, difficulty, calibration, or learning
  claim.
- No MCP request/response schema, replay format, ruleset, state-hash, or
  historical v0.11.2 evidence-artifact change.
- Do not expose rival-private operating values.

## Sources

- `docs/playtest-findings-v0.11.2.md`, identifying the missing month-specific
  operating-outcome link.
- Existing `CompetitiveTransition.next` operating fields and shared
  `competitive_debrief` output.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, and the harness team specification.

## Expected files

- `src/debrief/report.rs`, debrief tests, and the MCP end-session test.
- Version, changelog, SPEC, roadmap, playtest guidance, lessons, and workspace
  handoffs.

## Validation target

- Each committed player month renders one realized operating-result line with
  demand, treated volume, unmet demand, revenue, cost, and margin.
- Direct debrief and MCP paths share the same output.
- Transition behavior and the seed-42 golden hash remain unchanged.
- Focused and full Rust/Python checks, domain QA, CI, and three review passes
  complete before merge readiness.

## Global skills

- `preferred-workflow`, `simple-code-writer`, `code-reviewer`, and
  `hs-policy-domain-qa`.
