# Evidence Map - Emergency Department Service Line

## Assumptions
- **ED Staffing Intensity:** Emergency Departments operate 24/7 and have much higher staffing intensity compared to inpatient med-surg units and outpatient clinics. Standard literature indicates ED nurse-to-patient ratios are typically 1:2 to 1:3 for acute patients, and physician coverage is constant.
- **Resource Constraints:** In our strategy game model, this translates to:
  - 1 Nurse per 2 ED capacity units (compared to 1 Nurse per 5 Med-Surg beds).
  - 1 Physician per 4 ED capacity units (compared to 1 Physician per 10 Outpatient units).
  - 1 Admin per 10 ED capacity units (compared to 1 Admin per 20 total beds + outpatient capacity).
- **Service Integration:** ED serves as the entry point for the hospital, making it highly visible and critical for public access and overall quality index metrics. Understaffing or overcrowding (deficit in effective ED capacity) directly penalizes both access and quality indices.

## Precedents
- Med-Surg beds: 1 Nurse per 5 beds.
- Outpatient capacity: 1 Physician per 10 capacity.
- Admins: 1 Admin per 20 total capacity.
- Nurse strike effects: emergency travel nurse costs ($30k/mo) and half capacity.
- Medicaid negotiation: neutral posture only.

## Evidence Quality
- **High:** Staffing shortages are the primary driver of ED diversion, boarding, and patient dissatisfaction.
- **Medium:** The specific numerical targets (1:2 nurse, 1:4 physician) are stylized abstractions to ensure gameplay balance and decision-making tension rather than exact empirical translations.

## Uncertainty
- The impact of ED capacity on commercial payer negotiations is modeled as indirect via quality index updates, rather than as a separate negotiating track, keeping the payer ontology compact.
