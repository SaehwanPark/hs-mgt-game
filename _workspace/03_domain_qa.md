# Domain QA — Competitive Gameplay Design Package

## Status

**pass**

The competitive gameplay design package is ready for PR handoff. No Critical or
High findings require revision before merge. Residual risks are documented and
acceptable for a design-only slice.

## Reviewed Inputs

- `_workspace/00_input/request-summary.md`
- `_workspace/01_evidence_map.md`
- `_workspace/02_mechanism_design.md`
- `docs/gameplay-competitive-sketch.md`
- `docs/core-loop-spec.md`
- `docs/competitive-scenario-brief.md`
- `docs/executive-report-format.md`
- `docs/action-catalog-draft.md`
- `docs/cli-command-grammar-draft.md`
- ADRs 0003–0006
- Updated: `docs/proposal.md`, `docs/roadmap.md`, `docs/system-boundary.md`,
  `SPEC.md`, `ARCHITECTURE.md`
- Canonical: `docs/design_principles.md`, `docs/proposal.md`, ADR-0001

## Findings

### Scope and phase alignment

- Design package correctly targets parallel campaign without stabilization
  regression. Matches user-confirmed placement and orchestrator phase gates.
- Phase 6.0 track in roadmap distinguishes K AI competitors from Phase 9
  classroom roles. No scope confusion detected.

### Determinism and replay

- ADRs 0003–0006 preserve ADR-0001 boundary. Stochasticity assigned to named
  streams (`monthly_events`, `annual_policy`, `ai_player_{id}`).
- Simultaneous resolution uses deterministic `system_id` ordering for conflicts.
  Documented for future debrief transparency.

### Educational framing

- Consultant recommendations labeled advisory; multiple defensible paths preserved.
- Nonprofit obligations and tradeoffs explicit in competitive scenario brief.
- Debrief hooks compare advice vs player choices without normative scoring collapse.

### Strategic and policy plausibility

- Bounded level-1 AI appropriate per phase1 implications memo (no global equilibrium).
- Monthly/annual cadence plausible for regional executive strategy.
- EHR `project` delay example grounded in real implementation timelines as abstraction.

### False precision

- Numeric AP/PC values labeled as balancing abstractions in mechanism design and
  action catalog. Evidence map flags playtest iteration need.

### Low — documentation consistency

- Some historical playtest docs still say "four-turn"; not updated (out of slice
  scope). `phase1-implications-memo.md` and `actor-cards.md` reconciled.

## Required Fixes

None.

## Residual Risks

| Risk | Severity | Mitigation in design |
| --- | --- | --- |
| Competitive runtime may require `transition_competitive()` fork | Medium | ADR-0004 allows fork if merge unsafe |
| AP/PC balance unvalidated | Medium | Playtest after slice I3 |
| Two CLI models coexist | Low | ADR-0006 scopes Stata REPL to competitive only |
| Consultant advice feels prescriptive | Low | Explicit non-binding label; debrief comparison |
| Replay artifact version bump | Low | Deferred to first competitive runtime slice |

## Verification Evidence

- Design docs cross-link without contradiction between `system-boundary.md` and
  `competitive-scenario-brief.md`.
- All 15 sketch requirement sections in `gameplay-competitive-sketch.md` have
  acceptance criteria.
- `cargo fmt --check` and `cargo test` to run before PR (golden hash unchanged).
