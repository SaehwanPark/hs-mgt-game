# Presentation Contract — Phase 4.1 static regional board v0.12.64

## Goal and authorization

Promote the proven identity, facility, status, map, and overlay vocabulary into
the first static board integration. The board consumes only the existing typed
actor-visible `competitive-regional-world-v1` envelope or the equivalent static
presentation fixture.

## DTO-to-scene source ledger

| Scene field | Actor-visible source | Boundary |
| --- | --- | --- |
| Institution identity/name/role | `RegionalWorldEntity.id`, `.name`, `.role`, `.visibility` | No hidden identity, role, or private detail |
| Institution status | `RegionalWorldEntity.status` | Text/symbol status only; no client severity |
| Institution ordering | `RegionalWorldEntity.layout_slot`, then stable ID | Local layout order; not geography or importance |
| Facility label/kind | `RegionalWorldFacility.name`, `.kind` | Generic facility fallback for unknown kind |
| Overlay label/value/unit | `RegionalWorldOverlay` | Visible source-linked value only |
| Source labels | Entity/facility/overlay/missing `.source` | Source remains visible beside the interpretation |
| Missingness | `RegionalWorldMissing.id`, `.label`, `.detail`, `.source` | Unavailable detail is shown, not inferred |
| Report focus | Existing fixture briefing `.target_id` | Local focus/navigation only; no transition |

## Visual and interaction contract

- `gui/regional-board.mjs` is a pure, deterministic adapter. It normalizes
  missing or unknown IDs and preserves visible fields without deriving hidden
  severity, geography, causality, intent, probability, or future outcome.
- `gui/scene.mjs` renders the mapped entities, facilities, status text, source
  text, and up to four visible overlay cards with an explicit overflow count.
- `gui/app.mjs` mounts the SVG beside the existing semantic map/list/detail
  surface. Entity and facility SVG controls focus the owning institution; the
  existing detail panel remains the semantic fallback and selection source.
- Visible report target buttons call the same local selection path as board
  cards. No selection state enters the host or simulation.
- The board is static under reduced motion. Glyphs, labels, status text, source
  text, focus rings, and missingness remain available without color, motion, or
  audio.

## Accessibility and fallback requirements

- Screen-reader order is heading/navigation, graphical board, semantic entity
  list, overlay list, then selected detail; the semantic list/detail remains
  available when SVG is unavailable.
- SVG entity/facility controls are keyboard reachable with Enter/Space handling
  and visible focus rings. The static proof repeats this contract.
- Unknown institution IDs use the generic identity token; unknown facility kinds
  use the generic marker. Missing detail is rendered as explicit text.
- The deterministic snapshot fixture protects output changes without claiming
  human usability or screenshot-based design validation.

## Authority, history, and replay boundaries

The adapter and renderer accept DTO/fixture values only. They do not call a
host, submit commands, mutate simulation state, resolve stochastic inputs,
write history, compute hashes, alter replay, drive audio, or create debrief
facts. Live DTO authority remains in `src/mcp/regional_world.rs`.

## Asset provenance and verification

`visual.runtime-regional-board-adapter` and the updated SVG scene renderer are
project-generated, registry-approved semantic assets with source hashes and
written equivalents. Focused adapter/snapshot tests, existing GUI tests, asset
validation, credits, metadata, syntax, Rust, Python, documentation-link, and
presentation-contract checks are required before handoff.

## Non-goals and next gate

This slice does not implement consequence linkage, project-state transitions,
rival observability timing, replay visual sequencing, or first-month integration
tests. Those remain Phase 4.2. It does not replace the host with a browser
simulation or assert real geography, distance, travel time, ownership,
jurisdiction, or performance.
