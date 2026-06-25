# Request Summary — Competitive Gameplay Design Package

## Scope

Fully develop the user-provided competitive gameplay sketch into durable design
artifacts and sync SDD/canonical documentation. Deliver a **parallel competitive
regional-market campaign** design (1 human + K AI health-system players) without
changing runtime behavior or breaking the existing five-turn stabilization demo
at v0.1.27.

## Non-goals

- No runtime code changes in this slice
- No refactoring of the stabilization demo into competitive mode
- No Medicare/Medicaid expansion, service-line modeling, or graphical UI
- No global multi-agent equilibrium solver
- No empirical calibration or policy forecasting claims
- No breaking golden hash `6fb1ebbea564274f` for stabilization demo
- No CI clippy or release automation

## Sources

- User gameplay sketch (monthly turns, executive report, K AI competitors,
  simultaneous actions, action economy, Stata CLI, delayed effects, yearly
  policy, random events)
- Canonical docs: `README.md`, `docs/proposal.md`, `docs/roadmap.md`,
  `docs/design_principles.md`
- Current implementation: v0.1.27 five-turn stabilization vertical slice
- ADR-0001 deterministic transition boundary
- `_workspace/01_evidence_map.md`, `_workspace/02_mechanism_design.md` (prior slices)

## Expected files

### Workspace handoffs

- `_workspace/00_input/request-summary.md` (this file)
- `_workspace/01_evidence_map.md` (update)
- `_workspace/02_mechanism_design.md` (rewrite for competitive campaign)
- `_workspace/03_domain_qa.md` (domain QA pass)
- `_workspace/final/handoff.md` (completion handoff)

### New canonical design docs

- `docs/gameplay-competitive-sketch.md`
- `docs/core-loop-spec.md`
- `docs/executive-report-format.md`
- `docs/action-catalog-draft.md`
- `docs/cli-command-grammar-draft.md`
- `docs/competitive-scenario-brief.md`
- `docs/decision-records/0003-simultaneous-monthly-player-actions.md`
- `docs/decision-records/0004-multi-system-player-state.md`
- `docs/decision-records/0005-action-economy-and-monthly-budget.md`
- `docs/decision-records/0006-stata-like-cli-layer.md`

### Updated docs

- `docs/proposal.md`, `docs/roadmap.md`, `docs/system-boundary.md`
- `docs/scenario-format-draft.md`, `docs/first-scenario-brief.md`
- `docs/actor-cards.md`, `docs/glossary.md`, `LESSONS.md`
- `docs/phase5-scope-register.md`, `docs/phase1-implications-memo.md`
- `docs/decision-records/README.md`
- `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `Cargo.toml`, `README.md`

## Validation

- Domain QA pass in `_workspace/03_domain_qa.md` with no unresolved Critical/High
  findings
- Every sketch bullet mapped in `docs/gameplay-competitive-sketch.md`
- ADRs 0003–0006 consistent with ADR-0001
- `cargo fmt --check` and `cargo test` pass with zero gameplay changes
- Three code-reviewer passes on doc diff before PR merge

## Global skills

- `hs-policy-evidence-mapper`, `hs-policy-mechanism-designer`, `hs-policy-domain-qa`
- `spec-driven-developer`, `preferred-workflow`, `code-reviewer`

## Roadmap phase

Phase 3 (core loop specification) + Phase 6.0 competitive campaign design track.
Implementation deferred to follow-on vertical slices I1–I8.
