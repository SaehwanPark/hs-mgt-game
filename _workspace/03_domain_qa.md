# Domain QA - Emergency Department Service Line

- **Status:** Pending (Design Review Phase)
- **Role:** Domain QA Reviewer

## Checklist & Review Criteria

- [ ] **State/Observation Separation:** The human player only observes reported and effective emergency capacity, while the underlying true state is updated deterministically in the transition kernel.
- [ ] **Deterministic Replay Boundary:** All emergency capacity changes are queued through the `effect_queue` and resolved deterministically during transitions. The state hash incorporates `emergency_capacity` to ensure exact replay alignment.
- [ ] **Educational Balance:** The staffing formulas reflect the realistic policy challenge that Emergency Departments are high-intensity resource environments where shortages cause compounding quality and access issues.
- [ ] **Backward Compatibility:** Existing custom scenarios that do not specify `emergency_capacity` default safely to standard values (e.g. 15 for Riverside, 20 for Northlake) during parsing, avoiding serializing/deserializing failures.

## Findings & Risk Mitigation
- **Risk:** High staffing targets for ED could cause immediate turn-0 deficits for systems with low starting staff.
- **Mitigation:** Ensure starting staff (nurses, physicians, admins) in the scenario files are sufficient to cover the initial beds, outpatient capacity, and default/explicit emergency capacity, or start with no deficits at month 1.
