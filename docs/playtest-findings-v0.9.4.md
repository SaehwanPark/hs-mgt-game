# AI-Agent Playtest Findings v0.9.4

- **Status:** Phase 7 scripted agent evidence
- **Date:** 2026-07-06
- **Code version:** 0.9.4
- **Harness:** `python3 scripts/run_automated_playtests.py` over local MCP stdio
- **Campaigns:** `stabilization-v1`, `competitive-regional-v1`
- **Seeds:** `42`, `43`, `44`
- **Difficulty:** normal for competitive runs
- **Agent profiles:** Fiscal Caution, Capacity Growth, Balanced Strategy, Naive First-Time

These findings are simulated-agent evidence only. They do not measure human
learning, classroom engagement, empirical calibration, real-world policy
validity, or numerical balance.

## Run Matrix

| Campaign | Seeds | Profiles | Completed sessions | Validation failures |
| --- | --- | ---: | ---: | ---: |
| `stabilization-v1` | 42, 43, 44 | 4 | 12 | 0 |
| `competitive-regional-v1` | 42, 43, 44 | 4 | 12 | 0 |

All scripted sessions completed through the MCP playtest harness without
crashes, hangs, incomplete batches, or command validation failures.

## Strategy And Outcome Patterns

### Stabilization

| Metric | Range |
| --- | ---: |
| Cash | 15-70 |
| Access | 73-93 |
| Workforce trust | 64-68 |
| Community trust | 57-75 |
| Policy pressure | 35-59 |

Capacity Growth produced the highest access outcomes and lowest cash runway.
Naive First-Time preserved the most cash but had the weakest community-trust
outcomes. Balanced Strategy stayed between those extremes, preserving the
expected tradeoff among cash, access, and trust.

### Competitive

| Metric | Range |
| --- | ---: |
| Cash | 5-60 |
| Access | 70-73 |
| Staffed beds | 118-123 |
| Workforce trust | 30-60 |
| Community trust | 64-66 |
| Political capital | 15 |

Representative competitive final hashes:

| Seed | Fiscal Caution | Capacity Growth | Balanced Strategy | Naive First-Time |
| ---: | --- | --- | --- | --- |
| 42 | `e9cb05324ff5ab3d` | `0321a0d91a57fc46` | `5b221a911e97f76c` | `7e530a394a78bffe` |
| 43 | `3ed622680a05722b` | `ff3cda219966a9d0` | `2f72815ee9e95d4e` | `730a633e4ab170e4` |
| 44 | `cc02350cd77d622e` | `dbfd12910cadf61a` | `9927638123ee9e80` | `45ae273a72439a75` |

Capacity Growth again created the strongest pressure on cash and workforce
trust while increasing staffed beds. Fiscal Caution and Naive First-Time
preserved more cash and workforce trust, with lower access movement. Balanced
Strategy produced the highest access in this scripted batch but still carried
meaningful workforce-trust cost.

## Rubric Scores

| Dimension | Score | Evidence note |
| --- | ---: | --- |
| Command comprehension | 5 | All 24 scripted sessions completed without validation failures. |
| Strategic tension | 4 | Profiles produced clear cash, access, beds, and workforce-trust tradeoffs. |
| Causal transparency | 4 | Existing debrief and metric summaries support profile-level interpretation. |
| Pacing proxy | 5 | No hangs, stalls, or incomplete scripted batches occurred. |
| Action overload proxy | 4 | Scripted policies used multi-command competitive batches successfully. |
| Debrief coherence | 4 | Final metrics and debrief surfaces were sufficient for summary synthesis. |
| Exploit discovery | 2 | Matrix is useful smoke evidence, but not broad enough for exploit claims. |

## Gameplay Validity Hypotheses

- **Scripted agents can complete both current campaigns through the MCP
  boundary:** Pass. All expected sessions completed.
- **No profile is forced into immediate collapse under the tested seeds:** Pass.
  Even Capacity Growth completed with positive cash, though cash and workforce
  trust were strained.
- **Profiles produce materially different tradeoffs:** Pass. Cash ranged from
  `5` to `60` in competitive play and access ranged from `73` to `93` in
  stabilization.
- **The batch can support evidence-labeled follow-up without runtime changes:**
  Pass. No crash, hang, parser failure, or debrief blocker appeared.

## Evidence Limits

- These are scripted simulated-player runs, not human playtests.
- The findings do not support claims about measured learning, classroom
  effectiveness, policy validity, or empirical calibration.
- The profiles are intentionally simple and do not explore the full command
  space, difficulty space, service-line portfolio, or adversarial exploit paths.
- The competitive result summaries are useful for smoke validation, not for
  concluding that current balance is final.

## Prioritized Follow-Up

1. Keep using Phase 7 playtest evidence as the gate before adding new mechanics
   or actors; this batch did not identify an urgent runtime bug.
2. For the next validation slice, prefer a richer competitive strategy-space
   diagnostic or free-form agent run that exercises newer service-line commands
   directly.
3. Do not tune balance from this batch alone; use it as a regression and
   comprehension baseline after the ASC service-line expansion.
