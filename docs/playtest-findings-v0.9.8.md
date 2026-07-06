# AI-Agent Difficulty-Tier Playtest Synthesis v0.9.8

- **Status:** Phase 7 targeted difficulty-tier diagnostics slice
- **Date:** 2026-07-06
- **Code version:** 0.9.8
- **Harness:** `python3 scripts/run_automated_playtests.py --target difficulty-sweep --json-output ...`
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
command validation failures. Stabilization sessions are unchanged from the
default baseline. Competitive sessions exercise the protocol-required difficulty
variation while preserving the v0.9.6 scripted command paths.

## Competitive Outcomes by Difficulty

| Difficulty | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Representative hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Easy | 12 | 1-20 | 73-75 | 118-121 | 34-58 | 66-67 | 15 | `88d40bbfabf028ad`, `5d86f296694e3170`, `905fe9285a486d82` |
| Hard | 12 | 1-20 | 73-75 | 118-121 | 34-58 | 66-67 | 15 | `8a86dd27fdbddcc5`, `89521249dead95f1`, `96d17f648d3e550f` |

Difficulty changes rival composition (`easy` = 1 rival, `hard` = 3 rivals) and
therefore changes committed state hashes, but the fixed scripted profiles
produce identical final player tradeoff metrics for the same seed and profile
across Easy and Hard. This is expected for deterministic player commands that do
not adapt to rival count or CPU pressure.

## Competitive Profile Outcomes (Pooled Across Difficulties)

| Profile | Sessions | Cash | Access | Beds | Workforce Trust | Community Trust | PC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Fiscal Caution | 6 | 5 | 75 | 118 | 57 | 66 | 15 |
| Capacity Growth | 6 | 9 | 73 | 121 | 34 | 66 | 15 |
| Balanced Strategy | 6 | 1 | 75 | 121 | 48 | 67 | 15 |
| Naive First-Time | 6 | 20 | 75 | 118 | 58 | 66 | 15 |

Profile ordering matches the v0.9.6 Normal-difficulty baseline: Capacity Growth
still produces the lowest workforce trust, while Naive First-Time preserves the
most cash.

## Stabilization Outcome Ranges

| Metric | Range |
| --- | ---: |
| Cash | 15-70 |
| Access | 73-93 |
| Workforce trust | 64-68 |
| Community trust | 57-75 |
| Policy pressure | 35-59 |

Stabilization policies were not changed in this slice. Their outcome ranges
remain consistent with the v0.9.6 baseline.

## Gameplay Validity Hypotheses

- **Scripted agents can complete competitive runs at Easy and Hard through MCP:**
  Pass. All 24 competitive sessions completed with zero validation failures.
- **The harness records difficulty in batch artifacts and diagnostics:** Pass.
  JSON artifacts include a `difficulties` field and per-session `difficulty`
  metadata; diagnostics report outcomes grouped by difficulty.
- **Difficulty variation changes committed competitive state:** Pass. Easy and
  Hard runs for the same seed/profile produce different final hashes.
- **Difficulty variation changes scripted player tradeoff metrics in this batch:**
  Fail for this evidence set. Fixed policies produce identical player cash,
  access, beds, trust, and political-capital endpoints for the same seed/profile
  across Easy and Hard.
- **The batch supports balance tuning:** Fail. This evidence is about validation
  coverage and difficulty recording, not formula calibration.

## Evidence Limits

- Batch diagnostics use MCP transition summaries and debriefs, not full replay
  artifacts.
- Scripted policies do not adapt to difficulty-tier rival counts or CPU budgets.
- Identical player endpoints across Easy/Hard do not prove difficulty is
  ineffective; they show that static scripted commands mask rival-pressure
  differences in player-facing debrief metrics.
- These findings do not support formula tuning, empirical calibration, human
  learning claims, or policy-validity claims.

## Prioritized Follow-Up

1. Keep `--target difficulty-sweep` as a focused diagnostic target rather than
   folding it into the default baseline batch.
2. Use difficulty-adaptive or rival-aware scripted policies, or free-form agent
   profiles, when testing whether difficulty tiers change strategic outcomes.
3. Do not change balance or runtime mechanics from this artifact alone.
