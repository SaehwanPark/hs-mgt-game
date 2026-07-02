# Evidence Map: Free-Form Profile Synthesis Slice

## Scope

Map the v0.1.54 free-form first-time executive finding into the next bounded
validation step: two additional free-form profiles with different strategic
priorities using the existing MCP interface. This artifact supports evidence
documentation and follow-up selection only; it does not approve formula tuning
or runtime expansion.

## Sources Reviewed

- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.1.54.md`
- Existing MCP session observations, legal-command hints, histories, and
  debriefs captured during the free-form runs

## Evidence Observed

- v0.1.54 completed one free-form profile for both current campaigns at seed 42
  with zero validation failures.
- v0.1.55 completed two additional free-form profiles for both current
  campaigns at seed 42 with zero validation failures.
- The fiscal profile protected cash in both campaigns and produced lower access
  gains: stabilization ended at cash 68 and access 75; competitive ended at
  cash 60 and access 70.
- The access-expansion profile spent heavily for capacity and legitimacy:
  stabilization ended at cash 30 and access 90; competitive ended at cash 10,
  access 76, staffed beds 126, and workforce trust 56.

## Assumptions

- Free-form simulated-agent completion is stronger command-surface evidence than
  scripted-policy completion but still weaker than human play.
- Three total seed-42 free-form profiles can support provisional
  command-comprehension and strategy-diversity observations, not characterize
  balance or strategy-space dominance.
- Competitive final-metric reporting should remain derived from committed
  history or end-session debrief output, not active-play hidden state.

## Design Implications

- The current free-form evidence now supports a lightweight synthesis across
  first-time, fiscal, and access-expansion priorities.
- If repeated free-form competitive runs stay passive or underuse commitments,
  review monthly report guidance and command help before considering formula
  changes.
- Keep strategy-space diagnostics lightweight until repeated scripted or
  free-form findings show a concrete tooling need.

## Risks

- **False precision:** three seed-42 free-form profiles are not an outcome
  distribution or equilibrium result.
- **Educational overclaim:** simulated-agent success does not measure human
  comprehension or classroom learning.
- **Operator-run artifact limits:** the runs document choices and evidence, but
  do not add repeatable LLM orchestration.
