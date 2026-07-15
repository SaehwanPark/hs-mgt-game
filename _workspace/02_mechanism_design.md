# Mechanism Design — Visual/audio Phase 12 visual identity and marker provenance v0.12.28

## Goal and Roadmap Phase

Complete the smallest remaining visual-language/asset-contract slice needed to
make the existing competitive first-month regional world readable after the
Phase 11 launch/load handoff. This is presentation-layer Phase 12 work; no
simulation mechanism changes.

## Slice Boundary

- Campaign surfaces: existing competitive regional map and its selected entity,
  facility, overlay, and visible process rows.
- System identities: Riverside, Northlake, Summit, plus an explicit generic
  institution fallback.
- Markers: facility, demand, capacity, project, staffing, payer/policy, and
  timeline, plus generic visible information fallback.
- Status: existing stable/watch/constrained/critical/improving/uncertain/
  delayed/revised/reported vocabulary is catalogued but not recalculated.
- Asset policy: generated text/glyph/CSS tokens only; no external files.

## Actors and Authority

- The executive uses tokens for orientation and progressive disclosure.
- The browser owns only presentation rendering and local selection state.
- The host/MCP projection owns entity identity facts, facility facts, metric
  values, status values, process values, source labels, and missingness.
- The visual catalog owns no actor utility, payoff, constraint, or strategy.

## State, Beliefs, and Observations

- True state, private rival operations, stochastic inputs, effect queues, and
  hidden coordinates remain unavailable.
- Identity mapping reads only exact visible IDs or conservative visible names;
  marker mapping reads visible kind/label/category strings.
- A missing/unknown value renders the generic token and a visible source or
  unavailable label. No token implies a hidden value.
- Catalog selection is deterministic and does not enter commands, transitions,
  history, hashes, replay, or debrief output.

## Commands, Events, and Effects

- No commands, events, or effects are added.
- Map selection continues to change only local presentation selection.
- Existing host-provided statuses, source labels, and metrics remain unchanged.
- Registry/credits files document generated presentation primitives only.

## Strategic Interaction

There is no new strategic interaction. The visual system supports recognition of
existing owned and public systems and their visible pressures without changing
the information available to any actor.

## Assumptions and Parameters

- Known system IDs are `riverside`, `northlake`, and `summit`.
- Each catalog entry has a stable ID, visible label, symbol, token class,
  source/equivalent description, generated ownership, and approval status.
- Unknown IDs, empty kinds, and unsupported categories use `generic`.

## Educational Debrief Hooks

- No new debrief claim is introduced. The visual token may make an existing
  source/equivalent easier to locate, while causal attribution and learning
  remain host-provided and separately unevaluated.

## Determinism and Replay Notes

- Lookup is a pure deterministic function of visible input text.
- Rendering and registry metadata are outside the Rust core and cannot alter
  state hashes or replay artifacts.
- Replaying a host envelope regenerates the same visual tokens for the same
  visible IDs/categories, including generic fallback.

## Open Questions

- A later campaign-specific visual identity layer may need a host-provided
  campaign namespace; this phase intentionally does not introduce one.
- Licensed/recorded assets, SVG production, and visual human evaluation remain
  future gates.
