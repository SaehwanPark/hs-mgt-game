# Static-vs-Adaptive Live Capture v0.10.13

- **Status:** Phase 7 simulated-agent evidence
- **Date:** 2026-07-07
- **Code version:** 0.10.13
- **Campaign:** `competitive-regional-v1`
- **Difficulties:** `normal`, `hard`
- **Seeds:** `42`, `43`, `44`
- **Policy variants:** `static`, `adaptive`
- **Source artifact:** `_workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md`

This slice compares static deterministic profile policies against the existing
difficulty-adaptive wrapper in one live MCP capture artifact. It is an evidence
artifact only: no runtime mechanics, command grammar, scenario schema, MCP DTO,
replay format, state hash, or balance value changed.

## Run Matrix

| Variant | Difficulty | Profiles | Seeds | Completed sessions | Validation failures | Access pledges |
| --- | --- | --- | --- | ---: | ---: | ---: |
| static | normal, hard | 4 | 42, 43, 44 | 24 | 0 | 42 |
| adaptive | normal, hard | 4 | 42, 43, 44 | 24 | 0 | 42 |

All 48 sessions completed the 24-month competitive campaign.

## Findings

1. The live capture path supports a static/adaptive comparison artifact without
   changing Rust MCP DTOs or runtime exports. Each run includes actor-visible
   observations, legal command hints, submitted commands, validation outcomes,
   transition hashes, final observations, and debriefs.
2. Normal static and Normal adaptive runs are identical for all tested profiles,
   as expected: the adaptive wrapper only changes commands at Hard difficulty.
3. Hard adaptive runs increased monitoring compared with Hard static runs:
   Fiscal Caution increased from 18 to 33 monitor commands, Capacity Growth from
   24 to 39, Balanced Strategy from 30 to 39, and Naive First-Time from 12 to 36.
4. Capacity Growth and Balanced Strategy showed endpoint tradeoffs under Hard
   adaptation. Capacity Growth preserved more cash (`9` to `18`) and workforce
   trust (`34` to `58`) while ending with slightly lower access (`73` to `72`)
   and staffed beds (`121` to `119`). Balanced Strategy preserved more cash
   (`1` to `10`) and workforce trust (`48` to `55`) while ending with slightly
   lower access (`75` to `74`) and staffed beds (`121` to `119`).
5. Fiscal Caution and Naive First-Time showed higher monitoring under Hard
   adaptation but stable endpoint metrics for access, community trust, market
   share, and staffed beds in this seed/profile matrix.

## Evidence Limits

- These are deterministic simulated-agent policies, not human play or live LLM
  play.
- Three seeds, two difficulty labels, two policy variants, one campaign, and
  four scripted policies are insufficient for empirical calibration, balance
  changes, policy-validity claims, classroom-effectiveness claims, or human-
  learning claims.
- Static/adaptive differences reflect the policy wrapper's behavior, not an
  isolated measurement of difficulty settings alone.
- The diagnostic parses final metrics from debrief text and does not expose
  hidden active-play state.

## Follow-Up Routing

- Use this slice as evidence that the live capture workflow can compare policy
  variants side by side before runtime tuning.
- If difficulty evidence remains a priority, the next stronger gate should use
  a new bounded agent or reviewer policy that was not authored from the same
  deterministic profile scripts.
- Keep runtime tuning, access-pledge cooldowns, and broad analytics tooling
  gated on stronger repeated evidence.

## Verification

```bash
python3 -m py_compile scripts/play_game.py
python3 -m py_compile scripts/run_automated_playtests.py
python3 -m py_compile _workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py
python3 _workspace/experiments/v0.10.13-live-static-adaptive-capture/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json --output _workspace/experiments/v0.10.13-live-static-adaptive-capture/diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
