# Mechanism Design - Psychiatric Service Line & Behavioral Health crisis holding mechanics

## Actor Set
- **Health Systems (Riverside, Northlake, Summit):** Can expand psychiatric capacity via direct investment or by launching a `PsychiatricUnit` project.
- **Workforce (Nurses, Physicians, Admins):** Allocated hierarchically to satisfy ICU, Obstetrics, and Med-Surg needs before Psychiatric, Outpatient, and Emergency units.
- **Patients (Psychiatric Flow):** Demand for psychiatric services triggers emergency department boarding or diversion if psychiatric beds are full/understaffed.

## Action Vocabulary
1.  `invest domain=psychiatric amount=<int>` (alias `psych`): Immediate capital investment in psychiatric beds.
    *   **Cash cost:** `amount` (each Psychiatric bed costs 20 units of cash).
    *   **Access/market share increments:** `access_delta = amount / 20`, `market_share = amount / 40` immediately.
    *   **Delay:** 1 month (capacity delta resolves next month).
2.  `project kind=psychiatric_unit budget=<int>` (alias `psych_unit`): Launches a Psychiatric Unit expansion.
    *   **Duration:** 6 months.
    *   **AP Cost:** 2.
    *   **Cash draw:** `budget / 6` per month.
    *   **Yields:** +5 Psychiatric capacity upon completion.

## State Boundary
- `HealthSystemState` adds `psychiatric_capacity: i32`.
- `PendingEffectKind` adds `PsychiatricCapacity { capacity_delta: i32, project_draw: Option<i32> }`.
- `PlayerObservation` and `AiPlayerObservation` add `psychiatric_capacity: i32`.

## Observation Model
- **REPL executive report dashboard:**
  ```text
    • Psychiatric capacity: <psychiatric_capacity> beds (effective: <effective_psych>)
    • Psychiatric ED boarding: <boarded_psych> patients
  ```
  *(Psychiatric ED boarding line is visible only when boarded_psych > 0)*
- **In-flight projects:**
  `PsychiatricUnit (<N> mos left, $<D>k/mo draw)`

## Causal Effects

### 1. Psychiatric Staffing Targets
The system-wide staffing targets are updated to:
*   `target_nurses = (system.staffed_beds + 4) / 5 + (system.emergency_capacity + 1) / 2 + system.icu_capacity + (system.obstetrics_capacity + 1) / 2 + (system.psychiatric_capacity + 3) / 4;`
*   `target_physicians = (system.outpatient_capacity + 9) / 10 + (system.emergency_capacity + 3) / 4 + (system.icu_capacity + 1) / 2 + (system.obstetrics_capacity + 4) / 5 + (system.psychiatric_capacity + 9) / 10;`
*   `target_admins = (system.staffed_beds + system.outpatient_capacity + 19) / 20 + (system.emergency_capacity + 9) / 10 + (system.icu_capacity + 4) / 5 + (system.obstetrics_capacity + 9) / 10 + (system.psychiatric_capacity + 14) / 15;`

### 2. Hierarchical Allocation Order (ICU -> Obstetrics -> Beds -> Psychiatric -> Clinics -> ED)
*   **Nurses:**
    1.  ICU first: `nurses_icu = system.nurses.min(system.icu_capacity)`
    2.  Obstetrics second: `nurses_obs = (system.nurses - nurses_icu).max(0).min((system.obstetrics_capacity + 1) / 2)`
    3.  Med-Surg Beds third: `nurses_beds = (system.nurses - nurses_icu - nurses_obs).max(0).min((system.staffed_beds + 4) / 5)`
    4.  Psychiatric fourth: `nurses_psych = (system.nurses - nurses_icu - nurses_obs - nurses_beds).max(0).min((system.psychiatric_capacity + 3) / 4)`
    5.  Emergency Department fifth: `nurses_ed = (system.nurses - nurses_icu - nurses_obs - nurses_beds - nurses_psych).max(0).min((system.emergency_capacity + 1) / 2)`
*   **Physicians:**
    1.  ICU first: `physicians_icu = system.physicians.min((system.icu_capacity + 1) / 2)`
    2.  Obstetrics second: `physicians_obs = (system.physicians - physicians_icu).max(0).min((system.obstetrics_capacity + 4) / 5)`
    3.  Psychiatric third: `physicians_psych = (system.physicians - physicians_icu - physicians_obs).max(0).min((system.psychiatric_capacity + 9) / 10)`
    4.  Outpatient Clinics fourth: `physicians_outpatient = (system.physicians - physicians_icu - physicians_obs - physicians_psych).max(0).min((system.outpatient_capacity + 9) / 10)`
    5.  Emergency Department fifth: `physicians_ed = (system.physicians - physicians_icu - physicians_obs - physicians_psych - physicians_outpatient).max(0).min((system.emergency_capacity + 3) / 4)`

### 3. Effective Capacities
*   `effective_icu = system.icu_capacity.min(nurses_icu * 1).min(physicians_icu * 2)`
*   `effective_obs = system.obstetrics_capacity.min(nurses_obs * 2).min(physicians_obs * 5)`
*   `effective_beds = system.staffed_beds.min(nurses_beds * 5)`
*   `effective_psych = system.psychiatric_capacity.min(nurses_psych * 4).min(physicians_psych * 10)`
*   `effective_outpatient = system.outpatient_capacity.min(physicians_outpatient * 10)`
*   `effective_emergency = system.emergency_capacity.min(nurses_ed * 2).min(physicians_ed * 4)`

*Note: During a nurse strike, effective_psych is halved, just like other capacity services.*

### 4. Psychiatric ED Boarding & Diversion Calculation
*   Psychiatric admission demand: `psychiatric_demand = (system.psychiatric_capacity + 9) / 10` (10% of psychiatric capacity, ceiling division).
*   Psychiatric crisis overflow: `psychiatric_overflow = (psychiatric_demand - effective_psych).max(0)`.
*   These overflowed patients board in the ED, directly consuming ED bays:
    *   `boarded_psych = psychiatric_overflow.min(effective_emergency)`
    *   `effective_emergency = (effective_emergency - boarded_psych).max(0)`
*   If psychiatric overflow exceeds available ED bays, the remaining patients are diverted/turned away:
    *   `diverted_psych = (psychiatric_overflow - boarded_psych).max(0)`
    *   `system.community_trust = (system.community_trust - diverted_psych).max(0)`
    *   `system.quality_index = (system.quality_index - diverted_psych).max(0)`

### 5. Quality & Access Penalties
Staffing/capacity deficit penalties apply over all physical capacity:
*   `total_physical = staffed_beds + outpatient_capacity + emergency_capacity + icu_capacity + obstetrics_capacity + psychiatric_capacity`
*   `total_effective = effective_beds + effective_outpatient + effective_emergency + effective_icu + effective_obs + effective_psych`
*   `penalty = ((1.0 - total_effective / total_physical) * 15.0).round()`
*   Penalty is subtracted from `access_index` and `quality_index`.
