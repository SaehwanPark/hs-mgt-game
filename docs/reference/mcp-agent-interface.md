# MCP Agent Interface

**Status:** Implemented and current for v0.14.3
**Audience:** AI-agent clients, contributors, instructors testing autonomous play

The `hs-mgt-game-mcp` binary exposes a local Model Context Protocol server over
stdio. It lets an AI agent play all three current bounded campaigns without
using terminal prompts. The GUI loopback host and MCP adapter share host
authority, actor-visible projections, history/replay, and checkpoint boundaries.

## Run

```bash
cargo run --bin hs-mgt-game-mcp
```

MCP clients should launch the binary as a stdio server. The default MCP process
keeps active session state and any checkpoint snapshot in process memory;
durable checkpoint archives, discovery, and restoration are provided by the
loopback GUI host when its configured persistence path is available. Clients
never own save bytes.

## Tools

| Tool | Purpose |
| --- | --- |
| `start_session` | Start `stabilization-v1`, `competitive-regional-v1`, or `regional-affiliation-v1` |
| `get_observation` | Read the current actor-visible observation and command format |
| `get_action_catalog` | Read the host-ordered competitive action catalog and parameter metadata |
| `get_resolution` | Read a committed competitive-month resolution |
| `get_regional_world` | Read the actor-visible competitive regional-world projection |
| `get_campaign_coverage` | Read actor-visible stage, decision, history, replay, and debrief coverage for all campaigns |
| `validate_turn` | Validate a competitive command batch without advancing the session |
| `submit_turn` | Submit one command string and advance one turn/month |
| `get_history` | Read append-only transition summaries and state hashes |
| `get_replay` | Verify and read host-owned replay metadata and summaries |
| `save_session` | Request a host-owned checkpoint snapshot |
| `load_session` | Restore a validated host-owned checkpoint snapshot |
| `get_presentation` | Read the actor-visible competitive presentation envelope |
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
stabilization, competitive, or regional-affiliation scenario file.

### `submit_turn`

Stabilization uses the existing turn-specific numeric command formats returned
by `legal_commands`.

Competitive uses the existing Stata-like batch syntax, for example:

```text
invest domain=beds amount=20; commit pledge_type=access level=2
```

Invalid commands return a tool-level structured error and do not advance the
session.

Competitive validation errors preserve the plain `error` string and may include
additive structured fields:

```json
{
  "error": "cash required 65 exceeds available 60",
  "code": "insufficient_cash",
  "resource_limit": {
    "resource": "cash",
    "required": 65,
    "available": 60
  },
  "hint": "Reduce cash spending, choose hold or monitor, or wait for resources before resubmitting."
}
```

The structured fields are present only when the server can classify the
competitive validation failure. Parser, session, scenario, and other generic
errors may return only `error`. Clients should treat `code`, `resource_limit`,
and `hint` as optional.

## Boundary

The MCP layer is an interface adapter. It reuses the existing scenario
validation, parsers, observation helpers, validation functions, transition
functions, and debrief helpers. It does not add randomness, rewrite history, or
expose hidden true state beyond the current actor-visible observation and
committed transition summaries.

For `competitive-regional-v1`, `end_session` includes final player tradeoff and
resource metrics derived from the player-controlled system in committed history. This is an
end-of-run debrief surface, not an active-play observation surface, and it does
not add rival private-state reporting.

## Deferred

- Streamable HTTP transport and auth
- Durable MCP session persistence
- Multi-client session coordination
- Scenario migration tooling
