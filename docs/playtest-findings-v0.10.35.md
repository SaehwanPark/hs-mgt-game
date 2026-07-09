# Difficulty Pressure Dimension Gate v0.10.35

- **Status:** Phase 7 difficulty evidence gate
- **Date:** 2026-07-09
- **Code version:** 0.10.35
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/playtest-findings-v0.9.8.md`
  - `docs/playtest-findings-v0.9.9.md`
  - `docs/playtest-findings-v0.10.12.md`
  - `docs/playtest-findings-v0.10.13.md`
  - `docs/playtest-findings-v0.10.15.md`
  - `docs/playtest-findings-v0.10.16.md`
  - `docs/playtest-findings-v0.10.20.md`
  - `docs/expansion-proposal-review.md`
  - `docs/playtest-findings-v0.10.34.md`
- **Exemplar artifacts:**
  - `_workspace/experiments/v0.9.8-difficulty-sweep/results.json`
  - `_workspace/experiments/v0.9.9-difficulty-adaptive/results.json`
  - `_workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
  - `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
  - `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`

This gate reviews current difficulty evidence before promoting any difficulty
mechanic. It follows the `v0.10.34` instructor facilitation note and the
`v0.10.31` expansion proposal review. The purpose is to choose one visible
difficulty pressure dimension for future design or testing, not to change
balance.

This slice does not add new runs and does not change runtime mechanics,
command grammar, validation rules, scenario schemas, MCP DTOs, replay formats,
state hash logic, action costs, project costs, service-line effects,
difficulty values, scoring, or balance.

## Current Difficulty Surface

The current campaign already exposes difficulty through several bounded
surfaces:

| Surface | Current expression | Evidence reading |
| --- | --- | --- |
| Rival count | Easy has fewer rivals; Hard and Expert add more rivals | More rivals can increase market context, but current evidence does not isolate rival count from player policy adaptation |
| Human action budget | Expert lowers monthly human AP; Easy raises it | This is visible pressure, but Expert clearability is not validated by recent evidence |
| CPU action budget | Expert gives AI rivals more AP; Easy gives less | CPU AP is explicit, but hidden resource strength or omniscience should not be inferred |
| Adaptive playtest policy | Hard scripted policies add monitoring and reduce some aggressive investments | Useful for pressure testing, but partly measures the wrapper policy rather than difficulty alone |
| Live retry surface | Live Access Operator had more Hard retries than Normal in `v0.10.15` | Retry visibility is now addressed by `v0.10.20`; it should remain evidence metadata, not balance proof |
| Debrief comparison | Recent notes compare cash runway, follow-through, workforce posture, growth, and rival pressure | Strong for teachability, but not a validated assessment instrument |

## Selected Dimension

The next bounded difficulty dimension should be **rival information and
monitoring pressure visibility**.

Rationale:

1. Current difficulty evidence repeatedly shows monitoring as the top
   non-hold action in Hard pressure runs, especially in `v0.10.12` and
   `v0.10.15`.
2. The expansion review recommends harder tiers through visible pressure,
   information quality, and rival behavior rather than hidden omniscience or a
   punitive player-resource cut.
3. Recent instructor-facing notes already ask whether players adapted to rival
   and payer pressure, but current artifacts do not yet isolate whether
   difficulty changes are legible as information pressure rather than just
   more rivals or less slack.
4. Retry classification was already closed in `v0.10.20`, so the next
   difficulty gate should move away from resource-limit metadata and toward
   what players can observe, monitor, and explain.

## Recommended Next Slice

The next PR-sized follow-up, if difficulty remains the active priority, should
design or test one rival-information pressure surface. Good examples include:

- a documentation-only design note defining how Easy, Normal, Hard, and Expert
  should differ in rival information delay, monitor value, or public disclosure;
- a bounded evidence review comparing existing monitored versus unmonitored
  Hard runs for decision-quality traceability;
- a small diagnostics or debrief wording improvement only if reviewers cannot
  see whether monitoring changed later choices.

Any runtime implementation should wait until that follow-up identifies a
specific gap that current observations, histories, diagnostics, or debriefs
cannot already explain.

## Do Not Promote From This Gate

Do not promote these changes from this gate alone:

- Expert winnability claims;
- difficulty value changes;
- hidden rival omniscience;
- punitive player-resource cuts;
- broad balance passes;
- command-cost or AP-budget changes;
- access-pledge cooldowns;
- scoring redesign;
- new strategic actor classes;
- GUI, M&A, or release work.

## Evidence Limits

- This gate uses scripted, adaptive-policy, live-capture, reviewer-policy, and
  operator-authored artifacts, not human classroom observation.
- Current evidence uses one campaign, a small seed/profile set, and historical
  artifacts with different policy shapes.
- Monitoring frequency is a signal of pressure, not proof that monitoring
  improves learning, endpoint metrics, or strategy quality.
- This gate supports future slice selection, not empirical calibration, human
  learning measurement, policy validity, or forecasting.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.9.8-difficulty-sweep/results.json
python3 -m json.tool _workspace/experiments/v0.9.9-difficulty-adaptive/results.json
python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json
python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.35-diagnostics.md
git diff --check
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
```
