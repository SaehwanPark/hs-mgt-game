# ADR-0013: Fixture-only audio direction prototype

- Status: Accepted
- Date: 2026-07-20
- Scope: Phase 1.3 audio-direction prototype

## Context

The browser already has generated oscillator recipes, but the current catalog
does not distinguish the direction of confirmation, rejection, report arrival,
institutional identity, neutral ambience, visible pressure, and environmental
texture. The roadmap calls for a hybrid audio direction while preserving the
visual/text-first interface and actor-visible boundary.

## Decision

Add a dependency-free, fixture-only audio-direction board with declarative
Web Audio recipes and explicit engineering targets. The proof page may preview
recipes after a user gesture, but it does not load a host, create simulation
state, classify hidden conditions, or replace the live audio client.

The initial vocabulary uses distinct interval/contour patterns for cues and
low-level generated noise for non-semantic beds. All entries carry a visible
source and text equivalent. Pressure audio is authorized only by visible
pressure categories.

## Consequences

- Contributors can compare a bounded vocabulary before runtime integration.
- Generated recipes avoid third-party licensing and network dependencies.
- Loudness, peak, duration, and loop targets are explicit and testable.
- Human listening, hardware calibration, priority scheduling, and user
  preference behavior remain open gates.
- The existing live GUI audio catalog and host/simulation contracts remain
  unchanged in this slice.
