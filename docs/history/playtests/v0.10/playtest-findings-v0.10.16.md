# Live Difficulty Evidence Synthesis v0.10.16

- **Status:** Phase 7 simulated-agent evidence synthesis
- **Date:** 2026-07-08
- **Code version:** 0.10.16
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.12.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.13.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.14.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.15.md`

This slice compares the recent live-capture difficulty evidence before any
runtime tuning. It is synthesis only: no runtime mechanics, command grammar,
scenario schema, MCP DTO, replay format, state hash logic, or balance value
changed.

## Evidence Matrix

| Version | Evidence shape | Sessions | Seeds | Difficulty tiers | Profiles / policies | Validation signal |
| --- | --- | ---: | --- | --- | --- | --- |
| `v0.10.12` | Live difficulty-pressure capture using the existing adaptive wrapper | 24 | `42`, `43`, `44` | Normal, Hard | 4 scripted policies | 0 final validation failures |
| `v0.10.13` | Static-vs-adaptive live-capture comparison | 48 | `42`, `43`, `44` | Normal, Hard | 4 scripted policies x 2 variants | 0 final validation failures |
| `v0.10.14` | Independent reviewer-agent live capture | 18 | `42`, `43`, `44` | Normal, Hard | 3 reviewer policies | 0 final validation failures |
| `v0.10.15` | Live LLM/sub-agent difficulty gate | 6 | `42` | Normal, Hard | 3 live profiles | 0 final validation failures; 9 live retries |

Across these inputs, all accepted command streams completed the 24-month
competitive campaign. The strongest new signal came from `v0.10.15`, where the
Live Access Operator exposed cash-pressure retries that did not appear in the
final replay validation count.

## Synthesis Findings

1. Static and deterministic policy matrices are useful regression gates, but
   they can hide decision-process pressure. `v0.10.12` and `v0.10.13` completed
   broad Normal/Hard matrices without final validation failures, while
   `v0.10.15` showed live retries during command selection.
2. Non-adaptive reviewer policies are not difficulty evidence by themselves.
   `v0.10.14` produced identical Normal/Hard endpoints for each profile because
   the policies did not branch on difficulty-visible pressure.
3. Hard difficulty is currently most visible through action-selection friction,
   not through a validated balance conclusion. The Access Operator needed seven
   Hard live retries and two Normal live retries, mostly after cash depletion,
   even though the accepted command streams later replayed cleanly.
4. Access-heavy play remains the most useful follow-up surface. It combines
   repeated public access commitments, depleted cash, and validation retries in
   a way that could affect player guidance, debrief review, or validation
   messaging before any balance formula changes.

## Selected Next Issue

The next bounded development issue should be **cash-pressure and validation-retry
visibility for access-heavy live agents under Hard difficulty**.

Recommended first slice:

- Preserve runtime mechanics and validation rules.
- Improve the evidence or player-facing explanation surface that distinguishes
  accepted command streams from rejected or retried cash-overrun attempts.
- Prefer guidance, debrief, or diagnostic wording before changing balance
  values, cooldowns, command costs, or action availability.

## Evidence Limits

- These are simulated-agent and operator-authored evidence artifacts, not human
  play, classroom learning evidence, empirical calibration, or policy-validity
  evidence.
- The matrices reuse one campaign and a small set of seeds/profiles.
- Final diagnostics parse debrief text and do not expose hidden active-play
  state.
- The `v0.10.15` live retry signal is useful for choosing a follow-up issue, not
  sufficient for runtime tuning by itself.

## Follow-Up Routing

- Do not tune difficulty, access pledges, command costs, or balance formulas from
  this synthesis alone.
- If implementation continues from this issue, keep the next PR narrow:
  guidance/debrief/diagnostic visibility first; runtime tuning only after a
  later evidence gate names a concrete mechanism problem.
- Continue recording retry/source metadata for live-decision evidence.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
