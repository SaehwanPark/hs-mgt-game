# Presentation Contract — Phase 3.2 event markers v0.12.62

## Goal and Authorization

Complete the remaining fixture-only Phase 3.2 map/environment vocabulary with
event markers and a small interaction proof. The proof is authorized to show
the shared symbolic map tokens and local viewport controls; it is not
authorized to enter the live GUI or create a browser simulation model.

## Player Questions and Consequences

- What visible category does this event marker represent?
- Can the player reach every map item in a predictable keyboard order?
- Can the player inspect the symbolic board at supported viewport sizes?
- Can zoom and pan change only the local presentation viewport?
- What remains visible if a marker ID or interaction value is unavailable?

## Actor-Visible Source Ledger

| Element | Visible source | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| Event marker | Fixture-provided visible event category | Severity, urgency, causality, intent, resolution, or future outcome | Marker label, glyph, shape, and text card |
| Marker fallback | Unknown event-marker ID | Guessed event class or importance | Generic marker label and outlined token |
| Map position | Fixture symbolic grid coordinate | Real distance, geography, travel time, ownership, or jurisdiction | Named column/row coordinate |
| Zoom | Local proof control | More detail, certainty, or strategic importance | Current zoom text and bounded step label |
| Pan | Local proof control | Movement, distance, reach, or access | Current bounded x/y offset text |

## Visual, Motion, and Audio Semantics

- Event markers use stable shapes, glyphs, and text labels; color is optional
  and never the sole channel.
- Marker metadata explicitly sets severity and priority encoding to `none`.
- Event markers are static in this slice. Reduced motion uses the same static
  marker and text treatment.
- Zoom is limited to declared fixture steps. Pan is limited to declared local
  offsets. Neither control changes map facts or host state.
- The proof preserves a fixed document/keyboard order: heading, return link,
  viewport, zoom controls, pan controls, each marker card, then each target-size
  legend card.

## Accessibility and Fallbacks

- Every marker has a written equivalent and a non-color pattern.
- The proof uses semantic headings, landmarks, buttons, keyboard-focusable
  marker/legend cards, visible current-state text, and focus-visible styling.
- Compact, standard, and wide CSS layouts retain labels without requiring
  horizontal scrolling in the proof surface.
- Unknown marker IDs use `event-marker-generic`; invalid zoom or pan values are
  clamped to declared defaults/bounds.
- Reduced-motion media rules remove any optional viewport transition.

## Authority, History, and Replay Boundaries

The event catalog and proof consume only fixture data. Local selection, zoom,
and pan are reversible presentation state. They do not submit commands, call a
host, alter transition evaluation, stochastic inputs, history, state hashes,
replay artifacts, audio state, or debrief output.

## Asset Provenance and Release Requirements

The event-marker catalog is a hand-authored project-generated semantic asset
with a registry entry, source hash, accessible equivalent, visible source,
modification note, and approved status. It has no external or generated image
file and therefore no release derivative.

## Verification and Evidence Limits

Focused tests must cover all marker categories, deterministic fallback,
no-severity semantics, no-motion semantics, keyboard order, target viewport
metadata, zoom/pan bounds, registry hash/provenance, and JavaScript syntax.
These checks are technical evidence only; they do not substitute for human
design, contrast, lived accessibility, learning, or live-browser evaluation.

## Non-Goals and Open Questions

- Do not promote the proof into `gui/index.html` or the live host adapter.
- Do not interpret markers as operational events, causal effects, severity,
  or hidden rival activity.
- Do not add audio or animation in this slice.
- Future board integration must map marker meaning from an actor-visible host
  field before using the catalog outside fixtures.
