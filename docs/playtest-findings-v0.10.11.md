# Live-Capture Matrix v0.10.11

- **Status:** Phase 7 simulated-agent evidence
- **Date:** 2026-07-07
- **Code version:** 0.10.11
- **Campaign:** `competitive-regional-v1`
- **Difficulties:** `normal`, `hard`
- **Seeds:** `42`, `43`, `44`
- **Source artifact:** `_workspace/experiments/v0.10.11-live-capture-matrix/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.11-live-capture-matrix/diagnostics.md`

This slice expands the v0.10.9 live MCP capture path into a small matrix over
the same three deterministic persona policies. It is an evidence artifact only:
no runtime mechanics, command grammar, scenario schema, MCP DTO, replay format,
state hash, or balance value changed.

## Run Matrix

| Profile | Difficulty | Seeds | Completed sessions | Validation failures | Access pledges |
| --- | --- | --- | ---: | ---: | ---: |
| Solvency Monitor | normal, hard | 42, 43, 44 | 6 | 0 | 0 |
| Access Operations | normal, hard | 42, 43, 44 | 6 | 0 | 6 |
| Workforce Quality | normal, hard | 42, 43, 44 | 6 | 0 | 0 |

All 18 sessions completed the 24-month competitive campaign.

## Findings

1. The existing Python MCP wrapper captured the full matrix without Rust MCP DTO
   changes. Each run includes actor-visible observations, legal command hints,
   submitted commands, validation outcomes, transition hashes, final
   observations, and debriefs.
2. No validation failures appeared across the 18 sessions.
3. Access pledges remained bounded by policy design: Access Operations made one
   access pledge per run, while Solvency Monitor and Workforce Quality made none.
4. Endpoint metrics were stable across the tested seeds and difficulty labels
   for these conservative persona policies. Access Operations ended with cash
   `35`, access `73`, quality `75`, workforce trust `58`, community trust `65`,
   and market share `24`; the other two profiles preserved cash `60`, access
   `68`, quality `74`, workforce trust `60`, and community trust `64`.
5. The identical endpoint ranges across Normal and Hard for this matrix are a
   cue about conservative policy coverage, not proof that difficulty tiers are
   fully differentiated or balanced.

## Evidence Limits

- These are deterministic simulated-agent policies, not human play or live LLM
  play.
- Three seeds, two difficulty labels, one campaign, and three conservative
  policies are insufficient for balance conclusions, empirical calibration,
  policy-validity claims, classroom-effectiveness claims, or human-learning
  claims.
- The repeated policies are controls for capture stability and diagnostic
  comparison; they should not be counted as independent player samples.
- The diagnostic parses final metrics from debrief text and does not expose
  hidden active-play state.

## Follow-Up Routing

- Use this matrix as workflow evidence that the live-capture path can support
  seed/difficulty slices without changing runtime interfaces.
- If future work needs stronger difficulty evidence, use less conservative
  observation-driven policies or human/LLM play before changing balance values.
- Keep access-pledge cooldowns and pledge-effect tuning gated on stronger
  repeated evidence; this slice does not justify runtime tuning.

## Verification

```bash
python3 -m py_compile scripts/play_game.py
python3 -m py_compile _workspace/experiments/v0.10.11-live-capture-matrix/run_sessions.py
python3 _workspace/experiments/v0.10.11-live-capture-matrix/run_sessions.py
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.11-live-capture-matrix/results.json --output _workspace/experiments/v0.10.11-live-capture-matrix/diagnostics.md
python3 -m json.tool _workspace/experiments/v0.10.11-live-capture-matrix/results.json >/dev/null
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```
