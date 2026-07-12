# Mechanism Design - Affiliation-First Regional Consolidation v0.11.13

## Goal and Roadmap Phase

Phase 7.7 expansion proposal gate, preparing one Phase 9 regional affiliation
design without changing the current competitive runtime.

## Slice Boundary

- Setting: Riverside Community Health evaluates a loose affiliation with one
  fictional neighboring nonprofit system.
- Primary choice: remain independent, pursue the affiliation, or defer while
  gathering information.
- Sequence: partner assessment, proposed commitments, institutional review,
  conditional outcome, and early integration consequences.
- Acquisition is a future comparison branch, not part of the first runtime
  design.
- No public command names, scenario fields, numeric parameters, or Rust types
  are introduced by this artifact.

## Actors and Authority

- Riverside CEO: proposes the affiliation, allocates preparation resources,
  and makes community/workforce commitments.
- Partner nonprofit system: accepts, rejects, or conditions the proposal based
  on solvency, mission, autonomy, service continuity, and outside options.
- State regulator/community-review institution: may approve, condition, delay,
  or reject the proposal; it is not controlled by Riverside.
- Labor representatives: respond to staffing, job, wage, and integration
  commitments.
- Commercial payer and community coalition: respond to concentration,
  service continuity, access, and community-benefit signals.

## State, Beliefs, and Observations

Future true state may include partner capacity and solvency, workforce status,
service continuity, payer exposure, commitment obligations, review status, and
integration progress. Player-visible observations should expose reported
partner condition, public community concerns, labor signals, payer posture, and
review status with explicit uncertainty or delay. Committed history must retain
what Riverside knew at decision time; later review findings must not rewrite it.

## Commands, Events, and Effects

The design vocabulary is conceptual only:

- assess partner;
- propose affiliation;
- negotiate community/workforce commitments;
- submit for institutional review; and
- execute staged integration after approval.

Invalid operations include acting without partner consent, submitting a
duplicate review, or exceeding an explicitly defined commitment authority.
Modeled outcomes include review delay, conditional approval, failed
affiliation, labor opposition, payer response, service disruption, and
integration drag. These are not validation errors.

## Strategic Interaction

The partner and Riverside negotiate a credible affiliation package. The review
institution evaluates public and competition concerns. Labor and community
actors respond to commitments and perceived service risk. Payers and rivals may
change leverage after the affiliation. The design must show that independence,
affiliation, and deferral can each be defensible under different observations;
no hidden optimal path is permitted.

## Assumptions and Parameters

- Mechanism direction is literature-grounded; prototype numbers are not.
- Review outcomes, labor responses, payer responses, and integration shocks
  would be named resolved inputs in a future runtime implementation.
- Legal review is an educational abstraction and must not claim to predict a
  real agency decision.
- Community benefit and service continuity are distinct from Riverside's
  financial utility.

## Educational Debrief Hooks

- What did Riverside know before proposing the affiliation?
- Which commitments improved continuity or legitimacy and which consumed
  scarce capital?
- Did an unfavorable result reflect a poor decision, a hidden realization, or
  an institutional response outside Riverside's authority?
- How did the organizational outcome differ from community welfare and access?
- What would the independence or deferral counterfactual have preserved?

## Determinism and Replay Notes

No runtime transition changes are included. If promoted later, all uncertainty
must be resolved before the deterministic transition, with stable named streams
and append-only records for review, labor, payer, and integration outcomes.
Actor observations must remain separate from true state and debrief output.

## Open Questions

- Which one partner attribute set is sufficient for the first playable slice?
- What is the minimum commitment vocabulary that preserves meaningful tradeoffs?
- Should affiliation be a staged project or a single scenario decision?
- Which service-continuity and distributional metrics are necessary before
  implementation?
