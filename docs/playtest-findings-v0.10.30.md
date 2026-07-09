# Workforce-Protective Evidence Review v0.10.30

- **Status:** Phase 7 focused evidence review
- **Date:** 2026-07-09
- **Code version:** 0.10.30
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/playtest-findings-v0.10.16.md`
  - `docs/playtest-findings-v0.10.21.md`
  - `docs/playtest-findings-v0.10.26.md`
  - `docs/playtest-findings-v0.10.28.md`
  - `docs/playtest-findings-v0.10.29.md`
- **Exemplar artifacts:**
  - `_workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
  - `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
  - `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `_workspace/experiments/v0.10.24-access-debrief-validation/results.json`

This review follows the `v0.10.29` debrief comparison surface. It narrows one
under-explained comparison axis: workforce-protective play. The goal is to make
the evidence reviewable for instructors and contributors without treating
current artifacts as balance proof or as validation of a hidden strategy class.

This slice does not add new runs and does not change runtime mechanics,
command grammar, validation rules, scenario schemas, MCP DTOs, replay formats,
state hash logic, action costs, access-pledge effects, difficulty values,
scoring, or balance.

## Workforce-Protective Signals

Workforce-protective play should not be identified by a single metric or by
spending restraint alone. In the current evidence set, it is most defensible as
a pattern across visible reports and accepted commands:

| Signal | Evidence to inspect | Interpretation limit |
| --- | --- | --- |
| Staffing follow-through | `recruit` commands, staffed capacity, accepted command history | Recruiting alone does not prove a sustainable workforce strategy |
| Trust preservation | Final workforce trust, monthly pressure summaries, debrief notes | Higher trust can come from low activity, not only thoughtful protection |
| Pacing under cash pressure | Holds, delayed projects, cash-overrun retries, final cash runway | Cash preservation can mean caution, inability to spend, or script simplicity |
| Risk awareness | Monitor commands, rival summaries, payer posture, labor or staffing warnings | Monitoring is only protective if later decisions respond to the signal |
| Commitment discipline | Access pledges paired with staffing, payer, capacity, or project follow-through | Public commitments without operations can raise legitimacy but remain fragile |

## Evidence Reading

The strongest workforce-protective evidence appears indirectly. The `v0.10.21`
live synthesis notes that Hard adaptive policies increased monitoring and
preserved cash or workforce trust for some profiles. The `v0.10.28`
strategy-space synthesis then names workforce-protective play as visible when
policies reduce aggressive spending, monitor rivals, or pair commitments with
staffing follow-through, but it also states that current artifacts do not
isolate workforce protection as a clean standalone strategy.

That limitation should guide interpretation. A run with high final workforce
trust is not automatically a better workforce strategy if the player avoided
meaningful access, payer, or capacity tradeoffs. A run with lower trust is not
automatically a failed workforce strategy if it made costly access or capacity
choices that the debrief can trace to visible conditions. The review question is
whether the player managed workforce risk while still acting on the broader
institutional problem.

## Instructor Prompts

Use these prompts after reviewing the final debrief, monthly history, and
diagnostics for at least two contrasting competitive runs:

1. Did the player protect workforce trust through active follow-through, or
   mostly by avoiding commitments and capital strain?
2. When the player recruited, did staffing choices connect to visible service
   bottlenecks, access commitments, or rival pressure?
3. Did holds and delayed projects preserve option value, or did they defer the
   institutional conflict the player needed to address?
4. Did monitoring create better decisions later, or did it remain a passive
   information-gathering action?
5. Did the debrief make workforce tradeoffs traceable without implying that
   workforce trust is the sole objective?

## Routing Recommendation

For the next PR-sized slice, prefer a focused growth or capacity-oriented
evidence review if instructors need a parallel comparison axis. Prefer a
runtime mechanics investigation only if a future artifact identifies a concrete
command-cost, validation, staffing-allocation, strategic-behavior, or balance
defect.

Do not promote workforce-trust formula changes, recruitment-cost changes,
staffing allocation changes, action availability changes, difficulty
adjustment, new validation rules, scoring changes, or runtime balance tuning
from this review.

## Evidence Limits

- This review uses simulated-agent, deterministic-policy, reviewer-policy, and
  operator-authored evidence, not human classroom observation.
- Workforce-protective play is an interpretive review posture, not a hidden
  player class, validated learner archetype, equilibrium result, or balance
  proof.
- The current artifacts do not isolate workforce protection as a clean
  standalone strategy; they expose workforce signals inside broader finance,
  access, payer, rival, and capacity tradeoffs.
- This review supports instructor and contributor discussion, not empirical
  learning measurement, policy validity, calibration, or forecasting.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json >/dev/null
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json --output /tmp/hs-mgt-game-v0.10.30-difficulty-diagnostics.md
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json --output /tmp/hs-mgt-game-v0.10.30-static-adaptive-diagnostics.md
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
git diff --check
```
