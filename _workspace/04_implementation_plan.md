# Implementation Plan - Emergency Department Service Line

## 1. Domain Struct Changes
- `src/model/competitive_world.rs`:
  - Add `pub emergency_capacity: i32` to `HealthSystemState`.
  - Add `EmergencyCapacity { capacity_delta: i32, project_draw: Option<i32> }` to `PendingEffectKind`.
- `src/model/campaign.rs`:
  - Add `pub emergency_capacity: i32` to `PlayerObservation`.
- `src/sim/observe_ai.rs`:
  - Add `pub emergency_capacity: i32` to `AiPlayerObservation`.

## 2. Command Vocabulary Expansion
- `src/model/competitive_command.rs`:
  - Add `Emergency` to `InvestDomain` enum.
  - Add `EmergencyPavilion` to `ProjectKind` enum.
  - Update `ProjectKind::resolve_months` to return `6` for `EmergencyPavilion`.
  - Update `is_public_command` in `src/sim/transition_competitive.rs` and `command_intel_summary` to support `Emergency` and `EmergencyPavilion`.
  - Update `ActionCost` mapping in `CompetitiveCommand::action_cost`:
    - For `ProjectKind::EmergencyPavilion`, AP cost is 2, monthly draw is `budget / 6`.

## 3. Transition Kernel updates
- `src/sim/effects_competitive.rs`:
  - Handle `PendingEffectKind::EmergencyCapacity` resolution inside `resolve_pending_effects` by incrementing `system.emergency_capacity` and adjusting active projects/draws.
- `src/sim/transition_competitive.rs`:
  - Update `apply_command` for `InvestDomain::Emergency`:
    - `let emergency_delta = amount / 15;`
    - `let access_delta = amount / 15;`
    - Immediate `access_index` increment of `access_delta` and `market_share_index` increment of `amount / 30`.
    - Enqueue `PendingEffectKind::EmergencyCapacity { capacity_delta: emergency_delta, project_draw: None }`.
  - Update `apply_command` for `ProjectKind::EmergencyPavilion`:
    - Enqueue `PendingEffectKind::EmergencyCapacity { capacity_delta: 15, project_draw: Some(monthly_draw) }`.
  - Refactor `apply_staffing_constraints`:
    - Compute targets:
      - `target_nurses = (system.staffed_beds + 4) / 5 + (system.emergency_capacity + 1) / 2;`
      - `target_physicians = (system.outpatient_capacity + 9) / 10 + (system.emergency_capacity + 3) / 4;`
      - `target_admins = (system.staffed_beds + system.outpatient_capacity + system.emergency_capacity + 19) / 20;`
    - Calculate effective capacities:
      - Allocate nurses to beds first: `nurses_for_beds = system.nurses.min((system.staffed_beds + 4) / 5)`.
      - Allocate remaining nurses to emergency: `nurses_for_ed = (system.nurses - nurses_for_beds).max(0)`.
      - Allocate physicians to outpatient first: `physicians_for_outpatient = system.physicians.min((system.outpatient_capacity + 9) / 10)`.
      - Allocate remaining physicians to emergency: `physicians_for_ed = (system.physicians - physicians_for_outpatient).max(0)`.
      - `effective_beds = system.staffed_beds.min(nurses_for_beds * 5);`
      - `effective_outpatient = system.outpatient_capacity.min(physicians_for_outpatient * 10);`
      - `effective_emergency = system.emergency_capacity.min(nurses_for_ed * 2).min(physicians_for_ed * 4);`
    - Update `total_physical = system.staffed_beds + system.outpatient_capacity + system.emergency_capacity;`
    - Update `total_effective = effective_beds + effective_outpatient + effective_emergency;`
    - Compute `penalty` and apply to access/quality.

## 4. State Hash & Display Alignment
- `src/model/competitive_hash.rs`:
  - Add `|emergency={}` to system formatting block in `competitive_state_hash_record` and format `system.emergency_capacity`.
- `src/sim/observe_competitive.rs`:
  - Populate `emergency_capacity` in `PlayerObservation`.
  - Update `in_flight_projects_label` to recognize `PendingEffectKind::EmergencyCapacity` and format as `EmergencyPavilion`.
- `src/sim/observe_ai.rs`:
  - Populate `emergency_capacity` in `AiPlayerObservation`.
- `src/cli/display/executive_report.rs`:
  - Calculate `eff_emergency` and display:
    `  • Emergency capacity: {} bays (effective: {})`

## 5. Parser, Auto-complete, and Help Topic Updates
- `src/cli/competitive_parse.rs`:
  - Update `InvestDomain` parsing to recognize `"emergency"`.
  - Update `ProjectKind` parsing to recognize `"emergency_pavilion"`.
- `src/cli/guidance.rs` & `src/cli/repl.rs`:
  - Add autocomplete options for `"emergency"` domain and `"emergency_pavilion"` project kind.
  - Document the new investment domain and project kind in command topic help guides.

## 6. Scenario System Compatibility
- `src/scenario/mod.rs`:
  - Add `pub emergency_capacity: Option<i32>` to `ScenarioSystemState`.
  - Default it during mapping to `HealthSystemState`:
    - system_id 0 => 15
    - system_id 1 => 20
    - system_id 2 => 10
    - system_id 3 => 8
    - system_id 4 => 25
    - default => 15
- `src/competitive/genesis.rs`:
  - Add `emergency_capacity` to `RivalTemplate` and initialize all presets.
  - Update `genesis_roster_lines` to print emergency bays.

## 7. AI Decision Support
- `src/actors/ai_player.rs`:
  - Update targets in `generate_candidates`:
    - `target_nurses = (observation.staffed_beds + 4) / 5 + (observation.emergency_capacity + 1) / 2;`
    - `target_physicians = (observation.outpatient_capacity + 9) / 10 + (observation.emergency_capacity + 3) / 4;`
    - `target_admins = (observation.staffed_beds + observation.outpatient_capacity + observation.emergency_capacity + 19) / 20;`
  - Update `best_response_commands` to handle `emergency` investment responses.
