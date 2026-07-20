# Implementation Plan — Visual/audio Phase 1.1 art direction v0.12.35

## Task restatement

Produce three source-only visual direction references, compare them against the
project's presentation/authority/accessibility constraints, select one, and
record the decision before building a renderer or production asset kit.

## Minimal implementation plan

1. Create three well-formed, labeled SVG reference boards: institutional flat,
   civic terrain, and editorial desktop.
2. Record scores, color-independent/small-size/large-text checks, selection, and
   rejected-style reasons in a design board and ADR.
3. Register source references with hashes and deterministic credits.
4. Add focused XML/static contract tests and align roadmap/SDD/handoff docs.

## Acceptance criteria

- All Phase 1.1 checklist items have committed evidence.
- Variant A is selected without implying true geography or hidden state.
- SVG references have titles, descriptions, labels, stable viewBoxes, no
  external references, and no runtime authority path.
- Existing GUI, host, simulation, history, replay, audio, and debrief behavior
  remain unchanged.

## Non-goals and stop conditions

No runtime renderer, facility library, map integration, animation, audio
production, third-party asset, new dependency, or human design/accessibility
claim. Stop if a visual decision requires a new host field or client inference.
