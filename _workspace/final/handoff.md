# Final Handoff - ICU Service Line & ED Boarding Mechanics

## Summary of Changes
1.  **State and Observation Extensions:**
    *   Added `icu_capacity` to `HealthSystemState` in `src/model/competitive_world.rs` (defaulting to 0).
    *   Added `PendingEffectKind::IcuCapacity` to track in-flight ICU Wing projects.
    *   Extended `PlayerObservation` in `src/model/campaign.rs` and `AiPlayerObservation` in `src/sim/observe_ai.rs` with the `icu_capacity` field.
2.  **Command and Cost Vocabulary:**
    *   Added `InvestDomain::Icu` and `ProjectKind::IcuWing` to `src/model/competitive_command.rs`.
    *   Configured `IcuWing` duration to 12 months, AP cost to 3 (compared to 2 for other projects), and cash draw to `budget / 12` monthly.
3.  **Transition Kernel Rules (Staffing & Boarding):**
    *   Implemented high-intensity ICU staffing targets (1 Nurse per 1 Bed, 1 Physician per 2 Beds, 1 Admin per 5 Beds).
    *   Added ICU first in the hierarchical staffing allocation: ICU -> Med-Surg Beds -> Outpatient Clinics -> Emergency Department.
    *   Implemented ED Boarding: critical admissions demand is calculated as `(staffed_beds + 19) / 20` (5% of staffed beds). If `effective_icu < critical_admissions`, the remainder board in the ED, consuming ED bays on a 1-to-1 basis.
    *   Added strike active suspension for ICU Wing projects.
4.  **CLI and User Interface:**
    *   Updated the Stata CLI parser, auto-completion candidate arrays, and command help topic guides to support ICU and IcuWing.
    *   Updated the REPL Executive report dashboard to calculate and display ICU capacity, effective ICU capacity, ED boarding count, and updated emergency capacity.
5.  **State Hash and Deterministic Replay:**
    *   Included `icu_capacity` in the `competitive_state_hash_record` in `src/model/competitive_hash.rs` to ensure exact deterministic validation.
    *   Updated the seed-42 golden hash test assertion to the new schema-compliant value `"2904083fb91b2770"`.
6.  **Test Coverage:**
    *   Added the `test_icu_department_mechanics` integration unit test in `src/sim/transition_competitive.rs` to verify ICU investment, staffing targets, hierarchical allocation, ED boarding, and capacity-deficit index penalties.

## Verification Results
*   Ran `cargo fmt` and `cargo test`.
*   All 273 tests passed successfully.
