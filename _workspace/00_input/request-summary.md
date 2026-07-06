# Request Summary - Implement Ambulatory Surgery Center (ASC) Service Line

## Phase / Gate
Phase 6.1: Simulation Breadth (Track 5) - Ambulatory Surgery Center (ASC) Service Line

## Scope
Implement an Ambulatory Surgery Center (ASC) Service Line with capacity-staffing trade-offs, specialized staffing targets, hierarchical allocation prioritizing ASC after Oncology/Infusion and before Outpatient, and outpatient surgical deferral mechanics:
1.  **State Fields:** Add `asc_capacity` to `HealthSystemState` in `src/model/competitive_world.rs`, defaulting to 0 for scenario/genesis backward compatibility. Add `PendingEffectKind::AscCapacity { capacity_delta: i32, project_draw: Option<i32> }` to `PendingEffectKind`.
2.  **Command Grammar:** Add `Asc` (alias `"asc"`, `"surg"`) to `InvestDomain` enum. Add `AscUnit` (duration: 6 months, capacity: +6 bays, cost: 2 AP, budget: $24k) to `ProjectKind` enum in `src/model/competitive_command.rs`. Update action cost and duration mappings.
3.  **Staffing Constraints:**
    *   ASC (outpatient surgery) staffing targets: 1 Nurse per 2 bays, 1 Physician per 4 bays, 1 Admin per 12 bays.
    *   Hierarchical nurse/physician allocation order: ICU first, Obstetrics second, Med-Surg third, Cardiology fourth, Psychiatric fifth, Neurology sixth, Oncology seventh, Infusion eighth, ASC ninth, Outpatient Clinics tenth, Emergency Department eleventh.
4.  **ASC Mechanics:**
    *   ASC outpatient admission demand: `(system.asc_capacity + 7) / 8` (12.5% of ASC capacity, ceiling division).
    *   If `effective_asc < asc_demand`, the unserved outpatient volume `asc_demand - effective_asc` cannot board in the ED (outpatient service). They are deferred, triggering:
        *   `-1` community trust penalty per deferred ASC patient.
        *   `-1` market share index penalty per deferred ASC patient (competitors absorb the demand).
5.  **Strike & CON Delays:** Ensure `PendingEffectKind::AscCapacity` projects are suspended during RNA strikes.
6.  **CLI & Dashboard:** Update executive report, CLI parsers, autocompletion, and guidance help topics.
7.  **AI Decisions:** Update target calculation and candidate generation in `src/actors/ai_player.rs`.
8.  **Golden Hash / Tests:** Verify transition logic with focused unit tests, and update/record the competitive golden hash.

## Non-Goals
- No changes to stabilization campaign loops.
- No specialized cardiac/neuro specialty surgical suites or hybrid ORs.
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
- `src/model/competitive_hash.rs`
- `src/scenario/mod.rs`
- `tests/golden_competitive_seed42.rs`
