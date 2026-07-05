# Operational Coding Plan - Psychiatric Service Line & Behavioral Health crisis holding mechanics

## Task restatement

Implement the Psychiatric (Behavioral Health) service line with associated capacity, staffing targets, hierarchical allocation rules prioritizing Psychiatric fourth (after Med-Surg and before Outpatient), emergency department boarding mechanics, and access/trust diversion penalties. This must be implemented while preserving all existing campaign, parser, AI, and verification rules without causing backward compatibility breaks in stabilization or competitive scenarios.

## Current understanding

- **Relevant code appears to be in:**
  - `src/model/competitive_world.rs` (State definitions, `PendingEffectKind`)
  - `src/model/competitive_command.rs` (Domain and project command enum types)
  - `src/model/campaign.rs` (Player observation struct)
  - `src/sim/observe_ai.rs` (AI player observation struct)
  - `src/sim/effects_competitive.rs` (Applying project completion effects)
  - `src/sim/transition_competitive.rs` (Command application, staffing targets, hierarchy, boarding, and diversion penalties)
  - `src/sim/observe_competitive.rs` (Formatting observations, in-flight projects label)
  - `src/cli/competitive_parse.rs` (Command input parsing)
  - `src/cli/display/executive_report.rs` (Executive REPL dashboard metrics rendering)
  - `src/cli/guidance.rs` (Topic help topic text)
  - `src/cli/repl.rs` (Tab autocomplete candidates)
  - `src/actors/ai_player.rs` (AI player command candidate generation)
  - `src/competitive/genesis.rs` & `src/competitive/fixtures.rs` (Initial competitive worlds)
  - `src/model/competitive_hash.rs` (System hash record for deterministic validation)
  - `src/scenario/mod.rs` (Scenario loading and defaults)
- **Desired behavior is:**
  - Psychiatric capacity (`psychiatric_capacity`) is added to the system state, defaulting to 0.
  - Adding `InvestDomain::Psychiatric` (alias `"psychiatric"`, `"psych"`) and `ProjectKind::PsychiatricUnit` (alias `"psychiatric_unit"`, `"psych_unit"`, duration 6 months, yields +5 capacity).
  - Psychiatric staffing targets: Nurses (1 Nurse per 4 beds), Physicians (1 Physician per 10 beds), Admins (1 Admin per 15 beds).
  - Allocation order: ICU -> Obstetrics -> Med-Surg Beds -> Psychiatric -> Outpatient Clinics -> ED.
  - ED Boarding: Psychiatric demand (10% of psychiatric capacity, ceiling division) in excess of effective psychiatric capacity is boarded in the ED on a 1-to-1 basis, directly reducing effective emergency capacity.
  - Diversion: Psychiatric overflow boarding in ED that exceeds available emergency capacity is diverted, causing `-1` community trust and `-1` quality index per patient.
- **Existing behavior that must not change is:**
  - Stabilization campaign execution and rules.
  - All existing 273 unit/integration tests must pass.
  - Existing custom scenarios or session saves must continue to load without errors.

## Assumptions

- Adding a new `InvestDomain` and `ProjectKind` variant is backwards-compatible since we will exhaustively update all match statements across the codebase.
- Setting default value for `psychiatric_capacity` to 0 in scenarios and genesis templates prevents turn-1 staffing deficits or discrepancies.
- The competitive state hash must include `psychiatric_capacity` in its format to maintain strict deterministic verification.

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1.  **Inspect files:** Verify existing service lines (e.g. `icu_capacity` and `obstetrics_capacity`) are defined in `src/model/competitive_world.rs` and matching locations.
2.  **State and Command Types changes:**
    *   Add `pub psychiatric_capacity: i32` to `HealthSystemState` in `src/model/competitive_world.rs` (with `#[serde(default)]`).
    *   Add `PsychiatricCapacity { capacity_delta: i32, project_draw: Option<i32> }` to `PendingEffectKind` in `src/model/competitive_world.rs`.
    *   Add `psychiatric_capacity` to `PlayerObservation` in `src/model/campaign.rs` and `AiPlayerObservation` in `src/sim/observe_ai.rs`.
    *   Add `Psychiatric` variant to `InvestDomain` and `PsychiatricUnit` variant to `ProjectKind` in `src/model/competitive_command.rs`. Update `resolve_months` (returns 6) and `action_cost` (AP cost 2, monthly draw = budget / 6).
3.  **Harness and Scenario defaults:**
    *   In `src/scenario/mod.rs`, add `pub psychiatric_capacity: Option<i32>` to `ScenarioSystemState`, default to 0 on mapping.
    *   In `src/competitive/genesis.rs` and `src/competitive/fixtures.rs`, initialize `psychiatric_capacity` to 0.
4.  **Transition Kernel changes:**
    *   In `src/sim/effects_competitive.rs`, resolve `PendingEffectKind::PsychiatricCapacity` inside `resolve_pending_effects` by adding `capacity_delta` and adjusting draws.
    *   In `src/sim/transition_competitive.rs`:
        *   Update `apply_command` match arms:
            *   For `InvestDomain::Psychiatric`, immediate cost is `amount`. Delta beds = `amount / 20`. Immediately increase access by `amount / 20` and market share by `amount / 40`. Enqueue `PendingEffectKind::PsychiatricCapacity { capacity_delta, project_draw: None }` with 1 month delay.
            *   For `ProjectKind::PsychiatricUnit`, enqueue `PendingEffectKind::PsychiatricCapacity { capacity_delta: 5, project_draw: Some(monthly_draw) }`.
        *   In `apply_staffing_constraints`:
            *   Update `target_nurses`, `target_physicians`, `target_admins` formulas to add psychiatric requirements.
            *   Update hierarchical nurse and physician allocations to insert Psychiatric as the fourth priority (after Med-Surg and before Outpatient).
            *   Compute `effective_psych = system.psychiatric_capacity.min(nurses_psych * 4).min(physicians_psych * 10)`. Halve it if `rna_strike_active` is true.
            *   Compute psychiatric demand: `psychiatric_demand = (system.psychiatric_capacity + 9) / 10`.
            *   Compute psychiatric crisis overflow: `psychiatric_overflow = (psychiatric_demand - effective_psych).max(0)`.
            *   Board overflow patients in ED: `boarded_psych = psychiatric_overflow.min(effective_emergency)`. Deduct `boarded_psych` from `effective_emergency`.
            *   Compute diverted psychiatric patients: `diverted_psych = (psychiatric_overflow - boarded_psych).max(0)`.
            *   Apply penalties: `-1` community trust and `-1` quality index per diverted psychiatric patient. Log an event if `diverted_psych > 0` or if `boarded_psych > 0`.
            *   Add `psychiatric_capacity` to `total_physical` and `effective_psych` to `total_effective`.
5.  **State Hash updates:**
    *   In `src/model/competitive_hash.rs`, append `|psych={}` to formatting string and format `system.psychiatric_capacity`.
6.  **Observation Model changes:**
    *   In `src/sim/observe_competitive.rs`, populate `psychiatric_capacity`. Update `in_flight_projects_label` to recognize `PendingEffectKind::PsychiatricCapacity`.
    *   In `src/sim/observe_ai.rs`, populate `psychiatric_capacity`.
7.  **AI Player changes:**
    *   In `src/actors/ai_player.rs`, update target calculations in `generate_candidates` and match arms to avoid non-exhaustive compiler warnings.
8.  **Parser and Auto-complete updates:**
    *   In `src/cli/competitive_parse.rs`, parse `psychiatric` (and `psych`) domain and `psychiatric_unit` (and `psych_unit`) project kind.
    *   In `src/cli/repl.rs`, add `"psychiatric"` to domain candidates and `"psychiatric_unit"` to project kinds.
    *   In `src/cli/guidance.rs`, update topic help strings for `invest` and `project` commands.
    *   In `src/cli/display/executive_report.rs`, compute `eff_psych` and format in the report. If boarding occurs, format `  • Psychiatric ED boarding: {} patients`.
9.  **Integration Unit Test:** Add a unit test verifying Psychiatric allocation, ED boarding, diversion, trust/quality penalties, and project resolution.
10. **Replay Hash update:** Run the golden hash generation integration test, fetch the new competitive seed-42 golden state hash, and update the assertion in `tests/golden_competitive_seed42.rs`.

## Files and functions likely to change

- `src/model/competitive_world.rs`: Add fields to `HealthSystemState` and `PendingEffectKind`
- `src/model/competitive_command.rs`: Add variants to `InvestDomain`, `ProjectKind`, and matching arms
- `src/model/campaign.rs`: Add `psychiatric_capacity` to `PlayerObservation`
- `src/scenario/mod.rs`: Add `psychiatric_capacity` to `ScenarioSystemState`
- `src/competitive/genesis.rs`: Initialize `psychiatric_capacity` to 0
- `src/competitive/fixtures.rs`: Initialize `psychiatric_capacity` to 0
- `src/sim/observe_ai.rs`: Add field to `AiPlayerObservation` and map it
- `src/sim/effects_competitive.rs`: Add resolution arm for `PendingEffectKind::PsychiatricCapacity`
- `src/sim/transition_competitive.rs`: Update `apply_command`, `apply_staffing_constraints` (targets, hierarchy, boarding/diversion), and add unit test
- `src/sim/observe_competitive.rs`: Map field to observation, update project label mapping
- `src/model/competitive_hash.rs`: Format state hash with `psychiatric_capacity`
- `src/cli/competitive_parse.rs`: Add parser support for `"psychiatric"` and `"psychiatric_unit"`
- `src/cli/repl.rs`: Add autocomplete strings
- `src/cli/guidance.rs`: Update help texts
- `src/cli/display/executive_report.rs`: Render Psychiatric capacity, effective capacity, and ED boarding on dashboard
- `src/actors/ai_player.rs`: Handle new enum variants and update targets
- `tests/golden_competitive_seed42.rs`: Update golden state hash assertion after test run

Avoid editing files outside this list unless the plan is found to be incomplete. If that happens, stop and explain why.

## Tests and checks

Run `cargo test`.

Expected result:
- All unit and integration tests compile and pass.
- Standard playtests run without crash or hang.

If tests fail:
1. Fix failures directly related to this change.
2. Do not fix unrelated failures unless required to unblock validation.
3. Report unrelated failures separately.

## Acceptance criteria

- `project kind=psychiatric_unit budget=30` parses and schedules a 6-month project drawing $5/month.
- Completing the project yields `psychiatric_capacity += 5` beds.
- `invest domain=psychiatric amount=20` immediately yields +1 psychiatric capacity bed next month.
- If psychiatric beds are staffed with at least 1 nurse per 4 beds and 1 physician per 10 beds, and no deficit occurs, boarding is 0.
- If a staffing deficit in Psychiatric beds occurs, effective capacity drops, causing patients to board in the ED. If the ED is full, excess psychiatric patients are diverted, causing `-1` community trust and `-1` quality index per patient.
- Existing campaigns run without regression, and the updated golden seed-42 hash is asserted successfully.

## Non-goals

- Do not change stabilization campaign rules.
- Do not introduce specialized inpatient substance use rehab wards.
- Do not perform unrelated refactoring.

## Stop conditions

Stop and ask for review if:
- More than 20 production files need edits.
- The implementation requires changing the core simultaneous resolver sequence itself.
- Tests reveal unexpected changes in the stabilization campaign loop outcomes.

## Review checklist

Before finalizing, verify:
- The diff implements only the requested Psychiatric behavior.
- The change is covered by focused unit tests verifying hierarchical allocation, effective capacity, boarding, and diversion.
- Existing behavior is preserved.
- No unrelated formatting, renaming, or cleanup was introduced.
- Error handling and edge cases are explicit.
- The final summary lists files changed and tests run.

## Risk label

Risk: Medium

Reason: This change affects system state fields, parser inputs, transition logic, AI decision targets, state hashes, and CLI dashboards, which could impact regression test hashes and scenario compatibility if not isolated carefully.
