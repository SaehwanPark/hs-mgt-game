# Domain QA - Future Queue Re-ranking and SDD Alignment

## Status

Pass.

## Reviewed Inputs

- User request to implement the Future queue re-ranking and SDD alignment plan.
- `docs/harness/health-policy-strategy-game/team-spec.md`
- `docs/proposal.md`
- `docs/roadmap.md`
- `docs/design_principles.md`
- `docs/expansion-proposal-review.md`
- `SPEC.md`
- `ARCHITECTURE.md`
- `_workspace/00_input/request-summary.md`

## Findings

- The slice stays within SDD alignment scope. It restructures planning guidance
  without promoting any Future item into runtime implementation.
- The new promotion rules require a phase/gate, evidence source, narrow changed
  artifact or behavior, verification criteria, and non-goals before any Future
  item moves into `Present`.
- Competitive teachability and validation are correctly ranked before
  difficulty, M&A, GUI, breadth, and release-readiness work because repeated
  play remains the next evidence risk.
- Difficulty, regional affiliation/acquisition, and GUI work remain bounded by
  the prior proposal review and do not imply tuning, legal forecasting, toolkit
  choice, or asset distribution.
- Architecture/documentation discipline is now a cross-cutting guardrail rather
  than a competing product track, which better matches the repo's narrow-slice
  development principle.
- The review preserves deterministic replay, actor-observation separation,
  append-only history, debrief traceability, and visible assumptions.

## Required Fixes

None.

## Residual Risks

- The new ranking is a planning judgment, not proof that lower-ranked tracks are
  unimportant.
- Expert winnability still needs future scripted/live-agent or human evidence
  before runtime difficulty changes are accepted.
- GUI implementation choices, toolkit selection, asset manifests, packaging,
  and accessibility validation remain unresolved future work.
- M&A design still needs domain review before any scenario or ruleset schema is
  extended.

## Verification Evidence

- `rg` stale-queue/version scan over SDD and companion docs
- `git diff --check`
- `cargo fmt --check`
- `cargo clippy --all-targets -- -D warnings`
- `cargo test -- --test-threads=1`
