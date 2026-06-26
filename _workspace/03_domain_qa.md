# Domain QA

Status: pass

## Checks

- Scope remains a bounded interface slice over existing campaigns.
- MCP does not add hidden randomness or read wall-clock/filesystem/network state
  during transition evaluation.
- Actor-visible observations remain distinct from true state.
- Histories are append-only summaries of committed transitions with state
  hashes.
- Invalid commands are invalid operations, not unfavorable modeled outcomes, and
  do not advance state.
- Educational debriefing remains derived from committed history.

## Known Limits

- Competitive MCP debrief is intentionally brief until the competitive campaign
  has a full replay/debrief artifact.
- In-memory sessions are acceptable for local agent play but not for classroom
  multi-client orchestration.
