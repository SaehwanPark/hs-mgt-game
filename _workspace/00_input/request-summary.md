# Request Summary - Live Consultant Advice and Advisory History

## Scope

- Roadmap phase: Phase 7 competitive teachability and validation loop.
- Task type: development continuation and bounded runtime vertical slice.
- Selected slice: restore deterministic state-conditioned consultant options for
  every competitive CLI/MCP month and retain the exact options shown for
  debrief comparison.

## Sources

- `README.md`, `docs/proposal.md`, `docs/roadmap.md`, and
  `docs/design_principles.md`
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/expansion-proposal-review.md`
- U.S. Bureau of Labor Statistics Management Analysts profile

## Expected Files

- `src/model/campaign.rs`, `src/model/competitive_history.rs`, and competitive
  observation/resolution paths
- `src/mcp/session.rs`, `src/debrief/report.rs`, and focused tests
- `SPEC.md`, `CHANGELOG.md`, package metadata, competitive design docs, and
  `_workspace/03_domain_qa.md` / `_workspace/final/handoff.md`

## Validation Target

- Every competitive month exposes four deterministic, non-binding options from
  the human actor's `PlayerObservation`.
- The exact options shown are retained with the committed transition and are
  compared with the player's commands in the debrief.
- State transitions, AI behavior, commands, ruleset values, and state hashes do
  not change.

## Non-Goals

- No advisor market, advisor roster, payroll, candidate pool, hire/fire command,
  AI advice policy, scenario schema, balance change, or human-learning claim.
