# Project-Recovery Use Diagnostics v0.10.56

- **Batch id:** v0.10.56-project-recovery-use
- **Code version:** 0.10.56
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** `hard`
- **Source:** `_workspace/experiments/v0.10.55-asc-project-observation/results.json` / v0.10.55-asc-project-observation
- **Evidence type:** deterministic response-conditioned project-limit recovery capture

## Run Summary

| Profile | Seed | Status | Transitions | Expected failures | Retries | Final hash |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| Project-Recovery Use / hard / seed 42 | 42 | complete | 24 | 1 | 1 | 09a3b81bb5eec4b3 |
| Project-Recovery Use / hard / seed 43 | 43 | complete | 24 | 1 | 1 | ec30c132f4d92155 |
| Project-Recovery Use / hard / seed 44 | 44 | complete | 24 | 1 | 1 | b62f7b549e4f0bf6 |

## Recovery Surface

- Stable `too_many_concurrent_projects` codes: 3/3.
- Response-conditioned recoveries: 3/3.
- Structured validation fields consumed: 0/3.
- Same-turn recovery observations: 3/3.
- Safe `hold` retries: 3/3.
- Debriefs explaining the two-project ceiling: 3/3.

## Interpretation

- The simulated policy selected `hold` from the plain project-limit error and unchanged actor-visible observation.
- No structured validation hint or resource-limit payload was consumed.
- These records support response-surface traceability only; they do not establish human comprehension, learning, or advice quality.

## Evidence Limits

- The project ceiling is a game abstraction, not an empirical health-system constraint.
- Response-conditioned simulated-policy behavior is traceability evidence, not human comprehension or learning evidence.
- The three-seed Hard matrix does not establish balance, winnability, strategy quality, calibration, or policy validity.
- Project validation hints and broader project guidance remain deferred unless a separate artifact identifies unexplained recovery failure.
