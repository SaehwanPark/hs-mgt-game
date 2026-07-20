# Access-Heavy Comprehension Evidence Review v0.10.22

- **Status:** Phase 7 simulated-agent evidence review
- **Date:** 2026-07-08
- **Code version:** 0.10.22
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.15.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.16.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.20.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.21.md`
- **Exemplar artifact:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`

This review follows the `v0.10.21` routing question: whether access-heavy
players can distinguish public access pledges from durable operational
follow-through under cash pressure. It uses existing live-capture evidence only.
It does not add new runs and does not change runtime mechanics, command grammar,
validation rules, scenario schemas, MCP DTOs, replay formats, state hash logic,
action costs, access-pledge effects, or balance values.

## Evidence Slice

| Run | Difficulty | Access pledges | Live retries | Cash-overrun retries | Final cash | Final access | Final quality | Workforce trust | Community trust | Final hash |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Live Access Operator / seed 42 | Normal | 1 | 2 | 1 | 0 | 71 | 72 | 50 | 65 | `ac0dfcdf3cf099e4` |
| Live Access Operator / seed 42 | Hard | 2 | 7 | 6 | 0 | 75 | 81 | 56 | 66 | `8b14af9072eb9c1c` |

Both accepted command streams completed the 24-month campaign with zero final
validation failures. The rejected attempts are visible only through live retry
metadata captured during command selection.

## Comprehension Findings

1. The current artifact and diagnostic surfaces are sufficient for reviewer
   comprehension. They expose access pledge counts, accepted command streams,
   live retry counts, cash-overrun classification, final tradeoff metrics, and
   detailed debrief text without changing runtime behavior.
2. The debrief already distinguishes public commitments from observed outcomes
   indirectly: it lists the player's committed commands by month, rival public
   and private actions, final resources, and final tradeoff metrics. A reviewer
   can see that repeated access commitments do not prevent cash exhaustion.
3. The current player-facing explanation is still distributed across several
   surfaces. Understanding requires reading diagnostics for retry pressure,
   debrief logs for accepted commands, and final outcomes for operational
   tradeoffs. That is adequate for Phase 7 evidence review, but not ideal as a
   classroom or first-time-player explanation.
4. The strongest intervention candidate is debrief wording, not runtime tuning.
   A future slice should add a concise access-follow-through debrief note when a
   run combines public access pledges, low ending cash, and limited operational
   follow-through. That note should stay explanatory rather than punitive.
5. Command-surface or balance changes are not justified by this evidence. The
   accepted streams completed cleanly, and the retry signal shows action-selection
   friction under cash pressure rather than a proven mechanic defect.

## Follow-Up Routing

Recommended next PR-sized slice:

- add a focused competitive debrief explanation for access-heavy runs that
  separates public access pledges from durable follow-through actions such as
  capacity investment, staffing, monitoring, and payer posture;
- cover the wording with debrief tests using existing deterministic fixtures;
- preserve action costs, pledge effects, validation rules, and difficulty values.

Keep guidance wording, command-surface messaging, access-pledge cooldowns,
command-cost tuning, difficulty adjustment, and runtime balance changes deferred
until that debrief slice is reviewed.

## Evidence Limits

- These are simulated-agent and operator-authored artifacts, not human play or
  classroom evidence.
- The strongest access-heavy signal still comes from one campaign, one seed,
  and one live profile across Normal and Hard difficulty.
- Diagnostics parse captured wrapper data and debrief-derived summaries; they do
  not expose hidden active-play state.
- This review supports product-risk routing, not empirical calibration, policy
  validity, human-learning claims, or balance validation.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.22-diagnostics.md
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
git diff --check
```
