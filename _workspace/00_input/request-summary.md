# Request Summary - Consultant Advice Traceability Evidence

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation loop.
- Task type: development continuation and bounded evidence slice.
- Selected slice: verify that the restored deterministic consultant options are
  visible in MCP observations, retained in committed history, and available in
  debriefs across existing competitive profiles, seeds, and difficulty tiers.

## Sources

- `README.md`, `docs/proposal.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/expansion-proposal-review.md`
- `docs/mcp-playtesting-guide.md` and the v0.10.39 handoff

## Expected Files

- `_workspace/experiments/v0.10.40-consultant-advice-evidence/`
- `docs/playtest-findings-v0.10.40.md`, `docs/mcp-playtesting-guide.md`,
  `SPEC.md`, `CHANGELOG.md`, package metadata, and project handoffs

## Validation Target

- All 24 months complete for each existing scripted profile at seeds 42–44 on
  Normal and Hard difficulty without validation failures.
- Every captured observation has four non-binding A–D options that exactly
  match the stored transition options, while each debrief retains its monthly
  advisory record.
- State transitions, AI behavior, commands, ruleset values, and state hashes
  remain unchanged.

## Non-Goals

- No advisor market, advisor roster, payroll, candidate pool, hire/fire command,
  AI advice policy, scenario schema, balance change, or human-learning claim.
- No replay, state-hash, scenario, or shared-diagnostics change. Add only the
  consultant options already stored in history to the MCP transition summary so
  the wrapper can compare its rendered observation with committed history.
