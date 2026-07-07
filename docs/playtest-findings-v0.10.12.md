# Live Difficulty-Pressure Capture v0.10.12

- **Status:** Phase 7 simulated-agent evidence
- **Date:** 2026-07-07
- **Code version:** 0.10.12
- **Campaign:** `competitive-regional-v1`
- **Difficulties:** `normal`, `hard`
- **Seeds:** `42`, `43`, `44`
- **Source artifact:** `_workspace/experiments/v0.10.12-live-difficulty-pressure/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.12-live-difficulty-pressure/diagnostics.md`

This slice reuses the existing automated playtest profiles through the live MCP
capture wrapper. Hard runs use the existing difficulty-adaptive policy wrapper,
which adds rival-aware monitoring and pressure-sensitive command adjustments.
It is an evidence artifact only: no runtime mechanics, command grammar,
scenario schema, MCP DTO, replay format, state hash, or balance value changed.

## Run Matrix

| Profile | Difficulty | Seeds | Completed sessions | Validation failures | Access pledges |
| --- | --- | --- | ---: | ---: | ---: |
| Fiscal Caution | normal, hard | 42, 43, 44 | 6 | 0 | 12 |
| Capacity Growth | normal, hard | 42, 43, 44 | 6 | 0 | 6 |
| Balanced Strategy | normal, hard | 42, 43, 44 | 6 | 0 | 12 |
| Naive First-Time | normal, hard | 42, 43, 44 | 6 | 0 | 12 |

All 24 sessions completed the 24-month competitive campaign.

## Findings

1. The existing MCP wrapper captured the pressure-policy matrix without Rust MCP
   DTO changes. Each run includes actor-visible observations, legal command
   hints, submitted commands, validation outcomes, transition hashes, final
   observations, and debriefs.
2. No validation failures appeared across the 24 sessions.
3. Hard difficulty runs triggered more monitoring through the adaptive wrapper:
   all Hard profiles classified as `Intel-Gatherer`, while Normal runs were
   split between `Balanced Strategy` and `Intel-Gatherer`.
4. Capacity Growth and Balanced Strategy showed differentiated Normal/Hard
   endpoint metrics. Capacity Growth preserved more cash and workforce trust on
   Hard (`18` cash, `58` workforce trust) than Normal (`9` cash, `34`
   workforce trust), with slightly lower access and staffed beds. Balanced
   Strategy similarly preserved more cash and workforce trust on Hard (`10`
   cash, `55` workforce trust) than Normal (`1` cash, `48` workforce trust).
5. Fiscal Caution and Naive First-Time remained stable across difficulty labels
   for the tested endpoint metrics, suggesting those policies do not strongly
   exercise the added rival pressure.

## Evidence Limits

- These are deterministic simulated-agent policies, not human play or live LLM
  play.
- Three seeds, two difficulty labels, one campaign, and four scripted policies
  are insufficient for empirical calibration, balance changes, policy-validity
  claims, classroom-effectiveness claims, or human-learning claims.
- The Hard/Normal differences come partly from the existing adaptive policy
  wrapper, so they show a useful pressure-testing path rather than an isolated
  measurement of difficulty settings alone.
- The diagnostic parses final metrics from debrief text and does not expose
  hidden active-play state.

## Follow-Up Routing

- Use this slice as evidence that live capture can inspect pressure-seeking
  policies and Normal/Hard comparisons without changing runtime interfaces.
- If difficulty evidence remains a priority, next compare static and adaptive
  policies side by side in a single live-capture artifact before changing
  balance values.
- Keep runtime tuning, access-pledge cooldowns, and broad analytics tooling
  gated on stronger repeated evidence.

## Verification

```bash
python3 -m py_compile scripts/play_game.py
python3 -m py_compile scripts/run_automated_playtests.py
python3 -m py_compile _workspace/experiments/v0.10.12-live-difficulty-pressure/run_sessions.py
python3 _workspace/experiments/v0.10.12-live-difficulty-pressure/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json --output _workspace/experiments/v0.10.12-live-difficulty-pressure/diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
