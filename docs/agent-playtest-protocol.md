# AI-Agent Playtest Protocol

**Status:** Active Phase 7 validation protocol  
**Audience:** Contributors, domain reviewers, and agent-playtest operators  
**Version:** v0.11.1 (governed by ADR-0009)

This protocol replaces planned recruitment of external human playtesters for the
current validation path because recruitment and participant-study costs are not
feasible for this personal project. It uses AI agents or sub-agents to play the bounded
campaign slices through the local MCP interface, then synthesizes reproducible
evidence about command comprehension, strategic diversity, pacing proxies,
exploit risk, causal transparency, and debrief coherence.

Agent playtests are not human-subjects research, classroom learning evaluation,
or policy validation. They can show how simulated players navigate the game
surface under documented personas; they cannot prove actual learner engagement,
human cognitive load, or real-world policy effects.

## Current Playable Scope

| Campaign | Current status | Agent-playtest target |
| --- | --- | --- |
| `stabilization-v1` | Five-turn playable slice | First-pass comprehension, tradeoffs, and debrief coherence |
| `competitive-regional-v1` | 24-month campaign | Competitive command comprehension, simultaneous rival pressure, and monthly tradeoffs |

Medicare and Medicaid strategic actors (beyond standard integration), empirical
calibration, and human learning-outcome measurement remain outside this protocol.

## Required Harness

Use the local MCP stdio server as the reproducible play boundary:

```bash
cargo run --bin hs-mgt-game-mcp
```

The baseline automation is documented in
[`mcp-playtesting-guide.md`](mcp-playtesting-guide.md):

```bash
python3 scripts/run_automated_playtests.py
```

Scripted policies and LLM/sub-agent personas may both be used. A run is
acceptable evidence only when its artifact records:

- campaign, seed, difficulty, and code version;
- agent profile or policy name;
- prompt/persona text for LLM or sub-agent runs;
- actor-visible observations and legal command hints seen by the agent;
- submitted commands, validation failures, transition history, and final debrief;
- synthesis notes that separate observed run behavior from interpretation.

## Agent Profiles

Every synthesis batch should include at least three distinct profiles:

| Profile | Intended behavior |
| --- | --- |
| Fiscal cautious | Protect cash runway, use lower-risk commitments, avoid aggressive spending |
| Capacity growth | Prioritize access, beds, and recruitment even under financial pressure |
| Balanced strategy | Trade off cash, access, workforce trust, and policy legitimacy |

Additional profiles may test specific risks, such as syntax confusion, aggressive
payer negotiation, monitoring-heavy competitive play, or deliberately naive
first-time play. Label adversarial or stress-test agents separately from
plausible player personas.

## Session Matrix

The v0.11.1 operating-loop validation matrix uses five deterministic policy
lanes across seeds `42`, `43`, and `44`, and Easy/Normal/Hard/Expert competitive
difficulties. It captures actor-visible observations, legal commands, submitted
commands, transition summaries, hashes, and debriefs for each 24-month run.
This is a bounded simulated-policy matrix, not a learner or balance study.

For each findings document, run the smallest matrix that answers the question
being tested:

- default baseline: seed `42`, all three required profiles, both current
  campaigns;
- seed variation: at least three named seeds when testing stochastic sensitivity;
- difficulty variation: normal by default, plus one focused difficulty change
  when testing competitive pacing or resource pressure;
- regression rerun: repeat the prior findings matrix after player-facing or
  validation changes that should affect playtest evidence.

Do not tune numeric balance from a single profile, seed, or campaign.

## Gameplay Validity Hypotheses

Each synthesis should state which hypotheses it tests. The default competitive
preview batch should test these five unless the findings document explains why a
smaller scope is sufficient:

- At least three materially different strategies can complete the current slice
  without collapse under plausible seeds.
- No single first-month command or command batch dominates across required
  profiles and plausible seeds.
- Agents can explain the main cause of an outcome after reading the debrief and
  transition history.
- Rival behavior is institutionally recognizable but not perfectly predictable
  from the player's actor-visible report.
- A first-time simulated player can complete a month using only actor-visible
  observations, legal command hints, and player-facing docs, without consulting
  implementation documentation.

Failed hypotheses are useful evidence. Record whether the follow-up belongs in
player guidance, command help, debriefing, balance investigation, scenario
authoring, or runtime behavior.

## Strategy-Space Diagnostics

When the batch is large enough to support comparison, include compact
diagnostics:

- action frequencies by campaign, profile, seed, and month or turn;
- outcome distributions for cash, access, trust, political capital, and other
  scenario-relevant metrics;
- strategy clusters or repeated command patterns;
- regret-style notes where an obvious alternative was available from the same
  actor-visible information;
- sensitivity to stochastic inputs across named seeds;
- dominance or near-dominance findings.

Do not present diagnostics as equilibrium analysis or empirical calibration.
They are validation aids for gameplay, comprehension, and debrief quality.

## Observation Rubric

Score each agent batch from 1 to 5 and include short evidence notes:

| Dimension | Evidence source |
| --- | --- |
| Command comprehension | Validation failures, command retries, legal-command use |
| Strategic tension | Divergence among profile choices and outcomes |
| Causal transparency | Agent explanations, transition summaries, debrief traceability |
| Pacing proxy | Number of turns completed, repeated stalls, prompt length friction |
| Action overload proxy | Evidence that agents ignore, misuse, or over-repeat commands |
| Debrief coherence | Whether debrief separates decisions, uncertainty, outcomes, and tradeoffs |
| Exploit discovery | Repeated dominant paths, resource loopholes, or nonsensical high-scoring play |

Use "proxy" deliberately for pacing and action overload. Agent behavior can flag
friction, but it does not measure human cognitive burden.

## Synthesis Template

Create versioned findings documents such as
`docs/playtest-findings-v0.1.48.md`. Do not overwrite prior findings.

```text
Session batch id:
Date:
Code version:
Campaigns:
Seeds:
Difficulties:
Agent profiles:
Harness:

Run matrix:
-

Observed command or validation friction:
-

Strategy and outcome patterns:
-

Rubric scores:
Command comprehension:
Strategic tension:
Causal transparency:
Pacing proxy:
Action overload proxy:
Debrief coherence:
Exploit discovery:

Evidence limits:
-

Prioritized follow-up:
-
```

## Evidence Limits

Agent playtest findings may justify:

- command-help and observation wording improvements;
- MCP automation affordances;
- bounded competitive hardening;
- exploit investigation;
- debrief and causal-explanation revisions;
- scenario-authoring or evidence-ledger follow-up.

Agent playtest findings must not be presented as:

- validated human comprehension;
- measured educational effectiveness;
- formal classroom assessment evidence;
- empirical calibration of real health-system parameters;
- policy forecasts or claims about actual institutions.

If the project later needs human educational evidence, create a separate,
funded and approved evaluation plan rather than reviving recruitment silently.
