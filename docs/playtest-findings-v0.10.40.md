# Consultant Advice Validation Evidence v0.10.40

- **Status:** Phase 7 bounded simulated-agent evidence slice
- **Date:** 2026-07-10
- **Code version:** 0.10.40
- **Campaign:** `competitive-regional-v1`
- **Matrix:** four existing policies × seeds `42`, `43`, and `44` × Normal and Hard
- **Evidence artifact:**
  - `_workspace/experiments/v0.10.40-consultant-advice-validation/results.json`
  - `_workspace/experiments/v0.10.40-consultant-advice-validation/diagnostics.md`

## Evidence shape

The runner reused the existing Fiscal Caution, Capacity Growth, Balanced
Strategy, and Naive First-Time policies through `play_session` with
`capture_trace=True`. It recorded actor-visible observations, legal command
hints, submitted commands, accepted transition summaries, validation failures,
and end-session debriefs.

All 24 runs completed the full 24-month campaign with zero validation failures.
Every run contained 24 consultant-option observations, 24 retained debrief
option records, 24 advisory-comparison lines, and at least two visible option
signatures. Capacity Growth produced two signatures; the other profiles
produced three in the captured matrix.

## Interpretation

- The existing consultant surface is present at every captured competitive
  decision point.
- Option titles vary with visible cash, workforce, community, and intelligence
  categories rather than requiring hidden rival state.
- The exact option titles shown before accepted commands are retained in the
  corresponding month-level debrief records.
- The matrix validates reproducibility and inspectability, not whether an agent
  followed the advice or achieved a better outcome.

## Evidence limits and routing

- These are deterministic simulated-agent traces, not human classroom
  observations or an assessment instrument.
- Repeated policy/seed runs are not independent player samples.
- Normal/Hard coverage is not a difficulty, balance, or Expert-winnability
  claim because the policies are reused controls rather than adaptive human
  decision makers.
- No advice-quality, learning, calibration, policy-validity, or advisor-market
  conclusion is justified.
- Keep the advisor market, payroll, roster, hiring, firing, AI advice behavior,
  and runtime tuning deferred until a separate evidence or design gate names a
  concrete need.

## Verification

```bash
python3 -m py_compile _workspace/experiments/v0.10.40-consultant-advice-validation/run_sessions.py
python3 _workspace/experiments/v0.10.40-consultant-advice-validation/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.40-consultant-advice-validation/results.json
python3 -m unittest tests/test_playtest_wrapper.py
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
cargo test --test golden_competitive_seed42 -- --test-threads=1
python3 scripts/run_automated_playtests.py
git diff --check
```
