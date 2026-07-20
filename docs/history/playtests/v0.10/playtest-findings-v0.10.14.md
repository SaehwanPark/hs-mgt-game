# Independent Reviewer-Agent Live Capture v0.10.14

- **Status:** Phase 7 simulated-agent evidence
- **Date:** 2026-07-08
- **Code version:** 0.10.14
- **Campaign:** `competitive-regional-v1`
- **Difficulties:** `normal`, `hard`
- **Seeds:** `42`, `43`, `44`
- **Profiles:** Reviewer Fiscal Steward, Reviewer Access Operator, Reviewer Competitive Analyst
- **Source artifact:** `_workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.14-independent-reviewer-agent-capture/diagnostics.md`

This slice adds a bounded live MCP capture matrix using independent
observation-conditioned reviewer policies that are not copied from the existing
deterministic month-table profiles. It is an evidence artifact only: no runtime
mechanics, command grammar, scenario schema, MCP DTO, replay format, state hash,
or balance value changed.

## Run Matrix

| Difficulty | Profiles | Seeds | Completed sessions | Validation failures | Access pledges |
| --- | ---: | --- | ---: | ---: | ---: |
| normal | 3 | 42, 43, 44 | 9 | 0 | 3 |
| hard | 3 | 42, 43, 44 | 9 | 0 | 3 |

All 18 sessions completed the 24-month competitive campaign.

## Findings

1. The existing live MCP capture path supports independent reviewer-agent
   policies without changing Rust MCP DTOs, runtime exports, or shared
   diagnostics.
2. The reviewer policies completed all runs without validation failures while
   preserving conservative action budgets and at most one access pledge per run.
3. The Reviewer Access Operator produced the strongest access endpoint in this
   matrix (`79`) by combining one early access pledge with public-payer
   negotiation. The Fiscal Steward and Competitive Analyst both ended at access
   `68` while preserving different cash/quality/market-share tradeoffs.
4. Normal and Hard endpoint metrics were identical for each profile in this
   matrix. The policies are not difficulty-adaptive, so this does not isolate or
   validate difficulty balance.
5. Action patterns were distinct enough for diagnostic classification: Fiscal
   Steward was classified as Balanced Strategy, Access Operator as Conservative
   / Passive, and Competitive Analyst as Intel-Gatherer.

## Evidence Limits

- These are deterministic simulated-agent reviewer policies, not human play or
  live LLM play.
- Three profiles, three seeds, two difficulty labels, and one campaign are
  insufficient for empirical calibration, classroom-effectiveness claims,
  policy-validity claims, or runtime tuning.
- The policy heuristics are operator-authored and observation-conditioned; they
  are useful for comparison against earlier deterministic policies but are not
  independent human samples.
- The diagnostic parses final metrics from debrief text and does not expose
  hidden active-play state.

## Follow-Up Routing

- Treat this as stronger evidence that the current capture/diagnostic workflow
  can evaluate new bounded reviewer policies before runtime changes.
- Do not tune access pledges, difficulty, or balance formulas from this matrix.
- If difficulty remains the priority, the next gate should use either live LLM
  month-by-month decisions or a documented human-play observation protocol rather
  than another operator-authored deterministic policy family.

## Verification

```bash
python3 -m py_compile scripts/play_game.py
python3 -m py_compile scripts/run_automated_playtests.py
python3 -m py_compile scripts/diagnose_runs.py
python3 -m py_compile _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/run_sessions.py
python3 _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json --output _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json >/dev/null
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
