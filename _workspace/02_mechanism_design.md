# Mechanism Design - Oncology Service Line & Infusion Center Mechanics

## Goal and Roadmap Phase
Phase 6.1: Simulation Breadth (Track 5) - Oncology Service Line & Infusion Center Mechanics.

## Slice Boundary
- **Included:**
  * Inpatient Oncology Bed capacity & Outpatient Infusion Center Bay capacity.
  * Specialized staffing targets (nurse, physician, admin) for both services.
  * Greedy staffing priority hierarchy (Oncology 6th, Infusion 7th).
  * Oncology inpatient ED boarding and diversion penalties.
  * Infusion Center outpatient treatment deferral penalties.
  * Command grammar aliases for invest and project actions.
  * AI competitor response and REPL autocomplete/dashboard formatting.
- **Excluded:**
  * Radiation vaults, clinical pharmacy inventory, or 340B drug pricing logic.
  * Patient demographic/cohort level details.

## Actors and Authority
- **Player CEO & Rival CEOs:** Have authority to:
  * Invest immediately in Oncology beds (`domain=oncology`) and Infusion bays (`domain=infusion`).
  * Initiate long-term Oncology inpatient wing (`kind=oncology_unit`) and Outpatient Infusion center (`kind=infusion_center`) capital projects.
  * Recruit staff (nurses, physicians, admins) to support the service line expansions.
- **Clinical Staff (Nurses/Physicians):** Allocated greedily based on the hierarchical priority rule.

## State, Beliefs, and Observations
- **True State additions:**
  * `oncology_capacity: i32` (physical inpatient beds, default 0).
  * `infusion_capacity: i32` (physical outpatient infusion bays, default 0).
  * `PendingEffectKind::OncologyCapacity { capacity_delta: i32, project_draw: Option<i32> }`
  * `PendingEffectKind::InfusionCapacity { capacity_delta: i32, project_draw: Option<i32> }`
- **Observations:** Exposes:
  * `oncology_capacity` and `infusion_capacity` physical vs effective.
  * In-flight oncology/infusion projects in the detailed project tracking dashboard.
  * ED boarding / Outpatient treatment deferrals in the monthly summary report.

## Commands, Events, and Effects
### Commands
- `invest domain=oncology amount=<int>`:
  * Cash Cost: `amount` ($20k per bed).
  * Access: Immediate increase `amount / 20`.
  * Market Share: Immediate increase `amount / 40`.
  * Effect: Enqueues `PendingEffectKind::OncologyCapacity { capacity_delta: amount / 20, project_draw: None }` for next month.
- `invest domain=infusion amount=<int>`:
  * Cash Cost: `amount` ($15k per bay).
  * Access: Immediate increase `amount / 15`.
  * Market Share: Immediate increase `amount / 30`.
  * Effect: Enqueues `PendingEffectKind::InfusionCapacity { capacity_delta: amount / 15, project_draw: None }` for next month.
- `project kind=oncology_unit budget=45`:
  * AP Cost: 3, cash draw: $5k/month for 9 months.
  * Completion: Enqueues `PendingEffectKind::OncologyCapacity { capacity_delta: 6, project_draw: Some(5) }` after 9 months.
- `project kind=infusion_center budget=30`:
  * AP Cost: 2, cash draw: $5k/month for 6 months.
  * Completion: Enqueues `PendingEffectKind::InfusionCapacity { capacity_delta: 8, project_draw: Some(5) }` after 6 months.

### Events
- **RNA Strike:** Suspends active Oncology and Infusion capital projects, and halves effective capacity of both services due to temporary staffing shortages.

### Effects
- **Oncology ED Boarding & Diversion:**
  * Demand = `(system.oncology_capacity + 9) / 10`.
  * Overflow = `(demand - effective_oncology).max(0)`.
  * Boarded = `overflow.min(effective_emergency_capacity)`. Boarded patients consume ED bays and reduce emergency capacity.
  * Diverted = `overflow - boarded`. Diverted oncology patients suffer `-2` community trust and `-2` quality index penalties due to fractured care loops.
- **Infusion Treatment Deferral:**
  * Demand = `(system.infusion_capacity + 4) / 5`.
  * Unserved = `(demand - effective_infusion).max(0)`.
  * Penalty: Outpatients cannot board in the ED; they are deferred. Triggers `-1` community trust and `-1` market share index penalties per deferred patient.

## Strategic Interaction
- Rival AI players will evaluate candidate commands for oncology and infusion projects. If a rival sees the player expanding oncology/infusion, it may initiate a counter-expansion to protect its market share.

## Assumptions and Parameters
- **Staffing Targets:**
  * Oncology (Inpatient): Nurse:bed = 1:3, Physician:bed = 1:8, Admin:bed = 1:12.
  * Infusion (Outpatient): Nurse:bay = 1:4, Physician:bay = 1:15, Admin:bay = 1:20.
- **Hierarchical Priority Allocation:**
  * ICU (1st) -> Obstetrics (2nd) -> Med-Surg (3rd) -> Cardiology (4th) -> Psychiatric (5th) -> Oncology (6th) -> Infusion (7th) -> Outpatient Clinics (8th) -> ED (9th).

## Educational Debrief Hooks
- Appends decision quality warnings if:
  * Oncology inpatient diversion occurs: `"Oncology inpatient care was diverted due to capacity/staffing constraints, disrupting cancer treatments."`
  * Infusion treatment deferrals occur: `"Chemotherapy infusion appointments were deferred, compromising outpatient oncology quality."`

## Determinism and Replay Notes
- Transitions are fully deterministic. All random inputs are pre-calculated at the turn-start boundary, ensuring identical commands under a identical seed yield identical outcomes. State hash incorporates `oncology_capacity` and `infusion_capacity` to prevent drift.

## Open Questions
- None.
