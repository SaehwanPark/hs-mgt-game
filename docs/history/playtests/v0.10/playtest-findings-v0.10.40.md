# Consultant Advice Traceability Evidence v0.10.40

- **Status:** Phase 7 competitive teachability and validation evidence
- **Campaign:** `competitive-regional-v1`
- **Matrix:** existing Fiscal Caution, Capacity Growth, Balanced Strategy, and
  Naive First-Time policies; seeds 42, 43, and 44; Normal and Hard difficulty
- **Evidence artifact:**
  `_workspace/experiments/v0.10.40-consultant-advice-evidence/results.json`

This slice evaluates the generic consultant baseline restored in v0.10.39. It
adds the already-stored consultant options to the additive MCP transition
summary, then captures MCP observations, accepted commands, committed
transitions, state hashes, and end-session debriefs without changing simulation
behavior.

## Questions

1. Does every competitive observation expose four non-binding A–D options?
2. Do the rendered options exactly match options stored with the corresponding
   committed transition?
3. Does the debrief retain a monthly record of those options?
4. Can existing scripted command families be described alongside the options
   without implying that advice determined the command or outcome?

## Result

All 24 runs completed 24 months with zero validation failures. Every month had
four rendered options that exactly matched its committed transition record, and
every debrief retained 24 monthly option records. The options varied between
two or three visible-observation-conditioned signatures per run. The artifact
is regenerated twice and must remain byte-for-byte stable.

The alignment mapping is descriptive only: `invest` maps to A, `recruit` to B,
`monitor` to C, and `commit` to D. Negotiation, projects, holds, and unmatched
commands are reported as no generic-option alignment.

## Interpretation

This is an observation/debrief traceability check, not advice-quality evidence.
The policies were authored independently of the consultant text, so aligned
commands do not show advice uptake, decision quality, learning, causal impact,
or a need for a differentiated advisor roster.

If all matrix runs complete with exact continuity, the repaired generic baseline
remains sufficient for the current Phase 7 gate. A future advisor-market proposal
requires a separate documented need that this baseline cannot meet.

## Non-Goals

- No advisor roster, payroll, hiring/firing, candidate pool, or AI advice.
- No balance, difficulty, command, scenario, replay, or state-hash change.
  The only MCP DTO addition exposes consultant options already retained in
  competitive history.
- No human-learning, policy-validity, empirical-calibration, or advice-quality
  claim.

## Verification

```bash
python3 -m py_compile _workspace/experiments/v0.10.40-consultant-advice-evidence/run_sessions.py
python3 _workspace/experiments/v0.10.40-consultant-advice-evidence/run_sessions.py
python3 -m json.tool _workspace/experiments/v0.10.40-consultant-advice-evidence/results.json
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
python3 scripts/run_automated_playtests.py
git diff --check
```
