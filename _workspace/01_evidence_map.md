# Evidence Map: Free-Form Agent Playtest Evidence Slice

## Scope

Map the v0.1.52 scripted naive-profile finding into the next bounded validation
step: one free-form first-time executive profile using the existing MCP
interface. This artifact supports evidence documentation and follow-up
selection only; it does not approve formula tuning or runtime expansion.

## Sources Reviewed

- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/playtest-findings-v0.1.52.md`
- Existing MCP session observations, legal-command hints, histories, and
  debriefs captured during the free-form run

## Evidence Observed

- v0.1.52 completed 24 scripted-policy sessions, including a deterministic
  `Naive First-Time` profile.
- That scripted profile showed legal low-complexity completion but did not test
  whether a free-form simulated player could choose commands from observations
  and legal hints.
- v0.1.54 completed one free-form profile for both current campaigns at seed 42
  with zero validation failures.
- The free-form stabilization run chose an access-focused path and ended at
  cash 45, access 84, workforce trust 64, and community trust 70.
- The free-form competitive run monitored Northlake, recruited nurses, invested
  in beds, made an access pledge, and negotiated neutrally, ending at cash 30,
  access 71, staffed beds 124, workforce trust 57, and community trust 65.

## Assumptions

- Free-form simulated-agent completion is stronger command-surface evidence than
  scripted-policy completion but still weaker than human play.
- A single seed-42 free-form run can validate the feasibility of the evidence
  path, not characterize balance or strategy-space dominance.
- Competitive final-metric reporting should remain derived from committed
  history or end-session debrief output, not active-play hidden state.

## Design Implications

- Additional free-form profiles with distinct priorities are the next evidence
  step before strategy-space or balance conclusions.
- If repeated free-form competitive runs stay passive or underuse commitments,
  review monthly report guidance and command help before considering formula
  changes.
- Keep strategy-space diagnostics lightweight until repeated scripted or
  free-form findings show a concrete tooling need.

## Risks

- **False precision:** one free-form profile is not an outcome distribution or
  equilibrium result.
- **Educational overclaim:** simulated-agent success does not measure human
  comprehension or classroom learning.
- **Operator-run artifact limits:** the run documents choices and evidence, but
  does not add repeatable LLM orchestration.
