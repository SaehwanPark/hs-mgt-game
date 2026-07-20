# AI-Agent Post-Guidance Validation v0.10.4

- **Status:** Phase 7 post-guidance validation
- **Date:** 2026-07-06
- **Code version:** 0.10.4
- **Harness:** Local MCP stdio client via operator capture script
  `_workspace/experiments/v0.10.4-post-guidance-validation/run_sessions.py`
- **Campaign:** `competitive-regional-v1`
- **Seeds:** `42`, `43`, `44`
- **Difficulty:** `hard`
- **Agent profiles:** Free-Form Fiscal Steward; Free-Form Access Expansion
  Advocate; Free-Form First-Time Executive
- **Policy variants:** baseline, guidance-aware

These findings are free-form **simulated-agent** evidence only. They test whether
the v0.10.3 guidance distinction between public access pledges and durable
operational follow-through can be represented by a bounded operator policy. They
do not measure human learning, classroom effectiveness, empirical calibration,
real-world policy validity, numerical balance, or equilibrium behavior.

## Variant Definitions

| Variant | Definition |
| --- | --- |
| `baseline` | v0.10.1/v0.10.2 free-form policy behavior, unchanged. |
| `guidance_aware` | Suppress access pledges when reported access is at least 85 or another access pledge occurred in the prior two months, then redirect to the existing fallback actions. |

Fallback actions use existing legal commands only: payer negotiation under cash
strain, capacity investment under low access, nurse recruitment under workforce
pressure, monitoring on scheduled rival-intel cues, or `hold`.

## Run Matrix

| Campaign | Seeds | Difficulty | Profiles | Variants | Completed sessions | Validation failures |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `competitive-regional-v1` | 42, 43, 44 | hard | 3 | 2 | 18 | 0 |

All 18 sessions completed the full 24-month campaign without crashes, hangs,
incomplete sessions, or command validation failures.

## Command and Outcome Summary

| Variant | Profile | Sessions | Access pledges | Holds | Negotiates | Commits | Cash | Access | Beds | Workforce Trust | Community Trust | PC | Failures | Distinct hashes |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | Free-Form Fiscal Steward | 3 | 24 | 72 | 12 | 24 | 60 | 84 | 118 | 60 | 72 | 15 | 0 | 3 |
| baseline | Free-Form Access Expansion Advocate | 3 | 69 | 69 | 0 | 69 | 38 | 100 | 120 | 58 | 100 | 15 | 0 | 2 |
| baseline | Free-Form First-Time Executive | 3 | 69 | 66 | 0 | 69 | 40 | 100 | 120 | 58 | 87 | 15 | 0 | 2 |
| guidance_aware | Free-Form Fiscal Steward | 3 | 24 | 72 | 12 | 24 | 60 | 84 | 118 | 60 | 72 | 15 | 0 | 3 |
| guidance_aware | Free-Form Access Expansion Advocate | 3 | 12 | 69 | 57 | 12 | 38 | 85 | 120 | 58 | 72 | 14 | 0 | 3 |
| guidance_aware | Free-Form First-Time Executive | 3 | 24 | 66 | 45 | 24 | 40 | 85 | 120 | 58 | 72 | 15 | 0 | 3 |

## Variant Totals

| Variant | Sessions | Access pledges | Holds | Invest | Recruit | Monitor | Negotiate | Commit | Validation failures |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| baseline | 9 | 162 | 207 | 6 | 6 | 6 | 12 | 162 | 0 |
| guidance_aware | 9 | 60 | 207 | 6 | 6 | 6 | 114 | 60 | 0 |

## Gameplay Validity Hypotheses

- **Guidance-aware policies complete the campaign:** Pass. All nine
  guidance-aware sessions completed 24 months with zero validation failures.
- **Guidance-aware policies reduce repeated access pledges:** Pass. Aggregate
  access pledges fell from 162 baseline pledges to 60 guidance-aware pledges
  across the same seed/profile matrix.
- **The guidance-aware policy preserves endpoint metrics:** Partial pass. Fiscal
  Steward endpoints were unchanged. Access Expansion Advocate and First-Time
  Executive retained cash, beds, and workforce trust, but ended at lower access
  and community trust after redirecting pledges toward neutral payer negotiation.
- **This artifact justifies runtime balance changes:** Fail. The evidence shows
  that operator-policy interpretation can change command behavior and endpoint
  tradeoffs. It does not prove that command rules, transition formulas, pledge
  effects, or balance values should change.

## Evidence Limits

- Operator policies are deterministic observation heuristics, not LLM or human
  play.
- Only three seeds, three profiles, one campaign, and Hard difficulty were
  exercised.
- The guidance-aware fallback commands are diagnostic controls, not recommended
  player strategy.
- Results use MCP transition summaries and debriefs, not full replay artifacts.
- The artifact does not support formula tuning, empirical calibration,
  human-learning claims, classroom-effectiveness claims, or policy-validity
  claims.

## Prioritized Follow-Up

1. Treat the v0.10.3 guidance hardening as behaviorally plausible for simulated
   operators: pledge loops fell without validation failures.
2. Do not add runtime pledge cooldowns or tune pledge effects from this artifact
   alone; the guidance-aware variant reduced access/community-trust endpoints
   for access-heavy profiles.
3. If future LLM or human play still repeats pledge loops, test a separate
   player-facing prompt/help revision before changing simulation mechanics.
4. Keep post-guidance validation separate from default scripted batches; compare
   findings rather than merging policy variants into the baseline runner.
