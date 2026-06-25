# Handoff — Competitive Gameplay Design Package (v0.1.28)

## Summary

Delivered full design and SDD sync for the **competitive regional market
campaign** (`competitive-regional-v1`) as a parallel track to the stabilization
demo. No runtime changes.

## Changed files

### New

- `docs/gameplay-competitive-sketch.md`
- `docs/core-loop-spec.md`
- `docs/competitive-scenario-brief.md`
- `docs/executive-report-format.md`
- `docs/action-catalog-draft.md`
- `docs/cli-command-grammar-draft.md`
- `docs/decision-records/0003-simultaneous-monthly-player-actions.md`
- `docs/decision-records/0004-multi-system-player-state.md`
- `docs/decision-records/0005-action-economy-and-monthly-budget.md`
- `docs/decision-records/0006-stata-like-cli-layer.md`

### Updated

- `_workspace/00_input/request-summary.md`
- `_workspace/01_evidence_map.md`
- `_workspace/02_mechanism_design.md`
- `_workspace/03_domain_qa.md`
- `docs/proposal.md`, `docs/roadmap.md`, `docs/system-boundary.md`
- `docs/scenario-format-draft.md`, `docs/first-scenario-brief.md`
- `docs/actor-cards.md`, `docs/glossary.md`, `LESSONS.md`
- `docs/phase5-scope-register.md`, `docs/phase1-implications-memo.md`
- `docs/decision-records/README.md`
- `SPEC.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `README.md`, `Cargo.toml`

## Verification

- `cargo fmt --check`
- `cargo test` (golden hash `6fb1ebbea564274f` unchanged)
- Domain QA: pass (`_workspace/03_domain_qa.md`)

## Known limits

- Competitive campaign not playable; design artifacts only
- Stabilization demo unchanged
- AP/PC numeric balances are abstractions pending playtest

## Recommended next slice

**I1 + I2:** `feat/campaign-router` + `feat/monthly-executive-report`

- Thin CLI campaign selector (`stabilization-v1` vs competitive stub)
- Monthly calendar labels and executive report sections (observation-only;
  can use mock data before full multi-system state)

## Phase dependencies

- I4 multi-system state before I5 simultaneous resolver
- I3 action economy before competitive CLI command validation
- I8 Stata CLI after I3 and typed command shapes exist
