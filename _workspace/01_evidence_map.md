# Evidence Map - Ambulatory Surgery Center (ASC) Service Line

## Scope
Implement an outpatient Ambulatory Surgery Center (ASC) Service Line with capacity-staffing trade-offs, specialized staffing targets, hierarchical nurse/physician allocation, and outpatient surgical deferral mechanics.

## Sources Reviewed
- **AORN Guidelines:** Association of periOperative Registered Nurses (AORN) recommendations suggest specialized staffing for surgical bays (pre-op, intra-op, post-op PACU). Standard nursing ratios range from 1 nurse per 2 bays depending on patient acuity.
- **Outpatient Surgical Trends:** Health-policy literature highlights the shift of low-acuity surgical procedures from inpatient main operating rooms to freestanding ASCs, which lower costs and improve convenience but require highly specialized staff.
- **Surgical Delays & Deferrals:** Delays in scheduled surgeries lead to immediate patient dissatisfaction, loss of physician loyalty, and leakage of market share to competing outpatient facilities.

## Mechanisms and Institutions
- **ASC Bays:** Physical operating/procedure rooms and pre-op/post-op bays. Saturated capacity results in outpatient surgical deferral rather than emergency department (ED) boarding.
- **Hierarchical Allocation:** Specialized surgical care pulls clinical staff from general outpatient clinics and emergency departments.
- **Commercial Payer Sensitivity:** ASC services are highly profitable, particularly for commercial insurers, making them a key strategic lever for health systems.

## Actor Incentives and Information
- **Health Systems:** Freestanding ASCs are high-margin entities that capture low-acuity surgical cases, preserving inpatient main OR capacity for high-acuity trauma or complex surgery.
- **Patients:** Value outpatient surgical access, convenience, and low out-of-pocket costs. Capacity bottlenecks lead to surgery deferrals, which degrade trust and patient experience.
- **Rivals:** Actively expand ASC capacity to capture profitable outpatient surgical market share. Saturated ASC bays lead to patient leakage to rivals.

## Assumptions
1.  **ASC Staffing Targets:**
    *   Nurses: 1 Nurse per 2 bays (target: `(system.asc_capacity + 1) / 2`).
    *   Physicians (Surgeons/Anesthesiologists): 1 Physician per 4 bays (target: `(system.asc_capacity + 3) / 4`).
    *   Admins: 1 Admin per 12 bays (target: `(system.asc_capacity + 11) / 12`).
2.  **ASC Demand & Deferral:**
    *   ASC outpatient demand: 12.5% of physical ASC capacity (`(system.asc_capacity + 7) / 8`, ceiling division).
    *   ASC overflow cannot board in the ED (outpatient service). Saturated ASC capacity leads to treatment deferrals, triggering `-1` community trust and `-1` market share index penalties per deferred patient.

## Unresolved Questions
- **Certificate of Need (CON) laws:** The regulation of ASC facility expansion varies heavily by state. For simplicity, we model ASC unit additions as standard capital projects without complex regulatory approval hurdles.
- **Anesthesia Staffing Models:** We simplify the surgical team (surgeons, anesthesiologists, CRNAs) into a single "physician" target for ASC capacity constraints.

## Design Implications
- Physical capacity and staffing constraints must be calculated dynamically for ASC (outpatient).
- Nurse and physician greedy allocation must prioritize ASC (ninth) after Infusion (eighth) and before Outpatient Clinics (tenth) and ED (eleventh).
- Outpatient overflow is deferred, directly reducing market share and community trust without consuming ED bays.

## Risks
- **Greedy Allocation Starvation:** Placing ASC above general outpatient clinics and ED means severe nursing shortages will starve general clinics and the ED first. This is a realistic strategic trade-off.
- **State Hash Collision:** Adding ASC capacity to the state hash must be done carefully to maintain deterministic validation.
