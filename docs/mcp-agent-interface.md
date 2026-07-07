# MCP Agent Interface

**Status:** Implemented v0.1.41  
**Audience:** AI-agent clients, contributors, instructors testing autonomous play

The `hs-mgt-game-mcp` binary exposes a local Model Context Protocol server over
stdio. It lets an AI agent play the current bounded campaigns without using
terminal prompts.

## Run

```bash
cargo run --bin hs-mgt-game-mcp
```

MCP clients should launch the binary as a stdio server. The server keeps session
state in memory for the lifetime of the process.

## Tools

| Tool | Purpose |
| --- | --- |
| `start_session` | Start `stabilization-v1` or `competitive-regional-v1` |
| `get_observation` | Read the current actor-visible observation and command format |
| `submit_turn` | Submit one command string and advance one turn/month |
| `get_history` | Read append-only transition summaries and state hashes |
| `end_session` | Close the session and return a debrief summary |

### `start_session`

Input:

```json
{
  "campaign": "stabilization-v1",
  "seed": 42
}
```

For competitive play:

```json
{
  "campaign": "competitive-regional-v1",
  "seed": 42,
  "difficulty": "normal",
  "scenario_path": "scenarios/competitive-v1-template.toml"
}
```

Difficulty may be `easy`, `normal`, `hard`, or `expert`; omitted difficulty
defaults to `normal`. `scenario_path` is optional and may point to a validated
stabilization or competitive scenario file.

### `submit_turn`

Stabilization uses the existing turn-specific numeric command formats returned
by `legal_commands`.

Competitive uses the existing Stata-like batch syntax, for example:

```text
invest domain=beds amount=20; commit pledge_type=access level=2
```

Invalid commands return a tool-level structured error and do not advance the
session.

## Boundary

The MCP layer is an interface adapter. It reuses the existing scenario
validation, parsers, observation helpers, validation functions, transition
functions, and debrief helpers. It does not add randomness, rewrite history, or
expose hidden true state beyond the current actor-visible observation and
committed transition summaries.

For `competitive-regional-v1`, `end_session` includes final player tradeoff and
resource metrics derived from the human system in committed history. This is an
end-of-run debrief surface, not an active-play observation surface, and it does
not add rival private-state reporting.

## Deferred

- Streamable HTTP transport and auth
- Durable MCP session persistence
- Multi-client session coordination
- Scenario migration tooling
