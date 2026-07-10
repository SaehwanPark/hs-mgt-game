# Evidence Map - Consultant Advice Usage

## Scope

Evaluate whether deterministic simulated policies can interpret and act on the
repaired generic consultant baseline before considering a future advisor roster.

## Sources Reviewed

- `docs/expansion-proposal-review.md`
- `docs/mcp-playtesting-guide.md`
- v0.10.39 observation, history, and debrief implementation/handoff artifacts
- v0.10.40 consultant-advice traceability artifact and findings

## Mechanisms and Institutions

- Generic advice is a decision-support and traceability surface: it must use
  only actor-visible information, remain non-binding, and preserve what was
  shown for later discussion.
- The evidence matrix tests those implementation and educational-explanation
  boundaries; it does not test a labor market, advice quality, causal impact,
  or learning.

## Actor Incentives and Information

- The human player receives options derived from its own visible observation.
- The control policy ignores those options. The advice-aware policy uses only
  visible cues and resources, making selection and command alignment explicit
  simulated-policy signals rather than evidence of human uptake or effectiveness.

## Unresolved Questions

- Whether four generic options provide enough useful context for a documented
  decision-support need remains unresolved.
- Whether resource-safe fallback produces useful strategic variation remains
  unresolved and is not a balance question for this slice.
- Existing scripted captures cannot establish human comprehension, learning,
  preference, or the causal value of an advisor roster.

## Design Implications

- Require exact observation/history/debrief continuity before interpreting any
  command-family alignment signals.
- Compare advice-aware traces with v0.10.40-matching control hashes before
  attributing any difference to the policy wrapper.
- Keep the advisor-market promotion gate closed unless later evidence identifies
  a concrete limitation in the repaired baseline.

## Risks

- Advice text can be mistaken for a recommendation quality or learning claim.
- A wrapper parser can drift from MCP rendering; the runner must fail visibly on
  missing or mismatched options rather than silently treating them as absent.
