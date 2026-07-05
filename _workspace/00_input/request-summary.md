# Request Summary - Emergency Department Service Line Implementation

## Phase / Gate
Phase 6.1: Simulation Breadth (Track 5)

## Scope
Implement a new service line (Emergency Department) with staffing constraints and capacity tradeoffs in the competitive campaign.
- Add `emergency_capacity` (representing Emergency Department bays/rooms) to the `HealthSystemState` struct.
- Add `Emergency` to the `InvestDomain` enum, allowing players and AI to quiet-invest in ED capacity.
- Add `EmergencyPavilion` to the `ProjectKind` enum, allowing players to build a major ED project with a 6-month resolution delay and cash draws.
- Update `PendingEffectKind` to support `EmergencyCapacity` increments.
- Define Emergency Department staffing target ratios:
  - 1 Nurse per 2 ED capacity
  - 1 Physician per 4 ED capacity
  - 1 Admin per 10 ED capacity
- Update `apply_staffing_constraints` in `src/sim/transition_competitive.rs` to compute targets, sum deficit-based workforce trust reductions, and apply effective ED capacity limitations.
  - `effective_emergency = system.emergency_capacity.min(system.nurses * 2).min(system.physicians * 4)`
- Enforce overall capacity utility-ratio access and quality index drops based on beds, outpatient capacity, and emergency capacity combined.
- Support CLI parsing, autocompletes, and help topics for the new `InvestDomain::Emergency` and `ProjectKind::EmergencyPavilion`.
- Update `observe_for_human`, `observe_for_ai`, `in_flight_projects_label`, and the REPL executive report layout to display emergency capacity and status.

## Non-Goals
- No changes to the stabilization campaign loop rules.
- No changes to commercial payer pressure or public payer negotiation logic (Medicaid/Medicare).
- No changes to save serialization files (autosave/resume backward compatibility is maintained by wrapping/defaulting the new field).

## Sources
- `docs/roadmap.md` §6.1
- `src/model/competitive_world.rs`
- `src/model/competitive_command.rs`
- `src/sim/transition_competitive.rs`
- `src/sim/observe_competitive.rs`
- `src/cli/display/executive_report.rs`

## Expected Files to Change
- `src/model/competitive_world.rs`
- `src/model/competitive_command.rs`
- `src/model/competitive_hash.rs`
- `src/sim/observe_competitive.rs`
- `src/sim/observe_ai.rs`
- `src/sim/effects_competitive.rs`
- `src/sim/transition_competitive.rs`
- `src/cli/competitive_parse.rs`
- `src/cli/display/executive_report.rs`
- `src/cli/guidance.rs`
- `src/cli/repl.rs`
- `src/scenario/mod.rs`
- `src/actors/ai_player.rs`
- `SPEC.md`
- `CHANGELOG.md`
- `Cargo.toml`
