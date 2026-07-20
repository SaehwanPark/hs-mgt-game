# ADR-0012: Select the institutional flat visual direction

**Status:** Accepted for Phase 1.2 technical rendering proof
**Date:** 2026-07-20
**Decision owners:** Project maintainer and visual/audio contributor

## Context

The visual/audio roadmap requires a coherent style before facility and regional
assets are produced. The current browser surface is a thin client over
actor-visible projections, so the style must provide spatial and institutional
legibility without implying true geography, hidden state, or a second game
engine.

## Decision

Use the flat institutional direction in Variant A of the v0.12.35 reference
board as the default visual vocabulary for the next SVG rendering proof:

- compact institutional cards with stable labels and symbols;
- an oblique/schematic relationship board rather than true geographic mapping;
- restrained flat fills, lines, and shapes with text-first status language;
- reusable facility, process, and pressure marker primitives; and
- progressive disclosure from regional context to entity/facility detail.

Native SVG remains the source/reference format. This decision does not authorize
runtime integration or production release derivatives.

## Alternatives considered

- Variant B, civic terrain: rejected because roads, districts, and terrain
  suggest unsupported geography, routing, and distance semantics.
- Variant C, editorial desktop: rejected because it reads as a dashboard and
  weakens persistent place and relationship cues, despite low implementation
  risk.
- Photorealistic or proprietary-game imitation: rejected by the product brief,
  licensing policy, and accessibility/fallback contract.

## Consequences

Positive:

- The next renderer can reuse stable institution, facility, status, and process
  primitives while keeping source labels visible.
- Text, symbols, and shape make meaning survive color loss, mute, and reduced
  motion.
- The direction is compatible with the existing actor-visible presentation
  boundary and does not require a new dependency.

Costs and limits:

- The board is schematic, not a geographic model; layout slots need explicit
  disclaimers.
- Artistic quality and human accessibility still require later evaluation.
- Large asset production and facility detail remain future bounded slices.
