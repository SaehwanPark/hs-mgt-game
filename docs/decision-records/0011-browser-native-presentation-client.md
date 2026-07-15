# ADR-0011: Browser-Native Presentation Client and Host Authority

**Status:** Accepted
**Date:** 2026-07-14
**Deciders:** Project maintainer and implementation agent

## Context

The visual/audio proposal needs a first technology choice without creating a
second simulation engine. The repository already contains a dependency-free
browser proof that renders injected MCP-shaped data and delegates submission
through `HsMgtGameAdapter`. The Rust engine owns deterministic transitions,
resolved stochastic inputs, actor observations, immutable history, replay hashes,
and debriefs.

## Decision

Use browser-native HTML, CSS, JavaScript ES modules, and native SVG as the first
presentation stack. Keep the client non-authoritative and connect it to the
existing host/MCP boundary. The client may own navigation, selection, draft
batches, viewport state, animation progress, and local accessibility/audio
preferences. The host remains authoritative for observations, command legality,
stochastic resolution, transitions, history, hashes, and debriefs.

Audio playback may later use the browser Web Audio API, but cue classification
must remain a deterministic presentation mapping testable without loading or
playing assets. No framework, bundler, remote asset service, networked core, or
deployment convention is introduced by this decision.

## Consequences

### Positive

- The first static desktop can reuse the existing thin-client proof without a
  dependency or a competing state model.
- Semantic HTML and SVG provide a direct path to labels, keyboard operation,
  status text, and color-independent presentation.
- Native browser audio can remain optional and outside simulation history.
- CLI, MCP, and future graphical actions can share the same canonical commands
  and validation path.

### Negative / tradeoffs

- Current MCP output is partly string-based, so later live integration needs a
  typed, actor-visible adapter contract rather than direct world serialization.
- Browser rendering and audio behavior still require phase-specific verification
  across viewport, focus, reduced-motion, mute, and missing-asset conditions.
- A later need for richer tooling may justify a framework or bundler, but that is
  a new decision and must be supported by a concrete evidence gap.

## Alternatives considered

| Alternative | Why not chosen |
| --- | --- |
| Browser framework and bundler first | Adds dependencies and build conventions before the static information architecture is validated. |
| Canvas-first renderer | Makes semantic labels and accessibility harder for the schematic first slice. |
| GUI-owned simulation model | Duplicates formulas, risks hidden-state leakage, and breaks replay/hash authority. |
| Networked service first | Adds hosting, authentication, and session concerns before local presentation value is proven. |
| Audio in the Rust core | Couples playback/assets to deterministic simulation and can change replay semantics. |

## Follow-ups

- Phase 1 should test the static desktop using injected actor-visible fixtures.
- Phase 2 must inventory and, only where necessary, promote structured adapter
  projections for the first-month surfaces.
- Phase 5 must add the audio registry, credits, controls, fallback behavior, and
  recording-sink tests without changing hashes or histories.
