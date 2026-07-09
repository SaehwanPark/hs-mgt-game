# Rival Information Pressure Design v0.10.36

- **Status:** Phase 7 difficulty design note
- **Date:** 2026-07-09
- **Code version:** 0.10.36
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/playtest-findings-v0.9.8.md`
  - `docs/playtest-findings-v0.9.9.md`
  - `docs/playtest-findings-v0.10.12.md`
  - `docs/playtest-findings-v0.10.15.md`
  - `docs/playtest-findings-v0.10.16.md`
  - `docs/playtest-findings-v0.10.20.md`
  - `docs/playtest-findings-v0.10.35.md`
  - `docs/expansion-proposal-review.md`
- **Exemplar artifacts:**
  - `_workspace/experiments/v0.9.8-difficulty-sweep/results.json`
  - `_workspace/experiments/v0.9.9-difficulty-adaptive/results.json`
  - `_workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
  - `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`

This note follows the `v0.10.35` difficulty pressure dimension gate. It defines
one bounded design surface for future difficulty work: rival information and
monitoring pressure visibility. The purpose is to make the next evidence or
implementation slice reviewable before changing runtime mechanics.

This slice does not add new playtest runs and does not change runtime
mechanics, command grammar, validation rules, scenario schemas, MCP DTOs,
replay formats, state hash logic, action costs, project costs, service-line
effects, difficulty values, scoring, or balance.

## Design Intent

Difficulty should make rival pressure more or less legible through observable
information conditions, not through hidden omniscience or arbitrary player
punishment. A future runtime slice, if promoted, should make tier differences
visible through what players can observe, monitor, and later explain in the
debrief.

The design hypothesis is that difficulty tiers can vary along three inspectable
information surfaces:

| Surface | Player-facing meaning | Design constraint |
| --- | --- | --- |
| Rival information delay | How stale rival summaries and market signals feel when decisions are made | Delays must be explicit observations, not rewritten history |
| Monitor value | How much actionable context a monitor command can reveal | Monitoring should improve traceability without becoming a mandatory tax |
| Public disclosure | How much rival action is visible without deliberate monitoring | Passive disclosure should differ by tier without exposing hidden true state |

## Tier Shape

The table below is a design target for future testing, not an implemented ruleset.

| Tier | Information posture | Monitoring posture | Review question |
| --- | --- | --- | --- |
| Easy | Rival pressure should be slower, more publicly legible, and easier to connect to final outcomes | Monitoring can confirm obvious signals and teach the habit without being necessary every month | Can a new player understand what rivals did without feeling surprised by hidden pressure? |
| Normal | Rival pressure should remain partly visible through public summaries, with occasional need to monitor before major commitments | Monitoring should clarify payer, rival, or market pressure when the player is making a consequential choice | Can the default campaign teach information tradeoffs without forcing one monitoring cadence? |
| Hard | Rival pressure should be more time-sensitive and less fully disclosed without deliberate monitoring | Monitoring should have clearer strategic value, especially before growth, payer, or access-heavy commitments | Can a disciplined player adapt to pressure without hidden rival omniscience or a single optimal path? |
| Expert | Rival pressure may be severe and faster-moving, but must remain auditable through explicit observations, histories, and debriefs | Monitoring may become a core survival tool, but Expert clearability must be validated before any claim of winnability | Can at least one strong strategy clear the tier through cash discipline, monitoring, workforce follow-through, and selective growth? |

## Promotion Criteria

Before implementing a runtime difficulty change from this design note, a future
slice should identify one concrete gap that current observations, histories,
diagnostics, or debriefs cannot already explain. Acceptable promotion evidence
includes:

1. monitored versus unmonitored Hard or Expert runs where later choices are not
   traceable from current artifacts;
2. reviewer or instructor feedback that the same final outcome is hard to
   explain because rival information timing is unclear;
3. a diagnostics finding showing monitor commands are frequent but not
   interpretable as decision support; or
4. a domain QA finding that a proposed difficulty tier would otherwise rely on
   hidden rival knowledge.

If promoted, the smallest runtime slice should change one surface only:
information delay, monitor value, or public disclosure. It should preserve
deterministic replay, actor-specific observations, append-only history, and
debrief attribution.

## Do Not Promote From This Note

Do not promote these changes from this design note alone:

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

- This note uses scripted, adaptive-policy, live-capture, reviewer-policy, and
  operator-authored artifacts, not human classroom observation.
- The tier shape is a design hypothesis, not empirical calibration or a tested
  learner model.
- Monitoring frequency is a pressure signal, not proof that monitoring improves
  learning, endpoint metrics, or strategy quality.
- Expert clearability remains unvalidated until a future evidence slice shows
  at least one severe but clearable path.
- This note supports future slice selection, not policy validity, forecasting,
  or runtime balance.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.9.8-difficulty-sweep/results.json
python3 -m json.tool _workspace/experiments/v0.9.9-difficulty-adaptive/results.json
python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json
git diff --check
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
```
