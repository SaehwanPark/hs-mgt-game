# Consultant Advice Evidence Synthesis v0.10.42

- **Status:** Phase 7 competitive teachability and validation synthesis
- **Date:** 2026-07-10
- **Code version:** 0.10.42
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:** v0.10.39 generic advice/history implementation,
  v0.10.40 traceability capture, and v0.10.41 usage capture
- **Validation artifacts:**
  - `_workspace/experiments/v0.10.40-consultant-advice-evidence/results.json`
  - `_workspace/experiments/v0.10.41-consultant-advice-usage/results.json`

This synthesis closes the consultant-advice evidence chain from generic
state-conditioned options through rendered/history/debrief traceability and
visible-cue simulated-policy usage. It is a project-state and evidence slice;
it does not add new playtest runs or change runtime behavior.

## Evidence Chain

| Version | Evidence shape | Result | Runtime change |
| --- | --- | --- | --- |
| `v0.10.39` | Generic monthly advice and advisory-history repair | Four deterministic non-binding options are produced from actor-visible observations and retained for debrief comparison | Additive observation/history behavior |
| `v0.10.40` | Traceability capture across four profiles, seeds 42–44, and Normal/Hard | 24 runs completed with zero validation failures, 24 exact observation/history matches, and 24 debrief option records per run | Additive MCP transition-summary field |
| `v0.10.41` | Paired advice-aware and advice-ignoring simulated policies across two profiles, seeds 42–44, and Normal/Hard | 24 paired runs completed with zero validation failures; all advice-ignoring controls matched the v0.10.40 hashes; selection, fallback, and safe-hold signals were captured | No runtime change |

## Synthesis Findings

1. The generic advice baseline is now visible, retained, and inspectable at the
   observation, committed-history, and debrief boundaries.
2. The v0.10.41 wrapper demonstrates that a deterministic policy can parse
   visible options, use visible cues, and fall back when inherited commands are
   not affordable. These are simulated-policy traces, not evidence that a
   human followed or benefited from the advice.
3. Advice-aware and control policies intentionally submit different commands,
   so endpoint differences cannot establish causal advice value, decision
   quality, balance effects, or learning.
4. The evidence identifies no concrete limitation in the generic baseline that
   would justify a differentiated advisor roster, payroll, candidate pool,
   hiring, firing, or AI-advisor mechanic.

## Decision and Routing

Retain the generic consultant baseline as the current decision-support surface.
Keep the advisor-market proposal in `docs/expansion-proposal-review.md`
deferred. Promote advisor runtime work only after a separate artifact identifies
a specific teachability, strategy, debrief, or audience need that the generic
baseline cannot meet and demonstrates viable recurring-cost and human/AI parity
conditions.

The next Phase 7 slice should remain evidence-led. Do not infer a new runtime
mechanics issue from option-selection counts, fallback counts, command-family
alignment, or endpoint differences alone.

## Evidence Limits

- The evidence uses deterministic simulated agents and scripted controls, not
  human players or classroom observations.
- Advice wording and option selection remain gameplay abstractions, not
  validated interventions or calibrated recommendations.
- The matrices establish visibility, continuity, reproducibility, and wrapper
  behavior only; they do not establish advice quality, causal impact, policy
  validity, human learning, or Expert winnability.
- Repeated controls are useful regression comparisons, not independent human
  samples.

## Non-Goals

- No advisor roster, payroll, candidate pool, hire/fire command, AI advice,
  scenario, balance, difficulty, scoring, replay, MCP schema, or state-hash
  change.
- No new playtest matrix, causal comparison, empirical calibration, or
  human-learning claim.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.40-consultant-advice-evidence/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.41-consultant-advice-usage/results.json >/dev/null
python3 _workspace/experiments/v0.10.41-consultant-advice-usage/run_sessions.py
python3 -m unittest discover -s tests -p 'test_*.py'
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
python3 scripts/run_automated_playtests.py
git diff --check
```
