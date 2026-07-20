# Expert Difficulty Validation v0.11.9

- **Status:** Phase 7 competitive difficulty clearability evidence after the
  v0.11.7 risk-posture and v0.11.8 resource-scaling changes
- **Date:** 2026-07-12
- **Code version:** 0.11.9
- **Campaign:** `competitive-regional-v1`
- **Matrix:** Access First, Commercial Focus, Workforce Resilience, Capital
  Modernization, and Coalition/Legitimacy profiles across seeds 42, 43, and 44
  at Expert difficulty
- **Evidence artifact:**
  `_workspace/experiments/v0.11.9-expert-difficulty-validation/results.json`

This slice tests bounded Expert campaign completion using deterministic
scripted policy lanes after the new difficulty posture and rival starting
resource dimensions. It does not change runtime mechanics, commands, scenarios,
replay formats, MCP schemas, state hashes, scoring, balance, or difficulty
values.

## Result

All 15 runs completed the full 24-month campaign with zero validation failures.
Each run retained actor-visible observations, legal command hints, submitted
commands, transition history, state hashes, and the final debrief.

| Profile | Seeds completed | Validation failures |
| --- | ---: | ---: |
| Access First | 42, 43, 44 | 0 |
| Commercial Focus | 42, 43, 44 | 0 |
| Workforce Resilience | 42, 43, 44 | 0 |
| Capital Modernization | 42, 43, 44 | 0 |
| Coalition/Legitimacy | 42, 43, 44 | 0 |

## Interpretation and Routing

The matrix provides limited evidence that Expert remains clearable for these
deterministic simulated policies and seeds after the recent difficulty
expansion. It does not establish general Expert winnability, balance, strategy
quality, causal value, human learning, empirical calibration, or policy
validity.

Keep Expert rules unchanged. Runtime difficulty tuning remains deferred until a
concrete player-facing, instructor-facing, or domain-review gap appears that
current observations, histories, diagnostics, and debriefs cannot explain.

## Evidence Limits

- These are deterministic simulated-policy traces, not human or classroom
  sessions.
- Full campaign completion is a bounded clearability proxy, not a formal win
  condition or broad winnability claim.
- Five profiles and three seeds do not establish all strategy families,
  scenarios, stochastic conditions, or player skill levels.
- Endpoint hashes and metrics are descriptive outcomes, not causal comparisons
  between randomized treatments.

## Verification

```bash
python3 -m py_compile _workspace/experiments/v0.11.9-expert-difficulty-validation/run_sessions.py
python3 -m unittest tests/test_expert_difficulty_validation.py
python3 _workspace/experiments/v0.11.9-expert-difficulty-validation/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.11.9-expert-difficulty-validation/results.json
python3 -m unittest discover -s tests -p 'test_*.py'
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
python3 scripts/run_automated_playtests.py
git diff --check
```
