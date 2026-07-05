# Evidence Map - ICU Service Line & ED Boarding Mechanics

## Assumptions
1.  **ICU Staffing Intensity:** Intensive Care Units (ICUs) are the most resource-intensive units in a hospital. Unlike Med-Surg beds (1 Nurse to 5 beds) or ED bays (1 Nurse to 2 bays), ICU beds require a 1-to-1 nurse-to-patient ratio for critical patients (consistent with California mandates and high-acuity recommendations). 
2.  **Physician Coverage:** ICUs require constant intensivist availability. We model this as 1 Physician per 2 ICU beds (compared to 1 Physician per 10 Outpatient units and 1 per 4 ED bays).
3.  **Admin Staffing:** To reflect the operational complexity of critical care management, we model 1 Admin per 5 ICU beds (compared to 1 Admin per 10 ED bays and 1 Admin per 20 total beds + clinics).
4.  **ED Boarding:** Critical care boarding in the Emergency Department (ED) occurs when patients requiring ICU admission are held in the ED because no ICU beds are available. This is a primary driver of ED overcrowding, patient safety issues, and operational inefficiency.
    *   We assume a baseline critical care admission rate of 5% of the system's total staffed med-surg beds (`(staffed_beds + 19) / 20` using ceiling division).
    *   Boarded patients consume ED bays on a 1-to-1 basis, reducing the effective ED capacity.

## Precedents
- Med-Surg beds: 1 Nurse per 5 beds.
- Outpatient capacity: 1 Physician per 10 capacity.
- ED bays: 1 Nurse per 2 bays, 1 Physician per 4 bays, 1 Admin per 10 bays.
- ICU beds: 1 Nurse per 1 bed, 1 Physician per 2 beds, 1 Admin per 5 beds.
- ED boarding is modeled as a direct deduction from ED capacity, reflecting how physical boarding blocks new ED patient flow.

## Evidence Quality
- **High:** ICU nurse-to-patient ratios are strictly regulated in several jurisdictions (e.g. 1:1 or 1:2 in California). ED boarding is widely documented in health services research as a major threat to patient safety and access.
- **Medium:** The specific 5% admission rate and 1:2 physician/1:5 admin targets are stylized abstractions designed to create balanced gameplay tension.

## Uncertainty
- The simplified 5% critical admission rate does not fluctuate stochastically (following the project's deterministic transition design) but remains a reliable, transparent operational metric.
