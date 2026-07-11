# Evidence Map

## Scope

Map the v0.11.1 operating-loop artifact into a bounded Phase 7 audit of
decision-to-debrief explainability without promoting runtime work.

## Sources Reviewed

- The v0.11.1 60-run, 1,440-month JSON artifact and strict audit.
- Existing actor-visible observations, submitted commands, transition effects,
  player-owned operating events, hashes, and debriefs.
- `docs/roadmap.md`, `SPEC.md`, the AI-agent playtest protocol, and ADR-0009.

## Mechanisms and Institutions

- Regional demand and market position determine player-owned demand.
- Effective staffed capacity determines treated and unmet demand.
- Quality and payer pressure affect operating revenue.
- Workforce and footprint affect operating cost and cash margin.
- The debrief records decisions and aggregated mechanisms but may not link every
  operating outcome to its month-specific decision section.

## Actor Incentives and Information

- The five policy lanes are test-client behaviors, not runtime actor classes.
- The audit uses only the player’s actor-visible observation and committed
  transition records for player-owned claims.
- Rival-private operating information is not copied into the new audit output.
- Organizational outcomes remain distinct from social welfare and educational
  evaluation.

## Assumptions

- Existing v0.11.1 signal classification is the authoritative abstraction for
  loss, capacity/demand, and workforce-capacity categories.
- Global attributed-mechanism and resolved-event lines are not month-level
  debrief evidence.
- Integer operating quantities are gameplay abstractions, not calibrated units.

## Unresolved Questions

- Whether month-specific operating outcome links improve debrief use requires a
  later bounded design or validation slice.
- The audit cannot establish causal effects, balance, learning, or enjoyment.

## Design Implications

- Keep the audit at the artifact boundary; do not add MCP or runtime fields.
- Report decision context, transition attribution, month-level debrief links,
  and global summaries as separate dimensions.
- Route any future debrief wording change through focused tests and domain QA.

## Risks

- Treating aggregated attribution as month-specific explanation.
- Over-reading trace completeness as educational effectiveness.
- Leaking or reinterpreting rival-private state while producing diagnostics.
