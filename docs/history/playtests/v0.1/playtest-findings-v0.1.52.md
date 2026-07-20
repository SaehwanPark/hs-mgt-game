# AI-Agent Playtest Findings v0.1.52

- **Status:** Phase 7 naive-profile scripted-agent evidence
- **Date:** 2026-07-01
- **Code version:** 0.1.52
- **Harness:** `python3 scripts/run_automated_playtests.py` over local MCP stdio

These findings are deterministic scripted-agent evidence only. The new
`Naive First-Time` profile is a deliberately simple policy used to probe command
hint and observation usability beyond the three optimized scripted profiles. It
does not measure human learning, classroom engagement, empirical calibration, or
real-world policy validity.

## Session Batch

| Campaign | Seeds | Difficulty | Profiles | Completed sessions |
| --- | --- | --- | --- | ---: |
| `stabilization-v1` | 42, 43, 44 | n/a | Fiscal Caution, Capacity Growth, Balanced Strategy, Naive First-Time | 12 |
| `competitive-regional-v1` | 42, 43, 44 | normal | Fiscal Caution, Capacity Growth, Balanced Strategy, Naive First-Time | 12 |

All 24 scripted sessions completed without validation failures. Competitive
outcome metrics use the v0.1.50 end-session debrief surface derived from
committed history.

## Naive Profile Commands

The naive profile intentionally uses legal, low-complexity commands instead of
an optimized policy.

| Campaign | Turn or month | Command |
| --- | ---: | --- |
| `stabilization-v1` | 1 | `6 10 108` |
| `stabilization-v1` | 2 | `5 4` |
| `stabilization-v1` | 3 | `5 4` |
| `stabilization-v1` | 4 | `5 4` |
| `stabilization-v1` | 5 | `5 4` |
| `competitive-regional-v1` | 1 | `monitor target=northlake depth=1; hold` |
| `competitive-regional-v1` | 2 | `hold` |
| `competitive-regional-v1` | 3 | `commit pledge_type=access level=1; hold` |

## Run Matrix

### Stabilization

| Seed | Profile | Final cash | Final access | Workforce trust | Community trust |
| ---: | --- | ---: | ---: | ---: | ---: |
| 42 | Fiscal Caution | 64 | 75 | 64 | 69 |
| 42 | Capacity Growth | 15 | 92 | 67 | 73 |
| 42 | Balanced Strategy | 32 | 89 | 68 | 73 |
| 42 | Naive First-Time | 70 | 73 | 64 | 57 |
| 43 | Fiscal Caution | 64 | 76 | 64 | 69 |
| 43 | Capacity Growth | 15 | 93 | 67 | 75 |
| 43 | Balanced Strategy | 32 | 90 | 68 | 75 |
| 43 | Naive First-Time | 70 | 74 | 64 | 59 |
| 44 | Fiscal Caution | 64 | 75 | 64 | 69 |
| 44 | Capacity Growth | 15 | 92 | 67 | 75 |
| 44 | Balanced Strategy | 32 | 89 | 68 | 75 |
| 44 | Naive First-Time | 70 | 76 | 64 | 61 |

The naive stabilization profile preserved the most cash but produced the lowest
reported access and community trust among tested profiles. That is useful
first-time-use evidence: legal low-intensity commands can complete the slice,
but they do not automatically preserve legitimacy or access outcomes.

### Competitive Preview

| Seed | Profile | Final hash | Cash | Access | Beds | Workforce trust | Community trust | PC |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 42 | Fiscal Caution | `3c0634b870c2d0cd` | 50 | 70 | 120 | 58 | 65 | 13 |
| 42 | Capacity Growth | `0051c77b4d9e31c1` | 5 | 70 | 129 | 54 | 64 | 12 |
| 42 | Balanced Strategy | `640c6c7654595008` | 25 | 73 | 125 | 56 | 66 | 11 |
| 42 | Naive First-Time | `c209a5f7df432711` | 60 | 70 | 118 | 60 | 65 | 13 |
| 43 | Fiscal Caution | `3c0634b870c2d0cd` | 50 | 70 | 120 | 58 | 65 | 13 |
| 43 | Capacity Growth | `0051c77b4d9e31c1` | 5 | 70 | 129 | 54 | 64 | 12 |
| 43 | Balanced Strategy | `640c6c7654595008` | 25 | 73 | 125 | 56 | 66 | 11 |
| 43 | Naive First-Time | `c209a5f7df432711` | 60 | 70 | 118 | 60 | 65 | 13 |
| 44 | Fiscal Caution | `3c0634b870c2d0cd` | 50 | 70 | 120 | 58 | 65 | 13 |
| 44 | Capacity Growth | `0051c77b4d9e31c1` | 5 | 70 | 129 | 54 | 64 | 12 |
| 44 | Balanced Strategy | `640c6c7654595008` | 25 | 73 | 125 | 56 | 66 | 11 |
| 44 | Naive First-Time | `c209a5f7df432711` | 60 | 70 | 118 | 60 | 65 | 13 |

The naive competitive profile completed all three months but mostly conserved
resources and avoided strategic commitments. It did not improve access, beds, or
community trust relative to the more purposeful profiles.

## Diagnostic Summary

| Campaign | Sessions | Cash range | Access range | Workforce range | Community range | Notes |
| --- | ---: | --- | --- | --- | --- | --- |
| Stabilization | 12 | 15-70 | 73-93 | 64-68 | 57-75 | Naive commands complete but expose weaker community-trust outcomes. |
| Competitive preview | 12 | 5-60 | 70-73 | 54-60 | 64-66 | Naive play preserves resources but underuses the competitive action space. |

Competitive resource ranges were staffed beds `118-129` and political capital
`11-13`, driven by profile choice. Competitive final hashes remained identical
per profile across seeds 42, 43, and 44.

## Gameplay Validity Hypotheses

- **Multiple strategies can complete the current slice:** Pass for this matrix.
  All 24 sessions completed without collapse or validation failure.
- **No single first-month command dominates across required profiles and
  plausible seeds:** Partial pass. Profiles produce distinct tradeoffs, and the
  naive profile is not dominant despite strong cash preservation.
- **Agents can explain the main cause of an outcome from debrief and history:**
  Not tested. This deterministic batch did not include agent-authored
  explanations.
- **Rival behavior is recognizable but imperfectly predictable:** Not tested
  beyond committed history summaries. The tested competitive profiles did not
  vary across seeds.
- **A first-time simulated player can complete a month using actor-visible
  information and command hints:** Partial pass. The naive policy completed
  using the current legal command surface, but it is still scripted rather than
  free-form.

## Rubric Scores

| Dimension | Score | Evidence note |
| --- | ---: | --- |
| Command comprehension | 4 | Four scripted profiles completed both campaigns with zero validation failures. |
| Strategic tension | 4 | Naive play adds a high-cash, lower-benefit path that does not dominate growth or balanced strategies. |
| Causal transparency | 3 | Debriefs support metric comparison, but agent-authored causal explanations remain untested. |
| Pacing proxy | 4 | The 24-session MCP batch completed quickly without stalls. |
| Action overload proxy | 3 | Naive play suggests low-complexity legal completion is possible, but free-form command selection remains untested. |
| Debrief coherence | 4 | Final debrief metrics make naive versus purposeful outcomes comparable. |
| Exploit discovery | 2 | No collapse or obvious exploit appeared; deterministic scripted profiles are insufficient for dominance claims. |

## Evidence Limits

- The naive profile is a deterministic scripted policy, not a free-form LLM or
  human player.
- The profile tests legal command completion and coarse outcome contrast; it
  does not prove command wording is sufficient for first-time human players.
- Seeds 42, 43, and 44 remain a small sensitivity sample.
- No numeric balance, formula, scenario, actor-behavior, or command-surface
  changes should be made from this batch alone.

## Prioritized Follow-Up

1. Run one free-form agent profile that must choose commands from observations,
   legal-command hints, and player-facing docs, then capture validation retries
   and debrief explanations.
2. Keep broader strategy-space diagnostics as analysis artifacts until repeated
   scripted or free-form findings show a concrete tooling need.
3. If naive competitive play remains too passive in free-form runs, evaluate
   command help and monthly report guidance before considering balance changes.
