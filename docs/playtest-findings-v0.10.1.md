# AI-Agent Free-Form Hard Seed-Variation Synthesis v0.10.1

- **Status:** Phase 7 free-form Hard competitive seed-variation diagnostics
- **Date:** 2026-07-06
- **Code version:** 0.10.1
- **Harness:** Local MCP stdio client via operator capture script
  `_workspace/experiments/v0.10.1-free-form-hard-seed-variation/run_sessions.py`
- **Campaign:** `competitive-regional-v1`
- **Seeds:** `42`, `43`, `44`
- **Difficulty:** `hard`
- **Agent profiles:** Free-Form Fiscal Steward; Free-Form Access Expansion
  Advocate; Free-Form First-Time Executive

These findings are free-form **simulated-agent** evidence only. Each profile used
the same deterministic observation-heuristic policies as v0.10.0. The policies
read actor-visible observations, MCP legal-command hints, and player-facing docs.
They do not measure human learning, classroom effectiveness, empirical
calibration, real-world policy validity, numerical balance, or equilibrium
behavior.

## Run Matrix

| Campaign | Seeds | Difficulty | Profiles | Completed sessions | Validation failures |
| --- | --- | --- | ---: | ---: | ---: |
| `competitive-regional-v1` | 42, 43, 44 | hard | 3 | 9 | 0 |

All nine sessions completed the full 24-month campaign without crashes, hangs,
incomplete sessions, or command validation failures.

## Competitive Outcomes by Profile and Seed

| Profile | Seed | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Final hash |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Free-Form Fiscal Steward | 42 | 60 | 84 | 118 | 60 | 72 | 15 | `9326f6e68777e594` |
| Free-Form Fiscal Steward | 43 | 60 | 84 | 118 | 60 | 72 | 15 | `2fcc8c0c223767da` |
| Free-Form Fiscal Steward | 44 | 60 | 84 | 118 | 60 | 72 | 15 | `7b4f7f3e66aca44d` |
| Free-Form Access Expansion Advocate | 42 | 38 | 100 | 120 | 58 | 100 | 15 | `f2484911a8e2a0de` |
| Free-Form Access Expansion Advocate | 43 | 38 | 100 | 120 | 58 | 100 | 15 | `a323b34216859fac` |
| Free-Form Access Expansion Advocate | 44 | 38 | 100 | 120 | 58 | 100 | 15 | `a323b34216859fac` |
| Free-Form First-Time Executive | 42 | 40 | 100 | 120 | 58 | 87 | 15 | `3199a483b748173d` |
| Free-Form First-Time Executive | 43 | 40 | 100 | 120 | 58 | 87 | 15 | `e818d72430a4eed7` |
| Free-Form First-Time Executive | 44 | 40 | 100 | 120 | 58 | 87 | 15 | `e818d72430a4eed7` |

Seed 42 reproduces the v0.10.0 endpoint metrics and hashes for all three
profiles. Across seeds 42, 43, and 44, final tradeoff metrics are stable by
profile while some final hashes differ, reflecting deterministic seed-specific
transition histories that can converge on the same reported endpoint metrics.

## Outcome Ranges Across Seeds

| Profile | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | Distinct hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Free-Form Fiscal Steward | 3 | 60 | 84 | 118 | 60 | 72 | 3 |
| Free-Form Access Expansion Advocate | 3 | 38 | 100 | 120 | 58 | 100 | 2 |
| Free-Form First-Time Executive | 3 | 40 | 100 | 120 | 58 | 87 | 2 |

The seed-variation batch supports a narrow claim: these three deterministic
free-form Hard policies complete across seeds 42-44 without validation failures
and preserve profile-distinct endpoint metrics in this seed set. It does not
support formula tuning or broader balance conclusions.

## Action-Frequency Signals

| Profile | Sessions | Holds | Invest | Recruit | Monitor | Negotiate | Commit |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Free-Form Fiscal Steward | 3 | 72 | 0 | 0 | 3 | 12 | 24 |
| Free-Form Access Expansion Advocate | 3 | 69 | 3 | 3 | 0 | 0 | 69 |
| Free-Form First-Time Executive | 3 | 66 | 3 | 3 | 3 | 0 | 69 |

Command frequencies were identical by profile across the three seeds. The
Access Expansion Advocate and First-Time Executive continue to exhibit repetitive
access-commitment loops once scrutiny cues persist. That remains a comprehension
and guidance diagnostic, not proof of optimal play.

## Gameplay Validity Hypotheses

- **Free-form Hard policies complete across seeds 42-44:** Pass. All nine
  sessions completed 24 months with zero validation failures.
- **Seed 42 reproduces v0.10.0:** Pass. All three seed-42 hashes and endpoint
  metrics match the v0.10.0 findings.
- **Endpoint metrics remain profile-distinct beyond seed 42:** Pass within this
  limited seed set. Fiscal Steward, Access Expansion Advocate, and First-Time
  Executive preserve distinct cash/access/community-trust endpoints across all
  three seeds.
- **Seed variation produces broad strategy-distribution evidence:** Partial
  pass. The artifact covers three seeds, but only three deterministic heuristic
  profiles at one difficulty tier and one campaign.
- **The batch supports balance tuning:** Fail. This is validation and strategy
  diversity evidence, not calibration or balance evidence.

## Evidence Limits

- Operator policies are deterministic observation heuristics, not LLM or human
  play.
- Only three seeds were exercised.
- The profile policies were intentionally unchanged from v0.10.0; this artifact
  does not test alternative free-form heuristics or prompt variants.
- Access-heavy profiles repeat commitments under persistent scrutiny cues.
- Batch diagnostics use MCP transition summaries and debriefs, not full replay
  artifacts.
- These findings do not support formula tuning, empirical calibration, human
  learning claims, or policy-validity claims.

## Prioritized Follow-Up

1. Treat free-form Hard completion across seeds 42-44 as sufficient for the
   current validation question; do not expand seed count until a new hypothesis
   requires it.
2. Test scrutiny-threshold or commitment-cooldown heuristics in a separate
   future slice if repetitive pledge loops should be evaluated as a
   comprehension risk.
3. Keep free-form Hard artifacts separate from scripted `--target
   difficulty-adaptive` batches; compare findings rather than merging targets.
4. Do not change balance or runtime mechanics from this artifact alone.
