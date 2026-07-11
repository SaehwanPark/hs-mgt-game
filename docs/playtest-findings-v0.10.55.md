# ASC Project Observation Coverage v0.10.55

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-11
- **Code version:** 0.10.55
- **Campaign:** `competitive-regional-v1`
- **Difficulty:** Hard
- **Seeds:** 42, 43, and 44
- **Source artifact:** v0.10.54 project-limit recovery capture
- **Capture artifact:**
  `_workspace/experiments/v0.10.55-asc-project-observation/results.json`

This deterministic wrapper-boundary capture verifies a concrete observation
gap found in the v0.10.54 project-limit schedule. An accepted ASC project was
counted by validation and charged its monthly draw but was not rendered in the
human actor's `In-flight projects` observation.

## Result

The observer now displays both active projects at month 7:

```text
In-flight projects: ClinicNetwork (6 mos left, $2k/mo draw), AscUnit (5 mos left, $1k/mo draw)
```

All three runs accepted the clinic and ASC projects, rejected the third project
with `too_many_concurrent_projects`, preserved the same-turn observation, and
advanced exactly once after a safe `hold` retry. All 24 transition hashes per
seed match the v0.10.54 source artifact.

## Interpretation and routing

This slice fixes a concrete actor-visible traceability gap without changing
project limits, validation hints, transition semantics, replay behavior,
debrief wording, balance, or difficulty. Structured project hints and broader
project guidance remain deferred until separate evidence identifies unexplained
decision friction.

## Evidence limits

- The ASC project is a game abstraction, not an empirical health-system
  constraint.
- The capture is deterministic simulated-policy evidence, not human or
  classroom evidence.
- Visibility and hash continuity do not establish comprehension, learning,
  strategy quality, balance, winnability, calibration, or policy validity.

## Verification

```bash
python3 -m unittest tests/test_asc_project_observation.py
python3 _workspace/experiments/v0.10.55-asc-project-observation/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.55-asc-project-observation/results.json
```
