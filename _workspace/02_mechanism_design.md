# Mechanism Design

## Interface Mechanism

The MCP server remains an adapter around existing campaign mechanisms. It
creates in-memory sessions, returns actor-visible observations, accepts existing
command strings, validates them at the same boundary as CLI play, and commits
completed turn/month transitions to append-only histories.

## Campaign Coverage

- `stabilization-v1`: five existing executive decision turns with turn-specific
  numeric command text.
- `competitive-regional-v1`: three-month preview with existing Stata-like
  competitive command batches.
- `Free-Form First-Time Executive`: operator-run simulated-agent profile that
  chooses commands from actor-visible observations, legal-command hints, and
  player-facing docs.

## Observation Boundary

MCP responses expose current observations and transition summaries only. They do
not expose hidden true state except where already represented by current player
briefing values, legal-command hints, committed public history, or end-session
debrief metrics.

## Failure Modes

- Unknown sessions, unsupported campaigns, unsupported difficulty labels,
  invalid commands, and completed sessions return tool-level structured errors.
- Failed command validation does not mutate session state or history.
- This slice records validation failures and retries if they occur; it does not
  change parser or validation behavior.

## Deferred

Network transport, auth, persistence, long competitive campaigns, replay export,
scenario expansion, LLM-runner orchestration, balance changes, and analytics
tooling are deferred until repeated evidence justifies them.
