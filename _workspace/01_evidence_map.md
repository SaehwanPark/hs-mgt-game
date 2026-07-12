# Evidence Map - Regional Affiliation Runtime Proposal v0.11.14

## Scope

Convert the completed v0.11.13 affiliation-first design gate into a bounded
runtime proposal without presenting the game as a legal, financial, or policy
forecast.

## Sources Reviewed

- Existing DOJ/FTC merger-guideline and HHS consolidation sources cited in
  `docs/expansion-proposal-review.md`.
- `docs/proposal.md`, `docs/roadmap.md`, `docs/design_principles.md`,
  `docs/system-boundary.md`, and `docs/scenario-format-draft.md`.
- `_workspace/01_evidence_map.md`, `_workspace/02_mechanism_design.md`, and
  `_workspace/03_domain_qa.md` from v0.11.13 as the prior design checkpoint.

## Mechanisms and Institutions

| Mechanism | Evidence status | Proposal implication |
| --- | --- | --- |
| Partner fit and solvency | Direction supported; values are abstractions | Expose reported partner signals while keeping true condition hidden |
| Institutional review | Direction supported; outcome is not a legal forecast | Model approval, conditions, delay, and rejection as resolved outcomes |
| Community benefit and continuity | Direction supported; metrics are design abstractions | Keep commitments distinct from Riverside financial utility |
| Labor response | Direction supported; response thresholds are not calibrated | Resolve support, opposition, or disruption explicitly |
| Payer leverage | Direction supported; post-affiliation effect is stylized | Record payer response separately from review and community response |
| Integration drag | Mechanism direction is plausible; magnitude is uncalibrated | Use explicit delayed integration input and attributed effects |

## Actor Incentives and Information

- Riverside values solvency, autonomy, access, workforce stability, and mission.
- The partner values solvency, service continuity, mission fit, autonomy, and
  outside options.
- Review institutions value competition, continuity, and public commitments but
  are not controlled by Riverside.
- Labor, payer, and community actors respond to commitments and perceived risk
  from their own observations rather than hidden true state.
- Educational evaluation must remain separate from all actor utilities and
  organizational outcome metrics.

## Assumptions

- The first runtime target is one fictional neighboring nonprofit partner.
- The scenario is opt-in, six monthly stages, and does not modify the default
  competitive campaign.
- Numeric bounds, command syntax, and concrete Rust types are implementation
  decisions for a later PR.
- All uncertain partner, review, labor, payer, community, and integration
  outcomes are explicit resolved inputs.

## Unresolved Questions

- Exact scenario-loader representation and command spelling remain deferred to
  the implementation PR.
- Numeric commitment costs, review timing, and integration effects require
  separate gameplay and domain validation.
- Replay and state-hash versioning must be chosen if affiliation inputs become
  part of the competitive transition wire shape.

## Design Implications

- Prefer a localized staged interaction over a general actor or deal-market
  framework.
- Preserve immutable decision-time observations and append-only outcomes.
- Require a debrief comparison among independence, deferral, and affiliation.
- Treat all regulatory language as a stylized educational abstraction.

## Risks

- False legal precision if review outcomes look predictive.
- Normative opacity if affiliation is rewarded or punished by a single score.
- Replay instability if future implementation hides stochastic responses inside
  transition evaluation.
- Scope expansion if the proposal becomes a full acquisition simulator.
