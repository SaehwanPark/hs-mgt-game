# Domain QA - ICU Service Line & ED Boarding Mechanics

- **Status:** Pass
- **Role:** Domain QA Reviewer

## Checklist & Review Criteria

- [x] **State/Observation Separation:** The human player only observes the ICU capacity, effective capacity, and ED boarding count through formatted REPL reports, while the underlying true state is updated deterministically in the transition kernel.
- [x] **Deterministic Replay Boundary:** All ICU capacity changes are enqueued in `effect_queue` and resolved during transition. The state hash record has been updated to include `icu_capacity` to guarantee deterministic replay validation.
- [x] **Educational & Operational Balance:** The staffing targets reflect the high-intensity environment of critical care (1 Nurse per 1 Bed, 1 Physician per 2 Beds, 1 Admin per 5 Beds). The hierarchical allocation model mimics standard clinical operations (critical care needs met first).
- [x] **ED Boarding Bottleneck:** ED boarding correctly deducts from effective ED capacity on a 1-to-1 basis when effective ICU capacity is less than the critical admissions demand (5% of med-surg beds). This captures the inter-departmental bottleneck.
- [x] **Backward Compatibility:** Default `icu_capacity` defaults to `0` in `HealthSystemState` deserialization and custom scenario parsing, avoiding turn-1 staffing deficits and serialization panics in existing scenarios/saves.

## Findings & Risk Mitigation
- **Verification:** Unit tests in `src/sim/transition_competitive.rs` (`test_icu_department_mechanics`) confirm that ICU investments, staffing targets, hierarchical allocation, ED boarding, and capacity-deficit index penalties evaluate to the exact expected mathematical values.
- **Strike Suspension:** The RNA nurse strike delays `PendingEffectKind::IcuCapacity` along with other capital project kinds, preventing completion of ICU expansions during active labor strikes.
