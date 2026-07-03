# Exemplary Scenario Brief: The Regional Workforce and Market Realignment Challenge

**Status:** Phase 6.2 design artifact  
**Audience:** Contributors, domain reviewers, playtest designers  
**Campaign id:** `competitive-exemplary-v1`  
**Relationship:** Complements `first-scenario-brief.md` and `competitive-scenario-brief.md`.

---

## 1. Scenario Concept

In this 24-month competitive campaign, the player leads **Riverside Community Health**, a safety-net-leaning nonprofit health system in a mid-sized regional market. Riverside faces simultaneous pressure from a severe nurse staffing shortage, a dominant commercial payer demanding cost cuts, a aggressive expansionist rival poaching commercial patients, and state regulatory constraints on facility growth.

The campaign tests whether players can maintain their safety-net mission and workforce stability without triggering a fiscal crisis or regulatory intervention.

---

## 2. Actor Profiles and Authority

### Human Player
- **Riverside Community Health (CEO):** Player 0. Safety-net mission. Low initial cash reserves but high community trust and political goodwill.
- **Authority:** Directs monthly Action Points (AP) and cash toward nurse wages, hiring recruitment campaigns, Certificate of Need (CON) facility applications, EHR projects, and competitor monitoring.

### Rival AI Systems
- **Northlake Health (Rival 1 - Expansionist):** A large, growth-oriented hospital group. Focuses on expanding outpatient clinic capacity in high-income suburbs to capture profitable commercial insurance patients.
- **Summit Care (Rival 2 - Margin-Focused):** A lean, multi-specialty system. Focuses on cost reduction, strict wage controls, and minimizing safety-net/uninsured patient exposure.

### Non-Player Characters (NPCs)
- **Riverside Nursing Association (RNA - Workforce NPC):** Represents Riverside's nurse workforce. Demands wages matching the regional average and mandatory nurse-to-patient staffing ratios.
- **Blue Shield (Commercial Payer NPC):** The dominant regional insurer. Holds high bargaining power and pushes for rate discounts.
- **State Health Department (Regulator NPC):** Administers the state's Certificate of Need (CON) program and monitors charitable community benefit spending.

---

## 3. Initial Setup and Parameters

| Parameter | Riverside Community Health | Northlake Health | Summit Care |
| :--- | :--- | :--- | :--- |
| **Starting Cash** | $500,000 | $1,200,000 | $900,000 |
| **Starting AP/month** | 3 AP | 3 AP | 3 AP |
| **Political Capital** | 4 | 2 | 2 |
| **Clinic Capacity** | 100 units | 150 units | 120 units |
| **Nurse Staffing Trust** | 70% | 85% | 60% |
| **Commercial Rate Index** | 1.0 (baseline) | 1.15 | 1.10 |

---

## 4. Key Strategic Tensions

1. **Workforce vs. Cash (Labor Tradeoff):** Raising nurse wages preserves nurse staffing trust and prevents strikes, but drains cash reserves, delaying capital expansions.
2. **Payer Leverage vs. Charity Care (Nonprofit Mission):** Negotiating higher rates with Blue Shield requires committing significant political capital and AP, and may invite regulatory audits of charity care compliance.
3. **Clinic Expansion vs. Competitor Poaching (CON & Market Share):** Building new outpatient capacity is necessary to defend market share against Northlake Health, but requires navigating state CON regulations which rivals can legally challenge to cause delays.

---

## 5. Timeline of Events and Delayed Consequences

```mermaid
chronology
  title competitive-exemplary-v1 Campaign Timeline
  01 : Month 1 - Campaign Baseline
  08 : Month 8 - Nurse Burnout Crisis
  10 : Month 10 - Northlake CON Challenge
  12 : Month 12 - Annual Blue Shield Rate Renewal
  18 : Month 18 - Delayed EHR / Strike Consequences
  24 : Month 24 - Final Evaluation & Debrief
```

- **Month 1: Campaign Baseline.** Riverside must allocate AP to balance nursing recruitment and monitor rivals.
- **Month 8: Nurse Burnout Crisis (Workforce Conflict).**
  - *Trigger:* Regional nurse shortage increases vacancy rates.
  - *Effect:* Nurse staffing trust drops by 15%. If Riverside's staffing ratio is below 80% capacity, RNA issues a strike warning. The player must choose to increase wages (costing $50,000/month and 1 AP) or face a 2-month strike in Month 10.
- **Month 10: CON Legal Challenge (Competitive Response & Policy Process).**
  - *Trigger:* Riverside's clinic build project reaches 50% completion.
  - *Effect:* Northlake Health files a formal CON objection. The project is suspended for 3 months unless Riverside spends 3 political capital or $100,000 in legal fees to expedite approval.
- **Month 12: Annual Blue Shield Rate Renewal (Payer Interaction).**
  - *Trigger:* Calendar checkpoint.
  - *Effect:* Simultaneous rate negotiations. Riverside must spend AP and political capital to secure rate increases. If Riverside fails to reach a contract, they go out-of-network, reducing commercial patient volume by 40% but increasing reimbursement rates on remaining patients by 20%.
- **Month 18: Delayed Consequences.**
  - *Effect:* If the nurse strike occurred in Month 10, patient safety ratings drop by 20%, leading to a permanent 10% reduction in commercial volume. If the EHR migration project was underfunded, data system lag reduces operational efficiency, increasing monthly operating costs by $20,000.
- **Month 24: Final Campaign Review.**
  - *Effect:* Final evaluation of access index, cash position, and policy legitimacy.

---

## 6. Observations and Information Uncertainty

- **Noisy Access Reports:** Riverside sees its reported access index with a +/- 5% random measurement noise and a 1-month delay.
- **Partial Rival Observability:** Northlake and Summit's private capital project planning is unobserved unless Riverside runs the `monitor` command on them. Their public rate adjustments are observed with a 1-month lag.
- **Qualitative Labor Sentiment:** Nurse trust is reported via qualitative alerts ("Stable", "Tense", "Critical") rather than a precise percentage, modeling real-world administrative uncertainty.

---

## 7. Defensible Strategic Directions

### Strategy A: Access Safety Net Defense (Access Focus)
- **Approach:** Prioritize workforce wage increases and safety-net capacity. Accept lower operating margins and slower facility growth.
- **Execution:** Settle nurse contracts early, recruit aggressively, and focus on regional access coalition partnerships.
- **Tradeoff:** Preserves high community trust and regulator approval, but leaves Riverside with low cash reserves and vulnerable to Northlake's market encroachment.

### Strategy B: Fiscal Preservation & Market Consolidation (Financial Focus)
- **Approach:** Contain labor costs, delay non-essential clinic builds, and focus on securing high-reimbursement commercial payer contracts.
- **Execution:** Reject excessive nurse wage demands, use temporary travel nurses to fill gaps, and aggressively negotiate rates with Blue Shield.
- **Tradeoff:** Strong cash reserves and high commercial rates, but faces high nurse turnover, risk of a labor strike, and regulatory scrutiny regarding nonprofit tax exemption.

---

## 8. Educational Assessment and Debrief Hooks

The instructor-visible debrief summary and reflection prompts should focus on:
1. **Decision Quality under Uncertainty:**
   - *"Evaluate your decision to monitor Northlake Health at Month 9. Did the intelligence gathered justify the AP cost, or would that AP have been better spent on nurse retention?"*
2. **Delayed and Cascading Effects:**
   - *"How did underfunding your nurse workforce in Year 1 cascade into going out-of-network with Blue Shield in Year 2?"*
3. **Strategic Incoherence:**
   - *"Did you attempt to combine safety-net expansion with wage freezes? Explain how this strategic inconsistency contributed to the Month 10 strike."*
4. **Policy vs. Welfare:**
   - *"Although Strategy B yielded the highest final cash reserves, discuss the social welfare impact of the resulting 20% drop in Riverside's local access index."*
