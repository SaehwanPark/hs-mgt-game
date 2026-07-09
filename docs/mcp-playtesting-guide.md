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
As of `v0.10.23`, competitive debriefs can include an access follow-through
note for low-cash access-heavy runs when public pledges outnumber durable
operational follow-through. Treat that note as explanatory product wording, not
as a balance change, validation failure, or human-learning result.
As of `v0.10.24`, bounded trigger/control MCP runs validate that the note
appears through end-session debriefs when expected and stays absent in nearby
controls. Keep follow-up work evidence-led; this validation does not justify
runtime tuning, pledge cooldowns, command-cost changes, or difficulty changes.
As of `v0.10.28`, the strategy-space synthesis compares finance-first,
access-heavy, workforce-protective, and growth-oriented signals across existing
competitive evidence. Treat those strategy labels as interpretive development
summaries, not hidden game classes, validated learner archetypes, or balance
proof.
As of `v0.10.29`, the debrief comparison surface turns the strategy-space
synthesis into a compact instructor/reviewer aid for comparing decision quality,
outcome quality, cash runway, durable follow-through, rival pressure, and
debrief traceability across repeated competitive runs. Treat it as discussion
design, not as human-learning validation, empirical calibration, or runtime
tuning evidence.
As of `v0.10.30`, the workforce-protective evidence review narrows one
comparison axis from the debrief surface. Treat workforce-protective play as an
interpretive review posture across staffing follow-through, workforce trust,
pacing, monitoring, and commitment discipline, not as a hidden strategy class,
validated learner archetype, standalone balance proof, or reason to tune
workforce formulas.
As of `v0.10.33`, the growth/capacity-oriented evidence review narrows a
parallel comparison axis from the debrief surface. Treat growth/capacity play
as an interpretive review posture across projects, investments, staffed
capacity, cash runway, access, and rival pressure, not as a hidden strategy
class, validated learner archetype, standalone balance proof, or reason to
tune project costs or capacity effects.
As of `v0.10.34`, the instructor debrief facilitation note sequences recent
comparison, workforce-protective, and growth/capacity evidence into classroom
or reviewer prompts. Treat it as a discussion aid, not as measured human
learning, a validated assessment instrument, or a reason to tune runtime
mechanics.
As of `v0.10.35`, the difficulty pressure dimension gate selects rival
information and monitoring pressure visibility as the next bounded difficulty
surface to design or test if difficulty remains the active priority. Treat it
as a routing gate, not as Expert winnability evidence, runtime tuning,
scoring evidence, or a reason to give rivals hidden omniscience.
As of `v0.10.36`, the rival information pressure design note defines
information delay, monitor value, and public disclosure as the reviewable
difficulty surfaces for future testing. Treat those tier descriptions as design
hypotheses, not implemented rules, empirical calibration, Expert winnability
proof, or a reason to change AP budgets, command costs, scoring, or balance.
As of `v0.10.37`, paired Hard/Expert live MCP captures compare monitored and
unmonitored rival-information policies at seed `42`. Treat the result as
observation-surface evidence for monitor value and debrief traceability, not as
human-learning validation, empirical calibration, Expert winnability proof, or
runtime tuning evidence.
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

To compare static and adaptive policies side by side in one live-capture
artifact:

```bash
python3 _workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json --output _workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md
```

Use `docs/playtest-findings-v0.10.13.md` as simulated-agent evidence for the
policy-wrapper comparison. Do not treat it as balance proof, empirical
calibration, human-learning evidence, or justification for runtime tuning by
itself.

To run independent observation-conditioned reviewer policies through the same
live-capture path:

```bash
python3 _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json --output _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/diagnostics.md
```

Use `docs/playtest-findings-v0.10.14.md` as simulated-agent reviewer evidence.
Do not treat it as balance proof, empirical calibration, human-learning
evidence, or justification for runtime tuning by itself.

To replay the accepted live month-by-month LLM/sub-agent difficulty-gate command
streams:

```bash
python3 _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md
```

Use `docs/playtest-findings-v0.10.15.md` as simulated-agent live-decision
evidence. It can inform follow-up guidance, debrief, and validation questions;
do not treat it as balance proof, empirical calibration, human-learning
evidence, or justification for runtime tuning by itself.

As of `v0.10.17`, live-capture diagnostics also report optional
`live_validation_retries` metadata when an artifact includes it. Use the
`Live Retry Signals` table to distinguish final replay validation failures from
cash-overrun or other rejected live decision attempts before the accepted
command stream.

As of `v0.10.18`, competitive MCP validation errors may include additive
structured fields alongside the existing `error` string. Resource-limit failures
such as cash overrun, AP overrun, and political-capital overrun include a stable
`code`, a `resource_limit` object, and a short `hint`. Use these fields in live
capture wrappers to classify retry causes without parsing human-readable error
text. Do not treat the presence of structured retry metadata as balance,
calibration, or runtime-tuning evidence by itself.

As of `v0.10.19`, the shared Python MCP wrapper preserves those additive fields
inside captured `validation_failures` and `live_validation_retries` records
while keeping the plain `error` string for compatibility. Diagnostics prefer
structured cash-retry metadata when present and fall back to legacy string-only
artifacts when older evidence files do not include `code` or `resource_limit`.

As of `v0.10.20`, the current retry-visibility gate is closed for live-capture
classification: the MCP server emits structured resource-limit fields, the
Python wrapper preserves them, and diagnostics prefer them while retaining
legacy fallback. Treat this as tooling confidence only. Runtime tuning, command
cost changes, pledge cooldowns, or difficulty changes still require a separate
evidence slice naming a concrete mechanic problem beyond retry classification.

As of `v0.10.21`, the live-capture evidence synthesis routes the next bounded
question toward access-heavy player understanding: can debrief and guidance
clearly distinguish public access pledges from durable operational follow-through
under cash pressure? Use existing live-capture artifacts and diagnostics first.
Do not expand retry metadata again or tune runtime mechanics unless a later
evidence slice identifies a concrete mechanic problem.

As of `v0.10.22`, the access-heavy comprehension review uses the existing
`v0.10.15` live-capture artifact and diagnostic report to compare the Live
Access Operator's Normal and Hard runs. Treat the next bounded follow-up as
explanatory competitive debrief wording for access-heavy runs, not runtime
tuning, command-cost changes, access-pledge cooldowns, or difficulty changes.

As of `v0.10.24`, `_workspace/experiments/v0.10.24-access-debrief-validation/`
contains bounded MCP trigger/control evidence for the access follow-through
debrief note. Use it as debrief-surface validation only, not as human-learning
or balance evidence.

As of `v0.10.25`, `docs/playtest-findings-v0.10.25.md` synthesizes the
`v0.10.21` through `v0.10.24` access-heavy evidence chain. Treat that synthesis
as a routing checkpoint: access follow-through is now covered as debrief
explanation, and future runtime changes still require a separate artifact that
identifies a concrete mechanics problem.

As of `v0.10.26`, `docs/playtest-findings-v0.10.26.md` compares recent
competitive evidence for teachability, debrief coherence, and repeated-play
interest. Treat that synthesis as a broader Phase 7 routing checkpoint:
follow-up work should prefer instructor-facing comparison prompts or broader
strategy-space synthesis before reopening runtime tuning.

As of `v0.10.27`, `docs/playtest-findings-v0.10.27.md` turns the competitive
teachability synthesis into instructor-facing comparison prompts. Use it for
discussion of decision quality versus outcome quality across existing evidence,
not as human-learning validation, empirical calibration, or runtime tuning
evidence.

As of `v0.10.29`, `docs/playtest-findings-v0.10.29.md` adds a compact
debrief comparison surface for repeated competitive runs. Use it to structure
instructor or reviewer discussion across strategy postures and final debriefs.
Do not treat it as a score, hidden strategy taxonomy, classroom-effectiveness
measure, balance proof, or justification for runtime changes.

As of `v0.10.30`, `docs/playtest-findings-v0.10.30.md` reviews
workforce-protective play as an interpretive comparison axis across staffing,
trust, pacing, monitoring, and commitment discipline. Use it for discussion and
future evidence routing, not as a standalone strategy class, validated learner
archetype, balance proof, or reason to tune workforce mechanics.

As of `v0.10.33`, `docs/playtest-findings-v0.10.33.md` reviews
growth/capacity-oriented play as an interpretive comparison axis across
projects, investments, staffed capacity, cash runway, access, and rival
pressure. Use it for discussion and future evidence routing, not as a
standalone strategy class, validated learner archetype, balance proof, or
reason to tune project costs, capacity effects, staffing allocation, or
difficulty.

As of `v0.10.34`, `docs/playtest-findings-v0.10.34.md` provides an instructor
debrief facilitation sequence across decision context, outcome context,
follow-through, workforce posture, growth posture, rival response, and debrief
clarity. Use it to guide repeated-run discussion, not to claim measured
learning or promote runtime tuning.
