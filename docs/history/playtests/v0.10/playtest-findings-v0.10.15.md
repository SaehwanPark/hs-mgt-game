# Live LLM Difficulty Gate v0.10.15

- **Status:** Phase 7 simulated-agent evidence
- **Date:** 2026-07-08
- **Code version:** 0.10.15
- **Campaign:** `competitive-regional-v1`
- **Difficulties:** `normal`, `hard`
- **Seed:** `42`
- **Profiles:** Live Fiscal Steward, Live Access Operator, Live Competitive Analyst
- **Source artifact:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`

This slice captures live month-by-month simulated-agent decisions from
actor-visible MCP observations and legal command hints, then replays the
accepted command streams through the existing observation-by-observation wrapper.
It is evidence only: no runtime mechanics, command grammar, scenario schema, MCP
DTO, replay format, state hash logic, or balance value changed.

## Run Matrix

| Difficulty | Profiles | Seed | Completed sessions | Final validation failures | Live retries | Access pledges |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| normal | 3 | 42 | 3 | 0 | 2 | 1 |
| hard | 3 | 42 | 3 | 0 | 7 | 2 |

All six replayed sessions completed the 24-month competitive campaign.

## Outcomes

| Profile | Difficulty | Cash | Access | Quality | Workforce Trust | Community Trust | Market Share | Final Hash |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Live Fiscal Steward | normal | 33 | 71 | 77 | 58 | 64 | 26 | `57a5496602fccaf6` |
| Live Fiscal Steward | hard | 40 | 68 | 72 | 56 | 64 | 28 | `23d4f7b21ec7386d` |
| Live Competitive Analyst | normal | 20 | 68 | 80 | 60 | 64 | 27 | `19aefaeb7adfe428` |
| Live Competitive Analyst | hard | 18 | 68 | 81 | 60 | 64 | 26 | `a40f40a8fce52d0c` |
| Live Access Operator | normal | 0 | 71 | 72 | 50 | 65 | 34 | `ac0dfcdf3cf099e4` |
| Live Access Operator | hard | 0 | 75 | 81 | 56 | 66 | 29 | `8b14af9072eb9c1c` |

## Findings

1. Live month-by-month decisions produced difficulty-specific behavior and
   endpoint differences without runtime changes. This is a stronger gate than
   static operator policies, but still too small for balance conclusions.
2. The Access Operator exposed the most useful pressure signal: Hard play needed
   seven live retries before the final accepted stream, mostly after cash was
   depleted, while Normal needed two retries and also ended with cash `0`.
3. The Fiscal Steward and Competitive Analyst completed both difficulty tiers
   with zero retries, no access pledges, and more conservative action sets.
4. The Hard Access Operator reached higher access, quality, workforce trust, and
   community trust than its Normal counterpart, but with repeated fallback
   behavior after cash reached `0`; this should be read as decision-process
   evidence, not as balance proof.
5. The delegated Competitive Analyst Normal session did not complete. The
   committed artifact uses a replacement local live decision stream from the
   same MCP observation/legal-command surface and records that source difference
   in the artifact.

## Evidence Limits

- These are simulated-agent decisions, not human play.
- One seed, one campaign, three profiles, and two difficulty tiers are not enough
  for empirical calibration, classroom-effectiveness claims, policy-validity
  claims, or runtime tuning.
- The replay artifact validates accepted command streams; it does not preserve
  every intermediate prompt from the delegated live sessions.
- The diagnostic parses final metrics from debrief text and does not expose
  hidden active-play state.

## Follow-Up Routing

- Treat this as evidence that live month-by-month agents can expose validation
  and cash-pressure differences that static policies hide.
- Do not tune difficulty, access pledges, or balance formulas from this slice by
  itself.
- If difficulty remains the priority, the next useful step is a synthesis that
  compares this live gate against `v0.10.12` through `v0.10.14` and identifies
  one concrete guidance, debrief, or validation issue before any runtime tuning.

## Verification

```bash
python3 -m py_compile scripts/play_game.py
python3 -m py_compile scripts/diagnose_runs.py
python3 -m py_compile _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py
python3 _workspace/experiments/v0.10.15-live-llm-difficulty-gate/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output _workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
