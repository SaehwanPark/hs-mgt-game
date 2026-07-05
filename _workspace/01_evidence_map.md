# Evidence Map - Oncology Service Line & Infusion Center Mechanics

## Scope
Implement an inpatient Oncology Service Line and an outpatient Infusion Center Service Line with specialized staffing targets, hierarchical nurse/physician allocation, inpatient ED boarding, and outpatient deferral mechanics.

## Sources Reviewed
- **ONS Guidelines:** Oncology Nursing Society (ONS) outpatient chemotherapy administration recommendations suggest 1 nurse per 3-4 patients depending on drug complexity.
- **Inpatient Staffing Models:** Literature on acute oncology wards indicates standard staffing ratios around 1 nurse per 3 beds due to high care complexity (neutropenic precautions, chemotherapy monitoring, pain control).
- **ED Boarding and Care Delays:** American Society of Clinical Oncology (ASCO) reports emphasize that delays in oncology care (both inpatient admission delays and outpatient chemotherapy deferrals) directly degrade clinical quality, patient safety, and market reputation.

## Mechanisms and Institutions
- **Inpatient Oncology beds:** Physical beds reserved for acute cancer care. Constrained by staffing targets. Overflow boards in the Emergency Department (ED), reducing effective ED capacity.
- **Outpatient Infusion bays:** Physical chairs/bays for outpatient chemotherapy and immunotherapy. Constrained by staffing targets. Saturated capacity results in appointment deferral rather than ED boarding.
- **Hierarchical Allocation:** High-acuity specialties (ICU, Obstetrics, Cardiology) and moderate-acuity specialties (Psychiatric, Oncology) pull clinical staff from general outpatient clinics and emergency departments.

## Actor Incentives and Information
- **Health Systems:** Oncology is traditionally a high-revenue service line that drives system profitability, but requires significant capital and specialized staff. Staffing shortage or bed shortages result in operational friction (boarding/deferral).
- **Patients:** Expect timely and safe cancer care cycles. Diversion or deferral directly reduces patient trust and system quality metrics.
- **Rivals:** Compete for profitable oncology market share. Saturated infusion centers cause patients to seek oncology care at rival systems.

## Assumptions
1.  **Oncology Staffing Targets:**
    *   Nurses: 1 Nurse per 3 beds (target: `(system.oncology_capacity + 2) / 3`).
    *   Physicians: 1 Oncologist per 8 beds (target: `(system.oncology_capacity + 7) / 8`).
    *   Admins: 1 Admin per 12 beds (target: `(system.oncology_capacity + 11) / 12`).
2.  **Infusion Staffing Targets:**
    *   Nurses: 1 Nurse per 4 bays (target: `(system.infusion_capacity + 3) / 4`).
    *   Physicians: 1 Oncologist per 15 bays (target: `(system.infusion_capacity + 14) / 15`).
    *   Admins: 1 Admin per 20 bays (target: `(system.infusion_capacity + 19) / 20`).
3.  **Oncology Inpatient Demand & Boarding:**
    *   Oncology inpatient demand: 10% of physical oncology capacity (`(system.oncology_capacity + 9) / 10`, ceiling division).
    *   Inpatient oncology overflow boards in the ED on a 1-to-1 basis.
    *   Diverted inpatient oncology patients (when ED capacity is also exhausted) trigger `-2` community trust and `-2` quality index penalties per patient.
4.  **Infusion Center Demand & Deferral:**
    *   Infusion demand: 20% of physical infusion capacity (`(system.infusion_capacity + 4) / 5`, ceiling division).
    *   Infusion overflow cannot board in the ED (outpatient service). Saturated infusion capacity leads to treatment deferrals, triggering `-1` community trust and `-1` market share index penalties per deferred patient.

## Unresolved Questions
- **340B Drug Discount Program:** Outpatient drug margins are a massive driver of US hospital finance, but modeling drug acquisition and billing rules is deferred as a non-goal for simplicity.
- **Radiotherapy and Surgical Oncology:** Specific radiation oncology vaults or surgical suites are simplified into a single outpatient Infusion Center concept and inpatient Oncology bed capacity.

## Design Implications
- physical capacity and staffing constraints must be calculated dynamically for both Oncology (inpatient) and Infusion (outpatient).
- Nurse and physician greedy allocation must prioritze Oncology (sixth) and Infusion (seventh) after Psychiatric (fifth) and before Outpatient Clinics (eighth) and ED (ninth).
- Inpatient overflow boards in the ED, directly reducing effective ED capacity alongside ICU and Psychiatric overflow.
- Outpatient overflow is deferred, directly reducing market share and community trust without consuming ED bays.

## Risks
- **Greedy Allocation Starvation:** Placing Oncology and Infusion above general outpatient clinics and ED means severe nursing shortages will starve general clinics and the ED first. This is a realistic trade-off but must be validated in simulation tests.
- **State Hash Collision:** Adding oncology capacity and infusion capacity to the state hash must be done carefully to maintain deterministic validation.
