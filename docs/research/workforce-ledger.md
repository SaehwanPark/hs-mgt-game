# Nursing Workforce & Retention Parameter/Evidence Ledger

This document serves as the official parameter and evidence ledger for the **Nursing Workforce & Retention** mechanism in the Health Policy Strategy Game. It grounds the integer values, thresholds, and transition formulas used in both the stabilization and competitive campaign models in empirical data, health services research, and policy precedents.

## 1. Mechanism Overview

The nursing workforce mechanism simulates the strategic tension between hospital capacity, labor expenditures, and nursing burnout/trust. 
- In the **stabilization campaign**, the player uses `RespondToWorkforcePressure` (specifying `retention_spend` and `schedule_relief_commitment`) to avert nurse work actions.
- In the **competitive campaign**, the player uses `Recruit` commands to hire nurses, which cost cash and AP, and resolve with a monthly delay. Recruiting also decreases workforce trust when capacity resolves.

---

## 2. Parameter and Formula Ledger

The table below maps the workforce-related parameters and formulas from the codebase to their model-confidence labels, specific source literature, and empirical justification.

### Confidence Labels Reference
- **Empirically calibrated**: Bounded by cited data and applied directly to ruleset.
- **Literature-grounded**: Mechanism direction/relationship supported by literature, but numeric ranges are simplified.
- **Expert-informed**: Based on practitioner or reviewer judgment.
- **Stylized abstraction**: Simplified to preserve a credible strategic relationship.
- **Gameplay-driven**: Selected for tension, pacing, or teachability.

### Ledger Mapping

| Parameter / Formula | Code Location | Current Value / Formula | Confidence Label | Source Citation / Precedent | Design Rationale & Grounding |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Nurse Staffing Burnout Trigger** | [labor.rs:L20](../../src/actors/labor.rs#L20) | `prior_workforce_trust < 60` | Literature-grounded | California AB 394 Safe Staffing Law (1999) | Ratios below safe minimums trigger labor tension. 60% represents the threshold below which understaffing forces union actions. |
| **Nurse Recruitment Delay** | [competitive_command.rs:L89](../../src/model/competitive_command.rs#L89) | `RecruitRole::Nurse = 1 month` | Literature-grounded | NSI National Health Care Retention & RN Staffing Report (2026) | National average time-to-fill for an RN vacancy is **78 days** (approx. 2.6 months). In a monthly CLI loop, a 1-month delay is a stylized, conservative representation of this hiring lag. |
| **Nurse Recruitment Cost** | [competitive_command.rs:L125-129](../../src/model/competitive_command.rs#L125-L129) | `$5` per nurse unit (AP cost = 1) | Stylized abstraction | NSI 2026 RN Staffing Report; BLS Occupational Employment Statistics | Represents advertising, onboarding, and training costs, scaled to fit the game's cash units. |
| **Beds Addition Trust Penalty** | [transition.rs:L45](../../src/sim/transition.rs#L45) | `next.workforce_trust -= add_staffed_beds / 4` | Literature-grounded | Aiken et al. (2002) JAMA study on nurse-to-patient ratios | Adding staffed beds without hiring additional nurses increases the patient-to-nurse ratio, which Aiken et al. showed increases the odds of nurse burnout and job dissatisfaction. |
| **Schedule Relief Trust Benefit** | [transition.rs:L90](../../src/sim/transition.rs#L90) | `next.workforce_trust += schedule_relief_commitment / 2` | Stylized abstraction | McHugh et al. (2011) Policy, Politics & Nursing Practice | Offering schedule relief and reducing overtime hours significantly improves retention and trust. Formulated as a linear recovery index. |
| **Labor Credible Offer Threshold** | [labor.rs:L18-19](../../src/actors/labor.rs#L18-L19) | `retention_spend >= ruleset.minimum_retention_spend` (5) and `schedule_relief >= ruleset.minimum_schedule_relief` (3) | Gameplay-driven | Default Demo Ruleset (`v0.1.9`) | Minimum credible thresholds for labor negotiations. Sourced for game pacing and preventing player exploitation of zero-cost inputs. |
| **Recruitment Capacity Trust Drop** | [effects_competitive.rs:L61](../../src/sim/effects_competitive.rs#L61) | `workforce_trust -= headcount` | Stylized abstraction | Selected workforce shortage literature | Trust declines when recruitment resolves and staffed beds increase, reflecting onboarding workload friction and staffing ratio constraints. |
| **Strike Temporary Cost Premium** | [exemplary-scenario-brief.md:L86](../design/exemplary-scenario-brief.md#L86) | `$30,000/month` | Literature-grounded | American Association of Colleges of Nursing (AACN) | Strike contingency costs (e.g., travel nurses) typically run 2x to 3x higher than standard registry rates. |

---

## 3. Key Lit-Review Grounding

### Safe Staffing Ratios (California AB 394)
California Assembly Bill 394 (passed in 1999, implemented in 2004) was the first US law to mandate unit-specific numerical nurse-to-patient staffing ratios (e.g., 1:5 in medical-surgical units, 1:2 in intensive care). Ratios below these levels are treated by nurses and unions as unsafe working conditions, resulting in immediate labor grievances. This supports the game's modeling of a distinct "staffing ratio trust threshold" below which strikes or union burnout crises trigger.

### Linda Aiken's JAMA 2002 Study
In a landmark study published in the *Journal of the American Medical Association*, Linda H. Aiken and colleagues demonstrated that for each additional patient per nurse beyond the baseline:
- The odds of patient mortality within 30 days increase by **7%**.
- The odds of nurse burnout increase by **23%**.
- The odds of nurse job dissatisfaction increase by **15%**.

This empirical finding directly supports the game's formula linking bed additions without hiring (`add_staffed_beds`) to a direct reduction in `workforce_trust`.

### RN Recruitment Lags (NSI 2026 Report)
The 2026 NSI National Health Care Retention & RN Staffing Report indicates that the average time-to-fill for a registered nurse vacancy is **78 days** (approximately 2.6 months), with specialized units taking over 80+ days. The game's competitive command delay of 1 month represents a stylized, fast-tracked hiring process, but preserves the strategic necessity of planning recruitment in advance of facility expansion.

---

## 4. Maintenance Rules for Future Formula Changes

Any future updates to the workforce simulation transition code or parameter values must follow these rules:
1. **Cite the Ledger**: Any PR changing parameters in `src/actors/labor.rs`, `src/sim/transition.rs`, or `src/sim/transition_competitive.rs` must reference a row in this ledger or add a new row.
2. **Keep Rationale Intact**: If a value is changed for gameplay balancing (e.g., modifying `minimum_retention_spend` to increase difficulty), the confidence label must be updated to `Gameplay-driven` and documented.
3. **Add Regression Tests**: Any change to transition calculations must include a deterministic regression test in `src/sim/transition_tests.rs` or `src/sim/validate_competitive_tests.rs` verifying that the modified formulas produce the expected output under seed-variation conditions.
