# AI-Agent Access-Loop Diagnostic v0.10.2

- **Status:** Phase 7 free-form Hard competitive access-loop diagnostic
- **Date:** 2026-07-06
- **Code version:** 0.10.2
- **Harness:** Local MCP stdio client via operator capture script
  `_workspace/experiments/v0.10.2-access-loop-diagnostic/run_sessions.py`
- **Campaign:** `competitive-regional-v1`
- **Seeds:** `42`, `43`, `44`
- **Difficulty:** `hard`
- **Agent profiles:** Free-Form Fiscal Steward; Free-Form Access Expansion
  Advocate; Free-Form First-Time Executive
- **Policy variants:** baseline, cooldown, threshold

These findings are free-form **simulated-agent** evidence only. They test whether
the repetitive access-commitment loop identified in v0.10.1 can be reduced by
bounded operator-policy variants. They do not measure human learning, classroom
effectiveness, empirical calibration, real-world policy validity, numerical
balance, or equilibrium behavior.

## Variant Definitions

| Variant | Definition |
| --- | --- |
| `baseline` | v0.10.1 free-form policy behavior, unchanged. |
| `cooldown` | Suppress repeated access pledges for two months after an access pledge. |
| `threshold` | Suppress access pledges while reported access is 85 or higher. |

The cooldown and threshold variants redirect suppressed access pledges to a
small fallback policy using existing legal commands: payer negotiation under
cash strain, capacity investment under low access, nurse recruitment under
workforce pressure, monitoring on scheduled rival-intel cues, or `hold`.

## Run Matrix

| Campaign | Seeds | Difficulty | Profiles | Variants | Completed sessions | Validation failures |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `competitive-regional-v1` | 42, 43, 44 | hard | 3 | 3 | 27 | 0 |

All 27 sessions completed the full 24-month campaign without crashes, hangs,
incomplete sessions, or command validation failures.

## Command and Outcome Summary

| Variant | Profile | Sessions | Access pledges | Holds | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Failures | Distinct hashes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | Free-Form Fiscal Steward | 3 | 24 | 72 | 60 | 84 | 118 | 60 | 72 | 15 | 0 | 3 |
| baseline | Free-Form Access Expansion Advocate | 3 | 69 | 69 | 38 | 100 | 120 | 58 | 100 | 15 | 0 | 2 |
| baseline | Free-Form First-Time Executive | 3 | 69 | 66 | 40 | 100 | 120 | 58 | 87 | 15 | 0 | 2 |
| cooldown | Free-Form Fiscal Steward | 3 | 24 | 72 | 60 | 84 | 118 | 60 | 72 | 15 | 0 | 3 |
| cooldown | Free-Form Access Expansion Advocate | 3 | 24 | 69 | 38 | 100 | 120 | 58 | 80 | 15 | 0 | 3 |
| cooldown | Free-Form First-Time Executive | 3 | 24 | 66 | 40 | 85 | 120 | 58 | 72 | 15 | 0 | 3 |
| threshold | Free-Form Fiscal Steward | 3 | 24 | 72 | 60 | 84 | 118 | 60 | 72 | 15 | 0 | 3 |
| threshold | Free-Form Access Expansion Advocate | 3 | 12 | 69 | 38 | 85 | 120 | 58 | 72 | 14 | 0 | 3 |
| threshold | Free-Form First-Time Executive | 3 | 24 | 66 | 40 | 85 | 120 | 58 | 72 | 15 | 0 | 3 |

## Variant Totals

| Variant | Sessions | Access pledges | Holds | Validation failures |
| --- | ---: | ---: | ---: | ---: |
| baseline | 9 | 162 | 207 | 0 |
| cooldown | 9 | 72 | 207 | 0 |
| threshold | 9 | 60 | 207 | 0 |

## Gameplay Validity Hypotheses

- **Bounded access-loop variants complete the campaign:** Pass. Cooldown and
  threshold variants completed all 18 non-baseline sessions with zero validation
  failures.
- **The repetitive pledge loop is reducible at the operator-policy layer:** Pass.
  Aggregate access pledges fell from 162 baseline pledges to 72 under cooldown
  and 60 under threshold across the same seed/profile matrix.
- **Reducing access pledges preserves endpoint metrics:** Partial pass. Fiscal
  Steward endpoints were unchanged, but Access Expansion Advocate and First-Time
  Executive lost community-trust and/or access gains under reduced pledging.
- **This artifact justifies runtime balance changes:** Fail. The diagnostic
  shows that policy/guidance variants can change behavior; it does not prove
  that command rules, transition formulas, or balance values should change.

## Evidence Limits

- Operator policies are deterministic observation heuristics, not LLM or human
  play.
- Only three seeds, three profiles, one campaign, and Hard difficulty were
  exercised.
- Cooldown and threshold fallback commands are diagnostic controls, not
  recommended player strategy.
- Results use MCP transition summaries and debriefs, not full replay artifacts.
- The artifact does not support formula tuning, empirical calibration,
  human-learning claims, or policy-validity claims.

## Prioritized Follow-Up

1. Treat repetitive access pledges as a guidance and operator-policy diagnostic
   before considering runtime mechanics changes.
2. If future human or LLM play repeats the loop, revise player-facing guidance to
   distinguish public pledges from durable capacity or workforce action.
3. Do not tune pledge effects or add command cooldowns from this artifact alone.
4. Keep this diagnostic separate from default scripted playtest batches; compare
   findings rather than merging targets.
