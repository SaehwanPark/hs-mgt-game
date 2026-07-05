# Request Summary - Implement Psychiatric Service Line & Behavioral Health Crisis Mechanics

## Phase / Gate
Phase 6.1: Simulation Breadth (Track 5) - Psychiatric Service Line & Behavioral Health Crisis Mechanics

## Scope
Implement a Psychiatric (Behavioral Health) Service Line with capacity-staffing trade-offs, specialized staffing targets, hierarchical allocation prioritizing Psychiatric after Med-Surg and before Outpatient, and a Psychiatric ED boarding/diversion crisis penalty representing the "behavioral health crisis holding" reality:
1.  **State Fields:** Add `psychiatric_capacity` to `HealthSystemState` in `src/model/competitive_world.rs`, defaulting to 0 for scenario/genesis backward compatibility. Add `PendingEffectKind::PsychiatricCapacity { capacity_delta: i32, project_draw: Option<i32> }` to `PendingEffectKind`.
2.  **Command Grammar:** Add `Psychiatric` (alias `"psychiatric"`, `"psych"`) to `InvestDomain` enum and `PsychiatricUnit` (duration: 6 months, capacity: +5 beds, cost: 2 AP, budget: $30k) to `ProjectKind` enum in `src/model/competitive_command.rs`. Update action cost mappings.
3.  **Staffing Constraints:**
    *   Psychiatric staffing targets: 1 Nurse per 4 beds, 1 Physician per 10 beds, 1 Admin per 15 beds. These are added to total system targets.
    *   Hierarchical allocation order: ICU first, Obstetrics second, Med-Surg Beds third, Psychiatric fourth, Outpatient Clinics fifth, Emergency Department sixth.
4.  **Behavioral Health ED Boarding & Diversion Mechanics:**
    *   Psychiatric admission demand is modeled as `(system.psychiatric_capacity + 9) / 10` (10% of psychiatric capacity, ceiling division).
    *   If `effective_psychiatric < psychiatric_demand`, the overflowed volume `psychiatric_demand - effective_psychiatric` represents patients in psychiatric crisis.
    *   These psychiatric crisis patients board in the ED on a 1-to-1 basis, directly reducing the effective emergency capacity (representing the "holding" of psychiatric patients in ED bays when specialized beds are full/understaffed).
    *   If the boarded psychiatric patients exceed the remaining effective emergency capacity, the excess patients are diverted/turned away, triggering:
        *   `-1` community trust penalty per diverted psychiatric patient.
        *   `-1` quality index penalty per diverted psychiatric patient (due to unsafe care transitions).
5.  **Strike & CON Delays:** Ensure `PendingEffectKind::PsychiatricCapacity` projects are suspended during RNA strikes.
6.  **CLI & Dashboard:** Update executive report, CLI parsers, autocompletion, and guidance help topics.
7.  **AI Decisions:** Update target calculation and candidate generation in `src/actors/ai_player.rs`.
8.  **Golden Hash / Tests:** Verify transition logic with focused unit tests, and update/record the competitive golden hash.

## Non-Goals
- No changes to stabilization campaign loops.
- No specialized pediatric psychiatric or substance abuse rehab facilities.
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
