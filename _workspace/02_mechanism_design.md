# Mechanism Design - Obstetrics Service Line & L&D Diversion Mechanics

## Actor Set
- **Health Systems (Riverside, Northlake, Summit):** Can expand obstetric capacity via direct investment or by launching an `ObstetricsUnit` project.
- **Workforce (Nurses, Physicians, Admins):** Allocated hierarchically to satisfy ICU and Obstetrics needs before other clinical units.
- **Patients (Obstetric Flow):** Demand for obstetric services triggers bypass/diversion if effective capacity is less than the monthly demand.

## Action Vocabulary
1.  `invest domain=obstetrics amount=<int>` (alias `obs`): Immediate capital investment in obstetric beds.
    *   **Cash cost:** `amount` (each Obstetrics bed costs 25 units of cash).
    *   **Access/market share increments:** `access_delta = amount / 25`, `market_share = amount / 50` immediately.
    *   **Delay:** 1 month (capacity delta resolves next month).
2.  `project kind=obstetrics_unit budget=<int>` (alias `obs_unit`): Launches a Labor & Delivery Unit expansion.
    *   **Duration:** 9 months.
    *   **AP Cost:** 2.
    *   **Cash draw:** `budget / 9` per month.
    *   **Yields:** +6 Obstetrics capacity upon completion.

## State Boundary
- `HealthSystemState` adds `obstetrics_capacity: i32`.
- `PendingEffectKind` adds `ObstetricsCapacity { capacity_delta: i32, project_draw: Option<i32> }`.
- `PlayerObservation` and `AiPlayerObservation` add `obstetrics_capacity: i32`.

## Observation Model
- **REPL executive report dashboard:**
  ```text
    • Obstetrics capacity: <obstetrics_capacity> beds (effective: <effective_obs>)
    • Obstetric diversion: <diverted_patients> patients
  ```
  *(Obstetric diversion line is visible only when diverted_patients > 0)*
- **In-flight projects:**
  `ObstetricsUnit (<N> mos left, $<D>k/mo draw)`

## Causal Effects

### 1. Obstetrics Staffing Targets
The system-wide staffing targets are updated to:
*   `target_nurses = (system.staffed_beds + 4) / 5 + (system.emergency_capacity + 1) / 2 + system.icu_capacity + (system.obstetrics_capacity + 1) / 2;`
*   `target_physicians = (system.outpatient_capacity + 9) / 10 + (system.emergency_capacity + 3) / 4 + (system.icu_capacity + 1) / 2 + (system.obstetrics_capacity + 4) / 5;`
*   `target_admins = (system.staffed_beds + system.outpatient_capacity + 19) / 20 + (system.emergency_capacity + 9) / 10 + (system.icu_capacity + 4) / 5 + (system.obstetrics_capacity + 9) / 10;`

### 2. Hierarchical Allocation Order (ICU -> Obstetrics -> Beds -> Clinics -> ED)
*   **Nurses:**
    1.  ICU first: `nurses_icu = system.nurses.min(system.icu_capacity)`
    2.  Obstetrics second: `nurses_obs = (system.nurses - nurses_icu).max(0).min((system.obstetrics_capacity + 1) / 2)`
    3.  Med-Surg Beds third: `nurses_beds = (system.nurses - nurses_icu - nurses_obs).max(0).min((system.staffed_beds + 4) / 5)`
    4.  Emergency Department fourth: `nurses_ed = (system.nurses - nurses_icu - nurses_obs - nurses_beds).max(0).min((system.emergency_capacity + 1) / 2)`
*   **Physicians:**
    1.  ICU first: `physicians_icu = system.physicians.min((system.icu_capacity + 1) / 2)`
    2.  Obstetrics second: `physicians_obs = (system.physicians - physicians_icu).max(0).min((system.obstetrics_capacity + 4) / 5)`
    3.  Outpatient Clinics third: `physicians_outpatient = (system.physicians - physicians_icu - physicians_obs).max(0).min((system.outpatient_capacity + 9) / 10)`
    4.  Emergency Department fourth: `physicians_ed = (system.physicians - physicians_icu - physicians_obs - physicians_outpatient).max(0).min((system.emergency_capacity + 3) / 4)`

### 3. Effective Capacities
*   `effective_icu = system.icu_capacity.min(nurses_icu * 1).min(physicians_icu * 2)`
*   `effective_obs = system.obstetrics_capacity.min(nurses_obs * 2).min(physicians_obs * 5)`
*   `effective_beds = system.staffed_beds.min(nurses_beds * 5)`
*   `effective_outpatient = system.outpatient_capacity.min(physicians_outpatient * 10)`
*   `effective_emergency = system.emergency_capacity.min(nurses_ed * 2).min(physicians_ed * 4)`

*Note: During a nurse strike, effective_obs is halved, just like other capacity services.*

### 4. Obstetric Diversion Calculation
*   Obstetric admission demand: `obstetric_demand = (system.obstetrics_capacity + 9) / 10` (10% of obstetric capacity, ceiling division).
*   Diverted patients: `diverted_patients = (obstetric_demand - effective_obs).max(0)`
*   Trust & Market Share penalties:
    *   `system.community_trust = (system.community_trust - diverted_patients * 2).max(0)`
    *   `system.market_share_index = (system.market_share_index - diverted_patients * 1).max(0)`

### 5. Quality & Access Penalties
Staffing/capacity deficit penalties apply over all physical capacity:
*   `total_physical = staffed_beds + outpatient_capacity + emergency_capacity + icu_capacity + obstetrics_capacity`
*   `total_effective = effective_beds + effective_outpatient + effective_emergency + effective_icu + effective_obs`
*   `penalty = ((1.0 - total_effective / total_physical) * 15.0).round()`
*   Penalty is subtracted from `access_index` and `quality_index`.
