# Operational Implementation Plan: Neurology & Stroke Center Service Line

This plan describes the continuation of development in the **Broader simulation breadth (Track 5)** of the Health Policy Strategy Game. It outlines how to implement a **Neurology & Stroke Center** service line using the project's `preferred-workflow` and `plan-designer` guidelines.

---

## 1. Task Restatement

Implement the **Neurology & Stroke Center** service line in the competitive regional campaign (`competitive-regional-v1`). This includes adding:
- Neurology capacity and pending effect models.
- Neurology direct investments and capital projects grammar.
- Unit-specific staffing targets (nurses, physicians, admins) and priority-based allocation.
- Inpatient emergency department (ED) holding boarding and diversion mechanics under capacity/staffing deficits.
- Associated parser, REPL autocompletion, executive report rendering, AI player candidates, state hash tracking, TOML scenario loaders, and integration test validation.
- All modifications must preserve backward compatibility for stabilization and competitive campaigns.

---

## 2. Current Understanding

### Base State and Version
- **Base Branch:** `main` (currently clean and up to date).
- **Current Version:** `0.9.0` (with Oncology & Infusion Service Lines complete).
- **Next Version Target:** `0.9.1` (Patch increment for PR delivery).
- **Latest State Hash (v6, oncology and infusion included):** `6044273e2c6c1374` (competitive seed 42).

### Architectural Rules
- Core transitions must remain deterministic.
- Stochasticity is resolved before transitions.
- Separation of True State vs. Player Observations must be preserved.
- Tab size: **2 spaces** throughout the codebase.
- Simple, minimal, and non-speculative code.

---

## 3. Assumptions

- Adding `InvestDomain::Neurology` and `ProjectKind::NeurologyUnit` is backward-compatible because we exhaustively update all match statements across the codebase, as documented in the "Exhaustive Enum Match" lesson of [LESSONS.md](../LESSONS.md).
- Default starting capacity for Neurology must be `0` to prevent turn-1 staffing deficits or discrepancies for old scenarios and unit tests, as per the "Default Capacities" lesson in [LESSONS.md](../LESSONS.md).
- The state hash format will append a `|neuro={}` slot to maintain deterministic validation.

---

## 4. Minimal Implementation Plan

### Step A: Branch Setup
1. Confirm local workspace is clean.
2. From the default branch `main`, fetch remote and pull latest changes:
   ```bash
   git checkout main
   git pull origin main
   ```
3. Create a temporary feature branch:
   ```bash
   git checkout -b feat/neurology-service-line
   ```

### Step B: State and Model Changes
1. **System State Expansion:**
   - In [competitive_world.rs](../src/model/competitive_world.rs), add `#[serde(default)] pub neurology_capacity: i32` to `HealthSystemState`.
   - Add `NeurologyCapacity { capacity_delta: i32, project_draw: Option<i32> }` variant to `PendingEffectKind`.
2. **Command Vocabulary:**
   - In [competitive_command.rs](../src/model/competitive_command.rs), add `Neurology` (aliases: `"neurology"`, `"neuro"`) to `InvestDomain`.
   - Add `NeurologyUnit` (aliases: `"neurology_unit"`, `"neuro_unit"`) to `ProjectKind`.
   - Map `ProjectKind::NeurologyUnit` in `resolve_months` to return `6` months.
   - Update `action_cost` mapping for `ProjectKind::NeurologyUnit` to cost `2` AP and draw `budget / 6` per month (requiring divisibility by 6).
3. **Player Observations:**
   - In [campaign.rs](../src/model/campaign.rs), add `pub neurology_capacity: i32` to `PlayerObservation`.
   - In [observe_ai.rs](../src/sim/observe_ai.rs), add `pub neurology_capacity: i32` to `AiPlayerObservation` and map it.

### Step C: Transition and Mechanics Integration
1. **Payer and Project Resolution:**
   - In [effects_competitive.rs](../src/sim/effects_competitive.rs), implement resolution logic for `PendingEffectKind::NeurologyCapacity`. If a nurse strike is active, suspend monthly project progress (matching Tower and ICU rules).
   - In [transition_competitive.rs](../src/sim/transition_competitive.rs):
     - In `apply_command`, handle `InvestDomain::Neurology`: immediate cash cost = `amount`, yields immediate access/market share increases, and schedules a `NeurologyCapacity { capacity_delta = amount / 20, project_draw: None }` effect resolving next month.
     - Handle `ProjectKind::NeurologyUnit`: schedules `NeurologyCapacity { capacity_delta = 6, project_draw = Some(monthly_draw) }` resolving in 6 months.
2. **Staffing Targets and Hierarchical Allocation:**
   - Staffing targets for Neurology: **1 Nurse per 3 beds**, **1 Physician per 6 beds**, **1 Admin per 10 beds**.
   - Nurse & Physician priority allocation ordering (Neurology is placed 6th, before Oncology and ED):
     `ICU (1st) -> Obstetrics (2nd) -> Med-Surg (3rd) -> Cardiology (4th) -> Psychiatric (5th) -> Neurology (6th) -> Oncology (7th) -> Infusion (8th) -> Outpatient Clinics (9th) -> Emergency Department (10th)`.
   - Compute `effective_neuro = system.neurology_capacity.min(nurses_neuro * 3).min(physicians_neuro * 6)`. Halve it if `rna_strike_active` is true.
3. **ED Boarding & Diversion Mechanics:**
   - Neurology admission demand: `(system.neurology_capacity + 7) / 8` (12.5% of neurology capacity, ceiling division).
   - Overflow: `neurology_overflow = (neurology_demand - effective_neuro).max(0)`.
   - Boarding: neurology overflow boards in available emergency capacity on a 1-to-1 basis (`boarded_neuro = neurology_overflow.min(effective_emergency)`). Deduct `boarded_neuro` from `effective_emergency`.
   - Diversion: `diverted_neuro = (neurology_overflow - boarded_neuro).max(0)`.
   - Penalties: `-2` community trust and `-2` quality index per diverted patient (due to compromised, time-sensitive stroke care).
   - Event logging: Log if `boarded_neuro > 0` or `diverted_neuro > 0`.

### Step D: State Hash Update
1. In [competitive_hash.rs](../src/model/competitive_hash.rs), bump schema version prefix (e.g., to `v7` if v6 is current) and append `|neuro={}` to the state hashing string. Feed `system.neurology_capacity` into the hash.

### Step E: CLI Parser and Autocomplete
1. In [competitive_parse.rs](../src/cli/competitive_parse.rs), support parsing `"neurology"` and `"neuro"` domains, and `"neurology_unit"` and `"neuro_unit"` project kinds.
2. In [repl.rs](../src/cli/repl.rs), add autocomplete strings.
3. In [guidance.rs](../src/cli/guidance.rs), update help guides for `invest` and `project` commands.
4. In [executive_report.rs](../src/cli/display/executive_report.rs), render Neurology capacity, effective capacity, and ED boarding count.

### Step F: Scenario Loader and AI Updates
1. In [mod.rs](../src/scenario/mod.rs), support `neurology_capacity` under `[[systems]]` in the scenario TOML, defaulting to 0 if omitted.
2. In [genesis.rs](../src/competitive/genesis.rs) and [fixtures.rs](../src/competitive/fixtures.rs), initialize `neurology_capacity` to 0.
3. In [ai_player.rs](../src/actors/ai_player.rs), handle the new domain/project variants in target calculations and match arms.

---

## 5. Files and Functions Likely to Change

- **State and Command Enums:**
  - [src/model/competitive_world.rs](../src/model/competitive_world.rs): `HealthSystemState`, `PendingEffectKind`
  - [src/model/competitive_command.rs](../src/model/competitive_command.rs): `InvestDomain`, `ProjectKind`, `resolve_months`, `action_cost`
- **Data Transfer and Loading:**
  - [src/model/campaign.rs](../src/model/campaign.rs): `PlayerObservation`
  - [src/sim/observe_ai.rs](../src/sim/observe_ai.rs): `AiPlayerObservation`
  - [src/scenario/mod.rs](../src/scenario/mod.rs): `ScenarioSystemState`
  - [src/competitive/genesis.rs](../src/competitive/genesis.rs): `genesis_competitive_world`
  - [src/competitive/fixtures.rs](../src/competitive/fixtures.rs): Initial state setups
- **Transition and Effects Engine:**
  - [src/sim/effects_competitive.rs](../src/sim/effects_competitive.rs): `resolve_pending_effects`
  - [src/sim/transition_competitive.rs](../src/sim/transition_competitive.rs): `apply_command`, `apply_staffing_constraints`
  - [src/model/competitive_hash.rs](../src/model/competitive_hash.rs): `record_competitive_hash`
- **CLI REPL Presentation:**
  - [src/cli/competitive_parse.rs](../src/cli/competitive_parse.rs): Parser logic
  - [src/cli/repl.rs](../src/cli/repl.rs): Autocomplete
  - [src/cli/guidance.rs](../src/cli/guidance.rs): Topic help
  - [src/cli/display/executive_report.rs](../src/cli/display/executive_report.rs): rendering
- **Strategic Rivals:**
  - [src/actors/ai_player.rs](../src/actors/ai_player.rs): target calculation matching
- **Verification Tests:**
  - [tests/golden_competitive_seed42.rs](../tests/golden_competitive_seed42.rs): State hash assertion

---

## 6. Tests and Checks

1. **Unit Verification:**
   - Add a test `test_neurology_department_mechanics` in [transition_competitive.rs](../src/sim/transition_competitive.rs) checking:
     - Priority allocation (nurses/physicians allocated to Neurology after Psychiatric and before Oncology).
     - Full capacity staffing vs understaffed boarding.
     - ED boarding math and diverted quality/trust penalties.
2. **Standard Suite Verification:**
   - Compile and verify everything using:
     ```bash
     cargo test
     ```
3. **Golden Replay Regenerating:**
   - Run the golden replay generator to discover the new golden hash (due to adding `neuro` to state hash schema).
   - Update `tests/golden_competitive_seed42.rs` with the updated state hash.

---

## 7. Acceptance Criteria

- Command `project kind=neurology_unit budget=30` successfully schedules a 6-month project drawing $5/month.
- Completing `neurology_unit` adds `+6` to `neurology_capacity`.
- Command `invest domain=neurology amount=20` immediately adds `+1` bed next month.
- Neurology demand equals `(capacity + 7) / 8`.
- If staffed beds are understaffed, patients board in the ED on a 1-to-1 basis.
- If ED is full, excess patients are diverted, costing `-2` community trust and `-2` quality index per patient.
- Existing campaigns run without regression.

---

## 8. Non-Goals

- Do not alter the stabilization campaign loops or parser.
- Do not introduce sub-specialties like pediatric neurology or stroke rehabilitation centers.
- Do not perform unrelated refactoring.

---

## 9. Stop Conditions

- Stop and report if compiler errors cannot be resolved via exhaustive match additions.
- Stop and report if the new hash breaks stabilization regression assertions.
- Stop if more than 20 production files require edits.

---

## 10. Review Checklist

Before finalizing, verify:
- [ ] Only Neurology-specific code changes are made.
- [ ] Ratios are implemented exactly as specified: nurse 1:3, physician 1:6, admin 1:10.
- [ ] Priority order places Neurology 6th (ICU -> Obs -> Med-Surg -> Cardio -> Psych -> Neuro -> Onco -> Infusion -> Outpatient -> ED).
- [ ] Trust and quality penalties are exactly `-2` for diverted patients.
- [ ] No formatting changes are introduced in unmodified sections.

---

## 11. PR Handoff Process

Once the feature has been implemented, validated, and reviewed locally on `feat/neurology-service-line`, the PR Handoff process must be executed:

1. **Commit changes:**
   - Use descriptive commit messages following the project format, e.g.:
     ```bash
     git commit -am "feat(neuro): implement Neurology & Stroke Center service line and boarding mechanics"
     ```
2. **Push the branch:**
   ```bash
   git push -u origin feat/neurology-service-line
   ```
3. **Open the PR:**
   - Use the GitHub CLI to open a pull request against `main`:
     ```bash
     gh pr create --title "feat: implement Neurology & Stroke Center service line" --body "Implements Neurology & Stroke Center service line with capacity-staffing trade-offs, hierarchical prioritization, ED boarding/diversion, and REPL CLI dashboards."
     ```
4. **Three-Pass Code Review Loop:**
   - Trigger 3 independent passes of the `code-reviewer` agent on the PR diff (`git diff main...HEAD`).
   - deduplicate and triage findings by severity. Fix all `Critical` and `High` findings.
   - Reply to the review feedback threads and finalize the PR for merging.

---

## 12. Risk Label

**Risk:** Medium  
*Reason:* Touches system state serialization, AI decision weights, parser inputs, and regression state hashes. Requires careful isolation to prevent regression in older test profiles.
