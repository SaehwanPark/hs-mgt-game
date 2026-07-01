# AI-Agent Playtest Findings v0.1.51

- **Status:** Phase 7 scripted-player seed-variation evidence
- **Date:** 2026-07-01
- **Code version:** 0.1.51
- **Harness:** `python3 scripts/run_automated_playtests.py` over local MCP stdio

These findings are scripted-agent evidence only. They do not measure human
learning, classroom engagement, empirical calibration, or real-world policy
validity.

## Session Batch

| Campaign | Seeds | Difficulty | Profiles | Completed sessions |
| --- | --- | --- | --- | ---: |
| `stabilization-v1` | 42, 43, 44 | n/a | Fiscal Caution, Capacity Growth, Balanced Strategy | 9 |
| `competitive-regional-v1` | 42, 43, 44 | normal | Fiscal Caution, Capacity Growth, Balanced Strategy | 9 |

All 18 scripted sessions completed without validation failures. The batch uses
the v0.1.50 competitive end-session debrief metrics for final player tradeoff
and resource outcomes.

## Run Matrix

### Stabilization

| Seed | Profile | Final cash | Final access | Workforce trust | Community trust |
| ---: | --- | ---: | ---: | ---: | ---: |
| 42 | Fiscal Caution | 64 | 75 | 64 | 69 |
| 42 | Capacity Growth | 15 | 92 | 67 | 73 |
| 42 | Balanced Strategy | 32 | 89 | 68 | 73 |
| 43 | Fiscal Caution | 64 | 76 | 64 | 69 |
| 43 | Capacity Growth | 15 | 93 | 67 | 75 |
| 43 | Balanced Strategy | 32 | 90 | 68 | 75 |
| 44 | Fiscal Caution | 64 | 75 | 64 | 69 |
| 44 | Capacity Growth | 15 | 92 | 67 | 75 |
| 44 | Balanced Strategy | 32 | 89 | 68 | 75 |

Across this small seed matrix, stabilization cash and workforce trust stayed
profile-driven, while reported access varied by one point and community trust
varied by up to two points under the higher-commitment profiles.

### Competitive Preview

| Seed | Profile | Final hash | Cash | Access | Beds | Workforce trust | Community trust | PC |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 42 | Fiscal Caution | `3c0634b870c2d0cd` | 50 | 70 | 120 | 58 | 65 | 13 |
| 42 | Capacity Growth | `0051c77b4d9e31c1` | 5 | 70 | 129 | 54 | 64 | 12 |
| 42 | Balanced Strategy | `640c6c7654595008` | 25 | 73 | 125 | 56 | 66 | 11 |
| 43 | Fiscal Caution | `3c0634b870c2d0cd` | 50 | 70 | 120 | 58 | 65 | 13 |
| 43 | Capacity Growth | `0051c77b4d9e31c1` | 5 | 70 | 129 | 54 | 64 | 12 |
| 43 | Balanced Strategy | `640c6c7654595008` | 25 | 73 | 125 | 56 | 66 | 11 |
| 44 | Fiscal Caution | `3c0634b870c2d0cd` | 50 | 70 | 120 | 58 | 65 | 13 |
| 44 | Capacity Growth | `0051c77b4d9e31c1` | 5 | 70 | 129 | 54 | 64 | 12 |
| 44 | Balanced Strategy | `640c6c7654595008` | 25 | 73 | 125 | 56 | 66 | 11 |

The bounded competitive preview produced identical final hashes and metric lines
for each scripted profile across seeds 42, 43, and 44. Within this batch,
strategy choice drove outcomes more than seed choice.

## Diagnostic Summary

| Campaign | Sessions | Cash range | Access range | Workforce range | Community range | Notes |
| --- | ---: | --- | --- | --- | --- | --- |
| Stabilization | 9 | 15-64 | 75-93 | 64-68 | 69-75 | Small stochastic variation appears in reported access and community trust. |
| Competitive preview | 9 | 5-50 | 70-73 | 54-58 | 64-66 | No observed seed variation for these profiles and seeds. |

Competitive resource ranges were staffed beds `120-129` and political capital
`11-13`, both driven by scripted profile differences in this matrix.

## Gameplay Validity Hypotheses

- **Multiple strategies can complete the current slice:** Pass for this seed
  matrix. All 18 sessions completed without collapse or validation failure.
- **No single first-month command dominates across required profiles and
  plausible seeds:** Partial pass. Scripted competitive profiles produce
  distinct cash, bed, workforce, community, and political-capital tradeoffs, but
  the three tested seeds did not change competitive outcomes.
- **Agents can explain the main cause of an outcome from debrief and history:**
  Partial pass. The competitive final metric surface now supports outcome
  comparison, but this scripted batch did not include agent-authored
  explanations.
- **Rival behavior is recognizable but imperfectly predictable:** Not tested
  beyond committed history variation. The seed matrix did not vary competitive
  rival outcomes under these profiles.
- **A first-time simulated player can complete a month using actor-visible
  information and command hints:** Not tested. These were pre-authored scripted
  policies.

## Rubric Scores

| Dimension | Score | Evidence note |
| --- | ---: | --- |
| Command comprehension | 4 | All scripted sessions completed with zero validation failures. |
| Strategic tension | 4 | Profile choices still create clear cash, access, trust, and resource tradeoffs. |
| Causal transparency | 3 | End-session metrics make competitive outcomes comparable; agent-authored causal explanations remain untested. |
| Pacing proxy | 4 | The 18-session MCP batch completed quickly without stalls. |
| Action overload proxy | 3 | Scripted profiles still do not test first-time command selection or overload. |
| Debrief coherence | 4 | Competitive debrief metrics close the v0.1.49 outcome-summary gap for scripted comparisons. |
| Exploit discovery | 2 | No collapse or obvious exploit appeared, but three seeds and scripted profiles are insufficient for dominance claims. |

## Evidence Limits

- This is an 18-session scripted-policy batch, not free-form agent play or human
  educational evaluation.
- Seeds 42, 43, and 44 are enough for first sensitivity evidence, not robust
  stochastic characterization.
- The competitive preview showed no seed variation for this matrix, which may
  reflect limited stochastic influence in the current bounded three-month path
  rather than a general determinism claim about future competitive campaigns.
- No numeric balance, formula, scenario, or actor-behavior changes should be
  made from this batch alone.

## Prioritized Follow-Up

1. Add one deliberately naive or free-form agent profile to test whether command
   hints, observations, and debriefs are usable without pre-authored policies.
2. Keep broader strategy-space diagnostics as analysis artifacts until repeated
   findings show a need for dedicated tooling.
3. If competitive stochastic sensitivity remains important, design a focused
   test around inputs or months where seeded events are expected to matter,
   rather than tuning formulas from this matrix.
