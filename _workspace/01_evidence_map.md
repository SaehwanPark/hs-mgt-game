# Evidence Map - LLM Access-Pledge Evidence

## Scope

Bounded Phase 7 validation of whether repeated access pledges appear in three
sub-agent generated Hard competitive command plans after current access guidance
and debrief QA.

## Sources Reviewed

- `docs/playtest-findings-v0.10.5.md`
- `docs/agent-playtest-protocol.md`
- `docs/mcp-playtesting-guide.md`
- `docs/design_principles.md`
- `_workspace/experiments/v0.10.7-llm-access-pledge-evidence/results.json`

## Mechanisms and Institutions

- Access pledges are public legitimacy commitments in the competitive campaign.
- Durable access follow-through can also appear through staffing, service-line
  capacity, monitoring, and payer actions.
- Public Medicare and Medicaid negotiations support neutral posture only.

## Actor Incentives and Information

- Fiscal Steward prioritized solvency and monitoring.
- Access Expansion Advocate prioritized access but used one pledge, then
  operational follow-through.
- First-Time Executive used one modest pledge, then avoided stacking public
  commitments under uncertainty.

## Assumptions

- Sub-agent command plans are simulated-player evidence, not human behavior.
- MCP replay is the authoritative validation boundary for command legality and
  deterministic completion.
- Replacing unaffordable or invalid plan entries with `hold` is an operator
  correction and must not be treated as autonomous retry behavior.

## Unresolved Questions

- Whether live LLM play with month-by-month observations would make different
  choices than fixed command-plan replay.
- Whether human players repeat access pledges after seeing current guidance.
- Whether access guidance improves educational interpretation in classroom use.

## Design Implications

- Current evidence does not support runtime cooldowns or pledge-effect tuning.
- Future access-pledge work should stay in guidance, debriefing, or more direct
  evidence capture unless repetition recurs in live LLM or human play.

## Risks

- False precision from three profiles, one seed, one campaign, and one
  difficulty.
- Over-reading corrected replay commands as fully autonomous player behavior.
- Mistaking reduced pledge repetition for better gameplay or learning.
