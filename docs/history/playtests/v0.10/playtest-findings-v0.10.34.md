# Instructor Debrief Facilitation Note v0.10.34

- **Status:** Phase 7 instructor facilitation note
- **Date:** 2026-07-09
- **Code version:** 0.10.34
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.24.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.28.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.29.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.30.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.33.md`
- **Exemplar artifacts:**
  - `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
  - `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `_workspace/experiments/v0.10.24-access-debrief-validation/results.json`

This note follows the `v0.10.29` debrief comparison surface, the `v0.10.30`
workforce-protective evidence review, and the `v0.10.33`
growth/capacity-oriented evidence review. It turns those artifacts into a
compact facilitation sequence for instructors and reviewers comparing repeated
competitive campaign runs.

This slice does not add new playtest runs and does not change runtime
mechanics, command grammar, validation rules, scenario schemas, MCP DTOs,
replay formats, state hash logic, action costs, project costs, service-line
effects, difficulty values, scoring, or balance.

## Facilitation Sequence

Use the sequence below after reviewing the final debrief, monthly history, and
diagnostics for at least two contrasting competitive runs.

| Step | Instructor question | Evidence to inspect | Guardrail |
| --- | --- | --- | --- |
| 1. Decision context | What did the player know when each major commitment was made? | Month observations, legal hints, accepted commands, validation retries | Do not judge early decisions only from final endpoints |
| 2. Outcome context | Which final tradeoffs were intended, tolerated, or surprising? | Final cash, access, workforce trust, community trust, political capital, rival pressure | Do not treat a favorable endpoint as proof that the strategy is generally optimal |
| 3. Follow-through | Were public commitments backed by operational capacity, staffing, payer posture, or monitoring? | Access pledges, recruitment, investments, projects, negotiations, monitor history | Do not infer that repeated pledges alone justify a cooldown or cost change |
| 4. Workforce posture | Did the player protect workforce trust while still acting on institutional pressure? | Recruiting, holds, staffing gaps, workforce trust, service bottlenecks | Do not treat trust as the sole objective |
| 5. Growth posture | Did capacity growth become durable staffed capacity, or did cash draw narrow later options? | Project timing, active draws, staffed capacity, final access, final cash | Do not equate project count with strategic growth quality |
| 6. Rival response | Did the player adapt to observed rival and payer pressure? | Monitor commands, rival summaries, payer posture, market share, debrief notes | Do not assume rival behavior was fully visible or predictable |
| 7. Debrief clarity | Can learners trace why outcomes happened and what was knowable at the time? | End-session debrief, transition summaries, observation traces | Do not present debrief clarity as measured human learning |

## Comparison Prompts

Ask these prompts across paired or small-group run comparisons:

1. Which decisions were reasonable from actor-visible information even if the
   final outcome was weak?
2. Which favorable outcomes depended on delayed effects, rival behavior, or
   stochastic inputs that the player could not fully know?
3. Where did the player convert commitments into durable operations, and where
   did commitments remain mostly symbolic?
4. Did workforce-protective choices preserve option value, or did they defer a
   necessary access, payer, or capacity conflict?
5. Did growth/capacity choices improve access and market position enough to
   justify cash draw and staffing strain?
6. Did monitoring or payer negotiation alter later choices, or did the run
   proceed without using available strategic information?

## Recommended Routing

Treat this facilitation note as the current instructor-facing bridge across
recent competitive teachability artifacts. The next bounded slice should stay
inside the competitive teachability and validation loop unless a future
artifact identifies a concrete mechanics issue.

Good follow-ups include a bounded difficulty evidence gate, a specific
diagnostics improvement if project timing or retry pressure remains hard to
see, or a domain-reviewed scenario design slice. Do not promote runtime tuning
from this note alone.

Do not promote access-pledge cooldowns, project-cost changes,
capacity-effect tuning, staffing allocation changes, action availability
changes, difficulty adjustment, new validation rules, scoring changes, or
runtime balance tuning from this facilitation note.

## Evidence Limits

- This note uses simulated-agent, deterministic-policy, reviewer-policy, and
  operator-authored evidence, not human classroom observation.
- The facilitation sequence is a discussion aid, not a validated assessment
  instrument, learner archetype taxonomy, equilibrium result, or balance proof.
- Existing artifacts expose strategy signals inside broader finance, workforce,
  access, payer, rival, project-timing, and debrief-traceability tradeoffs.
- This note supports instructor and contributor discussion, not empirical
  learning measurement, policy validity, calibration, or forecasting.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.34-live-diagnostics.md
git diff --check
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
```
