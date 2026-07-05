# Mechanism Design & Implementation Plan: Medicare Public Payer Integration

## Task restatement

Implement the Medicare public payer integration in the competitive regional campaign loop. This introduces `PayerId::Medicare` supporting quality compliance alignment with neutral posture, cost validation, transition quality/policy pressure effects, CLI parser support, REPL autocompletion, topic guidance help, and end-of-campaign debrief updates. All existing commercial and Medicaid negotiation mechanics, and the stabilization campaign loop, must be preserved.

## Current understanding

- **Payer Modeling:** Payers are represented by `PayerId` in `src/model/competitive_command.rs`. `PayerId::Medicaid` was added in v0.5.5.
- **Negotiation Rules:** Commercial carriers (`CarrierA`, `CarrierB`) allow `aggressive`, `neutral`, or `conservative` rate postures. Medicaid only allows `neutral`. We need to add `Medicare` and also restrict it to `neutral` posture.
- **Resource Costs:** Costs are calculated in `CompetitiveCommand::resource_costs` in `src/model/competitive_command.rs`. Medicaid costs 1 AP, 2 PC, and $5 cash. Medicare should cost 1 AP, 2 PC, and $10 cash.
- **State Transition:** Transition effects are applied in `transition_competitive.rs`. Medicaid adds +3 access index, -3 policy pressure, and logs a specific event. Medicare should add +3 quality index, -3 policy pressure, and log a specific event.
- **Validation:** Command validation in `src/sim/validate_competitive.rs` checks that Medicaid uses only neutral posture. We must add the same check for Medicare.
- **CLI and REPL:** Parser in `src/cli/competitive_parse.rs` needs to parse `"medicare"`. Complete and help topics in `src/cli/guidance.rs` and `src/cli/repl.rs` need to list `"medicare"`.

## Assumptions

- Medicare compliance does not affect commercial payer negotiations or commercial pressure indices.
- All systems (player and AI) can use the `negotiate payer=medicare` command if they have enough cash/PC.
- Medicare compliance only supports `neutral` posture; any other posture must fail validation.
- Existing tests and golden hashes for campaigns must not be broken except where the new option is added to autocompletes or guidance (no behavior changes to existing runs/seeds).

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. **Model Modification:**
   - Add `Medicare` to `PayerId` in `src/model/competitive_command.rs`.
   - Update `CompetitiveCommand::resource_costs` to charge $10 cash for `PayerId::Medicare`.
2. **CLI Parser & Guidance updates:**
   - Update `parse_payer_id` in `src/cli/competitive_parse.rs` to match `"medicare"`.
   - Update `format_competitive_command` in `src/competitive/resolution.rs` and `src/debrief/report.rs` to support formatting `PayerId::Medicare` as `"medicare"`.
   - Update `src/cli/guidance.rs` to include `"medicare"` in topics and command help instructions, detailing its costs (1 AP, 2 PC, $10 cash) and effects.
   - Update `src/cli/repl.rs` to include `"medicare"` in completion options for `payer=`.
3. **Validation Logic:**
   - Update `validate_command` in `src/sim/validate_competitive.rs` to check if `payer` is `Medicare` and return a validation error if the posture is not `Neutral`. Add `InvalidMedicarePosture` to `CompetitiveValidationError` (similar to Medicaid).
4. **Transition Logic:**
   - In `src/sim/transition_competitive.rs`, process `PayerId::Medicare` negotiations:
     - Apply `quality_index += 3` and `policy_pressure -= 3` as attributed effects.
     - Log a public action: `"{system_name}: Medicare quality compliance alignment"`.
     - Exclude Medicare negotiations from the commercial payer negotiation count in `apply_institution_phase` (like Medicaid).
5. **Testing & Golden Fixtures:**
   - Add unit tests in `src/sim/validate_competitive_tests.rs` for Medicare validation (neutral posture passes, non-neutral fails, insufficient resources fails).
   - Add unit tests in `src/sim/transition_competitive.rs` verifying transition effects.
   - Run `cargo test` and ensure all tests pass.
   - Update version to `0.5.7` (0.0.1 PR-equivalent increase) in `Cargo.toml` and record changes in `CHANGELOG.md` and `SPEC.md`.

## Files and functions likely to change

- `src/model/competitive_command.rs`: Add `PayerId::Medicare`, update `resource_costs`.
- `src/model/resources.rs`: Add `InvalidMedicarePosture` to `CompetitiveValidationError`.
- `src/cli/competitive_parse.rs`: Update `parse_payer_id` to parse `"medicare"`.
- `src/cli/guidance.rs`: Update command help, guidance strings, and examples for negotiate command.
- `src/cli/repl.rs`: Update autocompletion enum list.
- `src/competitive/resolution.rs`: Update CLI command formatter string.
- `src/debrief/report.rs`: Update report formatter string.
- `src/sim/validate_competitive.rs`: Enforce `RatePosture::Neutral` for Medicare.
- `src/sim/transition_competitive.rs`: Implement transition effects, log events.
- `src/sim/validate_competitive_tests.rs`: Add validation tests.
- `Cargo.toml`: Version bump to `0.5.7`.
- `SPEC.md`: Move feature to `Present`/`Done` and record details.
- `CHANGELOG.md`: Record new version and additions.

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
- Version is correctly bumped by `0.0.1` to `0.5.7`.
- `SPEC.md` and `CHANGELOG.md` are updated.

## Risk label

Risk: Low

Reason: Follows the established design pattern of Medicaid integration (v0.5.5), which is highly isolated and modular.
