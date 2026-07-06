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
competitive campaign previews. Competitive scripts submit commands across the
24-month campaign and include newer service-line, public-payer, staffing,
monitoring, and commitment actions. Treat these runs as simulated-player
evidence; they do not measure actual human learning or classroom effectiveness.

To execute the automated playtests and print a comparison table of their ending metrics:

```bash
python3 scripts/run_automated_playtests.py
```

To persist a compact JSON artifact for strategy-space diagnostics:

```bash
python3 scripts/run_automated_playtests.py --json-output _workspace/experiments/v0.9.6-playtest-policy-coverage/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.6-playtest-policy-coverage/results.json --output _workspace/experiments/v0.9.6-playtest-policy-coverage/diagnostics.md
```

To run the targeted project-command coverage diagnostic:

```bash
python3 scripts/run_automated_playtests.py --target project-coverage --json-output _workspace/experiments/v0.9.7-project-command-coverage/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.7-project-command-coverage/results.json --output _workspace/experiments/v0.9.7-project-command-coverage/diagnostics.md
```

To run the targeted difficulty-tier competitive sweep:

```bash
python3 scripts/run_automated_playtests.py --target difficulty-sweep --json-output _workspace/experiments/v0.9.8-difficulty-sweep/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.8-difficulty-sweep/results.json --output _workspace/experiments/v0.9.8-difficulty-sweep/diagnostics.md
```

To run the targeted difficulty-adaptive competitive sweep:

```bash
python3 scripts/run_automated_playtests.py --target difficulty-adaptive --json-output _workspace/experiments/v0.9.9-difficulty-adaptive/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.9.9-difficulty-adaptive/results.json --output _workspace/experiments/v0.9.9-difficulty-adaptive/diagnostics.md
```

### Expected Output
The script builds `hs-mgt-game-mcp`, launches the local stdio binary, runs both
campaigns for all four profiles across seeds `42`, `43`, and `44`, and
prints per-seed comparison tables plus compact metric ranges. Stabilization
metrics are parsed from the committed debrief. Competitive end-session debriefs
expose final player tradeoff metrics from committed history; treat those as
scripted-agent evidence, not human learning or empirical calibration evidence.
The optional JSON artifact records final observations, transition summaries,
debrief lines, validation failures, and metrics for lightweight diagnostics; it
is not a full replay artifact.
The `project-coverage` target is intentionally narrower than the default
baseline and is meant to exercise capital-project command paths, not to model a
recommended strategy or justify balance changes.
The `difficulty-sweep` target runs the four baseline competitive profiles at
`easy` and `hard` across seeds `42`, `43`, and `44`. It satisfies the agent
playtest protocol's difficulty-variation requirement without changing the default
Normal-only baseline batch.
The `difficulty-adaptive` target uses the same Easy/Hard matrix but wraps
baseline profiles with rival-aware command adjustments on Hard difficulty only
(Easy passes through static month tables). Reduced aggressive invests, added
monitors/holds, and workforce-commit preference when trust is low apply on Hard.
Use it when testing whether difficulty tiers change scripted player tradeoff
metrics; compare results against the static `difficulty-sweep` batch rather than
treating either batch as balance evidence.

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

## Free-Form Agent Evidence Runs

Use this procedure when collecting a bounded free-form agent artifact rather
than adding another scripted policy. The operator or agent should choose
commands only from player-facing docs, current MCP observations, and the
`legal_commands` hints returned by the server.

1. Use seed `42` unless the findings question requires seed variation.
2. Run both current campaigns: `stabilization-v1` and
   `competitive-regional-v1` with normal difficulty.
3. Record the agent profile or persona, observations shown, legal command hints,
   submitted command text, validation errors and retries, transition hashes,
   final debrief, and the agent's causal explanation after reading the history
   and debrief.
4. Label the result as free-form agent evidence. Do not present it as human
   learning evidence, empirical calibration, balance validation, or policy
   forecasting.

The run may use `scripts/play_game.py` interactively or a small operator-owned
MCP client wrapper. Do not commit a new LLM runner unless repeated findings show
that the existing client cannot capture the needed evidence.
