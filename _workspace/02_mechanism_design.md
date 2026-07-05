# Mechanism Design - Emergency Department Service Line

## Actor Set
- **Health Systems (Riverside, Northlake, Summit):** Can now expand ED capacity via quiet investments or a major capital project.
- **Workforce (Nurses, Physicians, Admins):** Must be recruited and balanced to meet the new ED staffing targets. Deficits cause burnout (trust drops) and reduce effective ED capacity.

## Action Vocabulary
- `invest domain=emergency amount=<int>`: Increases emergency capacity.
  - Cash cost: `amount` (each unit of ED capacity requires 15 units of cash).
  - Access/market share increments: `access_delta = amount / 15`, `market_share = amount / 30` immediately.
  - Delay: 1 month (capacity delta resolves next month).
- `project kind=emergency_pavilion budget=<int>`: Builds a major ED project.
  - Duration: 6 months.
  - Cash draw: `budget / 6` per month.
  - Yields +15 emergency capacity upon completion.

## State Boundary
- `HealthSystemState` adds field `emergency_capacity: i32`.
- `PlayerObservation` and `AiPlayerObservation` add field `emergency_capacity: i32`.
- `PendingEffectKind` adds `EmergencyCapacity { capacity_delta: i32, project_draw: Option<i32> }`.

## Observation Model
- REPL executive dashboard displays:
  `  • Emergency capacity: <capacity> bays (effective: <effective>)`
- In-flight projects display:
  `EmergencyPavilion (<N> mos left, $<D>k/mo draw)`

## Causal Effects
- **ED Staffing Target Formulas:**
  - `target_nurses_ed = (emergency_capacity + 1) / 2`
  - `target_physicians_ed = (emergency_capacity + 3) / 4`
  - `target_admins_ed = (emergency_capacity + 9) / 10`
  - These are added to the existing Bed and Outpatient targets to form overall system targets.
- **Effective ED Capacity:**
  - `effective_emergency = emergency_capacity.min(nurses_for_ed * 2).min(physicians_for_ed * 4)`
  - Where `nurses_for_ed` and `physicians_for_ed` represent the portion of staff allocated to ED after satisfying inpatient beds and outpatient clinics first (hierarchical allocation: beds first, clinics second, ED third).
- **Quality & Access Penalties:**
  - Staffing deficit penalty percentage is calculated over all physical capacity:
    `total_physical = staffed_beds + outpatient_capacity + emergency_capacity`
    `total_effective = effective_beds + effective_outpatient + effective_emergency`
    `penalty = ((1.0 - total_effective / total_physical) * 15.0).round()`
