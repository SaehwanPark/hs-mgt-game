# Domain QA - Oncology Service Line & Infusion Center Mechanics

- **Status:** Complete
- **Role:** Domain QA Reviewer

## Checklist & Review Criteria

- [x] **State/Observation Separation:** Player only observes the Oncology and Infusion capacities, effective capacity, and boarding/deferral counts through formatted REPL reports, while the underlying true state is updated deterministically in the transition kernel.
- [x] **Deterministic Replay Boundary:** All Oncology/Infusion capacity increases are enqueued in `effect_queue` and resolved during transition. The state hash record has been updated to `v6` to include `onco` and `infuse` fields to guarantee deterministic replay validation.
- [x] **Educational & Operational Balance:** Staffing targets reflect specialty clinical guidelines:
  - Inpatient Oncology: Nurse:bed = 1:3, Physician:bed = 1:8, Admin:bed = 1:12.
  - Outpatient Infusion: Nurse:bay = 1:4, Physician:bay = 1:15, Admin:bay = 1:20.
  The hierarchical allocation model prioritizes Oncology (6th) and Infusion (7th) before ED (8th) for nurses, and Oncology (5th) and Infusion (6th) before Outpatient Clinics (7th) and ED (8th) for physicians.
- [x] **Oncology ED Boarding & Diversion:** Oncology inpatient overflow boards in the Emergency Department (ED), reducing effective emergency capacity on a 1-to-1 basis. If ED capacity is also exhausted, they are diverted, incurring community trust (-2) and quality index (-2) penalties.
- [x] **Infusion Deferrals:** Unserved outpatient infusion volume is deferred, suffering community trust (-1) and market share (-1) penalties.
- [x] **Backward Compatibility:** Default capacities default to `0` in `HealthSystemState` deserialization, avoiding turn-1 staffing deficits and serialization panics.

## Findings & Risk Mitigation
- **Golden Hash Integration:** Bushed state hash schema to `v6` and updated expected seed-42 golden hash to `6044273e2c6c1374` to reflect the additional capacities.
- **AI Match Coverage:** AI player target staffing functions and command scoring are extended to support oncology and infusion domains.
- **Strike Suspension:** Oncology and Infusion capital projects are delayed during active nurse strikes, matching general project behavior. Also, effective capacities are halved during active strikes.
