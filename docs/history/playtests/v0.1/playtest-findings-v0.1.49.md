# AI-Agent Playtest Findings v0.1.49

**Status:** Phase 7 simulated-player evidence  
**Date:** 2026-06-30  
**Code version:** 0.1.49  
**Harness:** `python3 scripts/run_automated_playtests.py` over local MCP stdio  

These findings are AI-agent/scripted-policy evidence only. They do not measure
human learning, classroom engagement, empirical calibration, or real-world
policy validity.

## Session Batch

| Campaign | Seed | Difficulty | Profiles | Completed sessions |
| --- | --- | --- | --- | --- |
| `stabilization-v1` | 42 | n/a | Fiscal Caution, Capacity Growth, Balanced Strategy | 3 |
| `competitive-regional-v1` | 42 | normal | Fiscal Caution, Capacity Growth, Balanced Strategy | 3 |

All six scripted sessions completed without validation failures after the MCP
playtest harness was corrected to keep stabilization policies on stabilization
commands after Turn 1.

## Run Matrix

### Stabilization

| Profile | Command pattern | Final cash | Final access | Workforce trust | Community trust | Final hash |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Fiscal Caution | lower spend, modest rate ask, modest commitments | 64 | 75 | 64 | 69 | `78c0a130398a6b0b` |
| Capacity Growth | high bed, policy, workforce, coalition, and defensive spending | 15 | 92 | 67 | 73 | `23c83e4a4ba225bf` |
| Balanced Strategy | middle-high commitments across turns | 32 | 89 | 68 | 73 | `6fb1ebbea564274f` |

The stabilization debrief exposed the final tradeoff line, actor rationales,
attributed mechanisms, decision-quality prompt, and observation revision note
for each run.

### Competitive Preview

| Profile | Command pattern | Final hash |
| --- | --- | --- |
| Fiscal Caution | monitor, small nurse recruitment, low access pledge | `3c0634b870c2d0cd` |
| Capacity Growth | bed investment, larger nurse recruitment, aggressive payer negotiation | `0051c77b4d9e31c1` |
| Balanced Strategy | monitor plus recruitment, bed investment plus access pledge, neutral negotiation | `640c6c7654595008` |

The competitive MCP debrief exposed completion count, final hash, final
calendar, recruitment timing lesson, and the decision-vs-outcome boundary. It
does not yet expose final competitive outcome metrics through the automated
summary, so competitive outcome-distribution diagnostics are hash- and
command-pattern-based in this batch.

## Gameplay Validity Hypotheses

- **Multiple strategies can complete the current slice:** Pass for this seed.
  All three profiles completed both campaigns without collapse or validation
  failure.
- **No single first-month command dominates across profiles:** Pass as a
  first-pass signal. Stabilization first actions diverged by spend and rate ask;
  competitive first actions diverged among monitoring, capacity investment, and
  recruitment.
- **Agents can explain outcomes from debrief and history:** Partial pass.
  Stabilization debriefs provide strong causal attribution and decision-quality
  prompts. Competitive debriefs explain recruitment timing and the
  observation/history boundary but do not yet summarize final metric tradeoffs.
- **Rival behavior is recognizable but imperfectly predictable:** Partial pass.
  Competitive histories commit different final hashes under different player
  profiles, and observations expose public/rival context, but this small
  scripted batch did not ask agents to predict rivals independently.
- **A first-time simulated player can complete a month using actor-visible
  information and command hints:** Partial pass. The scripted policies completed
  the run through actor-visible MCP command surfaces after the harness fix, but
  pre-authored policies do not prove that a naive or free-form agent can infer
  the command strategy from player-facing docs.

## Rubric Scores

| Dimension | Score | Evidence note |
| --- | ---: | --- |
| Command comprehension | 4 | Corrected policies completed six sessions with zero validation failures; the prior bug was in harness campaign detection, not game command validation. |
| Strategic tension | 4 | Stabilization produced clear cash-access tradeoffs; competitive profiles selected materially different command clusters and final hashes. |
| Causal transparency | 3 | Strong in stabilization; competitive debrief remains too thin for final outcome explanation. |
| Pacing proxy | 4 | All bounded sessions completed quickly through MCP after the harness fix. |
| Action overload proxy | 3 | Scripted profiles did not stall, but they do not test naive command selection or overload. |
| Debrief coherence | 3 | Stabilization separates decisions, mechanisms, observations, and outcomes; competitive needs richer final tradeoff reporting. |
| Exploit discovery | 2 | No collapse or obvious exploit in this seed; one seed and scripted profiles are too small for dominance claims. |

## Evidence Limits

- This is a six-session scripted-policy batch at seed `42`, not a stochastic
  sensitivity study.
- The batch does not include free-form LLM/sub-agent personas or deliberately
  naive first-time agents.
- Competitive final metrics are not exposed in the automated summary, limiting
  outcome-distribution diagnostics for that campaign.
- No numeric balance or formula changes should be made from this batch alone.

## Prioritized Follow-Up

1. Add a bounded competitive MCP/debrief summary that exposes final player
   tradeoff metrics from committed history without revealing hidden state during
   active play.
2. Run a seed-variation batch after the competitive summary gap is closed.
3. Add one naive/free-form agent profile to test command comprehension and help
   text beyond scripted policies.
4. Keep broader diagnostics tooling deferred until repeated findings need more
   than the current script and findings document can provide.
