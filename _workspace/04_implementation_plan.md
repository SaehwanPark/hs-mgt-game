# Coding Implementation Plan - Medicare Public Payer Integration

## Task restatement

Implement the Medicare public payer integration in the competitive regional campaign loop. This introduces `PayerId::Medicare` supporting quality compliance alignment with neutral posture, validation checks, transition effects (+3 quality, -3 policy pressure), CLI parser updates, REPL autocompletion, topic guidance help, and end-of-campaign debrief updates. All existing commercial and Medicaid negotiation mechanics, and the stabilization campaign loop, must be preserved.

## Current understanding

- **Payer Modeling:** Payers are represented by the `PayerId` enum in `src/model/competitive_command.rs`. `PayerId::Medicaid` was added in `v0.5.5`.
- **Negotiation Rules:** Commercial carriers (`CarrierA`, `CarrierB`) allow `Aggressive`, `Neutral`, or `Conservative` rate postures. Medicaid and Medicare only allow `Neutral` posture.
- **Resource Costs:** Managed by `CompetitiveCommand::action_cost` in `src/model/competitive_command.rs`. Medicare compliance costs 1 AP, 2 PC, and $10 cash (compared to Medicaid's $5 cash).
- **State Transition:** Transition effects are applied in `src/sim/transition_competitive.rs`. Medicare compliance alignment increases `quality_index` by 3 and decreases `policy_pressure` by 3.
- **Payer Pressure:** In `src/sim/effects_competitive.rs`, commercial payer pressure is calculated in `apply_institution_phase`. Medicare must be excluded from this count, just like Medicaid.
- **Validation:** Command validation is in `src/sim/validate_competitive.rs`. If Medicare is negotiated with a non-neutral posture, it must fail validation with a new error `CompetitiveValidationError::InvalidMedicarePosture`.
- **CLI/REPL:** Parser in `src/cli/competitive_parse.rs` needs to support `"medicare"`. Complete and help topics in `src/cli/guidance.rs` and `src/cli/repl.rs` must list `"medicare"`.

## Assumptions

- Medicare compliance does not affect commercial payer negotiations or commercial pressure indices.
- All systems (player and AI) can use the `negotiate payer=medicare` command if they have enough cash/PC.
- Medicare compliance only supports `neutral` posture; any other posture must fail validation.
- Existing tests and golden hashes for campaigns must not be broken except where the new option is added to autocompletes or guidance (no behavior changes to existing runs/seeds).

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. **Model Modification:**
   - Add `Medicare` variant to `PayerId` enum in [src/model/competitive_command.rs](file:///Users/saehwan/repos/hs-mgt-game/src/model/competitive_command.rs).
   - Update `CompetitiveCommand::action_cost` in [src/model/competitive_command.rs](file:///Users/saehwan/repos/hs-mgt-game/src/model/competitive_command.rs) to charge $10 cash for `PayerId::Medicare`.
   - Add `InvalidMedicarePosture` to `CompetitiveValidationError` enum and implement its message formatting in [src/model/resources.rs](file:///Users/saehwan/repos/hs-mgt-game/src/model/resources.rs).
2. **CLI Parser & Guidance updates:**
   - Update `parse_payer` in [src/cli/competitive_parse.rs](file:///Users/saehwan/repos/hs-mgt-game/src/cli/competitive_parse.rs) to match and parse `"medicare"`.
   - Update `COMPETITIVE_COMMAND_SPECS` usage string in [src/cli/competitive_parse.rs](file:///Users/saehwan/repos/hs-mgt-game/src/cli/competitive_parse.rs) to list `"medicare"`.
   - Update `format_competitive_command` in [src/competitive/resolution.rs](file:///Users/saehwan/repos/hs-mgt-game/src/competitive/resolution.rs) and `src/debrief/report.rs` to format `PayerId::Medicare` as `"medicare"`.
   - Update `src/cli/guidance.rs` to include `"medicare"` in CLI help topics and detailed examples for the `negotiate` command.
   - Update `src/cli/repl.rs` to include `"medicare"` in completion options for `payer=`.
3. **Validation Logic:**
   - Update `validate_competitive_command` in [src/sim/validate_competitive.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/validate_competitive.rs) to enforce `RatePosture::Neutral` for `PayerId::Medicare` and return `CompetitiveValidationError::InvalidMedicarePosture` if non-neutral.
4. **Transition Logic:**
   - In [src/sim/transition_competitive.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/transition_competitive.rs), process `PayerId::Medicare` negotiations:
     - Apply `quality_index += 3` (clamped) and `policy_pressure -= 3` (clamped) as attributed effects.
     - Log a public event: `"{system_name}: Medicare compliance alignment (improved quality, reduced policy pressure)"`.
   - Update `command_intel_summary` in [src/sim/transition_competitive.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/transition_competitive.rs) to return `Some("{system_name}: Medicare compliance alignment")`.
   - Update `apply_institution_phase` in [src/sim/effects_competitive.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/effects_competitive.rs) to filter out Medicare negotiations from commercial payer negotiation counts (like Medicaid).
5. **Testing & Golden Fixtures:**
   - Add unit tests in [src/sim/validate_competitive_tests.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/validate_competitive_tests.rs) for Medicare validation (neutral passes, non-neutral fails, insufficient resources fails).
   - Add unit tests in [src/sim/transition_competitive.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/transition_competitive.rs) verifying Medicare transition effects, events, and metrics.
   - Run `cargo test` and ensure all tests pass.
   - Update version to `0.5.8` in `Cargo.toml`.
   - Document changes in `CHANGELOG.md` and `SPEC.md`.

## Files and functions likely to change

- [src/model/competitive_command.rs](file:///Users/saehwan/repos/hs-mgt-game/src/model/competitive_command.rs): `PayerId` enum, `CompetitiveCommand::action_cost`
- [src/model/resources.rs](file:///Users/saehwan/repos/hs-mgt-game/src/model/resources.rs): `CompetitiveValidationError` enum and `message()`
- [src/cli/competitive_parse.rs](file:///Users/saehwan/repos/hs-mgt-game/src/cli/competitive_parse.rs): `COMPETITIVE_COMMAND_SPECS` usage, `parse_payer`
- [src/cli/guidance.rs](file:///Users/saehwan/repos/hs-mgt-game/src/cli/guidance.rs): `command_topic_help_lines`, help strings
- [src/cli/repl.rs](file:///Users/saehwan/repos/hs-mgt-game/src/cli/repl.rs): autocompletion enum list
- [src/competitive/resolution.rs](file:///Users/saehwan/repos/hs-mgt-game/src/competitive/resolution.rs): `format_competitive_command`
- [src/debrief/report.rs](file:///Users/saehwan/repos/hs-mgt-game/src/debrief/report.rs): format helper for command summary
- [src/sim/validate_competitive.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/validate_competitive.rs): `validate_competitive_command`
- [src/sim/transition_competitive.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/transition_competitive.rs): `transition_competitive` negotiation branch, `command_intel_summary`, unit tests
- [src/sim/effects_competitive.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/effects_competitive.rs): `apply_institution_phase` PayerId matches filter
- [src/sim/validate_competitive_tests.rs](file:///Users/saehwan/repos/hs-mgt-game/src/sim/validate_competitive_tests.rs): unit tests for Medicare validation
- [Cargo.toml](file:///Users/saehwan/repos/hs-mgt-game/Cargo.toml): version bump
- [SPEC.md](file:///Users/saehwan/repos/hs-mgt-game/SPEC.md): Move feature track to Done
- [CHANGELOG.md](file:///Users/saehwan/repos/hs-mgt-game/CHANGELOG.md): Record new version and additions

Avoid editing files outside this list unless the plan is found to be incomplete. If that happens, stop and explain why.

## Tests and checks

Run `cargo test`.

Expected result:
- All 260+ tests pass successfully.
- Code compiles without warnings.

If tests fail:
1. Fix failures directly related to this change.
2. Do not fix unrelated failures unless required to unblock validation.
3. Report unrelated failures separately.

## Acceptance criteria

- `negotiate payer=medicare rate_posture=neutral` compiles, parses, validates, and runs.
- `negotiate payer=medicare rate_posture=aggressive` fails validation with `InvalidMedicarePosture`.
- Executing Medicare compliance alignment deducts 1 AP, 2 PC, and $10 cash, increasing quality index by 3 and decreasing policy pressure by 3.
- `help negotiate` displays details for Medicare.
- The REPL auto-completes `payer=medicare`.
- All existing tests continue to pass cleanly.

## Non-goals

- Do not change stabilization campaign rules.
- Do not modify commercial payer negotiations logic or rates.
- Do not add Medicare patient enrollment or reimbursement volume tracking.
- Do not perform drive-by formatting or cleanups in untouched files.

## Stop conditions

Stop and ask for review if:
- Implementing Medicare requires changing the structure of `CompetitiveWorldState` or `HealthSystemState`.
- Any existing commercial payer rate-negotiation tests fail.
- Running `cargo test` hangs or timeouts.

## Review checklist

Before finalizing, verify:
- The diff implements only the requested Medicare behavior.
- The change is covered by focused tests in `validate_competitive_tests.rs` and `transition_competitive.rs`.
- Existing behavior is preserved.
- No unrelated formatting, renaming, or cleanup was introduced.
- Version is correctly bumped by `0.0.1` to `0.5.8`.
- `SPEC.md` and `CHANGELOG.md` are updated.

## Risk label

Risk: Low

Reason: Follows the established design pattern of Medicaid integration (v0.5.5), which is highly isolated and modular.
