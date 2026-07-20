# Project-Limit Recovery Evidence v0.10.54

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-11
- **Code version:** 0.10.54
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** Hard
- **Seeds:** 42, 43, and 44
- **Source artifact:** v0.10.51 adversarial resource probe
- **Capture artifact:**
  `_workspace/experiments/v0.10.54-project-limit-recovery/results.json`

This deterministic wrapper-boundary capture narrows the v0.10.51
`too_many_concurrent_projects` trace fact into one recovery question. It starts
two valid projects, submits a third project, preserves the rejected-turn
surface, retries with `hold`, and completes the campaign without changing
runtime behavior.

## Result

All three runs completed 24 months. Each run accepted a clinic-network project
in month 4 and an ASC project in month 6, then rejected a neurology-unit project
in month 7 with `too_many_concurrent_projects`.

The rejected command left the turn and actor-visible observation unchanged.
One `hold` retry advanced each run exactly once. The MCP response retained the
stable code and the plain error `concurrent projects 3 exceed limit 2`; it did
not include a structured `resource_limit` or `hint`. Each final debrief retained
the existing explanation that capital projects are limited to two concurrent
projects.

## Interpretation and Routing

The current surface supports machine-readable rejection, same-turn recovery,
and retrospective explanation across the tested seeds. The absent structured
hint remains a reproducible trace fact, not a demonstrated comprehension or
interface defect. Runtime and validation-hint promotion remain deferred.

A later player-facing, instructor-facing, or domain-review artifact would need
to show unexplained repeated project submissions or failed recovery before a
hint change moves into `SPEC.md` Present.

## Evidence Limits

- The two-project ceiling is a game abstraction, not a calibrated real-world
  health-system constraint.
- The probe is a deterministic simulated policy, not human or classroom
  evidence.
- Stable error codes, safe retries, and debrief coverage do not establish human
  comprehension, learning, strategy quality, balance, or winnability.
- Three seeds, one campaign, and one difficulty do not support calibration or
  policy-validity claims.

## Verification

```bash
cargo build --quiet --bin hs-mgt-game-mcp
python3 -m py_compile _workspace/experiments/v0.10.54-project-limit-recovery/run_sessions.py tests/test_project_limit_recovery.py
python3 -m unittest tests/test_project_limit_recovery.py
python3 _workspace/experiments/v0.10.54-project-limit-recovery/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.54-project-limit-recovery/results.json
```
