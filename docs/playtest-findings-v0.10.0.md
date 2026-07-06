# AI-Agent Free-Form Hard Competitive Playtest Synthesis v0.10.0

- **Status:** Phase 7 free-form Hard competitive diagnostics slice
- **Date:** 2026-07-06
- **Code version:** 0.10.0
- **Harness:** Local MCP stdio client via operator capture script
  `_workspace/experiments/v0.10.0-free-form-hard/run_sessions.py`
- **Campaign:** `competitive-regional-v1`
- **Seed:** `42`
- **Difficulty:** `hard`
- **Agent profiles:** Free-Form Fiscal Steward; Free-Form Access Expansion
  Advocate; Free-Form First-Time Executive

These findings are free-form **simulated-agent** evidence only. Each profile used
deterministic observation-heuristic policies (not LLM or human play) that read
actor-visible observations, MCP legal-command hints, and player-facing docs.
They do not measure human learning, classroom effectiveness,
empirical calibration, real-world policy validity, numerical balance, or
equilibrium behavior.

## Run Matrix

| Campaign | Seed | Difficulty | Profiles | Completed sessions | Validation failures |
| --- | ---: | --- | --- | ---: | ---: |
| `competitive-regional-v1` | 42 | hard | 3 | 3 | 0 |

All three sessions completed the full 24-month campaign without crashes, hangs,
incomplete sessions, or command validation failures.

## Profile Prompts

- **Free-Form Fiscal Steward:** Protect cash runway, favor low-risk moves,
  monitor rivals before committing, and use modest access commitments when
  legitimacy is at stake.
- **Free-Form Access Expansion Advocate:** Prioritize access, staffed capacity,
  and public legitimacy while preserving enough cash to finish the 24-month
  campaign at Hard difficulty.
- **Free-Form First-Time Executive:** Read only the current observation, legal
  command hints, and player-facing docs. Preserve cash flexibility but act on
  visible access, workforce, policy, and market pressure.

## Competitive Outcomes (Free-Form Hard, Seed 42)

| Profile | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Final hash |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Free-Form Fiscal Steward | 60 | 84 | 118 | 60 | 72 | 15 | `9326f6e68777e594` |
| Free-Form Access Expansion Advocate | 38 | 100 | 120 | 58 | 100 | 15 | `f2484911a8e2a0de` |
| Free-Form First-Time Executive | 40 | 100 | 120 | 58 | 87 | 15 | `3199a483b748173d` |

## Comparison vs v0.9.9 Difficulty-Adaptive Scripted Hard (Seed 42)

Seed 42 only; profile pairings below are thematic analogues, not matched-policy
baselines.

| Profile / baseline | Cash | Access | Beds | Workforce Trust | Community Trust | Final hash |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Free-Form Fiscal Steward | 60 | 84 | 118 | 60 | 72 | `9326f6e68777e594` |
| Scripted Fiscal Caution (adaptive Hard) | 7 | 75 | 118 | 57 | 66 | `df92b5b32a0a2807` |
| Free-Form Access Expansion Advocate | 38 | 100 | 120 | 58 | 100 | `f2484911a8e2a0de` |
| Scripted Capacity Growth (adaptive Hard) | 18 | 72 | 119 | 58 | 66 | `6e735edc9552c773` |
| Free-Form First-Time Executive | 40 | 100 | 120 | 58 | 87 | `3199a483b748173d` |
| Scripted Balanced Strategy (adaptive Hard) | 10 | 74 | 119 | 55 | 67 | `fa89fd6d8acf11f5` |
| Scripted Naive First-Time (adaptive Hard) | 20 | 75 | 118 | 58 | 66 | `ff9b08b306d4bf17` |

Free-form observation-driven play produces materially different endpoints than
the v0.9.9 adaptive scripted baselines on the same seed and difficulty tier.
Cash endpoints span 38–60 (free-form) versus 7–20 (scripted Hard). Access
endpoints reach 84–100 (free-form) versus 72–75 (scripted Hard). Community
trust reaches 72–100 (free-form) versus 66–67 (scripted Hard). All profiles
produce distinct final hashes.

## Submitted Commands (Selected Months)

### Free-Form Fiscal Steward

| Month | Command |
| ---: | --- |
| 1 | `monitor target=northlake depth=1; hold` |
| 2 | `negotiate payer=carrier_a rate_posture=conservative; hold` |
| 3 | `commit pledge_type=access level=1; hold` |
| 6 | `commit pledge_type=access level=1; hold` |
| 12 | `commit pledge_type=access level=1; hold` |
| 18 | `commit pledge_type=access level=1; hold` |
| 24 | `commit pledge_type=access level=1; hold` |

Fiscal Steward also committed on months 9, 15, and 21 (eight access commits total).

Causal path: early rival monitoring and conservative payer negotiation preserved
cash (60 final). Recurring modest access commitments under state scrutiny
raised access to 84 and community trust to 72 without capacity expansion.

### Free-Form Access Expansion Advocate

| Month | Command |
| ---: | --- |
| 1 | `invest domain=beds amount=12; recruit role=nurse headcount=2` |
| 2–24 | `commit pledge_type=access level=2; hold` (months 2–24) |

Causal path: early beds investment and nurse recruitment raised staffed capacity
to 120. Repeated access commitments under ongoing scrutiny reporting drove
access and community trust to 100, with cash falling to 38. The observation
loop favored continued access pledges once scrutiny cues persisted.

### Free-Form First-Time Executive

| Month | Command |
| ---: | --- |
| 1 | `recruit role=nurse headcount=2; monitor target=northlake depth=1` |
| 2 | `invest domain=beds amount=10; commit pledge_type=access level=1` |
| 3–24 | `commit pledge_type=access level=1; hold` (months 3–24) |

Causal path: early recruitment and bed investment established capacity (120
beds). Sustained level-1 access commitments under policy scrutiny raised access
to 100 and community trust to 87 while preserving more cash (40) than the
Access Expansion Advocate.

## Action-Frequency Signals

| Profile | Holds | Invest | Recruit | Monitor | Negotiate | Commit |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Fiscal Steward | 24 | 0 | 0 | 1 | 4 | 8 |
| Access Expansion Advocate | 23 | 1 | 1 | 0 | 0 | 23 |
| First-Time Executive | 22 | 1 | 1 | 1 | 0 | 23 |

Free-form profiles use commitment commands far more heavily than the v0.9.9
adaptive scripted batch (63 total commit commands across 12 Hard sessions:
four profiles × three seeds). Observation-driven access-scrutiny responses
differentiate outcomes beyond scripted month tables.

## Gameplay Validity Hypotheses

- **Free-form agents can complete the full 24-month Hard competitive campaign
  through MCP:** Pass. All three sessions completed with zero validation
  failures.
- **Observation-driven play produces different committed state than adaptive
  scripted Hard baselines:** Pass. All three free-form hashes differ from each
  other and from all four v0.9.9 adaptive Hard seed-42 hashes.
- **Free-form play differentiates strategy endpoints beyond scripted adaptive
  policies:** Partial pass (seed 42 only). Cash, access, and community-trust
  ranges exceed scripted Hard pooled ranges on this seed; Access Expansion
  Advocate and First-Time Executive reach access 100 versus scripted ceiling 75.
  Seed generalization is not tested in this slice.
- **Free-form play differs from the scripted Naive First-Time adaptive profile:**
  Partial pass. The First-Time Executive heuristic differs from scripted Naive
  endpoints and action mix on seed 42; it does not validate human first-time
  comprehension.
- **The batch supports balance tuning:** Fail. This evidence is about validation
  coverage and strategy diversity, not formula calibration.

## Evidence Limits

- Operator capture uses deterministic observation-heuristic policies, not an
  LLM or human player. The policies embody persona intent but are not open-ended
  reasoning.
- Only seed 42 was exercised; seed variation is not captured in this slice.
- Access Expansion Advocate and First-Time Executive entered repetitive
  commitment loops once scrutiny cues persisted. That pattern is diagnostically
  useful but does not prove optimal play.
- Batch diagnostics use MCP transition summaries and debriefs, not full replay
  artifacts.
- These findings do not support formula tuning, empirical calibration, human
  learning claims, or policy-validity claims.

## Prioritized Follow-Up

1. Extend free-form Hard evidence to seeds 43 and 44 before drawing
   strategy-diversity conclusions beyond seed 42.
2. Add scrutiny-threshold or commitment-cooldown heuristics in future free-form
   runs if repetitive pledge loops should be tested as a comprehension risk.
3. Keep free-form Hard runs separate from scripted `--target difficulty-adaptive`
   batches; compare artifacts rather than merging targets.
4. Do not change balance or runtime mechanics from this artifact alone.
