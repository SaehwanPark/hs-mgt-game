# Request Summary - Medicare Public Payer Integration

## Phase / Gate
Phase 6.1: Simulation Breadth (Track 5: Broader simulation breadth and new strategic actors)

## Scope
Design the plan to implement Medicare public payer integration in the competitive regional campaign loop.
Medicare will complement the existing Medicaid public payer (added in v0.5.5) and commercial payers (Carrier A and Carrier B).
Medicare will model quality-compliance alignment rules, where:
- Medicare is added to the `PayerId` enum and CLI parses `"medicare"`.
- Medicare negotiations only support `RatePosture::Neutral` posture, representing compliance / reporting alignment.
- Setting non-neutral rate posture for Medicare results in a validation error.
- Responding to Medicare compliance requires 1 AP, 2 PC, and $10 cash (higher compliance/reporting overhead than Medicaid).
- Resolving Medicare compliance grants a direct benefit to quality index (+3 quality_index) and reduces state policy pressure (-3 policy_pressure).
- Update help guidance, autocomplete, REPL summaries, and debriefing reports to cover Medicare.

## Non-Goals
- No changes to stabilization campaign loop rules.
- No structural changes to `HealthSystemState` beyond existing metrics.
- No patient cohort division by Medicare/Medicaid eligibility for this slice.
- No changes to commercial payer negotiation mechanics.

## Sources
- `docs/roadmap.md` §5.1, 6.1
- `docs/phase5-scope-register.md` (Deferred list)
- `src/model/competitive_command.rs`
- `src/sim/transition_competitive.rs`
- `src/sim/validate_competitive.rs`
- `src/cli/competitive_parse.rs`
- `src/cli/guidance.rs`

## Expected Files to Change
- `src/model/competitive_command.rs`
- `src/cli/competitive_parse.rs`
- `src/cli/guidance.rs`
- `src/cli/repl.rs`
- `src/competitive/resolution.rs`
- `src/debrief/report.rs`
- `src/sim/transition_competitive.rs`
- `src/sim/validate_competitive.rs`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
