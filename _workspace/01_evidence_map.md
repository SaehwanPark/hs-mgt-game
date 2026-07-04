# Evidence Map - Clinical Service Lines and Staffing (Phase 6 - Track 5)

## Assumptions
- Nonprofit health systems manage two distinct clinical flows: acute inpatient care and preventive/primary outpatient care.
- Beds require nurses to operate. Physical bed expansion without nurse recruitment leads to unstaffed beds and staff burnout.
- Outpatient clinics require physicians to handle patient visits. Capacity expansion without physician recruitment leads to reduced outpatient throughput and patient access friction.
- Workforce trust (morale) is highly sensitive to nurse workload and staffing deficits.

## Precedents
- **California AB 394 (Safe Staffing):** Mandates specific nurse-to-patient staffing ratios (e.g. 1 nurse to 5 patients in med-surg).
- **Aiken JAMA 2002 (Nurse Burnout):** Literature links lower nurse-to-patient staffing ratios directly to increased nurse burnout, intention to leave, and elevated 30-day mortality.
- **Primary Care Access (HRSA):** Shortages of physicians limit outpatient clinic operational capacity, directly correlating with lower regional access metrics.

## Calibration / Abstractions
- **Staffed Beds / Inpatient Ratio:** We calibrate the med-surg equivalent at 5 inpatient beds per 1 nurse.
- **Outpatient Capacity / Clinic Ratio:** We calibrate outpatient capacity at 10 clinic units per 1 physician.
- **Effective Capacity:** If staffing is deficient, effective capacity is capped at `headcount * ratio`.
- **Understaffing Penalty:** Staffing deficits subtract directly from `workforce_trust` (-1 per understaffed bed/clinic unit) and reduce `access_index` and `quality_index` proportionally to the unstaffed capacity.
