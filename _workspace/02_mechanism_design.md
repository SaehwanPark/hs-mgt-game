# Mechanism Design - Ambulatory Surgery Center (ASC) Service Line

## Goal and Roadmap Phase
Phase 6.1: Simulation Breadth (Track 5) - Ambulatory Surgery Center (ASC) Service Line.

## Slice Boundary
- **Included:**
  * Outpatient ASC capacity.
  * Specialized staffing targets (nurse, physician, admin) for ASC.
  * Greedy staffing priority hierarchy (ASC 9th).
  * ASC outpatient treatment deferral mechanics and penalties.
  * Command grammar aliases for invest and project actions.
  * AI competitor response and REPL autocomplete/dashboard formatting.
- **Excluded:**
  * Individual surgery type categories (orthopedic, ophthalmic, etc.).
  * Detailed surgical instrument inventory or OR scheduling slots.
  * Patient demographic/cohort level details.

## Actors and Authority
- **Player CEO & Rival CEOs:** Have authority to:
  * Invest immediately in ASC bays (`domain=asc`).
  * Initiate long-term ASC capital projects (`kind=asc_unit`).
  * Recruit staff (nurses, physicians, admins) to support the service line expansions.
- **Clinical Staff (Nurses/Physicians):** Allocated greedily based on the hierarchical priority rule.

## State, Beliefs, and Observations
- **True State additions:**
  * `asc_capacity: i32` (physical outpatient surgical bays, default 0).
  * `PendingEffectKind::AscCapacity { capacity_delta: i32, project_draw: Option<i32> }`
- **Observations:** Exposes:
  * `asc_capacity` physical vs effective.
  * In-flight ASC projects in the detailed project tracking dashboard.
  * Outpatient surgical treatment deferrals in the monthly summary report.

## Commands, Events, and Effects
### Commands
- `invest domain=asc amount=<int>`:
  * Cash Cost: `amount` ($20k per bay).
  * Access: Immediate increase `amount / 20`.
  * Market Share: Immediate increase `amount / 40`.
  * Effect: Enqueues `PendingEffectKind::AscCapacity { capacity_delta: amount / 20, project_draw: None }` for next month.
- `project kind=asc_unit budget=24`:
  * AP Cost: 2, cash draw: $4k/month for 6 months.
  * Completion: Enqueues `PendingEffectKind::AscCapacity { capacity_delta: 6, project_draw: Some(4) }` after 6 months.

### Events
- **RNA Strike:** Suspends active ASC capital projects, and halves effective capacity due to temporary staffing shortages.

### Effects
- **ASC Treatment Deferral:**
  * Demand = `(system.asc_capacity + 7) / 8` (12.5% of ASC capacity, ceiling division).
  * Unserved = `(demand - effective_asc).max(0)`.
  * Penalty: Outpatients cannot board in the ED; they are deferred. Triggers `-1` community trust and `-1` market share index penalties per deferred patient.

## Strategic Interaction
- Rival AI players will evaluate candidate commands for ASC projects. If a rival sees the player expanding ASC, it may initiate a counter-expansion to protect its market share.

## Assumptions and Parameters
- **Staffing Targets:**
  * ASC (Outpatient Surgery): Nurse:bay = 1:2, Physician:bay = 1:4, Admin:bay = 1:12.
- **Hierarchical Priority Allocation:**
  * ICU (1st) -> Obstetrics (2nd) -> Med-Surg (3rd) -> Cardiology (4th) -> Psychiatric (5th) -> Neurology (6th) -> Oncology (7th) -> Infusion (8th) -> ASC (9th) -> Outpatient Clinics (10th) -> ED (11th).

## Educational Debrief Hooks
- Appends decision quality warnings if:
  * ASC treatment deferrals occur: `"Ambulatory surgery center procedures were deferred due to capacity/staffing constraints, causing patient leakage."`

## Determinism and Replay Notes
- Transitions are fully deterministic. All random inputs are pre-calculated at the turn-start boundary. State hash incorporates `asc_capacity` to prevent drift.

## Open Questions
- None.
