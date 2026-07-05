# Evidence Map - Psychiatric Service Line & Behavioral Health crisis holding mechanics

## Assumptions
1.  **Psychiatric Staffing Intensity:** Psychiatric (Behavioral Health) inpatient units require specialized psychiatric nursing and psychiatric medical staff. Since psychiatric patients are generally lower physical-acuity but higher monitoring-intensity, we model psychiatric staffing targets as:
    *   Nurses: 1 Nurse per 4 psychiatric beds (target: `(system.psychiatric_capacity + 3) / 4`).
    *   Physicians: 1 Psychiatrist per 10 psychiatric beds (target: `(system.psychiatric_capacity + 9) / 10`).
    *   Admins: 1 Admin per 15 psychiatric beds (target: `(system.psychiatric_capacity + 14) / 15`).
2.  **Psychiatric ED Boarding (Crisis holding):** Psychiatric boarding in emergency departments is a major systemic crisis in the US health system. When psychiatric beds are full or understaffed, patients in psychiatric crisis are held in ED bays, consuming emergency capacity and staff time.
    *   We model psychiatric admission demand as 10% of the physical psychiatric capacity (`(system.psychiatric_capacity + 9) / 10` using ceiling division).
    *   Any deficit between psychiatric demand and effective psychiatric capacity (`psychiatric_demand - effective_psychiatric`) represents psychiatric patients who must board in the ED, directly consuming ED bays on a 1-to-1 basis.
3.  **Psychiatric Diversion:** If the ED capacity is also exhausted, psychiatric patients who cannot board must be diverted/turned away.
    *   Diverting a psychiatric patient causes a loss of community trust (`-1` trust per diverted patient) and a decrease in the quality index (`-1` quality index per diverted patient due to unsafe care transitions).

## Precedents
- Med-Surg beds: 1 Nurse per 5 beds, 1 Physician per 20 beds, 1 Admin per 20 beds.
- ICU beds: 1 Nurse per 1 bed, 1 Physician per 2 beds, 1 Admin per 5 beds.
- ED bays: 1 Nurse per 2 bays, 1 Physician per 4 bays, 1 Admin per 10 bays.
- Obstetrics beds: 1 Nurse per 2 beds, 1 Physician per 5 beds, 1 Admin per 10 beds.
- Psychiatric beds: 1 Nurse per 4 beds, 1 Physician per 10 beds, 1 Admin per 15 beds.
- ED boarding is used both for ICU overflow and Psychiatric overflow, making the Emergency Department the ultimate buffer and bottleneck of the hospital.

## Evidence Quality
- **High:** Psychiatric boarding in EDs is heavily documented in health policy literature (e.g., American College of Emergency Physicians clinical reports). Time-to-placement in psychiatric units is a major operational metric. Nurse-to-patient ratios of 1:4 to 1:6 are common in psychiatric inpatient wards.
- **Medium:** The specific 10% monthly demand rate, `-1` community trust penalty, and `-1` quality index penalty are stylized balancing parameters designed to create clear strategic tradeoffs.

## Uncertainty
- Psychiatric patient flow is simplified as deterministic relative to physical capacity to maintain exact reproducible simulation runs without introducing run-to-run stochasticity.
