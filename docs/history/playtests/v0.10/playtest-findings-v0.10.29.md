# Competitive Debrief Comparison Surface v0.10.29

- **Status:** Phase 7 instructor/debrief comparison surface
- **Date:** 2026-07-09
- **Code version:** 0.10.29
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.16.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.21.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.25.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.26.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.27.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.28.md`
- **Exemplar artifacts:**
  - `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `_workspace/experiments/v0.10.24-access-debrief-validation/results.json`

This comparison surface follows the `v0.10.28` strategy-space synthesis. It
turns existing simulated-agent, deterministic-policy, reviewer-policy, and
operator-authored evidence into a compact review aid for comparing repeated
competitive runs. It does not add new runs and does not change runtime
mechanics, command grammar, validation rules, scenario schemas, MCP DTOs,
replay formats, state hash logic, action costs, access-pledge effects,
difficulty values, scoring, or balance.

## Debrief Comparison Surface

Use the surface below after reviewing the final debrief, monthly history, and
diagnostic summary for two or more competitive runs.

| Review axis | Compare | Evidence to inspect | Do not infer |
| --- | --- | --- | --- |
| Decision quality | Whether accepted commands were reasonable from actor-visible reports | Month observations, legal hints, accepted commands, validation retries | A weak endpoint automatically means a bad decision |
| Outcome quality | Whether final tradeoff metrics fit the stated strategy | Final cash, access, workforce trust, community trust, political capital, rival pressure | A favorable endpoint proves the strategy is generally optimal |
| Cash runway | Whether the run preserved option value under Normal or Hard pressure | Final cash, cash-overrun retries, holds, delayed projects, rejected batches | Cash preservation alone is the correct objective |
| Durable follow-through | Whether commitments were backed by staffing, capacity, monitoring, payer posture, or projects | Access pledges, recruitment, investment, monitoring, negotiation, project history | Repeated pledges prove a cooldown or cost change is needed |
| Rival pressure | Whether the player adapted to observed rival moves and payer leverage | Monitor commands, rival summaries, payer posture, market events | Rival movement is fully predictable from player-visible data |
| Debrief traceability | Whether the debrief explains what happened and what was known at the time | End-session debrief, transition summaries, observation traces | Debrief clarity is measured human learning evidence |

## Strategy Posture Prompts

1. **Finance-first / conservative.** Did the player preserve option value while
   still acting on visible risks, or did caution become passivity? Compare cash
   runway, monitoring, and missed opportunities against an access-heavy or
   growth-oriented run.
2. **Access-heavy.** Which public commitments created legitimacy, and which
   durable actions made those commitments operationally credible? Compare access
   pledges against recruitment, investment, payer negotiation, projects, and
   final cash runway.
3. **Workforce-protective.** Did the player reduce workforce risk through
   staffing follow-through and pacing, or merely avoid spending? Compare trust,
   recruiting, holds, and delayed capacity choices.
4. **Growth / capacity-oriented.** Did capacity growth create useful access and
   market-position gains, or did project timing and cash draw narrow later
   options? Compare project history, staffed capacity, final access, and cash.

## Recommended Use

- Choose two contrasting runs before asking which strategy was "better."
- Ask first what the player knew at the time, then what the final outcome
  revealed later.
- Treat strategy labels as discussion handles, not hidden game classes or
  validated learner archetypes.
- Use the comparison to identify concrete future evidence questions. Do not use
  it as a shortcut to runtime tuning.

## Recommended Routing

For the next PR-sized slice, prefer a narrower evidence review only if this
surface reveals an under-explained comparison axis, such as workforce-protective
or growth-oriented play. Prefer a runtime mechanics investigation only if a
future artifact identifies a concrete command-cost, validation,
strategic-behavior, or balance defect.

Do not promote access-pledge cooldowns, effect tuning, action-cost changes,
difficulty adjustment, new validation rules, scoring changes, or runtime
balance tuning from this comparison surface.

## Evidence Limits

- These prompts are based on simulated-agent, reviewer-policy,
  deterministic-policy, and operator-authored evidence, not human classroom
  observation.
- The surface supports instructor and reviewer discussion design, not empirical
  learning measurement, policy validity, calibration, or forecasting.
- Strategy labels are interpretive development summaries, not validated learner
  archetypes, equilibrium results, or balance proof.
- The comparison surface should be revised after future human, classroom,
  instructor, or domain-review evidence rather than treated as a validated
  assessment instrument.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json >/dev/null
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.29-live-diagnostics.md
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.29-access-diagnostics.md
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
git diff --check
```
