# Request Summary - Clinical Service Lines and Staffing (Phase 6 - Track 5)

## Scope
Implement clinical service line capacity and staffing requirements in the competitive regional campaign.
Specifically:
- Differentiate between two service lines: Inpatient Beds (`staffed_beds`) and Outpatient Clinics (`outpatient_capacity`).
- Add `outpatient_capacity`, `nurses`, and `physicians` metrics to `HealthSystemState`.
- Map `InvestDomain::Beds` to physical inpatient capacity (`staffed_beds`) and `InvestDomain::Outpatient` to physical outpatient capacity (`outpatient_capacity`).
- Map `RecruitRole::Nurse` to `nurses` and `RecruitRole::Physician` to `physicians`.
- Implement dynamic staffing ratio constraints and understaffing penalties:
  - Target: 5 inpatient beds per nurse, 10 outpatient clinic units per physician.
  - Compute effective capacity based on staffing: `effective_beds = nurses * 5`, `effective_outpatient = physicians * 10`.
  - Penalize `access_index`, `quality_index`, and `workforce_trust` when physical capacity exceeds effective staffed capacity.
- Update `ProjectKind::Tower` and `ProjectKind::ClinicNetwork` to grant physical capacities.
- Update serialization, parsing, state hashing, CLI displays, and unit tests.

## Non-Goals
- No changes to stabilization campaign rules or schema.
- No changes to the Stata command grammar (keep the same 7 verbs and parameters).
- No multiplayer network capabilities.
- No new external crate dependencies.

## Sources
- `src/model/competitive_world.rs`
- `src/model/competitive_command.rs`
- `src/model/competitive_hash.rs`
- `src/sim/effects_competitive.rs`
- `src/sim/transition_competitive.rs`
- `src/cli/display/executive_report.rs`

## Expected Files
- `src/model/competitive_world.rs`
- `src/model/competitive_command.rs`
- `src/model/competitive_hash.rs`
- `src/sim/effects_competitive.rs`
- `src/sim/transition_competitive.rs`
- `src/cli/display/executive_report.rs`
- `Cargo.toml`
- `CHANGELOG.md`
- `SPEC.md`

## Validation Target
- All cargo tests pass cleanly (245+ tests).
- `cargo clippy --all-targets -- -D warnings` compiles without warnings.
- `cargo fmt --check` passes cleanly.
