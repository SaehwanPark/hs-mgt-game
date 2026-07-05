# Operational Coding Plan - Obstetrics Service Line & L&D Diversion Mechanics

## Task restatement

Implement the Obstetrics (Labor & Delivery) service line with associated capacity, staffing targets, hierarchical allocation rules prioritizing Obstetrics second (after ICU and before Med-Surg Beds), and an obstetric capacity-diversion penalty representing the "halo effect". This must be implemented while preserving all existing campaign, parser, AI, and verification rules without causing backward compatibility breaks in stabilization or competitive scenarios.

## Current understanding

- **Relevant code appears to be in:**
  - `src/model/competitive_world.rs` (State definitions, `PendingEffectKind`)
  - `src/model/competitive_command.rs` (Domain and project command enum types)
  - `src/model/campaign.rs` (Player observation struct)
  - `src/sim/observe_ai.rs` (AI player observation struct)
  - `src/sim/effects_competitive.rs` (Applying project completion effects)
  - `src/sim/transition_competitive.rs` (Command application, staffing targets, hierarchy, and diversion penalties)
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
  - Obstetrics capacity (`obstetrics_capacity`) is added to the system state, defaulting to 0.
  - Adding `InvestDomain::Obstetrics` (alias `"obstetrics"`, `"obs"`) and `ProjectKind::ObstetricsUnit` (alias `"obstetrics_unit"`, `"obs_unit"`, duration 9 months, yields +6 capacity).
  - Obstetrics staffing target ratios: Nurses (1 Nurse per 2 beds), Physicians (1 Physician per 5 beds), Admins (1 Admin per 10 beds).
  - Allocation order: ICU -> Obstetrics -> Med-Surg Beds -> Outpatient Clinics -> ED.
  - Diverting patients when obstetric demand (10% of obstetric capacity) exceeds effective obstetric capacity, yielding `-2` community trust and `-1` market share index per diverted patient.
- **Existing behavior that must not change is:**
  - Stabilization campaign execution and rules.
  - All existing 273 unit/integration tests must pass.
  - Existing custom scenarios or session saves must continue to load without errors.

## Assumptions

- Adding a new `InvestDomain` and `ProjectKind` variant is backwards-compatible since we will exhaustively update all match statements across the codebase.
- Setting default value for `obstetrics_capacity` to 0 in scenarios and genesis templates prevents turn-1 staffing deficits or discrepancies.
- The competitive state hash must include `obstetrics_capacity` in its format to maintain strict deterministic verification.

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1.  **Inspect files:** Verify existing service lines (e.g. `icu_capacity` and `emergency_capacity`) are defined in `src/model/competitive_world.rs` and matching locations.
2.  **State and Command Types changes:**
    *   Add `pub obstetrics_capacity: i32` to `HealthSystemState` in `src/model/competitive_world.rs` (with `#[serde(default)]`).
    *   Add `ObstetricsCapacity { capacity_delta: i32, project_draw: Option<i32> }` to `PendingEffectKind` in `src/model/competitive_world.rs`.
    *   Add `obstetrics_capacity` to `PlayerObservation` in `src/model/campaign.rs` and `AiPlayerObservation` in `src/sim/observe_ai.rs`.
    *   Add `Obstetrics` variant to `InvestDomain` and `ObstetricsUnit` variant to `ProjectKind` in `src/model/competitive_command.rs`. Update `resolve_months` (returns 9) and `action_cost` (AP cost 2, monthly draw = budget / 9).
3.  **Harness and Scenario defaults:**
    *   In `src/scenario/mod.rs`, add `pub obstetrics_capacity: Option<i32>` to `ScenarioSystemState`, default to 0 on mapping.
    *   In `src/competitive/genesis.rs` and `src/competitive/fixtures.rs`, initialize `obstetrics_capacity` to 0.
4.  **Transition Kernel changes:**
    *   In `src/sim/effects_competitive.rs`, resolve `PendingEffectKind::ObstetricsCapacity` inside `resolve_pending_effects` by adding `capacity_delta` and adjusting draws.
    *   In `src/sim/transition_competitive.rs`:
        *   Update `apply_command` match arms:
            *   For `InvestDomain::Obstetrics`, immediate cost is `amount`. Delta beds = `amount / 25`. Immediately increase access by `amount / 25` and market share by `amount / 50`. Enqueue `PendingEffectKind::ObstetricsCapacity { capacity_delta, project_draw: None }` with 1 month delay.
            *   For `ProjectKind::ObstetricsUnit`, enqueue `PendingEffectKind::ObstetricsCapacity { capacity_delta: 6, project_draw: Some(monthly_draw) }`.
        *   In `apply_staffing_constraints`:
            *   Update `target_nurses`, `target_physicians`, `target_admins` formulas to add obstetric requirements.
            *   Update hierarchical nurse and physician allocations to insert Obstetrics as the second priority (after ICU and before Med-Surg).
            *   Compute `effective_obs = system.obstetrics_capacity.min(nurses_obs * 2).min(physicians_obs * 5)`. Halve it if `rna_strike_active` is true.
            *   Compute obstetric demand: `obstetric_demand = (system.obstetrics_capacity + 9) / 10`.
            *   Compute `diverted_patients = (obstetric_demand - effective_obs).max(0)`.
            *   Apply penalties: `-2` community trust and `-1` market share index per diverted patient. Log an event if `diverted_patients > 0`.
            *   Add `obstetrics_capacity` to `total_physical` and `effective_obs` to `total_effective`.
5.  **State Hash updates:**
    *   In `src/model/competitive_hash.rs`, append `|obs={}` to formatting string and format `system.obstetrics_capacity`.
6.  **Observation Model changes:**
    *   In `src/sim/observe_competitive.rs`, populate `obstetrics_capacity`. Update `in_flight_projects_label` to recognize `PendingEffectKind::ObstetricsCapacity`.
    *   In `src/sim/observe_ai.rs`, populate `obstetrics_capacity`.
7.  **AI Player changes:**
    *   In `src/actors/ai_player.rs`, update target calculations in `generate_candidates` and match arms to avoid non-exhaustive compiler warnings.
8.  **Parser and Auto-complete updates:**
    *   In `src/cli/competitive_parse.rs`, parse `obstetrics` (and `obs`) domain and `obstetrics_unit` (and `obs_unit`) project kind.
    *   In `src/cli/repl.rs`, add `"obstetrics"` to domain candidates and `"obstetrics_unit"` to project kinds.
    *   In `src/cli/guidance.rs`, update topic help strings for `invest` and `project` commands.
    *   In `src/cli/display/executive_report.rs`, compute `eff_obs` and format in the report. If diversions occur, format `  • Obstetric diversion: {} patients`.
9.  **Integration Unit Test:** Add a unit test verifying Obstetrics allocation, diversion, trust/market-share penalties, and project resolution.
10. **Replay Hash update:** Run the golden hash generation integration test, fetch the new competitive seed-42 golden state hash, and update the assertion in `tests/golden_competitive_seed42.rs`.

## Files and functions likely to change

- `src/model/competitive_world.rs`: Add fields to `HealthSystemState` and `PendingEffectKind`
- `src/model/competitive_command.rs`: Add variants to `InvestDomain`, `ProjectKind`, and matching arms
- `src/model/campaign.rs`: Add `obstetrics_capacity` to `PlayerObservation`
- `src/scenario/mod.rs`: Add `obstetrics_capacity` to `ScenarioSystemState`
- `src/competitive/genesis.rs`: Initialize `obstetrics_capacity` to 0
- `src/competitive/fixtures.rs`: Initialize `obstetrics_capacity` to 0
- `src/sim/observe_ai.rs`: Add field to `AiPlayerObservation` and map it
- `src/sim/effects_competitive.rs`: Add resolution arm for `PendingEffectKind::ObstetricsCapacity`
- `src/sim/transition_competitive.rs`: Update `apply_command`, `apply_staffing_constraints` (targets, hierarchy, diversion penalties), and add unit test
- `src/sim/observe_competitive.rs`: Map field to observation, update project label mapping
- `src/model/competitive_hash.rs`: Format state hash with `obstetrics_capacity`
- `src/cli/competitive_parse.rs`: Add parser support for `"obstetrics"` and `"obstetrics_unit"`
- `src/cli/repl.rs`: Add autocomplete strings
- `src/cli/guidance.rs`: Update help texts
- `src/cli/display/executive_report.rs`: Render Obstetrics capacity and diversions on dashboard
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

- `project kind=obstetrics_unit budget=45` parses and schedules a 9-month project drawing $5/month.
- Completing the project yields `obstetrics_capacity += 6` beds.
- `invest domain=obstetrics amount=25` immediately yields +1 obstetric capacity bed.
- If obstetric beds are staffed with at least 1 nurse per 2 beds and 1 physician per 5 beds, and no deficit occurs, diversions are 0.
- If a staffing deficit in Obstetrics occurs (e.g. not enough nurses), effective capacity drops, and if it falls below 10% of capacity, patients are diverted, causing `-2` community trust and `-1` market share index per diverted patient.
- Existing campaigns run without regression, and the updated golden seed-42 hash is asserted successfully.

## Non-goals

- Do not change stabilization campaign rules.
- Do not introduce a NICU or other pediatric service lines.
- Do not add complex clinical pathways or clinical outcome factors outside trust/access/quality indices.
- Do not perform unrelated refactoring.

## Stop conditions

Stop and ask for review if:
- More than 20 production files need edits.
- The implementation requires changing the core simultaneous resolver sequence itself.
- Tests reveal unexpected changes in the stabilization campaign loop outcomes.

## Review checklist

Before finalizing, verify:
- The diff implements only the requested Obstetrics behavior.
- The change is covered by focused unit tests verifying hierarchical allocation, effective capacity, and diversion.
- Existing behavior is preserved.
- No unrelated formatting, renaming, or cleanup was introduced.
- Error handling and edge cases are explicit.
- The final summary lists files changed and tests run.

## Risk label

Risk: Medium

Reason: This change affects system state fields, parser inputs, transition logic, AI decision targets, state hashes, and CLI dashboards, which could impact regression test hashes and scenario compatibility if not isolated carefully.
