# MCP Playtesting Guide

This guide describes how to run automated and interactive gameplay playtests of the Health Policy Strategy Game using the Model Context Protocol (MCP) interface and the provided Python tooling. It is the operational runbook for the active [`AI-Agent Playtest Protocol`](agent-playtest-protocol.md).

## Architecture Overview

The playtesting harness decouples the simulation logic from the player client:
1. **MCP Server:** The Rust executable `hs-mgt-game-mcp` exposes tools over stdio using JSON-RPC 2.0. It keeps session state in memory.
2. **Python Client Wrapper:** Located in `scripts/play_game.py`. It starts the MCP server as a subprocess, performs the initialize handshake, and exposes high-level Python wrappers for:
   - Starting a campaign session (`start_session`)
   - Submitting commands and advancing turns (`submit_turn`)
   - Getting history and debriefs (`get_history` / `end_session`)

## Running Automated Playtests

We have automated four scripted profiles (Fiscal Caution, Capacity Growth,
Balanced Strategy, and Naive First-Time) across both the stabilization and
competitive campaign previews. Treat these runs as simulated-player evidence;
they do not measure actual human learning or classroom effectiveness.

To execute the automated playtests and print a comparison table of their ending metrics:

```bash
python3 scripts/run_automated_playtests.py
```

### Expected Output
The script builds `hs-mgt-game-mcp`, launches the local stdio binary, runs both
campaigns for all four profiles across seeds `42`, `43`, and `44`, and
prints per-seed comparison tables plus compact metric ranges. Stabilization
metrics are parsed from the committed debrief. Competitive end-session debriefs
expose final player tradeoff metrics from committed history; treat those as
scripted-agent evidence, not human learning or empirical calibration evidence.

## Creating a Custom Strategy Policy

You can define a custom programmatic policy to test new behaviors. A policy is a Python function that takes:
- `obs`: List of strings representing the current actor-visible observations.
- `legal`: List of strings containing hints or descriptions of legal command formats.
- `turn`: The current 1-indexed turn or month.

And returns a string command batch.

### Example Policy Function

```python
def my_custom_policy(obs, legal, turn):
  # Stabilization Turn 1 input: staffed_beds capital_spend requested_rate
  if turn == 1:
    return "6 12 110"
  
  # Competitive commands
  if turn == 2:
    return "recruit role=nurse headcount=3; monitor target=northlake depth=1"
    
  return "hold"
```

To run this policy:

```python
from play_game import play_session

result = play_session("competitive-regional-v1", seed=42, policy_fn=my_custom_policy)
print(result["debrief"])
```

## Interactive Play via MCP Client

You can also use the python script to play interactively in the terminal by omitting the `policy_fn`:

```python
python3 scripts/play_game.py stabilization-v1
```

This will print the observation and prompt you to input the commands manually, sending them directly to the underlying MCP server.
