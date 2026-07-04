# Evidence Map - Nursing Workforce & Retention Ledger (Phase 1)

## Scope
This evidence map converts literature and data on nursing labor markets, safe staffing ratios, recruitment lags, and strike costs into structured baseline parameters for the game's workforce simulation models.

---

## Sources Reviewed

1. **Aiken, L. H., Clarke, S. P., Sloane, D. M., Sochalski, J., & Silber, J. H. (2002).** *Hospital Nurse Staffing and Patient Mortality, Nurse Burnout, and Job Dissatisfaction*. JAMA, 288(16), 1987-1993.
   - *Key finding:* Each additional patient per nurse increases the odds of nurse burnout by 23% and mortality by 7%. Supports the game's penalty on `workforce_trust` when capacity increases without staff.
2. **California Assembly Bill 394 (AB 394, 1999).**
   - *Key finding:* Mandated shift-by-shift nurse-to-patient staffing ratios. Understaffing below these ratios is treated as an unsafe working condition, triggering grievances or union strikes.
3. **NSI Nursing Solutions, Inc. (2026).** *NSI National Health Care Retention & RN Staffing Report*.
   - *Key finding:* Average time-to-fill for an RN vacancy is 78 days (approx. 2.6 months), with specialized roles taking longer. Focuses on hiring delays.
4. **McHugh, M. D., Kelly, L. A., Smith, H. L., Wu, E. S., Vanak, J. M., & Aiken, L. H. (2011).** *Lower Mortality in Hospitals with Fewer Patients per Nurse*. Health Affairs, 30(5), 903-910.
   - *Key finding:* California safe-staffing mandate improved nurse retention and satisfaction.

---

## Mechanisms and Abstractions

1. **Recruitment Hiring Lag:**
   - *Real-world basis:* 78-day average hiring time.
   - *Abstractions:* 1-month recruitment delay for nurses (stylized 1-turn delay in CLI).
2. **Capacity Staffing Friction:**
   - *Real-world basis:* Staffing beds without nurses reduces quality and increases burnout.
   - *Abstractions:* Bed addition without recruitment reduces `workforce_trust` by `/ 4`.
3. **Union/Labor Action Trigger:**
   - *Real-world basis:* Grievances under poor staffing ratios.
   - *Abstractions:* `prior_workforce_trust < 60` triggers strike threat / work action.
4. **Retention and Schedule Relief Benefit:**
   - *Real-world basis:* Relieving schedule stress increases retention.
   - *Abstractions:* `workforce_trust += schedule_relief / 2`.
