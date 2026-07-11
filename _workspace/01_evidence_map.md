# Evidence Map - Project-Recovery Use Evidence

## Scope

Test whether the current plain project-limit response supports a safe
response-conditioned retry when the actor-visible observation still shows two
active projects.

## Sources Reviewed

- `README.md`, `docs/roadmap.md`, `docs/design_principles.md`, and `SPEC.md`.
- `docs/playtest-findings-v0.10.55.md` and its generated artifact.
- `docs/agent-playtest-protocol.md` and `docs/mcp-playtesting-guide.md`.
- The existing MCP wrapper and v0.10.54/v0.10.55 project-limit runners.

## Mechanism and Information Boundary

- The project ceiling, monthly draws, and delayed effects are existing game
  abstractions, not calibrated health-system constraints.
- The recovery policy receives actor-visible observation, legal command hints,
  plain validation error text, and the post-failure observation.
- The recovery branch excludes hidden state, history, error codes, structured
  hints, and resource payloads.

## Evidence Interpretation

- Same-turn preservation, safe retry, and hash continuity establish traceability.
- A response-conditioned deterministic policy does not establish human
  comprehension, learning, advice quality, balance, or strategy quality.
- Runtime validation hints remain deferred unless another artifact identifies a
  concrete unexplained recovery failure.

## Risks

- The fixed three-seed Hard matrix may not expose organic player friction.
- The project ceiling is a game abstraction and must not be presented as a
  real-world operational constraint.
