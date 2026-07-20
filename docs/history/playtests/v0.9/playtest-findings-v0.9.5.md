# AI-Agent Strategy-Space Diagnostics v0.9.5

- **Status:** Phase 7 strategy-space diagnostics artifact
- **Date:** 2026-07-06
- **Code version:** 0.9.5
- **Harness:** `python3 scripts/run_automated_playtests.py --json-output ...`
  followed by `python3 scripts/diagnose_runs.py ...`
- **Campaigns:** `stabilization-v1`, `competitive-regional-v1`
- **Seeds:** `42`, `43`, `44`
- **Difficulty:** normal for competitive runs
- **Agent profiles:** Fiscal Caution, Capacity Growth, Balanced Strategy,
  Naive First-Time

These diagnostics summarize simulated-agent evidence only. They do not measure
human learning, classroom effectiveness, empirical calibration, real-world
policy validity, numerical balance, or equilibrium behavior.

## Run Matrix

| Campaign | Seeds | Profiles | Completed sessions | Validation failures |
| --- | --- | ---: | ---: | ---: |
| `stabilization-v1` | 42, 43, 44 | 4 | 12 | 0 |
| `competitive-regional-v1` | 42, 43, 44 | 4 | 12 | 0 |

The batch completed without crashes, hangs, incomplete sessions, or command
validation failures. The new JSON batch artifact captured final observations,
transition summaries, debrief lines, metrics, validation failures, and
competitive final hashes for downstream diagnostics.

## Competitive Profile Outcomes

| Profile | Sessions | Cash | Access | Beds | Workforce trust | Community trust | PC | Representative hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Fiscal Caution | 3 | 50 | 70 | 118 | 58 | 65 | 15 | `e9cb05324ff5ab3d`, `3ed622680a05722b`, `cc02350cd77d622e` |
| Capacity Growth | 3 | 5 | 70 | 123 | 30 | 64 | 15 | `0321a0d91a57fc46`, `ff3cda219966a9d0`, `dbfd12910cadf61a` |
| Balanced Strategy | 3 | 25 | 73 | 121 | 34 | 66 | 15 | `5b221a911e97f76c`, `2f72815ee9e95d4e`, `9927638123ee9e80` |
| Naive First-Time | 3 | 60 | 70 | 118 | 60 | 65 | 15 | `7e530a394a78bffe`, `730a633e4ab170e4`, `45ae273a72439a75` |

Capacity Growth still creates the strongest cash and workforce-trust pressure.
Balanced Strategy produces the highest access in this scripted batch. Fiscal
Caution and Naive First-Time preserve more cash and workforce trust with lower
access movement.

## Competitive Action Frequency Signals

| Profile | Holds | Action commands | Top non-hold verb | Diagnostic classification |
| --- | ---: | ---: | --- | --- |
| Fiscal Caution | 72 | 9 | Monitor (3) | Conservative / Passive |
| Capacity Growth | 63 | 9 | Invest (3) | Conservative / Passive |
| Balanced Strategy | 66 | 15 | Monitor (3) | Conservative / Passive |
| Naive First-Time | 72 | 6 | Monitor (3) | Conservative / Passive |

The diagnostic classification is driven by the current scripted policies: each
competitive profile acts in the first three months, then mostly holds through
month 24. This is useful evidence about the playtest harness and strategy-space
coverage, not evidence that the runtime should be rebalanced.

## Stabilization Outcome Ranges

| Metric | Range |
| --- | ---: |
| Cash | 15-70 |
| Access | 73-93 |
| Workforce trust | 64-68 |
| Community trust | 57-75 |
| Policy pressure | 35-59 |

The stabilization results remain consistent with the v0.9.4 baseline. Strategy
posture drives the main cash/access/trust differences across the tested seeds.

## Gameplay Validity Hypotheses

- **Scripted agents can complete both current campaigns through MCP:** Pass.
  All 24 expected sessions completed with zero validation failures.
- **Profiles produce materially different end states:** Pass for cash, access,
  beds, and workforce trust, although command diversity after month 3 is weak.
- **The diagnostic tooling can preserve enough evidence for follow-up:** Pass.
  The JSON batch artifact and diagnostic report capture transition summaries,
  final metrics, debriefs, validation failures, and hashes without changing MCP
  DTOs or simulation behavior.
- **The current scripted competitive policies explore the full 24-month command
  space:** Fail. They primarily test early-month command comprehension and
  long-run stability under hold-heavy play.

## Evidence Limits

- The batch uses MCP transition summaries and debriefs, not full competitive
  replay artifacts.
- These diagnostics are validation aids for gameplay, comprehension, and
  explanation quality.
- The findings do not support formula tuning, empirical calibration, human
  learning claims, or policy-validity claims.
- Service-line commands added in recent runtime slices remain under-exercised by
  the current scripted profiles.

## Prioritized Follow-Up

1. Preserve the new JSON artifact and diagnostics flow as the default way to
   capture scripted Phase 7 evidence.
2. For the next playtest-policy slice, extend competitive scripted profiles
   beyond month 3 and include newer service-line commands directly.
3. Do not change balance or runtime mechanics from this diagnostic artifact
   alone; treat it as evidence about validation coverage.
