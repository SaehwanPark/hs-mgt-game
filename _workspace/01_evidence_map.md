# Evidence Map - Obstetrics Service Line & L&D Diversion Mechanics

## Assumptions
1.  **Obstetric Staffing Intensity:** Labor and Delivery (L&D) units require specialized obstetric nursing and medical staff. To reflect this high-intensity clinical environment (below ICU but above Med-Surg), we model obstetric staffing targets as:
    *   Nurses: 1 Nurse per 2 obstetric beds (target: `(system.obstetrics_capacity + 1) / 2`).
    *   Physicians: 1 OB/GYN per 5 obstetric beds (target: `(system.obstetrics_capacity + 4) / 5`).
    *   Admins: 1 Admin per 10 obstetric beds (target: `(system.obstetrics_capacity + 9) / 10`).
2.  **Childbirth Loyalty ("Halo Effect"):** Labor and Delivery is widely recognized in healthcare management as the primary entry point for young families into a health system, establishing multi-decade loyalty ("halo effect").
    *   We assume that diverting obstetric patients due to capacity or staffing deficits has disproportionate reputational and competitive impacts.
    *   Diverting a patient causes a loss of community trust (`-2` trust per diverted patient) and a leak of market share (`-1` market share index per diverted patient).
3.  **Inpatient Demand:** We model a baseline monthly obstetric demand of 10% of the physical obstetric capacity (`(system.obstetrics_capacity + 9) / 10` using ceiling division).

## Precedents
- Med-Surg beds: 1 Nurse per 5 beds, 1 Physician per 20 beds, 1 Admin per 20 beds.
- ICU beds: 1 Nurse per 1 bed, 1 Physician per 2 beds, 1 Admin per 5 beds.
- ED bays: 1 Nurse per 2 bays, 1 Physician per 4 bays, 1 Admin per 10 bays.
- Obstetrics beds: 1 Nurse per 2 beds, 1 Physician per 5 beds, 1 Admin per 10 beds.
- ED boarding is modeled as a physical capacity bottleneck, whereas obstetric deficits are modeled as patient diversion / regional bypass.

## Evidence Quality
- **High:** Childbirth as a driver of long-term family brand loyalty and lifetime healthcare value is well-documented in healthcare marketing and strategy literature. Specialized L&D nurse-to-patient staffing ratios (1:2 for active labor) are standard clinical guidelines (AWHONN).
- **Medium:** The specific 10% monthly demand rate, `-2` community trust penalty, and `-1` market share index penalty are stylized balancing parameters designed to create clear strategic tradeoffs.

## Uncertainty
- Actual obstetric patient volume is deterministic relative to physical capacity and does not model stochastic seasonal birth rate spikes, preserving the deterministic nature of transition evaluation.
