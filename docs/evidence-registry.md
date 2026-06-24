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

## Next Steps

- Link each mechanism row to primary sources as parameters are introduced.
- Separate empirical calibration ranges from gameplay balancing choices.
- Add scenario-specific evidence when the first external scenario format lands.
- Create a parameter-source ledger before replacing any prototype integer
  thresholds with evidence-backed ranges.
