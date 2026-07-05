# Request Summary - Implement Oncology Service Line & Infusion Center Mechanics

## Phase / Gate
Phase 6.1: Simulation Breadth (Track 5) - Oncology Service Line & Infusion Center Mechanics

## Scope
Implement an Oncology (Inpatient) Service Line and an Infusion Center (Outpatient) Service Line with capacity-staffing trade-offs, specialized staffing targets, hierarchical allocation prioritizing Oncology/Infusion after Psychiatric and before Outpatient, and ED boarding (inpatient) or deferral (outpatient) mechanics:
1.  **State Fields:** Add `oncology_capacity` and `infusion_capacity` to `HealthSystemState` in `src/model/competitive_world.rs`, defaulting to 0 for scenario/genesis backward compatibility. Add `PendingEffectKind::OncologyCapacity { capacity_delta: i32, project_draw: Option<i32> }` and `PendingEffectKind::InfusionCapacity { capacity_delta: i32, project_draw: Option<i32> }` to `PendingEffectKind`.
2.  **Command Grammar:** Add `Oncology` (alias `"oncology"`, `"onco"`) and `Infusion` (alias `"infusion"`, `"infuse"`) to `InvestDomain` enum. Add `OncologyUnit` (duration: 9 months, capacity: +6 beds, cost: 3 AP, budget: $45k) and `InfusionCenter` (duration: 6 months, capacity: +8 bays, cost: 2 AP, budget: $30k) to `ProjectKind` enum in `src/model/competitive_command.rs`. Update action cost and duration mappings.
3.  **Staffing Constraints:**
    *   Oncology (inpatient) staffing targets: 1 Nurse per 3 beds, 1 Physician per 8 beds, 1 Admin per 12 beds.
    *   Infusion (outpatient) staffing targets: 1 Nurse per 4 bays, 1 Physician per 15 bays, 1 Admin per 20 bays.
    *   Hierarchical nurse/physician allocation order: ICU first, Obstetrics second, Med-Surg third, Cardiology fourth, Psychiatric fifth, Oncology sixth, Infusion seventh, Outpatient Clinics eighth, Emergency Department ninth.
4.  **Oncology & Infusion Mechanics:**
    *   Oncology inpatient admission demand: `(system.oncology_capacity + 9) / 10` (10% of oncology capacity, ceiling division).
    *   If `effective_oncology < oncology_demand`, the overflowed volume `oncology_demand - effective_oncology` represents patients who board in the ED on a 1-to-1 basis, directly reducing effective emergency capacity.
    *   If the boarded oncology patients exceed the remaining effective emergency capacity, the excess patients are diverted, triggering:
        *   `-2` community trust penalty per diverted oncology patient.
        *   `-2` quality index penalty per diverted oncology patient (due to compromised care cycle).
    *   Infusion Center demand: `(system.infusion_capacity + 4) / 5` (20% of infusion capacity, ceiling division).
    *   If `effective_infusion < infusion_demand`, the unserved outpatient volume `infusion_demand - effective_infusion` cannot board in the ED (outpatient service). They are deferred, triggering:
        *   `-1` community trust penalty per deferred infusion patient.
        *   `-1` market share index penalty per deferred infusion patient (competitors absorb the demand).
5.  **Strike & CON Delays:** Ensure `PendingEffectKind::OncologyCapacity` and `PendingEffectKind::InfusionCapacity` projects are suspended during RNA strikes.
6.  **CLI & Dashboard:** Update executive report, CLI parsers, autocompletion, and guidance help topics.
7.  **AI Decisions:** Update target calculation and candidate generation in `src/actors/ai_player.rs`.
8.  **Golden Hash / Tests:** Verify transition logic with focused unit tests, and update/record the competitive golden hash.

## Non-Goals
- No changes to stabilization campaign loops.
- No specialized pediatric oncology or radiation therapy bunkers.
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
- `tests/golden_competitive_seed42.rs`
