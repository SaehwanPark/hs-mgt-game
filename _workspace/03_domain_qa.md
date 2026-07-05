# Domain QA - Psychiatric Service Line & Behavioral Health crisis holding mechanics

- **Status:** Pending (Drafted)
- **Role:** Domain QA Reviewer

## Checklist & Review Criteria

- [ ] **State/Observation Separation:** The human player only observes the Psychiatric capacity, effective capacity, and ED boarding count through formatted REPL reports, while the underlying true state is updated deterministically in the transition kernel.
- [ ] **Deterministic Replay Boundary:** All Psychiatric capacity changes are enqueued in `effect_queue` and resolved during transition. The state hash record has been updated to include `psychiatric_capacity` to guarantee deterministic replay validation.
- [ ] **Educational & Operational Balance:** The staffing targets reflect the specialty monitoring environment of behavioral health care (1 Nurse per 4 beds, 1 Physician per 10 beds, 1 Admin per 15 beds). The hierarchical allocation model prioritizes specialty services (ICU, Obstetrics, Med-Surg) before Psychiatric beds, and Psychiatric beds before general Outpatient/ED.
- [ ] **Psychiatric ED Boarding & Diversion:** If effective capacity drops below 10% of total capacity, overflowed patients board in the Emergency Department (ED), reducing effective emergency capacity on a 1-to-1 basis. If ED capacity is also exhausted, they are diverted, incurring community trust (-1) and quality index (-1) penalties.
- [ ] **Backward Compatibility:** Default `psychiatric_capacity` defaults to `0` in `HealthSystemState` deserialization and custom scenario parsing, avoiding turn-1 staffing deficits and serialization panics in existing scenarios/saves.

## Findings & Risk Mitigation
- **Golden Hash Integration:** Since `psychiatric_capacity` is added to the hash block, we will update the competitive seed-42 golden hash to avoid regression failures.
- **AI Match Coverage:** AI players will be updated with matching arms for the new command options to avoid compile errors.
- **Strike Suspension:** Psychiatric projects will be delayed during active nurse strikes, matching general project behavior.
