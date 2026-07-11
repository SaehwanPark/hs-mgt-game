# Expert Clearability Evidence v0.10.46

- **Status:** Phase 7 competitive difficulty and winnability evidence gate
- **Date:** 2026-07-10
- **Code version:** 0.10.46
- **Campaign:** `competitive-regional-v1`
- **Matrix:** Fiscal Caution, Capacity Growth, Balanced Strategy, and Naive
  First-Time profiles across seeds 42, 43, and 44 at Expert difficulty
- **Evidence artifact:**
  `_workspace/experiments/v0.10.46-expert-clearability-evidence/results.json`

This slice tests bounded Expert campaign completion using the existing scripted
profiles. It does not change difficulty values, runtime mechanics, commands,
scenarios, replay formats, MCP schemas, state hashes, scoring, or balance.

## Result

All 12 runs completed the full 24-month campaign with zero validation failures.
Each run retained actor-visible observations, legal command hints, submitted
commands, transition history, state hashes, and the final debrief.

Completion was observed for all four profiles across all three named seeds:

| Profile | Seeds completed | Validation failures |
| --- | ---: | ---: |
| Fiscal Caution | 42, 43, 44 | 0 |
| Capacity Growth | 42, 43, 44 | 0 |
| Balanced Strategy | 42, 43, 44 | 0 |
| Naive First-Time | 42, 43, 44 | 0 |

## Interpretation and Routing

The matrix provides limited evidence that the current Expert campaign is
completable by these deterministic policies across these seeds. It does not
establish general Expert winnability, balance, strategy quality, causal value,
human learning, or policy validity.

Keep Expert rules and rival information mechanics unchanged. Do not promote a
runtime difficulty change from this artifact alone. Future work should require
a concrete player-facing, instructor-facing, or domain-review gap that current
observations, history, diagnostics, and debriefs cannot explain.

## Evidence Limits

- These are deterministic simulated-policy traces, not human or classroom
  sessions.
- Full campaign completion is a bounded clearability proxy, not a formal win
  condition or broad winnability claim.
- Four profiles and three seeds do not establish all strategy families,
  scenarios, stochastic conditions, or player skill levels.
- Endpoint hashes and metrics are descriptive outcomes, not causal comparisons
  between randomized treatments.

## Verification

```bash
python3 -m py_compile _workspace/experiments/v0.10.46-expert-clearability-evidence/run_sessions.py
python3 -m unittest tests/test_expert_clearability_evidence.py
python3 _workspace/experiments/v0.10.46-expert-clearability-evidence/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.46-expert-clearability-evidence/results.json
python3 -m unittest discover -s tests -p 'test_*.py'
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
python3 scripts/run_automated_playtests.py
git diff --check
```
