# Mechanism and Scenario Design - Exemplary Scenario Brief (Phase 6.2)

## Goal and Roadmap Phase
- **Goal:** Design the conceptual framework for `competitive-exemplary-v1`, a 24-month competitive regional market campaign.
- **Roadmap Phase:** Phase 6.2 (Exemplary scenario authoring plan).

---

## Slice Boundary
This design covers the documentation-only brief (`docs/exemplary-scenario-brief.md`) which serves as the blueprint for scenario TOML structures.
- **Included:** 24 monthly turns, 1 human system (Riverside), 2 AI systems (Northlake, Summit), 3 NPC entities (Blue Shield, State Health Department, Riverside Nursing Association), 3 major scenario events, and 2 distinct strategic directions.
- **Excluded:** Multi-region networks, federal policy changes, and direct LMS integration.

---

## Actors and Authority
1. **Riverside Community Health (Human CEO):** Authority to deploy monthly Action Points (AP) and cash across capital projects, nurse hiring, wage increases, public access pledges, and monitoring.
2. **Northlake Health (AI CEO - Expansion Style):** Focuses on clinic expansions and poaching commercial insurance patient mix.
3. **Summit Care (AI CEO - Cost-Containment Style):** Focuses on margin protection, wage freezing, and minimizing Medicaid/uninsured patient exposure.
4. **Riverside Nursing Association (Workforce NPC):** Demands wage parity and safe staffing ratios. Can declare labor disputes or strike.
5. **Blue Shield (Commercial Payer NPC):** Bargains with hospital systems over reimbursement rates. Can refuse out-of-network providers.
6. **State Health Department (Regulator NPC):** Reviews Certificate of Need (CON) facility requests and audits nonprofit community benefit compliance.

---

## State, Beliefs, and Observations
- **True State (Engine Core):**
  - Financials: Cash reserves, operating margins, capital budget.
  - Operations: Clinic capacity, nurse staffing ratios, EHR project progress.
  - Relationships: Nurse trust, public access index, commercial contract rate multiplier.
- **Observations (Player-Facing):**
  - Noisy reported access index (delayed by 1 month, +/- 5% measurement noise).
  - Observed rival capacity expansions (revealed publicly only after 1 month).
  - Nurse satisfaction rating (rough qualitative index: high, moderate, low).
- **Beliefs (Rival AI):**
  - Rival systems maintain beliefs about the human's capacity expansion based on public actions, updated when the player performs unmonitored changes.

---

## Commands, Events, and Effects
### Verbs (Action Vocabulary)
- `project <name> [AP] [cash]`: Start/fund delayed projects (e.g. EHR migration, CON clinic build).
- `recruit [AP] [cash]`: Attempt to hire nurses to restore staffing ratios.
- `wage-offer <percent> [AP]`: Offer nurse salary raises to increase trust.
- `negotiate <payer> [AP] [pc]`: Bargain with Blue Shield, using political capital (pc).
- `monitor <rival> [AP]`: Gather intelligence on a rival's private projects.
- `hold`: Conserve AP and cash.

### Major Scenario Events
1. **Nurse Burnout Crisis (Month 8):** Triggers a drop in nurse trust. If staffing ratios are below safety thresholds, a strike warning is issued.
2. **Certificate of Need (CON) Legal Challenge (Month 10):** Northlake files an objection to Riverside's clinic build, delaying progress by 3 months unless Riverside spends 3 political capital.
3. **Annual Insurer Renewal (Month 12 & 24):** Rates are finalized; systems with low capacity or poor quality face rate reductions.

---

## Strategic Interaction
- **Market Share Poaching (Simultaneous):** If Riverside and Northlake both expand clinic capacity in the same zip code, the patient volume (and resulting cash) is split based on quality metrics and capacity size.
- **Bargaining with Payer:** Blue Shield compares each system's quality and cost structure. Riverside can negotiate in-network rates, but if negotiations fail, Riverside goes out-of-network (loss of patient volume, offset by higher out-of-network rates).

---

## Assumptions and Parameters
- **Starting Cash:** Riverside starts with $500,000.
- **Action Points:** Riverside receives 3 AP per month.
- **Staffing Cost:** Each nurse FTE costs $8,000/month.
- **CON Project Cost:** EHR migration costs $150,000 (3 months); clinic build costs $250,000 (6 months).

---

## Educational Debrief Hooks
- **Causal Debrief:** Highlight why cash reserves fell in Month 9 (strike wage settlement vs. delayed clinic revenue).
- **Decision Quality vs. Realization:** Prompts for the player:
  - "Did your decision to underfund nurse recruitment in Year 1 lead to the Year 2 rate cut from Blue Shield?"
  - "Evaluate the cost of ignoring Northlake's private project planning."

---

## Determinism and Replay Notes
- Random events are selected from a fixed scenario seed deck.
- The outcome of nurse recruitment is computed deterministically using the formula: `SuccessRate = BaseRate * StaffingTrust * AP_Allocated` with no runtime rand calls.

---

## Open Questions
- What is the most intuitive CLI formatting for displaying simultaneous rival actions when they are revealed to the player?
