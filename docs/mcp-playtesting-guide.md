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

## Free-Form Hard Competitive Runs

Use this procedure when collecting observation-driven free-form evidence on the
full 24-month competitive campaign at Hard difficulty. This extends the general
free-form procedure above. This slice omits stabilization and Normal difficulty;
it is competitive Hard only.

1. Build the MCP server: `cargo build --bin hs-mgt-game-mcp`.
2. Start `competitive-regional-v1` with `difficulty=hard` and seed `42` unless
   the findings question requires seed variation.
3. Use deterministic observation-heuristic policies or manual command entry
   (not LLM play unless separately documented). Choose commands only from
   player-facing docs, current MCP observations, and `legal_commands` hints.
   Record persona prompts, per-month observation cues, submitted commands,
   validation failures, transition hashes, and final debrief metrics.
4. Run at least two distinct free-form profiles. Recommended personas from prior
   evidence: Free-Form Fiscal Steward, Free-Form Access Expansion Advocate, and
   Free-Form First-Time Executive.
5. Compare outcomes against the v0.9.9 `--target difficulty-adaptive` Hard
   scripted baselines for the same seed rather than treating either artifact as
   balance evidence.
6. Label results as free-form simulated-agent evidence. Do not present them as
   human learning, empirical calibration, or policy forecasting.

Operator capture for free-form Hard competitive runs:

```bash
python3 _workspace/experiments/v0.10.0-free-form-hard/run_sessions.py
```

The operator script writes `_workspace/experiments/v0.10.0-free-form-hard/results.json`.
Findings are synthesized in versioned `docs/playtest-findings-v*.md` artifacts.

To extend the same three free-form Hard competitive profiles across seeds `42`,
`43`, and `44`:

```bash
python3 _workspace/experiments/v0.10.1-free-form-hard-seed-variation/run_sessions.py
```

The seed-variation script writes
`_workspace/experiments/v0.10.1-free-form-hard-seed-variation/results.json`.
Use it to test completion and profile endpoint stability across seeds, not to
justify balance or runtime changes.

To compare the v0.10.1 free-form Hard policies against bounded access-pledge
cooldown and reported-access-threshold variants:

```bash
python3 _workspace/experiments/v0.10.2-access-loop-diagnostic/run_sessions.py
```

The access-loop diagnostic script writes
`_workspace/experiments/v0.10.2-access-loop-diagnostic/results.json`. Use it to
test whether repetitive access commitments are reducible through operator-policy
or guidance changes. Do not treat it as evidence for runtime balance changes or
automatic command cooldowns.

To validate whether the v0.10.3 access-commitment guidance can reduce repeated
access pledges in a bounded operator policy:

```bash
python3 _workspace/experiments/v0.10.4-post-guidance-validation/run_sessions.py
```

The post-guidance validation script writes
`_workspace/experiments/v0.10.4-post-guidance-validation/results.json`. Use it to
compare unchanged baseline free-form Hard policies against a guidance-aware
variant that redirects repeated or high-access pledges to existing legal
fallback actions. Do not treat it as evidence for runtime balance changes,
automatic command cooldowns, or pledge-effect tuning.

The cross-artifact synthesis in `docs/playtest-findings-v0.10.5.md` summarizes
the `v0.10.0` through `v0.10.4` free-form Hard evidence without adding new runs.
Use it as the current routing note for access-pledge follow-up: repeated
baseline matrices are controls, not independent player evidence, and runtime
cooldowns or pledge-effect tuning still require a separate evidence gate.

The v0.10.7 sub-agent access-pledge slice replays three generated Hard
competitive command plans through MCP:

```bash
python3 _workspace/experiments/v0.10.7-llm-access-pledge-evidence/run_sessions.py
```

Use `docs/playtest-findings-v0.10.7.md` as bounded simulated-agent evidence
only. It does not justify runtime access cooldowns, pledge-effect tuning, or a
general LLM runner.

To capture observation-by-observation Hard competitive evidence through the
existing MCP wrapper:

```bash
python3 _workspace/experiments/v0.10.9-live-mcp-capture/run_sessions.py
```

The script writes
`_workspace/experiments/v0.10.9-live-mcp-capture/results.json` with actor-visible
observations, legal command hints, submitted commands, validation outcomes,
transition hashes, final observations, and final debriefs. Use
`docs/playtest-findings-v0.10.9.md` as workflow evidence for live capture, not as
human-learning, calibration, balance, or runtime-tuning evidence.

To generate a compact diagnostic report from that live-capture artifact:

```bash
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.9-live-mcp-capture/results.json --output _workspace/experiments/v0.10.10-live-capture-diagnostics/diagnostics.md
```

The report summarizes profile outcomes, action frequencies, validation failures,
access pledges, and final hashes. Use it as simulated-agent strategy-space
diagnostics only; it is not evidence for runtime tuning or balance changes.

To extend live capture across the current deterministic persona policies,
seeds `42`, `43`, and `44`, and Normal/Hard competitive difficulty tiers:

```bash
python3 _workspace/experiments/v0.10.11-live-capture-matrix/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.11-live-capture-matrix/results.json --output _workspace/experiments/v0.10.11-live-capture-matrix/diagnostics.md
```

Use `docs/playtest-findings-v0.10.11.md` as workflow evidence that the live MCP
capture path supports small seed/difficulty matrices. Do not treat the repeated
deterministic policies as independent player samples or evidence for runtime
tuning.

To run a live-capture matrix using the existing automated pressure policies and
the Hard difficulty-adaptive wrapper:

```bash
python3 _workspace/experiments/v0.10.12-live-difficulty-pressure/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json --output _workspace/experiments/v0.10.12-live-difficulty-pressure/diagnostics.md
```

Use `docs/playtest-findings-v0.10.12.md` as simulated-agent pressure evidence
for Normal/Hard comparison. Do not treat it as balance proof, empirical
calibration, human-learning evidence, or justification for runtime tuning by
itself.
