# Evidence Map - Medicare Public Payer Integration

## Domain Context & Precedents
- **Source:** MedPAC March 2025 Report to Congress, CMS Hospital Value-Based Purchasing (VBP) Program.
- **Mechanism:** Medicare payments are largely non-negotiable administered rates, but hospitals must comply with extensive quality reporting and value-based metrics (e.g., readmission rates, clinical outcomes, patient safety).
- **Lobbying and Compliance Costs:** Maintaining Medicare compliance requires dedicated quality registry reporting, clinical documentation improvement (CDI) programs, and administrative overhead. This translates to higher cash costs than Medicaid ($10k vs $5k) due to federal reporting requirements.
- **Strategic Impact:** Successful compliance increases reported clinical quality ratings (VBP incentives/Star Ratings) and reduces regulatory policy pressure.

## Causal Mapping
```
Player Action: Negotiate (payer=medicare, posture=neutral)
  -> Costs: 1 AP, 2 PC, $10 Cash
  -> Results:
       - Direct increase in Quality Index (+3 quality_index)
       - Direct decrease in Policy Pressure (-3 policy_pressure)
       - No change to Commercial Payer Pressure (isolated from Carrier A/B)
       - No direct change to Market Share (compliance-focused, not market-poaching)
```

## Abstractions and Assumptions
1. **Administered Rates:** Medicare does not allow rate negotiations. Posture is restricted to `neutral` only (representing compliance alignment).
2. **Quality Focus:** Unlike Medicaid compliance which improves geographical access index (safety net/Medicaid access), Medicare compliance rewards the system's clinical quality index (representing federal value-based care performance).
3. **Overhead Cost:** The $10 cash cost represents administrative compliance overhead, which is double the Medicaid compliance cost ($5) to reflect federal regulatory reporting density.
