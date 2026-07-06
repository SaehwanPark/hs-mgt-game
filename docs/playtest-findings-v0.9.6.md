# AI-Agent Playtest Policy Coverage v0.9.6

- **Status:** Phase 7 scripted playtest-policy coverage slice
- **Date:** 2026-07-06
- **Code version:** 0.9.6
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
validation failures. Compared with v0.9.5, the competitive scripted policies now
act beyond month 3 and directly exercise newer service-line, public-payer,
staffing, monitoring, and commitment commands.

## Competitive Profile Outcomes

| Profile | Sessions | Cash | Access | Beds | Workforce trust | Community trust | PC | Representative hashes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Fiscal Caution | 3 | 5 | 75 | 118 | 57 | 66 | 15 | `db396cb8c5362ddc`, `07ea95139054c286`, `0aab9a565fac80e4` |
| Capacity Growth | 3 | 9 | 73 | 121 | 34 | 66 | 15 | `16ace0dc772b82e0`, `9cf1e60776f2c4da`, `7503824ce07c4047` |
| Balanced Strategy | 3 | 1 | 75 | 121 | 48 | 67 | 15 | `cef701ede4d5c162`, `c88d320130c55d40`, `818a67d0a862c481` |
| Naive First-Time | 3 | 20 | 75 | 118 | 58 | 66 | 15 | `71b814663df88a84`, `655949d617c7121a`, `82e1ce0125a6758c` |

Capacity Growth still produces the lowest workforce trust, while Balanced
Strategy preserves more workforce trust than the growth profile at lower final
cash. Naive First-Time remains the most cash-preserving competitive profile in
this scripted batch.

## Competitive Action Frequency Signals

| Profile | Holds | Action commands | Top non-hold verb | Diagnostic classification |
| --- | ---: | ---: | --- | --- |
| Fiscal Caution | 72 | 57 | Monitor (18) | Balanced Strategy |
| Capacity Growth | 63 | 69 | Monitor (24) | Balanced Strategy |
| Balanced Strategy | 66 | 75 | Monitor (30) | Intel-Gatherer |
| Naive First-Time | 72 | 45 | Monitor (12) | Balanced Strategy |

The v0.9.6 policies materially improve command coverage versus v0.9.5, where
competitive scripts mostly acted in months 1-3 and then held through month 24.
The profiles are still scripted and intentionally conservative about cash
because the current validator correctly fails policies that cannot support
active project draws or recruitment costs.

## Stabilization Outcome Ranges

| Metric | Range |
| --- | ---: |
| Cash | 15-70 |
| Access | 73-93 |
| Workforce trust | 64-68 |
| Community trust | 57-75 |
| Policy pressure | 35-59 |

The stabilization policies were not changed in this slice. Their outcome ranges
remain consistent with the v0.9.5 baseline.

## Gameplay Validity Hypotheses

- **Scripted agents can complete both current campaigns through MCP:** Pass.
  All 24 expected sessions completed with zero validation failures.
- **Competitive policies now exercise months beyond the opening quarter:** Pass.
  All competitive profiles submit non-hold commands after month 3.
- **Recent service-line command coverage improved:** Pass. The batch directly
  exercises newer service-line investment domains including emergency, ICU,
  obstetrics, psychiatric, cardiology, oncology, infusion, and ASC.
- **The batch supports runtime balance tuning:** Fail. This evidence is about
  validation coverage and scripted command diversity, not formula calibration.

## Evidence Limits

- Batch diagnostics use MCP transition summaries and debriefs, not full
  competitive replay artifacts.
- These diagnostics are validation aids for gameplay, comprehension, and
  explanation quality.
- The findings do not support formula tuning, empirical calibration, human
  learning claims, or policy-validity claims.
- Project-command coverage remains intentionally limited because low-cash
  scripted profiles can fail later validation when active monthly draws exceed
  available cash.

## Prioritized Follow-Up

1. Preserve the v0.9.6 scripts as the default Phase 7 scripted coverage baseline.
2. Use future scripted-policy updates only when a specific command family or
   playtest question remains under-exercised.
3. Do not change simulation balance from this evidence alone; route balance
   questions through stronger repeated-run or scenario-specific evidence.
