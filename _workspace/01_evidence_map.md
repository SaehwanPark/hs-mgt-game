# Evidence Map — Affiliation Runtime Boundary Proposal v0.12.7

| Contract | Evidence | Result | Limit |
| --- | --- | --- | --- |
| True state | `src/model/affiliation.rs` | typed world state, ruleset, responses, commitments, review, integration | Source coverage is not a calibration claim. |
| Actor observation | `observe.rs`, MCP formatter, v0.12.2 artifact | alternatives, assumptions, commitments and public signals visible | Named simulated policies only. |
| Resolved inputs | `src/inputs/resolve_affiliation.rs` | explicit stochastic response bundle before transition | Stylized responses, not legal forecasts. |
| Deterministic transition | `src/affiliation/transition.rs` | validated command, effects, next state, hash | No general equilibrium claim. |
| History/replay | model transition/history, artifact verifier | prior/command/observation/inputs/effects/hash retained and replayed | Replay integrity is not human-learning evidence. |
| Debrief | `src/debrief/report.rs` | Riverside outcomes separated from actor utility/social welfare | No measured comprehension or welfare validity. |

## Committed artifact

- `_workspace/experiments/v0.12.2-affiliation-observation-context/results.json`
- 9 complete runs, 54 committed stages, zero validation failures.

Conclusion: the proposal contract is supported; no new runtime slice is
authorized without a new concrete evidence gap.
