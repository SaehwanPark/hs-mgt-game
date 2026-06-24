# Evidence Map

## Scope

Map enough project evidence to support the Phase 2 system-boundary and ontology
draft for the current four-turn deterministic prototype. This evidence map does
not calibrate formulas or approve new runtime mechanics.

## Sources Reviewed

- Canonical project docs establish deterministic transitions, true-state versus
  observation separation, strategic actor response, visible assumptions,
  educational debriefing, and narrow vertical slices before frameworks.
- `docs/phase1-lit-review.md` identifies the need for an evidence spine,
  explicit mechanism registers, official data ledgers, participatory design, and
  educational debrief design before broad calibration.
- Current implementation and project docs establish the existing four-turn demo:
  payer negotiation, state-policy response, workforce pressure, coalition
  opportunity, observation revisions, replay, and debrief.

## Boundary Evidence

- The fictional regional US market boundary follows the canonical first-version
  scope and avoids national-scale policy forecasting.
- The health system CEO role is appropriate for commands involving resource
  allocation, payer posture, workforce offers, access commitments, and coalition
  participation.
- Commercial insurer, state policy officials, nursing workforce representative,
  and regional provider coalition liaison are sufficient to demonstrate local
  strategic interaction without introducing a general actor framework.
- Medicare, Medicaid, competitors, employers, patients, and federal actors remain
  deferred because the current prototype does not yet need their authority,
  information, or decision procedures.

## Mechanisms and Institutions

- Capacity investment affects staffed beds, cash, access, and workforce trust.
  This is a project-doc-backed abstraction, not an empirically calibrated
  formula.
- Commercial payer response depends on reported access and requested rate. This
  is a design abstraction for payer-provider bargaining that demonstrates local
  strategic interaction without solving a global game.
- State policy response depends on access commitment, advocacy spend, reported
  access, and explicit policy signal. This is a design abstraction for a policy
  process interaction, not a complete legislative or administrative lifecycle.
- Workforce response depends on retention spend, schedule relief, trust, and
  labor pressure. This is a prototype abstraction for labor relations under
  capacity stress.
- Regional access coalition response depends on coalition investment, shared
  access commitment, community trust, reported access, and coalition leverage.
  This is a prototype abstraction for cooperative action under coordination
  pressure.
- Measurement delay, noise, and revisions enter through explicit resolved inputs
  and observations, preserving a deterministic transition core.

## Actor Incentives and Information

- Player health system: seeks access stabilization while preserving financial
  capacity, quality, workforce trust, community trust, and policy legitimacy.
- Commercial insurer: seeks affordable rates while preserving network access.
- State policy officials: seek credible access commitments and political
  defensibility under policy pressure.
- Nursing workforce representative: seeks credible retention and schedule relief
  under staffing stress.
- Regional provider coalition liaison: seeks credible shared access commitment
  and community legitimacy while managing coordination risk.
- Player and NPC decisions use reported observations and resolved inputs rather
  than omniscient true state.

## Assumptions

- Simple integer metrics are acceptable for the current architecture and
  concept-boundary proof.
- A hard-coded playable demo remains sufficient while Phase 2 vocabulary and
  scope are being stabilized.
- The system-boundary document should constrain scope before defining schemas,
  loaders, or parameter ledgers.
- Stable state fingerprints may be human-readable strings for now; no
  cryptographic hash is required yet.

## Unresolved Questions

- Which official data sources will parameterize payer mix, workforce pressure,
  hospital finance, access ranges, and policy context?
- How should future rulesets and scenarios be serialized and versioned?
- Which educational outcomes should be measured in the first playtest?
- Which actor objectives should be configurable in the first scenario?
- Which distributional outcomes must be first-class before external classroom
  use?

## Design Implications

- Keep all randomness and measurement artifacts outside the transition function.
- Preserve invalid-command validation separately from unfavorable modeled
  outcomes.
- Keep actor rationales and attributed effects available for debriefing and
  domain review.
- Document actor authority and information boundaries before adding new actor
  classes.
- Create a parameter ledger before replacing prototype thresholds with
  evidence-backed ranges.

## Risks

- False precision: prototype formulas must be labeled as abstractions.
- Premature frameworking: avoid loaders, plugin systems, and broad scenario
  schemas until repeated content requires them.
- Educational opacity: every strategic result should include an explanation.
- Scope drift: Phase 2 docs should not imply that deferred actors are already
  implemented strategic agents.
