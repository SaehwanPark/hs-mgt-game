# Evidence Registry

**Status:** Phase 2 draft converting Phase 1 research into actionable links  
**Source:** [`docs/phase1-lit-review.md`](phase1-lit-review.md)

This registry tracks mechanisms, evidence quality, and design use. It is not an
empirical calibration ledger, and it should not be treated as validation for
prototype integer parameters.

## Model-Confidence Labels

Future mechanism and parameter ledgers should use these labels when a mechanic
is prepared for calibration, debrief, or scenario-authoring work. These are
documentation labels only; they do not introduce a runtime schema.

| Label | Meaning |
| --- | --- |
| Empirically calibrated | Parameter range or behavior is linked to cited data and applied in a versioned ruleset |
| Literature-grounded | Mechanism direction or relationship is supported by literature, but current numbers are not calibrated |
| Expert-informed | Mechanism is based on documented reviewer or practitioner judgment |
| Stylized abstraction | Mechanism is intentionally simplified to preserve a credible strategic relationship |
| Gameplay-driven | Mechanism or value exists primarily for tension, pacing, or teachability and must be labeled as such |

Rows may carry more than one note, but do not blur empirical calibration with
gameplay balancing. A prototype threshold remains an abstraction until the
ledger records a source, range, and versioned ruleset use.

## Mechanism Registry

| Mechanism | Design use | Evidence status | Notes |
| --- | --- | --- | --- |
| Payer-provider rate negotiation | Turn 1 insurer decision | Abstraction | Integer thresholds; not calibrated to real contracts |
| State access mandate response | Turn 2 policy decision | Abstraction | Simplified oversight ladder |
| Workforce retention under pressure | Turn 3 labor decision; competitive recruitment | Literature-grounded | Detailed in [workforce-ledger.md](workforce-ledger.md) |
| Regional access coalition | Turn 4 coalition decision | Abstraction | Cooperative opportunity per roadmap §5.2 |
| Competitor capacity response | Turn 5 rival system decision | Abstraction | Competitive capacity interaction per roadmap §3.3 |
| Delayed/noisy access reporting | Observation model | Literature-informed | Supports decision vs. outcome debrief |
| Prior-period measurement revision | Observation briefing | Literature-informed | Revisions do not rewrite committed history |
| Deterministic replay | Architecture proof | Project requirement | ODD/STRESS-aligned documentation target |
| Actor decision rationales | History and debrief | Project requirement | Records why each local strategic actor selected an outcome |
| Attributed effects | Transition explanation | Project requirement | Supports causal inspection without claiming calibration |
| Competitive regional campaign (design) | Phase 6.0 parallel track | Design artifact | See [`gameplay-competitive-sketch.md`](gameplay-competitive-sketch.md), ADRs 0003–0006; not runtime |

## Boundary Evidence Notes

- Current actors and commands are justified by the roadmap's first vertical-slice
  requirements: payer negotiation, policy process, workforce pressure,
  cooperative opportunity, competitive capacity response, observation separation,
  replay, and debrief.
- Current formulas remain design abstractions. They should be replaced or
  bounded by official data and focused literature only when a mechanism is being
  prepared for calibration or agent-playtest validation.
- Official source candidates named in the Phase 1 literature review include CMS,
  KFF, MedPAC, MACPAC, and BLS. Selecting exact datasets is deferred until the
  parameter ledger is created.

## Unresolved Questions

- Which official datasets should anchor future parameter ranges?
- Which mechanisms need expert or domain-reviewer review before agent-playtest
  synthesis?
- How should educational debrief prompts be evaluated for learning objectives?
- Which actor objectives should be configurable versus fixed in the first
  scenario?
- Which distributional outcomes must be first-class before any future classroom
  or expert review?

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
| Nursing workforce pressure | Turn 3 labor signal and retention; competitive nurse recruitment | BLS healthcare occupations; California AB 394 safe staffing; Aiken JAMA 2002; NSI staffing report | linked | Detailed workforce ledger created at [workforce-ledger.md](workforce-ledger.md) |
| Community trust / coalition leverage | Turns 3–4 trust and coalition signals | KFF community health surveys (conceptual); local coalition case studies | candidate | Qualitative anchor only |
| Access and quality indices | Reported vs true access, quality | CMS quality programs (conceptual); literature on measurement error | literature-informed | Observation noise already modeled |
| Market competition / capacity | Turn 5 competitor capacity response | MedPAC hospital market concentration; IO literature on capacity competition | linked | Implemented at v0.1.21 per competitor actor card |
| Macroeconomic / utilization shocks | Future exogenous inputs | CMS NHE projections; recession utilization literature | candidate | Not in current five-turn demo |

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
- Add scenario-specific evidence when the first expanded scenario format lands.
