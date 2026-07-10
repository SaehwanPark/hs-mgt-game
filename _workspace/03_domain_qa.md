# Domain QA - Consultant Advice Usage Evidence

## Status

pass

## Reviewed Inputs

- `SPEC.md` v0.10.41 completion entry and Future promotion rules.
- `_workspace/00_input/request-summary.md`, `_workspace/01_evidence_map.md`,
  and `_workspace/02_mechanism_design.md`.
- `_workspace/experiments/v0.10.40-consultant-advice-evidence/` and
  `_workspace/experiments/v0.10.41-consultant-advice-usage/`.
- `_workspace/experiments/v0.10.41-consultant-advice-usage/run_sessions.py` and
  `tests/test_consultant_advice_usage.py`.
- `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`, and the harness team specification.

## Findings

- The slice remains bounded to generic decision-support usage evidence; it does
  not promote the deferred advisor market, payroll, hiring, or a new actor.
- Advice-aware policies read only actor-visible options, cues, and resources;
  inherited commands are guarded with visible-budget checks and safe-hold fallback.
- All 24 paired runs completed with 24 exact rendered/history matches and 24
  debrief records per run. Advice-ignoring control hashes match v0.10.40.
- Selection and command-family signals are explicitly descriptive simulated-agent
  evidence, not advice quality, causal, human-learning, or balance evidence.

## Required Fixes

- None.

## Residual Risks

- Advice wording remains a gameplay abstraction and has not been validated as
  an educational intervention, calibrated guidance, or a basis for a roster.
- Advice-aware endpoint differences are policy differences and cannot establish
  causal advice value.

## Verification Evidence

- `python3 _workspace/experiments/v0.10.41-consultant-advice-usage/run_sessions.py`
  completed all 24 paired runs with stable control hashes
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test --all -- --test-threads=1` (285 tests pass)
- `python3 scripts/run_automated_playtests.py`
- `git diff --check`
