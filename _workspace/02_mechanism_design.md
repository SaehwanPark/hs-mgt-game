# Mechanism Design

## Interface Mechanism

The MCP server is an adapter around existing campaign mechanisms. It creates
in-memory sessions, returns actor-visible observations, accepts existing command
strings, validates them at the same boundary as CLI play, and commits completed
turn/month transitions to append-only histories.

## Campaign Coverage

- `stabilization-v1`: five existing executive decision turns with turn-specific
  numeric command text.
- `competitive-regional-v1`: three-month preview with existing Stata-like
  competitive command batches.
- `Naive First-Time`: deterministic scripted profile that uses legal
  low-complexity commands to probe completion and outcome contrast without
  optimizing strategy.

## Observation Boundary

MCP responses expose current observations and transition summaries only. They do
not expose hidden true state except where already represented by current player
briefing values or committed public history.

## Failure Modes

- Unknown sessions, unsupported campaigns, unsupported difficulty labels,
  invalid commands, and completed sessions return tool-level structured errors.
- Failed command validation does not mutate session state or history.

## Deferred

Network transport, auth, persistence, long competitive campaigns, replay export,
scenario expansion, free-form agent orchestration, and balance changes are
deferred until agent-play evidence justifies them.
