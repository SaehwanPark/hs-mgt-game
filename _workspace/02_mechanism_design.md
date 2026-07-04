# Mechanism Design - Nursing Workforce & Retention Ledger (Phase 2)

## Scope
Defines the mapping between the conceptual model parameters and their mathematical expressions in code.

---

## 1. Actor Actions & Incentives

- **Nursing Workforce NPC:** Represents Riverside's nurse labor pool. Demands safe ratios (modeled as maintaining `workforce_trust` >= 60) and fair wages (modeled as `minimum_retention_spend` >= 5 and `minimum_schedule_relief` >= 3).
- **Player (CEO):** Balancing capacity growth (needs cash and AP) with labor stability (needs wage/retention spend).

---

## 2. Mathematical Mapping

### Stabilization Campaign (`src/sim/transition.rs`)

1. **Staffing Friction on Bed Addition:**
   $$\Delta T_{\text{workforce}} = -\frac{\text{add\_staffed\_beds}}{4}$$
   - *Label:* Literature-grounded (Aiken 2002 burnout metrics).
2. **Schedule Relief Impact:**
   $$\Delta T_{\text{workforce}} = +\frac{\text{schedule\_relief}}{2}$$
   - *Label:* Stylized abstraction.
3. **Workforce Strike Trigger:**
   $$\text{Decision} = \text{WorkAction} \quad \text{if} \quad \text{not } \text{credible\_offer}$$
   - *Label:* Gameplay-driven (Note: `T_workforce < 60` or `sick_call_pressure` activates `labor_pressure` which is required for a `Cooperative` outcome, but `WorkAction` triggers unconditionally if the offer is not credible).

### Competitive Campaign (`src/sim/transition_competitive.rs`)

1. **Hiring Lag:**
   $$\text{Delay}_{\text{nurse}} = 1 \text{ month}$$
   - *Label:* Literature-grounded (78-day NSI average).
2. **Recruitment Capacity Staffing Burden:**
   $$\Delta T_{\text{workforce}} = -\text{headcount}$$
   - *Label:* Stylized abstraction (applied when recruitment resolves).
