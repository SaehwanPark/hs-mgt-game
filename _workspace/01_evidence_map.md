# Evidence Map

## Scope

Map enough project evidence to justify the first deterministic architecture
proof: a small scripted turn involving a nonprofit health system, commercial
insurer response, capacity pressure, reported observations, and debriefable
effects.

## Sources Reviewed

- Canonical project docs establish deterministic transitions, true-state versus
  observation separation, strategic actor response, visible assumptions, and
  narrow vertical slices before frameworks.
- `docs/phase1-lit-review.md` identifies the need for an evidence spine,
  explicit mechanism registers, official data ledgers, and educational debrief
  design before broad calibration.

## Mechanisms and Institutions

- Capacity investment affects staffed beds, cash, access, and workforce trust.
  This is a project-doc-backed abstraction, not an empirically calibrated
  formula.
- Commercial payer response depends on reported access and requested rate. This
  is a design abstraction for payer-provider bargaining that demonstrates local
  strategic interaction without solving a global game.
- Policy pressure is modeled as an explicit resolved input. It is not generated
  inside the core transition.
- Measurement delay/noise enters through explicit resolved inputs, preserving a
  deterministic transition core.

## Actor Incentives and Information

- Player health system: seeks access stabilization while preserving financial
  capacity, quality, workforce trust, community trust, and policy legitimacy.
- Commercial insurer: seeks affordable rates while preserving network access.
- State policy environment: represented only as a pressure signal for this
  prototype, not as a complete lifecycle.
- Player observations use reported access and quality rather than omniscient
  true state.

## Assumptions

- Simple integer metrics are acceptable for the first proof of deterministic
  state movement.
- A scripted demo is sufficient to replace the placeholder CLI at this phase.
- Stable state fingerprints may be human-readable strings for now; no
  cryptographic hash is required yet.

## Unresolved Questions

- Which official data sources will parameterize payer mix, workforce pressure,
  hospital finance, and access ranges?
- How should future rulesets and scenarios be serialized and versioned?
- Which educational outcomes should be measured in the first playtest?

## Design Implications

- Keep all randomness and measurement artifacts outside the transition function.
- Preserve invalid-command validation separately from unfavorable modeled
  outcomes.
- Emit events, effects, and actor rationales so later debriefing can explain
  why outcomes occurred.

## Risks

- False precision: prototype formulas must be labeled as abstractions.
- Premature frameworking: avoid loaders, plugin systems, and broad scenario
  schemas until the first slice proves value.
- Educational opacity: every strategic result should include an explanation.
