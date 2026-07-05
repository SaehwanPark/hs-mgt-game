# Mechanism Design - ICU Service Line & ED Boarding Mechanics

## Actor Set
- **Health Systems (Riverside, Northlake, Summit):** Can expand ICU capacity via direct investment or by launching an `IcuWing` project.
- **Workforce (Nurses, Physicians, Admins):** Allocated hierarchically to satisfy critical-care needs before other units.
- **Patients (Inpatient Flow):** A portion of med-surg inpatients require ICU admission, triggering boarding if capacity is insufficient.

## Action Vocabulary
1.  `invest domain=icu amount=<int>`: Immediate capital investment in ICU beds.
    *   **Cash cost:** `amount` (each ICU bed costs 30 units of cash).
    *   **Access/market share increments:** `access_delta = amount / 30`, `market_share = amount / 60` immediately.
    *   **Delay:** 1 month (capacity delta resolves next month).
2.  `project kind=icu_wing budget=<int>`: Launches a major ICU Wing project.
    *   **Duration:** 12 months.
    *   **AP Cost:** 3.
    *   **Cash draw:** `budget / 12` per month.
    *   **Yields:** +10 ICU capacity upon completion.

## State Boundary
- `HealthSystemState` adds `icu_capacity: i32`.
- `PendingEffectKind` adds `IcuCapacity { capacity_delta: i32, project_draw: Option<i32> }`.
- `PlayerObservation` and `AiPlayerObservation` add `icu_capacity: i32`.

## Observation Model
- **REPL executive report dashboard:**
  ```text
    • ICU capacity: <icu_capacity> beds (effective: <effective_icu>)
    • ED boarding: <boarded_patients> patients
  ```
  *(ED boarding line is visible only when boarded_patients > 0)*
- **In-flight projects:**
  `IcuWing (<N> mos left, $<D>k/mo draw)`

## Causal Effects

### 1. ICU Staffing Targets
The system-wide staffing targets are updated to:
*   `target_nurses = (system.staffed_beds + 4) / 5 + (system.emergency_capacity + 1) / 2 + system.icu_capacity;`
*   `target_physicians = (system.outpatient_capacity + 9) / 10 + (system.emergency_capacity + 3) / 4 + (system.icu_capacity + 1) / 2;`
*   `target_admins = (system.staffed_beds + system.outpatient_capacity + 19) / 20 + (system.emergency_capacity + 9) / 10 + (system.icu_capacity + 4) / 5;`

### 2. Hierarchical Allocation Order (ICU -> Beds -> Clinics -> ED)
*   **Nurses:**
    1.  ICU first: `nurses_icu = system.nurses.min(system.icu_capacity)`
    2.  Med-Surg Beds second: `nurses_beds = (system.nurses - nurses_icu).max(0).min((system.staffed_beds + 4) / 5)`
    3.  Emergency Department third: `nurses_ed = (system.nurses - nurses_icu - nurses_beds).max(0).min((system.emergency_capacity + 1) / 2)`
*   **Physicians:**
    1.  ICU first: `physicians_icu = system.physicians.min((system.icu_capacity + 1) / 2)`
    2.  Outpatient Clinics second: `physicians_outpatient = (system.physicians - physicians_icu).max(0).min((system.outpatient_capacity + 9) / 10)`
    3.  Emergency Department third: `physicians_ed = (system.physicians - physicians_icu - physicians_outpatient).max(0).min((system.emergency_capacity + 3) / 4)`

### 3. Effective Capacities
*   `effective_icu = system.icu_capacity.min(nurses_icu * 1).min(physicians_icu * 2)`
*   `effective_beds = system.staffed_beds.min(nurses_beds * 5)`
*   `effective_outpatient = system.outpatient_capacity.min(physicians_outpatient * 10)`
*   `effective_emergency = system.emergency_capacity.min(nurses_ed * 2).min(physicians_ed * 4)`

### 4. ED Boarding Calculation
*   Critical admissions demand: `critical_admissions = (system.staffed_beds + 19) / 20` (5% of med-surg beds, ceiling division).
*   Boarded patients: `boarded_patients = (critical_admissions - effective_icu).max(0)`
*   ED capacity adjustment: `effective_emergency = (effective_emergency - boarded_patients).max(0)`

### 5. Quality & Access Penalties
Staffing/capacity deficit penalties apply over all physical capacity:
*   `total_physical = staffed_beds + outpatient_capacity + emergency_capacity + icu_capacity`
*   `total_effective = effective_beds + effective_outpatient + effective_emergency + effective_icu`
*   `penalty = ((1.0 - total_effective / total_physical) * 15.0).round()`
*   Penalty is subtracted from `access_index` and `quality_index`.
