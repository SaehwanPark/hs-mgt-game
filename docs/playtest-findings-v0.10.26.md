# Competitive Teachability Synthesis v0.10.26

- **Status:** Phase 7 simulated-agent evidence synthesis
- **Date:** 2026-07-09
- **Code version:** 0.10.26
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/playtest-findings-v0.10.16.md`
  - `docs/playtest-findings-v0.10.21.md`
  - `docs/playtest-findings-v0.10.22.md`
  - `docs/playtest-findings-v0.10.25.md`
- **Exemplar artifacts:**
  - `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
  - `_workspace/experiments/v0.10.24-access-debrief-validation/results.json`

This synthesis follows the `v0.10.25` routing checkpoint by stepping back from
the access follow-through mini-loop and comparing recent competitive playtest
evidence for teachability, debrief coherence, and repeated-play interest. It is
an evidence and project-state slice only. It does not add new runs and does not
change runtime mechanics, command grammar, validation rules, scenario schemas,
MCP DTOs, replay formats, state hash logic, action costs, access-pledge effects,
difficulty values, or balance.

## Evidence Chain

| Version | Evidence shape | Main teaching signal | Runtime change |
| --- | --- | --- | --- |
| `v0.10.16` | Live difficulty synthesis | Hard difficulty was most visible through decision friction and cash-pressure retries | No |
| `v0.10.21` | Live-capture synthesis | Existing capture surfaces were sufficient for bounded evidence gates | No |
| `v0.10.22` | Access-heavy comprehension review | The explanation was reviewable but distributed across diagnostics, history, and debriefs | No |
| `v0.10.25` | Access evidence synthesis | Access follow-through is now covered as debrief/guidance evidence, not mechanics evidence | No |

## Teachability Findings

1. The strongest current teaching surface is the relationship between public
   commitments, cash pressure, and durable operational follow-through. Recent
   access-heavy evidence gives students a concrete distinction between a visible
   pledge and the capacity, staffing, monitoring, payer, and project choices
   that make a pledge durable.
2. The current evidence supports structured debrief discussion more than
   balance tuning. Accepted command streams complete cleanly, while retry and
   low-cash signals show decision-process friction that can be explained through
   guidance, diagnostics, and end-of-run review.
3. Difficulty remains teachable when framed as constrained action selection,
   not as proof that the model needs formula changes. The recent Normal/Hard
   comparisons are useful for instructor prompts about adaptation, cash runway,
   and tradeoff visibility.

## Debrief Coherence Findings

1. The competitive debrief now has enough local explanation to make access-heavy
   low-cash runs interpretable without changing the deterministic core. The
   `v0.10.23` note and `v0.10.24` trigger/control validation closed the narrow
   follow-through explanation gap identified in `v0.10.22`.
2. The remaining coherence risk is cross-run comparison, not a missing single
   note. A learner or reviewer still has to connect diagnostics, monthly action
   history, final resources, and final tradeoff metrics to compare strategies
   across repeated plays.
3. Future debrief work should prefer instructor-facing comparison prompts or
   lightweight synthesis notes before adding new scoring categories or hidden
   optimization targets.

## Repeated-Play Interest Findings

1. The recent evidence suggests repeated play is most interesting when agents
   pursue visibly different strategic postures under the same campaign
   constraints. Static matrices remain useful controls, but observation-driven
   runs reveal richer decision pressure.
2. The next useful comparison is not another access-only loop. Prefer a broader
   strategy-space review that contrasts finance-first, access-heavy,
   workforce-protective, and growth-oriented play across existing artifacts.
3. Runtime changes should stay gated on a specific mechanics problem. Repeated
   pledge counts, retry metadata, or debrief visibility are not enough by
   themselves to justify cooldowns, command-cost changes, difficulty changes, or
   balance tuning.

## Recommended Routing

For the next PR-sized slice, prefer one of these paths:

- an instructor-facing comparison note that turns existing competitive evidence
  into discussion prompts about decision quality versus outcome quality;
- a strategy-space synthesis that compares several non-access-dominant profiles
  before choosing a new guidance or debrief intervention;
- a runtime mechanics investigation only if a later artifact identifies a
  concrete defect in command cost, validation, strategic behavior, or balance.

Do not reopen access-pledge cooldowns, effect tuning, action-cost changes,
difficulty adjustment, or new runtime validation from the current evidence.

## Evidence Limits

- These are simulated-agent, reviewer-policy, deterministic-policy, and
  operator-authored artifacts, not human play or classroom evidence.
- The strongest live decision-process signal still comes from a small number of
  profiles and seeds in one competitive campaign.
- Diagnostics and debriefs expose captured wrapper data and committed histories;
  they do not measure student learning or policy validity.
- This synthesis supports development routing, not empirical calibration,
  balance validation, or policy forecasting.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json
python3 -m json.tool _workspace/experiments/v0.10.24-access-debrief-validation/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.24-access-debrief-validation/results.json --output /tmp/hs-mgt-game-v0.10.26-diagnostics.md
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
git diff --check
```
