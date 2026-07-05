# Domain QA - Obstetrics Service Line & L&D Diversion Mechanics

- **Status:** Pass
- **Role:** Domain QA Reviewer

## Checklist & Review Criteria

- [x] **State/Observation Separation:** The human player only observes the Obstetrics capacity, effective capacity, and diversion count through formatted REPL reports, while the underlying true state is updated deterministically in the transition kernel.
- [x] **Deterministic Replay Boundary:** All Obstetrics capacity changes are enqueued in `effect_queue` and resolved during transition. The state hash record has been updated to include `obstetrics_capacity` to guarantee deterministic replay validation.
- [x] **Educational & Operational Balance:** The staffing targets reflect the high-intensity environment of maternal care (1 Nurse per 2 obstetric beds, 1 Physician per 5 beds, 1 Admin per 10 beds). The hierarchical allocation model prioritizes specialty services before general Med-Surg and Outpatient/ED.
- [x] **Obstetric Diversion (The "Halo Effect"):** If effective capacity drops below 10% of total capacity, patients are diverted, representing L&D regional bypass. Each diverted patient penalizes community trust (-2) and market share (-1), representing the family loyalty "halo effect."
- [x] **Backward Compatibility:** Default `obstetrics_capacity` defaults to `0` in `HealthSystemState` deserialization and custom scenario parsing, avoiding turn-1 staffing deficits and serialization panics in existing scenarios/saves.

## Findings & Risk Mitigation
- **Golden Hash Integration:** Since `obstetrics_capacity` is added to the hash block, we will update the competitive seed-42 golden hash to avoid regression failures.
- **AI Match Coverage:** AI players will be updated with matching arms for the new command options to avoid compile errors.
- **Strike Suspension:** L&D projects will be delayed during active nurse strikes, matching general project behavior.
