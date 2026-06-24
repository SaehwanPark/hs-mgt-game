# Evidence Registry

**Status:** Phase 2 draft converting Phase 1 research into actionable links  
**Source:** [`docs/phase1-lit-review.md`](phase1-lit-review.md)

This registry tracks mechanisms, evidence quality, and design use. It is not an
empirical calibration ledger, and it should not be treated as validation for
prototype integer parameters.

## Mechanism Registry

| Mechanism | Design use | Evidence status | Notes |
| --- | --- | --- | --- |
| Payer-provider rate negotiation | Turn 1 insurer decision | Abstraction | Integer thresholds; not calibrated to real contracts |
| State access mandate response | Turn 2 policy decision | Abstraction | Simplified oversight ladder |
| Workforce retention under pressure | Turn 3 labor decision | Abstraction | Inspired by labor-market tension literature |
| Regional access coalition | Turn 4 coalition decision | Abstraction | Cooperative opportunity per roadmap §5.2 |
| Delayed/noisy access reporting | Observation model | Literature-informed | Supports decision vs. outcome debrief |
| Prior-period measurement revision | Observation briefing | Literature-informed | Revisions do not rewrite committed history |
| Deterministic replay | Architecture proof | Project requirement | ODD/STRESS-aligned documentation target |
| Actor decision rationales | History and debrief | Project requirement | Records why each local strategic actor selected an outcome |
| Attributed effects | Transition explanation | Project requirement | Supports causal inspection without claiming calibration |

## Boundary Evidence Notes

- Current actors and commands are justified by the roadmap's first vertical-slice
  requirements: payer negotiation, policy process, workforce pressure,
  cooperative opportunity, observation separation, replay, and debrief.
- Current formulas remain design abstractions. They should be replaced or
  bounded by official data and focused literature only when a mechanism is being
  prepared for calibration or external playtesting.
- Official source candidates named in the Phase 1 literature review include CMS,
  KFF, MedPAC, MACPAC, and BLS. Selecting exact datasets is deferred until the
  parameter ledger is created.

## Unresolved Questions

- Which official datasets should anchor future parameter ranges?
- Which mechanisms need expert review before external playtesting?
- How should educational debrief prompts be evaluated for learning objectives?
- Which actor objectives should be configurable versus fixed in the first
  scenario?
- Which distributional outcomes must be first-class before external classroom
  use?

## Parameter-Source Ledger

Initial ledger of official source **candidates** for future parameterization.
No prototype integer in the current codebase is calibrated from these sources.
Status keys: `candidate` (identified, not applied), `linked` (cited in mechanism
design), `calibrated` (ranges applied in ruleset — none yet).

| Parameter domain | Prototype use (abstract) | Source candidate | Status | Notes |
| --- | --- | --- | --- | --- |
| Hospital finance / cash pressure | `cash_on_hand`, spend commands | CMS National Health Expenditure Data; AHA/Hospital Cost Report context via MedPAC reports | candidate | Use for plausible ranges only when calibrating |
| Commercial payer rates / network tension | Turn 1 rate request thresholds | KFF Employer Health Benefits Survey; MedPAC Medicare payment context as benchmark | candidate | Not contract-level modeling |
| State access / policy pressure | Turn 2 mandate and oversight ladder | State health department reports; MACPAC access narratives for Medicaid context | candidate | Federal Medicaid rules deferred |
| Nursing workforce pressure | Turn 3 labor signal and retention | BLS healthcare occupations; selected workforce shortage literature | candidate | No strike-law simulation |
| Community trust / coalition leverage | Turns 3–4 trust and coalition signals | KFF community health surveys (conceptual); local coalition case studies | candidate | Qualitative anchor only |
| Access and quality indices | Reported vs true access, quality | CMS quality programs (conceptual); literature on measurement error | literature-informed | Observation noise already modeled |
| Market competition / capacity | Planned Turn 5 competitor slice | MedPAC hospital market concentration; IO literature on capacity competition | candidate | Actor card required before runtime |
| Macroeconomic / utilization shocks | Future exogenous inputs | CMS NHE projections; recession utilization literature | candidate | Not in current four-turn demo |

### Ledger rules

- Replace a prototype threshold only when a row moves to `calibrated` with an
  explicit citation and CHANGELOG note.
- Separate **empirical calibration** (plausible real-world ranges) from
  **gameplay balancing** (fun, tension, teachability).
- Gameplay balancing choices must be documented even when not empirically sourced.

## Next Steps

- See [`phase1-implications-memo.md`](phase1-implications-memo.md) for
  research-to-design implications from Phase 1.
- See [`phase5-scope-register.md`](phase5-scope-register.md) for Phase 5 closure,
  deferred world elements, and recommended next runtime slice.
- Use [`actor-cards.md`](actor-cards.md) before adding future strategic actors.
- Use [`first-scenario-brief.md`](first-scenario-brief.md) to keep first-slice
  runtime expansion bounded.
- Link each mechanism row to primary sources as parameters are introduced.
- Separate empirical calibration ranges from gameplay balancing choices.
- Add scenario-specific evidence when the first external scenario format lands.
