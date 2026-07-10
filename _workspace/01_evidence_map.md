# Evidence Map - Consultant Advice Traceability

## Scope

Evaluate the repaired generic consultant baseline before considering a future
advisor roster.

## Sources Reviewed

- `docs/expansion-proposal-review.md`
- `docs/mcp-playtesting-guide.md`
- v0.10.39 observation, history, and debrief implementation/handoff artifacts

## Mechanisms and Institutions

- Generic advice is a decision-support and traceability surface: it must use
  only actor-visible information, remain non-binding, and preserve what was
  shown for later discussion.
- The evidence matrix tests those implementation and educational-explanation
  boundaries; it does not test a labor market, advice quality, or learning.

## Actor Incentives and Information

- The human player receives options derived from its own visible observation.
- Scripted policies ignore those options, making command-family alignment a
  traceability signal rather than evidence of advice uptake or effectiveness.

## Unresolved Questions

- Whether four generic options provide enough useful context for a documented
  decision-support need remains unresolved.
- Existing scripted captures cannot establish human comprehension, learning,
  preference, or the causal value of an advisor roster.

## Design Implications

- Require exact observation/history/debrief continuity before interpreting any
  command-family alignment signals.
- Keep the advisor-market promotion gate closed unless later evidence identifies
  a concrete limitation in the repaired baseline.

## Risks

- Advice text can be mistaken for a recommendation quality or learning claim.
- A wrapper parser can drift from MCP rendering; the runner must fail visibly on
  missing or mismatched options rather than silently treating them as absent.
