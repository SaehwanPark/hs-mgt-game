# AI-Agent Playtest Diagnostics v0.1.56

- **Status:** Phase 7 strategy-space diagnostics artifact
- **Date:** 2026-07-02
- **Code version:** 0.1.56
- **Harness:** Existing MCP stdio evidence from prior scripted and free-form
  findings
- **Evidence base:** v0.1.51, v0.1.52, v0.1.54, and v0.1.55 findings

These diagnostics summarize already-captured simulated-agent evidence. They do
not add a new playtest matrix, runtime automation, gameplay formula change,
human-learning evidence, empirical calibration, equilibrium analysis, or policy
forecast.

## Evidence Base

| Source | Campaigns | Seeds | Profiles | Sessions used |
| --- | --- | --- | --- | ---: |
| v0.1.51 scripted seed variation | Stabilization and competitive preview | 42, 43, 44 | Fiscal Caution, Capacity Growth, Balanced Strategy | 18 |
| v0.1.52 scripted naive profile | Stabilization and competitive preview | 42, 43, 44 | Above plus Naive First-Time | 24 |
| v0.1.54 free-form profile | Stabilization and competitive preview | 42 | Free-Form First-Time Executive | 2 |
| v0.1.55 free-form synthesis | Stabilization and competitive preview | 42 | Fiscal Steward, Access Expansion Advocate | 4 |

The v0.1.52 scripted batch subsumes the v0.1.51 scripted profiles for aggregate
counts, but v0.1.51 remains relevant for the first seed-variation
interpretation. All cited sessions completed with zero validation failures.

## Strategy Clusters

### Stabilization

| Cluster | Representative profiles | Typical command pattern | Observed outcome pattern |
| --- | --- | --- | --- |
| Fiscal caution | Fiscal Caution, Fiscal Steward | Modest capacity, low advocacy, low shared commitments, conservative defensive spend | Strong cash preservation with access gains in the low-to-mid 70s |
| Access/capacity growth | Capacity Growth, Access Expansion Advocate | High initial bed/capital spend, high advocacy, retention, coalition, and defensive commitments | Strong access and community-trust gains with steep cash drawdown |
| Balanced access | Balanced Strategy, Free-Form First-Time Executive | Moderate capacity, policy, workforce, coalition, and defensive choices | Access in the mid-to-high 80s while preserving more cash than growth paths |
| Naive low-complexity | Naive First-Time | Legal but repeated moderate/low commitments | Highest cash, weakest community trust, and lowest stabilization access among tested profiles |

### Competitive Preview

| Cluster | Representative profiles | Typical command pattern | Observed outcome pattern |
| --- | --- | --- | --- |
| Passive/fiscal | Naive First-Time, Fiscal Steward | Monitor or hold early, small access pledge, conservative or delayed negotiation | Cash stays high; access remains near 70; beds stay at or below 120 |
| Scripted fiscal caution | Fiscal Caution | Low-risk actions with more activity than naive play | Cash remains strong with modest capacity and access movement |
| Capacity/access growth | Capacity Growth, Access Expansion Advocate | Bed investment, nurse recruitment, access pledge, neutral payer posture | Highest beds and access, lowest cash, and visible workforce-trust cost |
| Balanced/free-form | Balanced Strategy, Free-Form First-Time Executive | Monitoring plus selective recruitment, beds, access pledge, and neutral negotiation | Middle cash, access, beds, and workforce outcomes |

## Outcome Ranges

### Stabilization Metrics

| Evidence set | Cash | Access | Workforce trust | Community trust |
| --- | --- | --- | --- | --- |
| Scripted v0.1.52 matrix | 15-70 | 73-93 | 64-68 | 57-75 |
| Free-form seed-42 profiles | 30-68 | 75-90 | 64-67 | 66-73 |
| Combined diagnostic range | 15-70 | 73-93 | 64-68 | 57-75 |

The combined stabilization range is profile-driven. Seeds 42, 43, and 44 moved
reported access by at most three points and community trust by at most four
points in the scripted matrix, while strategic posture explains the larger cash
and access spread.

### Competitive Preview Metrics

| Evidence set | Cash | Access | Beds | Workforce trust | Community trust | Political capital | Market share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Scripted v0.1.52 matrix | 5-60 | 70-73 | 118-129 | 54-60 | 64-66 | 11-13 | Not captured |
| Free-form seed-42 profiles | 10-60 | 70-76 | 118-126 | 56-60 | 65-67 | 11 | 25-26 |
| Combined diagnostic range | 5-60 | 70-76 | 118-129 | 54-60 | 64-67 | 11-13 | 25-26 where captured |

The competitive preview shows larger cash and capacity separation than access
separation. Active capacity strategies buy beds and access but consume cash and
strain workforce trust. Passive strategies are legal and legible but underuse
commitments, negotiations, projects, and capacity tools.

## Action Frequency Signals

For the competitive seed-42 profiles with explicit command logs:

| Verb | Scripted naive | Free-form first-time | Free-form fiscal steward | Free-form access advocate | Diagnostic note |
| --- | ---: | ---: | ---: | ---: | --- |
| `hold` | 3 | 1 | 3 | 0 | Heavy hold use correlates with cash preservation and limited access movement. |
| `monitor` | 1 | 1 | 1 | 1 | Monitoring is consistently understandable and useful for Northlake observability. |
| `invest` | 0 | 1 | 0 | 2 | Investment separates access/capacity strategies from passive strategies. |
| `recruit` | 0 | 1 | 0 | 1 | Recruitment is used by active strategies and carries workforce timing costs. |
| `commit` | 1 | 1 | 1 | 1 | Access pledges are used across profiles, but level varies meaningfully. |
| `negotiate` | 0 | 1 | 1 | 1 | Free-form profiles understood payer renewal context better than naive play. |
| `project` | 0 | 0 | 0 | 0 | No tested profile used projects in the three-month preview. |

This is a diagnostic sample, not a full strategy-space census. It does flag two
likely next review targets: project guidance is untested, and passive first-time
competitive play may need clearer monthly report cues before any balance change.

## Gameplay Validity Hypotheses

- **Multiple strategies can complete both current slices:** Pass for the current
  simulated-agent evidence. Scripted and free-form profiles all completed
  without validation failures.
- **No single first-month command dominates:** Partial pass. Distinct profiles
  produce real cash, access, bed, workforce, and trust tradeoffs, and naive
  cash preservation is not dominant. The tested matrix remains too small for a
  dominance claim.
- **First-time simulated players can use the current command surface:** Pass for
  bounded free-form seed-42 profiles and partial pass for the scripted naive
  profile. This is not human usability evidence.
- **Rival behavior is recognizable but imperfectly predictable:** Partial pass.
  Monitoring reveals Northlake activity, while Summit private activity remains
  hidden. The scripted seed matrix did not vary competitive outcomes.
- **Debrief and history support causal explanation:** Pass for the free-form
  profiles. Scripted profiles support metric comparison but do not include
  agent-authored explanations.

## Follow-Up Routing

| Finding | Route | Rationale |
| --- | --- | --- |
| Passive competitive profiles preserve cash but underuse tools | Guidance hardening | Review monthly report guidance and command help before changing formulas. |
| No profile used `project` in the three-month preview | Debrief or guidance review | The command may be a poor fit for a short preview or insufficiently cued. |
| Competitive access range remains narrow relative to cash/beds | Future diagnostics | More seeds, profiles, or longer campaign evidence should precede tuning. |
| Free-form profiles can explain outcomes from history/debrief | Debrief quality | Preserve committed-history causal explanation as a product surface. |
| Scripted seeds did not affect competitive outcomes | Evidence/parameters | Investigate only if stochastic sensitivity becomes an explicit design target. |

## Evidence Limits

- The evidence is simulated-agent evidence, not human playtesting.
- The free-form evidence is seed 42 only.
- The scripted competitive seed matrix produced identical outcomes across seeds
  42, 43, and 44 for each profile.
- Market share is captured only in v0.1.55 free-form competitive evidence.
- No runtime formula, scenario, command-surface, MCP DTO, replay, or golden-hash
  change should be made from this diagnostic artifact alone.

## Prioritized Recommendation

The next implementation slice should be a bounded competitive guidance or
debrief-quality review if future work needs code changes. Keep strategy-space
diagnostics as lightweight analysis artifacts until repeated playtest findings
name a specific automation need.
