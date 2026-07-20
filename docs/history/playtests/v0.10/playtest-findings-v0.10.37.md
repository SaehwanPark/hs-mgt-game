# Rival Information Monitor Evidence v0.10.37

- **Status:** Phase 7 paired MCP evidence slice
- **Date:** 2026-07-09
- **Code version:** 0.10.37
- **Campaign:** `competitive-regional-v1`
- **Seed:** `42`
- **Difficulty:** Hard and Expert
- **Evidence artifact:**
  - `_workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json`
  - `_workspace/experiments/v0.10.37-rival-info-monitor-evidence/diagnostics.md`

This slice follows the `v0.10.36` rival information pressure design note. It
tests one surface, monitor value, by comparing paired deterministic policies
that differ only in alternating monitor months. The monitored policy spends
odd months monitoring a rotating rival; the unmonitored policy replaces those
commands with `hold`. Non-monitor commands are otherwise identical.

This slice does not change runtime mechanics, command validation, stochastic
inputs, scenario schemas, MCP DTOs, replay formats, state hash logic, action
costs, project costs, service-line effects, difficulty values, scoring, or
balance.

## Evidence Shape

All four sessions completed the full 24-month competitive campaign with zero
validation failures.

| Difficulty | Variant | Final hash | Monitor intel lines | Public rival lines | Private activity gaps |
| --- | --- | --- | ---: | ---: | ---: |
| Hard | Monitored | `df8d6c0da2f78dfb` | 3 | 46 | 23 |
| Hard | Unmonitored | `df8d6c0da2f78dfb` | 0 | 46 | 23 |
| Expert | Monitored | `a77df3947ba47a33` | 3 | 69 | 23 |
| Expert | Unmonitored | `a77df3947ba47a33` | 0 | 69 | 23 |

The identical paired hashes and endpoints are expected in this artifact because
monitor commands are observation-surface actions in the current runtime. They
change what the player can see, not the underlying transition state.

## Interpretation

- Monitoring exposed private rival information in actor-visible observations
  that the unmonitored paired runs did not receive.
- The current public disclosure surface already exposes many rival actions,
  especially in Expert because the extra rival increases public-action volume.
- Private activity gaps remained visible in both monitored and unmonitored
  runs, so the game already tells players where information is incomplete.
- This artifact supports keeping monitor value as an observation and debrief
  traceability question before changing runtime difficulty mechanics.

## Routing

The next difficulty follow-up should stay evidence-led. Useful follow-ups would
compare whether players or reviewer policies actually change later decisions
after monitor intel, or whether Expert needs a broader clearability matrix. This
artifact alone does not justify tuning monitor costs, AP budgets, difficulty
values, rival AI, or public disclosure rules.

## Evidence Limits

- These are deterministic simulated-agent policies, not human classroom
  observations.
- The paired policy intentionally holds unmonitored months; it is a controlled
  information comparison, not a recommended player strategy.
- Identical final hashes do not prove monitoring lacks educational value; they
  only show that the current monitor surface affects observations rather than
  transition state.
- Expert completion under this conservative policy is not an Expert
  winnability claim across strategies, seeds, scenarios, or player skill.
- No empirical calibration, policy-validity, human-learning, scoring, or
  balance claim is made.

## Verification

```bash
python3 -m py_compile scripts/diagnose_runs.py _workspace/experiments/v0.10.37-rival-info-monitor-evidence/run_sessions.py
python3 _workspace/experiments/v0.10.37-rival-info-monitor-evidence/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json
python3 scripts/diagnose_runs.py _workspace/experiments/v0.10.37-rival-info-monitor-evidence/results.json --output _workspace/experiments/v0.10.37-rival-info-monitor-evidence/diagnostics.md
git diff --check
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test -- --test-threads=1
```
