# Mechanism Design - Clinical Service Lines and Staffing (Phase 6 - Track 5)

## State Boundary
Extend `HealthSystemState` in `src/model/competitive_world.rs` with:
- `outpatient_capacity: i32` (physical outpatient clinic units, initial: e.g. 100 for Riverside, 150 Northlake, 120 Summit).
- `nurses: i32` (active nurse headcount, initial: staffed beds / 5 med-surg ratio equivalent).
- `physicians: i32` (active physician headcount, initial: outpatient capacity / 10 equivalent).

## Action Vocabulary
- `Invest domain=beds amount=X`: Increases physical `staffed_beds` by `X / 5`.
- `Invest domain=outpatient amount=X`: Increases physical `outpatient_capacity` by `X / 10`.
- `Recruit role=nurse headcount=X`: Enqueues pending effect to add `X` to `nurses` (delay: 1 month).
- `Recruit role=physician headcount=X`: Enqueues pending effect to add `X` to `physicians` (delay: 3 months).
- `Project kind=tower budget=X`: Enqueues tower project which adds 20 to physical `staffed_beds` on completion.
- `Project kind=clinic_network budget=X`: Enqueues clinic network project which adds 30 to physical `outpatient_capacity` on completion.

## Causal Effects (Turn Resolution)
During turn resolution:
1. **Apply Pending Effects:** Due recruit/project/invest effects resolve and increase physical capacities or headcounts.
2. **Compute Staffing Ratios:**
   - Inpatient staffing surplus/deficit: `inpatient_deficit = max(0, (staffed_beds + 4) / 5 - nurses)`. (Using integer division ceil: `(beds + 4) / 5`).
   - Outpatient staffing surplus/deficit: `outpatient_deficit = max(0, (outpatient_capacity + 9) / 10 - physicians)`.
3. **Apply Burnout Penalties:**
   - Subtract `inpatient_deficit` and `outpatient_deficit` from `workforce_trust`.
4. **Compute Effective Capacities:**
   - `effective_beds = min(staffed_beds, nurses * 5)`.
   - `effective_outpatient = min(outpatient_capacity, physicians * 10)`.
5. **Adjust Access & Quality:**
   - Calculate capacity utility ratio: `utility_ratio = (effective_beds + effective_outpatient) as f32 / (staffed_beds + outpatient_capacity) as f32`.
   - Scale down access and quality by this ratio:
     - `system.access_index = clamp_metric((system.access_index as f32 * utility_ratio) as i32)`.
     - `system.quality_index = clamp_metric((system.quality_index as f32 * utility_ratio) as i32)`.

## Observation Model
Modify `PlayerObservation` and the executive report renderer:
- Display current physical and effective/staffed beds: `Beds: X (staffed: Y)`.
- Display current physical and effective/staffed clinics: `Clinics: X (staffed: Y)`.
- Display current nurse and physician headcounts.
