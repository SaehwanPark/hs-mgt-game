# Instructor Comparison Note v0.10.27

- **Status:** Phase 7 instructor-facing evidence note
- **Date:** 2026-07-09
- **Code version:** 0.10.27
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/playtest-findings-v0.10.16.md`
  - `docs/playtest-findings-v0.10.21.md`
  - `docs/playtest-findings-v0.10.22.md`
  - `docs/playtest-findings-v0.10.25.md`
  - `docs/playtest-findings-v0.10.26.md`
- **Exemplar artifacts:**
  - `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `_workspace/experiments/v0.10.24-access-debrief-validation/results.json`

This note turns the `v0.10.26` competitive teachability synthesis into
instructor-facing comparison prompts. It uses existing simulated-agent,
deterministic-policy, reviewer-policy, and operator-authored evidence. It does
not add new runs and does not change runtime mechanics, command grammar,
validation rules, scenario schemas, MCP DTOs, replay formats, state hash logic,
action costs, access-pledge effects, difficulty values, scoring, or balance.

## Instructor Comparison Prompts

1. **Public commitment versus durable follow-through.** Compare an
   access-heavy run with a more balanced run. Which choices created public
   legitimacy, and which choices changed capacity, staffing, monitoring, payer
   posture, or cash runway enough to make the public commitment durable?
2. **Decision quality versus outcome quality under pressure.** Identify a month
   where the final outcome looked weak but the submitted command batch was
   reasonable from the actor-visible report. What information was available,
   what remained uncertain, and what rival or delayed effects changed the
   result?
3. **Cash runway as a strategic constraint.** Compare Normal and Hard evidence
   where cash pressure or validation retries shaped accepted commands. Did the
   player preserve option value, or did the player turn a legitimate strategic
   aim into a brittle plan?
4. **Workforce follow-through and operational tempo.** Review runs that leaned
   on commitments, projects, or access expansion. Where did recruitment,
   workforce trust, and pending implementation capacity support the strategy,
   and where did they lag behind the promise?
5. **Rival pressure and payer posture.** Compare a run that monitored or
   adapted to rivals with a run that pursued a mostly internal plan. When was
   payer negotiation defensible, and when did limited leverage or rival
   expansion make the posture riskier than it first appeared?

## Suggested Classroom Framing

Use these prompts after students have reviewed the final debrief, monthly
history, and any available diagnostic summary. Ask students to separate:

- what the player knew at the time;
- what the player reasonably inferred;
- which outcomes came from delayed or rival response;
- which outcomes came from the player's own resource commitments; and
- which conclusions are about gameplay process rather than real-world policy
  validity.

This framing keeps the discussion aligned with the project's distinction between
decision quality and outcome quality. A weak final metric should not be treated
as automatic proof of a bad decision, and a favorable endpoint should not be
treated as proof that the strategy was broadly optimal.

## Recommended Routing

For the next PR-sized slice, prefer a broader strategy-space synthesis only if
the project needs to compare finance-first, access-heavy, workforce-protective,
and growth-oriented profiles across existing artifacts. Prefer a runtime
mechanics investigation only if a later artifact identifies a concrete defect in
command cost, validation, strategic behavior, or balance.

Do not promote access-pledge cooldowns, effect tuning, action-cost changes,
difficulty adjustment, new validation rules, scoring changes, or runtime balance
tuning from this note.

## Evidence Limits

- These prompts are based on simulated-agent, reviewer-policy,
  deterministic-policy, and operator-authored evidence, not human classroom
  observation.
- The note supports instructor discussion design, not empirical learning
  measurement, policy validity, calibration, or forecasting.
- The existing artifacts show reviewable tradeoffs, but they do not establish
  which prompt sequence best supports student learning.
- The prompts should be revised after any future human, classroom, or instructor
  pilot evidence rather than treated as a validated assessment instrument.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.27-diagnostics.md
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
git diff --check
```
