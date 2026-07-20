# Presentation Contract — Phase 4.2 visible consequence linkage v0.12.65

## Goal and authorization

Make the static board traceable to visible reports and host-committed
resolution/projection data without creating a client-side causal or simulation
model.

## Link source ledger

| Link | Source | Allowed presentation |
| --- | --- | --- |
| Public signal → entity | `RegionalWorldEntity.signals[].observed_month/source` | Focus entity and show public signal timing |
| Visible process → entity | `RegionalWorldEntity.processes[].source` | Focus entity and show host-reported process detail |
| Report → entity | Explicit fixture/host-visible `target_id` or visible name match | Local board focus; no hidden target inference |
| Resolution effect | `ResolutionEnvelope.effects[].metric/delta/text/source` | Show committed effect; target remains absent unless host supplies it |
| Replay sequence | `ResolutionEnvelope.turn/replay.selected_turn/replay.state_hash` | Immutable local historical review sequence |
| Entity → reports | Local selected entity ID and explicit report target IDs | Filter/relate visible reports only |

## Visual and interaction contract

- `gui/consequence-links.mjs` emits stable `public-signal`, `visible-process`,
  and `committed-effect` links. Regional links retain observed month and
  source; effects retain turn and state hash. Stable sorting uses turn, target,
  kind, source, and ID fields.
- Resolution effects without a host-provided `target_id` remain targetless;
  the UI shows them but offers no invented board focus.
- `gui/app.mjs` renders a linked-consequence list, report “View on regional
  board” controls, and selected-detail “Show related reports and consequences.”
  Each focus action updates the existing local selection and semantic detail
  path. Focus scrolling uses `behavior: "auto"`; selection does not depend on
  animation.
- Regional public signals retain observed month text and the private-rival
  boundary. Unknown IDs remain generic or targetless and never become hidden
  locations or inferred facilities.

## Accessibility and fallback requirements

- Consequence links are semantic list items with visible labels, detail, source,
  and ordinary keyboard buttons.
- The existing report, map, detail, resolution, history, and text surfaces stay
  in the DOM; linked controls add navigation but do not replace text.
- Missing detail and targetless effects remain explicit. Color, motion, and
  optional audio are not required to understand the link.

## Authority, history, and replay boundaries

The link module accepts envelope values only. It does not call a host, submit a
command, mutate simulation state, resolve stochastic inputs, rewrite history,
change a state hash, or create debrief facts. `replayConsequenceSequence`
returns distinct immutable turn/hash entries; historical review does not
overwrite the current board or host session.

## Asset provenance and verification

`visual.runtime-consequence-links` is a project-generated registry-approved
semantic asset with source hash, visible-source description, accessible
equivalent, and no release image. Focused consequence-link tests, existing GUI
resolution/first-month/regional tests, asset/credits/metadata/documentation
checks, full Python/Rust, formatting, presentation-contract, and diff checks
are required before handoff.

## Non-goals and next gate

This slice does not add new host target fields, facility geometry transitions,
client-side causality, private rival actions, or a browser replay engine. Later
roadmap phases own executive information containers, metric visualization,
motion, audio, and broader testing/QA.
