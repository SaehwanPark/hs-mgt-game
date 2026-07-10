# Consultant Advice Usage Evidence v0.10.41

- **Status:** Phase 7 competitive teachability and validation evidence
- **Campaign:** `competitive-regional-v1`
- **Matrix:** Fiscal Caution and Naive First-Time profiles; advice-aware and
  advice-ignoring modes; seeds 42, 43, and 44; Normal and Hard difficulty
- **Evidence artifact:**
  `_workspace/experiments/v0.10.41-consultant-advice-usage/results.json`

This slice evaluates whether deterministic simulated policies can explicitly
consider the generic consultant options restored in v0.10.39. The advice-aware
wrapper reads only actor-visible observations and resource hints, records its
selection or fallback, and is paired with an existing control policy that does
not inspect consultant text.

## Questions

1. Can an observation-driven policy parse all four non-binding A–D options?
2. Can it select an option from visible cues without using hidden state?
3. Does it fall back safely when the visible budget cannot support the option or
   an inherited command?
4. Do rendered options, committed transition history, and debrief records stay
   exactly continuous across both policy modes?

## Result

All 24 paired runs completed 24 months with zero validation failures. Every run
recorded 24 exact rendered/history option matches and 24 monthly debrief option
records. The advice-ignoring controls matched the corresponding v0.10.40 state
hashes across all seeds and difficulty levels.

The advice-aware policies produced visible selection and fallback signals. The
Fiscal Caution policy consistently selected the visible rival-information
option in this matrix. The Naive First-Time policy selected the workforce
option when visible nursing pressure was present and used safe fallback when
the inherited command was no longer affordable after an advice-aware action.

## Interpretation

These are deterministic simulated-policy traces. Selection and command-family
alignment do not establish advice uptake, advice quality, decision quality,
causal impact, human comprehension, or learning. Advice-aware runs intentionally
submit different commands from controls, so their endpoint hashes are not a
causal comparison.

The evidence supports keeping the generic advice baseline available for further
observation-driven testing. It does not justify promoting a differentiated
advisor roster, payroll, candidate pool, or hiring mechanic.

## Non-Goals

- No advisor roster, payroll, candidate pool, hire/fire command, AI advisor, or
  runtime simulation change.
- No balance, difficulty, command-cost, scenario, replay, MCP DTO, or state-hash
  change.
- No human-learning, advice-quality, policy-validity, or empirical-calibration
  claim.

## Verification

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 _workspace/experiments/v0.10.41-consultant-advice-usage/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.41-consultant-advice-usage/results.json
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
python3 scripts/run_automated_playtests.py
git diff --check
```
