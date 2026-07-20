# Rival Information Follow-Through Evidence v0.10.43

- **Status:** Phase 7 competitive teachability and validation evidence
- **Date:** 2026-07-10
- **Code version:** 0.10.43
- **Campaign:** `competitive-regional-v1`
- **Matrix:** seeds 42–44; Hard and Expert; monitor-reactive,
  monitor-ignoring, and unmonitored policies
- **Evidence artifact:**
  `_workspace/experiments/v0.10.43-rival-info-follow-through/results.json`

This slice follows the v0.10.37 monitor-value capture. It tests whether a
deterministic policy changes its next-month command after receiving rival intel
through the actor-visible monitor surface. It does not change runtime behavior
or treat policy differences as causal outcome evidence.

## Questions

1. Does the monitor signal appear in the next actor-visible observation with a
   source month that can be traced?
2. Does a monitor-reactive policy submit a deterministic response on that next
   turn using only visible text and resource hints?
3. Does the monitor-ignoring control receive the same signal but preserve its
   baseline command stream?
4. Do monitor-ignoring and unmonitored controls preserve identical state hashes,
   confirming that monitoring remains an observation-only surface?

## Result

All 18 runs completed the full 24-month campaign with zero validation failures.
Each monitor arm exposed three visible monitor-intel records per run. Every
monitor-reactive run recorded three next-turn responses to visible payer
signals. Every monitor-ignoring run retained the signals but marked them as
ignored. The monitor-ignoring and unmonitored controls matched state hashes for
all six seed/difficulty pairs.

The reactive policy changed commands after the visible payer signal, producing
different endpoint hashes from the controls. Those endpoint differences are
expected policy differences and are not evidence of causal monitor value,
decision quality, balance, or learning.

## Interpretation and Routing

The current observation surface is sufficient to trace a visible monitor signal
to a subsequent simulated-policy decision. The evidence does not identify a
runtime information-delay, monitor-cost, public-disclosure, difficulty, or
balance defect. Keep monitor mechanics unchanged and retain the result as a
teachability/debrief traceability artifact.

Future runtime changes require a separate finding showing that human or
reviewer-facing explanation cannot be recovered from current observations,
histories, diagnostics, and debriefs.

## Non-Goals and Evidence Limits

- No runtime, MCP schema, scenario, replay, state-hash, ruleset, difficulty,
  scoring, balance, or rival-AI change.
- No human-learning, advice-quality, policy-validity, or empirical-calibration
  claim.
- The three arms are deterministic simulated policies, not human treatments.
- Reactive endpoint differences cannot establish causal monitor benefit because
  the policies intentionally submit different commands.

## Verification

```bash
python3 -m py_compile _workspace/experiments/v0.10.43-rival-info-follow-through/run_sessions.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 _workspace/experiments/v0.10.43-rival-info-follow-through/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.43-rival-info-follow-through/results.json
python3 scripts/run_automated_playtests.py
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
git diff --check
```
