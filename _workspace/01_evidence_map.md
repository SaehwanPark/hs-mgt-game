# Evidence Map - Exemplary Scenario Authoring Plan (Phase 6.2)

## Scope
This evidence map supports the design of an exemplary scenario brief (`docs/exemplary-scenario-brief.md`) by linking U.S. healthcare system dynamics—such as financial squeezes, provider-payer rate negotiations, nursing staff burnout/strikes, Certificate of Need (CON) regulatory reviews, and competitive clinic capacity expansions—to structured game mechanisms, actor profiles, and debriefing goals.

---

## Sources Reviewed
1. **Payer provider rate negotiations & leverage:**
   - Dafny, L., Ho, K., & Lee, R. S. (2012). *The Price Effects of Monopsony Power in the Health Insurance Industry*. American Economic Review.
   - Town, R., & Vistnes, S. (2001). *Hospital bargaining power in negotiate-price markets*. Journal of Health Economics.
2. **Workforce constraints, burnout, and strikes:**
   - American Journal of Nursing (AJN). (2024). *Nursing Shortages and the Impact of Mandatory Staffing Ratios*.
   - Bureau of Labor Statistics (BLS). (2025). *Healthcare Occupations Employment and Wage Baselines*.
3. **Competitive capacity & Certificate of Need (CON):**
   - Devers, K. J., Brewster, L. R., & Casalino, L. P. (2003). *Changes in hospital competitive strategy: A new medical arms race*. Health Affairs.
   - National Conference of State Legislatures (NCSL). (2024). *Certificate of Need (CON) State Laws*.
4. **Safety-Net Hospital Margins & Policy Scrutiny:**
   - Medicare Payment Advisory Commission (MedPAC). (March 2025 Report). *Report to the Congress: Medicare Payment Policy* (Chapters on hospital financial performance and safety-net margins).
   - Kaiser Family Foundation (KFF). (2024). *Hospital Charity Care and Nonprofit Tax-Exempt Status Under Scrutiny*.

---

## Mechanisms and Institutions
1. **Safety-Net Operating Margin Compression:**
   - *Real-world basis:* Safety-net hospitals face low margins due to a high proportion of Medicaid/uninsured patients (payer mix) and rising labor costs.
   - *Abstractions:* Represented as a monthly cash draw that scales with capacity utilization, offset by Commercial and Public insurance rate ticks.
2. **Mandatory Staffing Ratio / Nurse Wage Escalation:**
   - *Real-world basis:* Legislative mandates (e.g., California's AB 394) or union strikes force hospitals to raise nurse wages and cap nurse-to-patient ratios.
   - *Abstractions:* A workforce threat event triggers. The player can recruit (costing cash and Action Points (AP)) or offer wage increases. Failing to meet minimum safety ratios reduces quality metrics, increases burnout, and can trigger a strike that halts capital projects.
3. **Certificate of Need (CON) and Clinic Expansion:**
   - *Real-world basis:* In CON states, hospitals must prove community need before building facilities. Rivals can file legal objections to delay or block approvals.
   - *Abstractions:* The player starts a `project` for facility expansion. A rival can execute a private counter-move to contest the CON, which delays the project or requires political capital expenditure to resolve.
4. **Payer Provider Rate Bargaining:**
   - *Real-world basis:* Annual provider-payer contracting cycles. Large insurers demand rate discounts; hospitals demand rate hikes, threatening to go out-of-network.
   - *Abstractions:* An annual negotiation cycle where the provider commits Action Points and political capital to secure a commercial rate increase. Rivals negotiating concurrently can dilute provider leverage.

---

## Actor Incentives and Information
1. **Riverside Community Health (Player 0):**
   - *Incentives:* Maintain financial solvency (cash reserve > 0) while defending its safety-net mission (access index and community trust).
   - *Information:* Full visibility of its own metrics (cash, AP, political capital), but delayed/noisy reports on regional access and private rival actions.
2. **Northlake Health (Rival 1 - Growth/Expansion Focus):**
   - *Incentives:* Maximize commercial market share and expand high-margin service lines.
   - *Information:* Invisible actions (e.g., private clinic planning) unless monitored.
3. **Blue Shield (Payer NPC):**
   - *Incentives:* Minimize payout rates and maintain premium competitiveness.
   - *Information:* Evaluates provider requests based on provider capacity and public pressure.
4. **State Health Department (Regulator NPC):**
   - *Incentives:* Maximize public access and safety-net stability, respond to political backlash.

---

## Assumptions
1. **Cost Shifting:** Higher commercial rates negotiated with Blue Shield can offset safety-net losses, but invite regulatory scrutiny if excessive.
2. **Labor-Capital Tradeoff:** Spending on workforce wages directly reduces cash reserves available for capital projects (like EHR migration).
3. **Information Delay:** Rival public capacity expansions are only observed with a one-month lag.

*If any assumption is found to be false during subsequent scenario authoring, we will stop and adjust the brief.*

---

## Unresolved Questions
1. How to balance the starting cash, AP, and political capital to ensure both "Access Safety Net Defense" and "Fiscal Preservation" paths are viable without one path being an obvious exploit.
2. The specific mathematical delays for Certificate of Need (CON) legal objections (e.g., whether to model it as a flat 3-month delay or variable).

---

## Design Implications
1. **Exemplary Brief Structure:** The brief must explicitly map out the 24-month timeline, highlighting the annual payer renewal tick (Month 12, 24) and the mid-campaign workforce crisis (Month 8).
2. **Scenario Variables:** We need scenario parameters for starting labor trust, insurer contract statuses, and CON approval durations.
3. **Debrief Focus:** The debrief should prompt the player to analyze:
   - "How did my response to the Nurse Strike at Month 8 affect my cash position for the Payer Negotiation at Month 12?"
   - "Did the rival's clinic expansion at Month 10 catch me off guard due to lack of `monitor` commands?"

---

## Risks
1. **False Precision Risk:** Modeling specific staffing ratios (e.g. 1:4) as a hard mathematical threshold could lead to gameplay optimization that doesn't reflect real-world clinical nuance.
   - *Mitigation:* Label staffing ratio impacts as stylized abstractions in the brief.
2. **Normative Bias:** The game should not penalize fiscal caution or favor safety-net defense by default; both must face severe, realistic tradeoffs.
