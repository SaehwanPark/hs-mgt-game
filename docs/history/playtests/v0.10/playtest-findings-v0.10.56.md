# Project-Recovery Use Evidence v0.10.56

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-11
- **Code version:** 0.10.56
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** Hard
- **Seeds:** 42, 43, and 44
- **Source artifact:** v0.10.55 ASC project observation capture
- **Capture artifact:**
  `_workspace/experiments/v0.10.56-project-recovery-use/results.json`

## Evidence question

Does the current project-limit response support a response-conditioned recovery
path using only the plain validation error and unchanged actor-visible
observation, without consuming structured validation fields?

## Result

All three runs accepted the clinic and ASC projects, rejected the third project
with `too_many_concurrent_projects`, preserved the same turn and observation,
selected `hold` from the plain error plus visible project state, and completed
24 transitions. The accepted-transition state hashes match v0.10.55 exactly.

| Measure | Result |
| --- | ---: |
| Stable project-limit codes | 3/3 |
| Response-conditioned recoveries | 3/3 |
| Structured validation fields consumed | 0/3 |
| Same-turn rejected observations | 3/3 |
| Safe `hold` retries | 3/3 |
| Debriefs explaining the project ceiling | 3/3 |

## Interpretation and routing

The existing plain project-limit response is sufficient for this deterministic
simulated policy to select a safe retry. This closes the current response-use
traceability question without identifying unexplained recovery friction.

Keep structured validation hints, resource payloads, broader project guidance,
and runtime tuning deferred. A future promotion requires player-facing,
instructor-facing, or domain-review evidence of a concrete recovery failure.

## Evidence limits

- The project ceiling is a game abstraction, not an empirical health-system
  constraint.
- The capture is deterministic simulated-policy evidence, not human or
  classroom evidence.
- Response-conditioned recovery does not establish comprehension, learning,
  advice quality, strategy quality, balance, winnability, calibration, or policy
  validity.

## Verification

```bash
python3 _workspace/experiments/v0.10.56-project-recovery-use/run_sessions.py
python3 -m unittest tests/test_project_recovery_use.py
python3 -m json.tool _workspace/experiments/v0.10.56-project-recovery-use/results.json
```
