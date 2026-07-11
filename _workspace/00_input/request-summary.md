# Request Summary - Consultant Advice Usage Evidence

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation loop.
- Task type: development continuation and bounded evidence slice.
- Selected slice: compare advice-aware and advice-ignoring simulated policies
  while verifying that visible consultant options remain continuous with
  committed history and debrief records.

## Sources

- `README.md`, `docs/proposal.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/expansion-proposal-review.md`
- `docs/mcp-playtesting-guide.md`, the v0.10.39 handoff, and the v0.10.40
  traceability artifact

## Expected Files

- `_workspace/experiments/v0.10.41-consultant-advice-usage/`
- `docs/playtest-findings-v0.10.41.md`, `docs/mcp-playtesting-guide.md`,
  `SPEC.md`, `CHANGELOG.md`, package metadata, and project handoffs

## Validation Target

- All 24 paired control/advice-aware runs complete 24 months at seeds 42–44 on
  Normal and Hard difficulty without validation failures.
- Every captured observation has four non-binding A–D options that exactly
  match the stored transition options, while each debrief retains its monthly
  advisory record.
- Advice-ignoring controls match the v0.10.40 state hashes; advice-aware traces
  record visible selection, fallback, and command-alignment signals.

## Non-Goals

- No advisor market, advisor roster, payroll, candidate pool, hire/fire command,
  AI advisor, scenario schema, balance change, causal advice claim, or
  human-learning claim.
- No runtime, MCP DTO, replay, state-hash, or shared-diagnostics change.
