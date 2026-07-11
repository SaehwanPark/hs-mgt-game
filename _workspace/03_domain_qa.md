# Domain QA - Adversarial Resource-Probe Evidence

## Status

pass

## Reviewed Inputs

- The v0.10.51 capture runner, generated results, diagnostics, and focused tests.
- `docs/playtest-findings-v0.10.51.md` and project handoff artifacts.
- `README.md`, `SPEC.md`, `docs/roadmap.md`, `docs/design_principles.md`, and
  the harness team specification.

## Findings

- The slice remains within the Phase 7 competitive validation gate.
- All three adversarial runs completed 24 months with five expected validation
  failures and five safe retries per run.
- Rejected commands remained on the same session turn; retries advanced the
  campaign exactly once.
- The capture is read-only and does not alter deterministic transitions,
  replay, MCP schemas, scenarios, difficulty, scoring, or debrief behavior.
- Validation compatibility, exploit evidence, actor utility, endpoint
  outcomes, social welfare, and educational evaluation remain distinct.
- No concrete unexplained runtime, command-surface, or debrief gap was
  identified.

## Required Fixes

None.

## Residual Risks

- The capture uses one deterministic adversarial simulated policy rather than
  human or classroom sessions.
- Intentional validation failures test guard compatibility and trace capture;
  they do not establish exploit value, balance, winnability, or comprehension.
- The missing resource hint on the concurrent-project error is recorded as a
  trace fact, not promoted as a product defect.

## Verification Evidence

Focused capture tests, deterministic artifact checks, the full Python suite,
formatting, clippy, Rust tests, automated playtests, and diff checks pass before
PR handoff.
