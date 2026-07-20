# Growth/Capacity-Oriented Evidence Review v0.10.33

- **Status:** Phase 7 focused evidence review
- **Date:** 2026-07-09
- **Code version:** 0.10.33
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.12.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.13.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.15.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.24.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.28.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.29.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.30.md`
- **Exemplar artifacts:**
  - `_workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
  - `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
  - `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `_workspace/experiments/v0.10.24-access-debrief-validation/results.json`

This review follows the `v0.10.30` workforce-protective evidence review. It
narrows the parallel comparison axis named there: growth/capacity-oriented
play. The goal is to make capacity-building runs easier to interpret for
instructors and contributors without treating current artifacts as balance
proof, human-learning evidence, or validation of a hidden strategy class.

This slice does not add new runs and does not change runtime mechanics,
command grammar, validation rules, scenario schemas, MCP DTOs, replay formats,
state hash logic, action costs, project costs, service-line effects,
difficulty values, scoring, or balance.

## Growth/Capacity Signals

Growth/capacity-oriented play should not be identified by project count alone.
In the current evidence set, it is most defensible as a pattern across accepted
commands, project timing, resource trajectories, and debrief explanation:

| Signal | Evidence to inspect | Interpretation limit |
| --- | --- | --- |
| Capacity action | `invest` and `project` commands, project kinds, active project draw history | High capacity activity can reflect scripted coverage rather than learner intent |
| Operational follow-through | Staffed beds, nurses, physicians, admins, access trajectory | New capacity is not durable if staffing or cash cannot support it |
| Cash runway | Final cash, active project draws, cash-overrun retries, holds after project starts | Cash stress can be a meaningful tradeoff, not automatically a balance defect |
| Access and market effect | Final access, community trust, market share, debrief causal notes | Better access does not prove growth is generally optimal |
| Rival response | Monitor commands, observed rival expansion, payer posture, market summaries | Rival pressure is only reviewable where the player had actor-visible evidence |

## Evidence Reading

The strongest growth/capacity evidence appears through contrast. The
`v0.10.28` strategy-space synthesis names growth-oriented policies as visible
when capacity and staffed-bed tradeoffs can be compared against cash-preserving
or workforce-protective runs. The `v0.10.29` comparison surface then gives
instructors a way to ask whether capacity growth created useful access and
market-position gains or narrowed later options through project timing and
cash draw. The `v0.10.30` workforce review keeps that axis separate from
workforce-protective play so capacity choices are not reduced to either trust
preservation or spending volume.

That separation matters. A run with several projects or investments is not
automatically a good growth strategy if it ignores cash, staffing, payer
leverage, or rival information. A run with low final cash is not automatically
a failed growth strategy if the accepted history shows deliberate capacity
building under visible access pressure and the debrief traces the consequences.
The review question is whether the player converted resources into durable
operational capacity while preserving enough option value to respond later.

## Instructor Prompts

Use these prompts after reviewing the final debrief, monthly history, and
diagnostics for at least two contrasting competitive runs:

1. Did the player add capacity in response to visible access, staffing, payer,
   or rival pressure, or did capacity building appear disconnected from the
   observation surface?
2. Did projects and investments resolve into staffed operational capacity, or
   did cash draw and staffing constraints make the expansion fragile?
3. Did the player preserve enough cash and political capital to adapt after
   committing to growth?
4. Did monitoring or payer negotiation change later growth decisions, or did
   growth proceed without using available strategic information?
5. Did the debrief make the growth tradeoff traceable without implying that
   more capacity is always the correct objective?

## Routing Recommendation

Treat growth/capacity-oriented play as a review posture for comparing repeated
competitive runs, not as a new runtime target. The next bounded slice should
remain within the competitive teachability and validation loop unless a future
artifact identifies a concrete mechanics issue. Good follow-ups include a
small instructor comparison update, a bounded difficulty evidence gate, or a
specific diagnostics improvement if reviewers cannot see project timing or
resource draw clearly enough from existing artifacts.

Do not promote project-cost changes, capacity-effect tuning, staffing
allocation changes, action availability changes, difficulty adjustment, new
validation rules, scoring changes, or runtime balance tuning from this review.

## Evidence Limits

- This review uses simulated-agent, deterministic-policy, reviewer-policy, and
  operator-authored evidence, not human classroom observation.
- Growth/capacity-oriented play is an interpretive review posture, not a hidden
  player class, validated learner archetype, equilibrium result, or balance
  proof.
- Existing diagnostics can classify `Capacity-Builder` runs from action
  frequencies, but that label does not prove strategic intent or educational
  effectiveness.
- The current artifacts expose capacity choices inside broader finance,
  workforce, access, payer, rival, and project-timing tradeoffs.
- This review supports instructor and contributor discussion, not empirical
  learning measurement, policy validity, calibration, or forecasting.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json
python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json --output /tmp/hs-mgt-game-v0.10.33-static-adaptive-diagnostics.md
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.33-live-diagnostics.md
git diff --check
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
```
