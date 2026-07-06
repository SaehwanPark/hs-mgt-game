# AI-Agent Difficulty-Adaptive Playtest Synthesis v0.9.9

- **Status:** Phase 7 targeted difficulty-adaptive diagnostics slice
- **Date:** 2026-07-06
- **Code version:** 0.9.9
- **Harness:** `python3 scripts/run_automated_playtests.py --target difficulty-adaptive --json-output ...`
  followed by `python3 scripts/diagnose_runs.py ...`
- **Campaigns:** `stabilization-v1`, `competitive-regional-v1`
- **Seeds:** `42`, `43`, `44`
- **Competitive difficulties:** `easy`, `hard`
- **Agent profiles:** Fiscal Caution, Capacity Growth, Balanced Strategy,
  Naive First-Time

These diagnostics summarize simulated-agent evidence only. They do not measure
human learning, classroom effectiveness, empirical calibration, real-world
policy validity, numerical balance, or equilibrium behavior.

## Run Matrix

| Campaign | Seeds | Profiles | Difficulties | Completed sessions | Validation failures |
| --- | --- | ---: | --- | ---: | ---: |
| `stabilization-v1` | 42, 43, 44 | 4 | n/a | 12 | 0 |
| `competitive-regional-v1` | 42, 43, 44 | 4 | easy, hard | 24 | 0 |

The targeted batch completed without crashes, hangs, incomplete sessions, or
command validation failures. Stabilization sessions are unchanged from prior
baselines. Competitive sessions use rival-aware policy adjustments on Hard
difficulty only; Easy passes through the base scripted month tables.

## Competitive Outcomes by Difficulty

| Difficulty | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Representative hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Easy | 12 | 1-20 | 73-75 | 118-121 | 34-58 | 66-67 | 15 | `88d40bbfabf028ad`, `5d86f296694e3170`, `905fe9285a486d82` |
| Hard | 12 | 7-20 | 72-75 | 118-119 | 55-58 | 66-67 | 15 | `df92b5b32a0a2807`, `d05da6103e01bf16`, `45121e08c2a05017` |

Hard adaptive policies shift pooled competitive endpoints: minimum cash rises
from `1` to `7`, access floor drops from `73` to `72`, and workforce-trust floor
rises from `34` to `55`. Beds ceiling drops from `121` to `119`.

## Competitive Profile Outcomes by Difficulty

| Profile | Difficulty | Cash | Access | Beds | Workforce Trust |
| --- | --- | ---: | ---: | ---: | ---: |
| Fiscal Caution | easy | 5 | 75 | 118 | 57 |
| Fiscal Caution | hard | 7 | 75 | 118 | 57 |
| Capacity Growth | easy | 9 | 73 | 121 | 34 |
| Capacity Growth | hard | 20 | 72 | 119 | 58 |
| Balanced Strategy | easy | 1 | 75 | 121 | 48 |
| Balanced Strategy | hard | 12 | 74 | 119 | 55 |
| Naive First-Time | easy | 20 | 75 | 118 | 58 |
| Naive First-Time | hard | 20 | 75 | 118 | 58 |

Capacity Growth and Balanced Strategy now produce materially different Easy/Hard
endpoints for the same seed. Naive First-Time remains unchanged because the
profile is already hold-heavy and triggers fewer adaptation rules.

## Adaptive Action Signals

| Difficulty | Holds | Action commands | Monitor | Invest | Recruit | Commit |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Easy | 273 | 246 | 84 | 48 | 21 | 63 |
| Hard | 279 | 309 | 147 | 48 | 21 | 63 |

Hard runs add more holds and monitor commands while preserving invest/recruit/commit
totals in this pooled batch. The adaptation layer is working as a rival-pressure
response without changing Rust simulation code.

## Stabilization Outcome Ranges

| Metric | Range |
| --- | ---: |
| Cash | 15-70 |
| Access | 73-93 |
| Workforce trust | 64-68 |
| Community trust | 57-75 |
| Policy pressure | 35-59 |

Stabilization policies were not changed in this slice.

## Gameplay Validity Hypotheses

- **Scripted agents can complete competitive runs at Easy and Hard through MCP:**
  Pass. All 24 competitive sessions completed with zero validation failures.
- **The harness records difficulty in batch artifacts and diagnostics:** Pass.
- **Difficulty variation changes committed competitive state:** Pass. Easy and
  Hard runs for the same seed/profile produce different final hashes because rival
  composition differs by tier and hard adaptation can change player commands.
- **Difficulty-adaptive policies differentiate scripted player tradeoff metrics:**
  Partial pass. Capacity Growth and Balanced Strategy now diverge across tiers;
  Fiscal Caution shifts slightly; Naive First-Time is unchanged.
- **The batch supports balance tuning:** Fail. This evidence is about validation
  coverage and adaptation behavior, not formula calibration.

## Evidence Limits

- Batch diagnostics use MCP transition summaries and debriefs, not full replay
  artifacts.
- Adaptation rules are deterministic heuristics over observation text, not
  LLM or best-response play.
- Identical Naive First-Time endpoints do not prove difficulty is ineffective;
  they show hold-heavy static policies can bypass the adaptation layer.
- These findings do not support formula tuning, empirical calibration, human
  learning claims, or policy-validity claims.

## Prioritized Follow-Up

1. Keep `--target difficulty-adaptive` as a focused diagnostic target separate
   from the static `difficulty-sweep` baseline.
2. Use free-form agent profiles at Hard difficulty when testing whether human-like
   adaptation produces broader strategy diversity than scripted heuristics.
3. Do not change balance or runtime mechanics from this artifact alone.
