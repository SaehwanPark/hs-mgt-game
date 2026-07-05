# Request Summary - Implement ICU Service Line & ED Boarding Mechanics

## Phase / Gate
Phase 6.1: Simulation Breadth (Track 5) - ICU Service Line & ED Boarding Mechanics

## Scope
Implement a complete Intensive Care Unit (ICU) Service Line with capacity-staffing trade-offs, hierarchical allocation, and ED boarding mechanics:
1.  **State Fields:** Add `icu_capacity` and `icu_effective` to `HealthSystemState` in `src/model/competitive_world.rs`, defaulting to 0 for scenario/genesis backward compatibility. Add `IcuCapacity { capacity_delta: i32, project_draw: Option<i32> }` to `PendingEffectKind`.
2.  **Command Grammar:** Add `Icu` to `InvestDomain` enum and `IcuWing` (duration: 12 months) to `ProjectKind` enum in `src/model/competitive_command.rs`. Update action cost mappings.
3.  **Staffing Constraints:**
    *   ICU staffing targets: 1 Nurse per 1 ICU bed, 1 Physician per 2 ICU beds, 1 Admin per 5 ICU beds. These are added to total system targets.
    *   Hierarchical allocation order: ICU first, Med-Surg Beds second, Outpatient Clinics third, Emergency Department fourth.
4.  **ED Boarding Mechanics:**
    *   Critical care admission demand is modeled as `(system.staffed_beds + 19) / 20` (5% of staffed beds, ceiling division).
    *   If `effective_icu_capacity < critical_admissions`, the excess patients are boarded in the ED.
    *   Each boarded patient consumes 1 bay of effective ED capacity (i.e. `effective_emergency = (effective_emergency - boarded_patients).max(0)`).
5.  **Strike & CON Delays:** Ensure `PendingEffectKind::IcuCapacity` projects are suspended during RNA strikes.
6.  **CLI & Dashboard:** Update executive report, CLI parsers, autocompletion, and guidance help topics.
7.  **AI Decisions:** Update target calculation and candidate generation in `src/actors/ai_player.rs`.
8.  **Golden Hash / Tests:** Verify transition logic with focused tests, and update/record the competitive golden hash.

## Non-Goals
- No changes to stabilization campaign loops or other service lines.
- No general framework extensions or macro-level payment modeling.

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
