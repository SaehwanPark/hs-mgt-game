# Live Evidence Synthesis v0.10.21

- **Status:** Phase 7 simulated-agent evidence synthesis
- **Date:** 2026-07-08
- **Code version:** 0.10.21
- **Campaign:** `competitive-regional-v1`
- **Evidence inputs:**
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.12.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.13.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.14.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.15.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.16.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.17.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.18.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.19.md`
  - `docs/history/playtests/v0.10/playtest-findings-v0.10.20.md`
- **Exemplar artifact:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json`
- **Diagnostic report:** `_workspace/experiments/v0.10.15-live-llm-difficulty-gate/diagnostics.md`

This synthesis closes the immediate live-capture evidence-routing loop after the
retry visibility checkpoint. It does not add new runs and does not change
runtime mechanics, command grammar, validation rules, scenario schemas, MCP
DTOs, replay formats, state hash logic, action costs, or balance values.

## Evidence Matrix

| Version | Evidence shape | Sessions / scope | Main signal | Runtime change |
| --- | --- | ---: | --- | --- |
| `v0.10.12` | Live difficulty-pressure capture using existing automated policies | 24 sessions | Hard adaptive policies increased monitoring and preserved cash/workforce trust for some profiles | No |
| `v0.10.13` | Static-vs-adaptive live-capture comparison | 48 sessions | Hard adaptation changed action patterns and endpoint tradeoffs for growth/balanced profiles | No |
| `v0.10.14` | Independent reviewer-agent live capture | 18 sessions | Conservative reviewer policies completed cleanly but did not isolate difficulty because they were not difficulty-adaptive | No |
| `v0.10.15` | Live month-by-month LLM/sub-agent difficulty gate | 6 sessions | Access-heavy live play exposed cash-pressure retries that final replay validation did not show | No |
| `v0.10.16` | Cross-artifact difficulty synthesis | 4 findings docs | Selected cash-pressure and retry visibility as the next bounded issue | No |
| `v0.10.17` | Live retry diagnostic visibility | Diagnostic update | Separated final validation failures from live decision retries | No runtime mechanics |
| `v0.10.18` | Structured MCP validation errors | MCP interface hardening | Added classifiable resource-limit payloads while preserving plain errors | No runtime mechanics |
| `v0.10.19` | Wrapper preservation of structured retry metadata | Wrapper/diagnostic update | Preserved structured retry fields in live-capture artifacts and preferred them in diagnostics | No runtime mechanics |
| `v0.10.20` | Retry visibility checkpoint | Documentation checkpoint | Closed the current retry-classification gate and deferred runtime tuning | No |

## Synthesis Findings

1. The current live-capture workflow is sufficient for bounded Phase 7
   simulated-agent evidence gates. It can record actor-visible observations,
   legal command hints, submitted commands, final validation failures, live
   retry metadata, transition hashes, and debrief outputs without changing core
   runtime surfaces.
2. Static and deterministic matrices remain useful regression gates, but the
   strongest decision-process signal came from live month-by-month access-heavy
   play in `v0.10.15`.
3. Structured retry metadata now resolves the immediate ambiguity between
   accepted command-stream validity and rejected cash-overrun attempts during
   command selection.
4. Retry classification does not identify a runtime mechanic problem by itself.
   The accepted command streams completed cleanly, and the observed retry
   pressure remains a guidance, debrief, and command-surface review signal
   before it is a balance signal.
5. Repeated operator-authored or deterministic policy matrices should remain
   controls. They must not be counted as independent player samples or used to
   justify broad formula tuning.

## Recommended Next Evidence Gate

The next bounded slice should test whether **access-heavy players understand
public pledges versus durable operational follow-through** after the current
guidance and retry-visibility work.

Recommended first slice:

- keep runtime mechanics and validation rules unchanged;
- reuse the existing live-capture wrapper and diagnostic report shape;
- capture or synthesize a small set of access-heavy live sessions where the
  debrief explanation is reviewed for whether it distinguishes public access
  commitments, cash constraints, capacity/staffing action, payer negotiation,
  and final tradeoff outcomes;
- decide from that review whether the next intervention belongs in guidance,
  debrief wording, command-surface messaging, or a later runtime evidence gate.

Do not change access-pledge effects, add pledge cooldowns, tune command costs,
or adjust difficulty from the current evidence alone.

## Evidence Limits

- These are simulated-agent, reviewer-policy, and operator-authored artifacts,
  not human play or classroom evidence.
- The strongest live retry signal still comes from one campaign, one seed, and
  three live profiles in `v0.10.15`.
- Diagnostics parse captured wrapper data and debrief-derived summaries; they do
  not expose hidden active-play state.
- The synthesis supports evidence routing and product-risk selection, not
  empirical calibration, policy validity, human-learning claims, or balance
  validation.

## Verification

```bash
python3 -m json.tool _workspace/experiments/v0.10.12-live-difficulty-pressure/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.13-live-static-adaptive-capture/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.14-independent-reviewer-agent-capture/results.json >/dev/null
python3 -m json.tool _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json >/dev/null
python3 scripts/diagnose_runs.py tests/fixtures/live_capture_batch.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.15-live-llm-difficulty-gate/results.json --output /tmp/hs-mgt-game-v0.10.21-diagnostics.md
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
```
