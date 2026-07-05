# Request Summary - Implement Obstetrics Service Line & L&D Diversion Mechanics

## Phase / Gate
Phase 6.1: Simulation Breadth (Track 5) - Obstetrics Service Line & Labor & Delivery (L&D) Diversion Mechanics

## Scope
Implement an Obstetrics (L&D) Service Line with capacity-staffing trade-offs, specialized staffing targets, hierarchical allocation prioritizing Obstetrics after ICU, and an obstetric capacity-diversion penalty representing the "halo effect":
1.  **State Fields:** Add `obstetrics_capacity` to `HealthSystemState` in `src/model/competitive_world.rs`, defaulting to 0 for scenario/genesis backward compatibility. Add `ObstetricsCapacity { capacity_delta: i32, project_draw: Option<i32> }` to `PendingEffectKind`.
2.  **Command Grammar:** Add `Obstetrics` to `InvestDomain` enum and `ObstetricsUnit` (duration: 9 months) to `ProjectKind` enum in `src/model/competitive_command.rs`. Update action cost mappings.
3.  **Staffing Constraints:**
    *   Obstetrics staffing targets: 1 Nurse per 2 beds, 1 Physician per 5 beds, 1 Admin per 10 beds. These are added to total system targets.
    *   Hierarchical allocation order: ICU first, Obstetrics second, Med-Surg Beds third, Outpatient Clinics fourth, Emergency Department fifth.
4.  **Obstetric Diversion Mechanics (The "Halo Effect"):**
    *   Obstetric admission demand is modeled as `(system.obstetrics_capacity + 9) / 10` (10% of obstetric capacity, ceiling division).
    *   If `effective_obstetrics < obstetric_demand`, the diverted volume `obstetric_demand - effective_obstetrics` triggers:
        *   `-2` community trust penalty per diverted patient (due to poor service access).
        *   `-1` market share index penalty per diverted patient (leaked to other systems, representing the loss of the childbirth family loyalty "halo effect").
5.  **Strike & CON Delays:** Ensure `PendingEffectKind::ObstetricsCapacity` projects are suspended during RNA strikes.
6.  **CLI & Dashboard:** Update executive report, CLI parsers, autocompletion, and guidance help topics.
7.  **AI Decisions:** Update target calculation and candidate generation in `src/actors/ai_player.rs`.
8.  **Golden Hash / Tests:** Verify transition logic with focused unit tests, and update/record the competitive golden hash.

## Non-Goals
- No changes to stabilization campaign loops.
- No neonatal intensive care unit (NICU) service line or complex obstetric diagnostic tracking.
- No modifications to the core simultaneous command resolution sequence itself.

## Expected Files to Change
- `src/model/competitive_world.rs`
- `src/model/competitive_command.rs`
- `src/model/campaign.rs`
- `src/sim/observe_ai.rs`
- `src/sim/effects_competitive.rs`
- `src/sim/transition_competitive.rs`
- `src/sim/observe_competitive.rs`
- `src/cli/competitive_parse.rs`
- `src/cli/display/executive_report.rs`
- `src/cli/guidance.rs`
- `src/cli/repl.rs`
- `src/actors/ai_player.rs`
- `src/competitive/genesis.rs`
- `src/competitive/fixtures.rs`
- `src/model/competitive_hash.rs`
- `src/scenario/mod.rs`
