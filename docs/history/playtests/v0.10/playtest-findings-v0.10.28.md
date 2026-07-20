# Competitive Strategy-Space Synthesis v0.10.28

- **Status:** Phase 7 simulated-agent strategy-space synthesis
- **Date:** 2026-07-09
- **Code version:** 0.10.28
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.12.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.13.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.15.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.21.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.24.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.25.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.26.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.27.md`
- **Exemplar artifacts:**
  - `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `_workspace/experiments/v0.10.24-access-debrief-validation/results.json`

This synthesis follows the `v0.10.27` instructor comparison note by comparing
the current competitive evidence across strategy postures. It uses existing
simulated-agent, deterministic-policy, reviewer-policy, and operator-authored
artifacts. It does not add new runs and does not change runtime mechanics,
command grammar, validation rules, scenario schemas, MCP DTOs, replay formats,
state hash logic, action costs, access-pledge effects, difficulty values,
scoring, or balance.

## Strategy-Space Signals

| Posture | Evidence source | Observed signal | Interpretation limit |
| --- | --- | --- | --- |
| Finance-first / conservative | Fiscal Caution, Live Fiscal Steward, conservative controls | Preserved cash better than access-heavy policies and often completed with holds or monitoring-heavy action sets | Conservative play is reviewable, but low activity can also reflect scripted policy simplicity rather than human caution |
| Access-heavy | Live Access Operator and access debrief trigger/control policies | Produced the clearest public-commitment and cash-pressure teaching signals, including low-cash endpoints and access pledge follow-through questions | Repeated pledges and retries are not enough to prove pledge costs, cooldowns, or balance are defective |
| Workforce-protective | Hard adaptive scripted profiles and access follow-through comparisons | Workforce trust was more visible when policies reduced aggressive spending, monitored rivals, or paired commitments with staffing follow-through | Current artifacts do not isolate workforce protection as a clean standalone strategy |
| Growth / capacity-oriented | Capacity Growth and project or investment-heavy scripted policies | Growth-oriented policies made capacity and staffed-bed tradeoffs visible, especially when compared against cash-preserving Hard adaptations | Existing diagnostics often classify these runs by top command frequency, not by a full strategic intent model |

The strategy labels above are interpretive development labels, not hidden game
classes. Existing diagnostics frequently classify runs as `Intel-Gatherer` or
`Conservative / Passive` because those labels are derived from action
frequencies. They are useful for finding patterns, but they should not be
treated as a validated taxonomy of player intent.

## Cross-Run Findings

1. **Repeated play is currently most teachable through comparison, not scoring.**
   The strongest learning surface is asking why two runs with different command
   patterns produced different cash, access, workforce trust, community trust,
   and rival-pressure outcomes.
2. **Access-heavy play remains the clearest stress case.** It exposes public
   commitment, cash runway, durable operational follow-through, and debrief
   explanation questions without requiring a runtime change.
3. **Finance-first and conservative runs provide important controls.** They show
   that clean completion and cash preservation can coexist with lower strategic
   activity, but the evidence does not prove that passive play is optimal or
   desirable.
4. **Workforce and capacity tradeoffs need comparison prompts more than new
   mechanics right now.** Recent artifacts make the tradeoffs visible, but they
   do not isolate a specific workforce or capacity formula defect.
5. **Difficulty evidence is still process evidence.** Normal/Hard comparisons
   expose cash pressure, retries, and adaptation behavior, but the current
   evidence does not justify difficulty retuning.

## Recommended Routing

For the next PR-sized slice, prefer one of these paths:

- a lightweight instructor or debrief comparison surface that helps reviewers
  compare strategy postures without creating a hidden optimization score;
- a bounded evidence review focused on one under-explained posture, such as
  workforce-protective or growth-oriented play, if future artifacts make it
  difficult to interpret;
- a runtime mechanics investigation only if a later artifact identifies a
  concrete command-cost, validation, strategic-behavior, or balance defect.

Do not promote access-pledge cooldowns, effect tuning, action-cost changes,
difficulty adjustment, scoring redesign, or new runtime validation from this
synthesis.

## Evidence Limits

- These are simulated-agent, reviewer-policy, deterministic-policy, and
  operator-authored artifacts, not human classroom observations.
- Current evidence compares a small number of profiles, seeds, and policy
  variants in one competitive campaign.
- Strategy labels are interpretive summaries over captured behavior, not
  validated learner archetypes or equilibrium results.
- Diagnostics and debriefs support gameplay and explanation review; they do not
  measure student learning, empirical calibration, policy validity, or real
  institutional outcomes.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json >/dev/null
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.28-live-diagnostics.md
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.28-access-diagnostics.md
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
git diff --check
```
