# Mechanism Design

## Goal and Roadmap Phase

Expand the Phase 2 conceptual boundary for the current fictional regional US
market prototype while preserving the existing deterministic CLI demo unchanged.

## Slice Boundary

Included:

- One player-controlled nonprofit health system.
- Existing commercial insurer, state policy, nursing workforce, and regional
  provider coalition interactions as documented concepts.
- Actor authority and information boundaries.
- Current true-state, observation, command, event, effect, replay, and debrief
  vocabulary.
- Explicit documentation of prototype formulas as abstractions.
- Deferred ontology work needed before scenario loading or calibration.

Excluded:

- Runtime behavior changes.
- New commands, actors, state fields, or random streams.
- Full campaign.
- General command parser.
- Persistent save files.
- Scenario data loader.
- Empirical calibration.
- General instructor reporting framework.
- New Cargo dependencies.

## Documentation Changes

- `docs/system-boundary.md` becomes the primary Phase 2 boundary artifact.
- `docs/evidence-registry.md` records current mechanism status and unresolved
  evidence questions without turning into a calibration ledger.
- `SPEC.md` records coalition work as complete and this Phase 2 slice as active.
- Workspace artifacts preserve the handoff so future implementation can continue
  without reconstructing the design context from chat history.

## Actors and Authority

- Health system CEO: may allocate health-system resources and make commitments
  through the current command vocabulary.
- Commercial insurer: may accept, counter, or reject a requested rate path.
- State policy officials: may grant flexibility, continue the mandate, or
  escalate oversight.
- Nursing workforce representative: may cooperate, offer limited support, or
  signal a work action.
- Regional provider coalition liaison: may accept full partnership, offer
  limited participation, or withdraw from the coalition.
- Deferred actors should not become strategic agents until a future slice defines
  their authority, information, objectives, and decision procedure.

## State, Beliefs, and Observations

- True state tracks cash, staffed beds, access, quality, workforce trust,
  community trust, commercial rate, and policy pressure.
- Player observation reports delayed/noisy access, current quality, policy
  briefing, and later prior-period access revisions.
- Later revisions are new observations rather than mutations of committed
  history.
- Actor decisions should remain based on actor-visible observations and resolved
  inputs.

## Causal and Evidence Boundaries

- Current causal categories are financial capacity, access capacity, workforce
  legitimacy, community legitimacy, policy pressure, and measurement/revision.
- Current formulas are inspectable design abstractions.
- Official data selection, parameter ranges, and balancing choices remain
  deferred to a future parameter-source ledger.

## Determinism and Replay Notes

- This slice must not change `transition()`, `resolve_inputs()`, or CLI behavior.
- Existing resolved inputs remain computed outside the transition core and
  committed into history.
- Existing tests and default demo output serve as regression checks for this
  documentation-only slice.

## Open Questions

- Which actor-card template should become canonical once a new actor is added?
- Which official data sources should anchor first parameter ranges?
- Which distributional outcomes must be promoted into true state before external
  classroom use?
- Whether future state fingerprints should use a cryptographic hash.
