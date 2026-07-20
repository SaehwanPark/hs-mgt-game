# Presentation Contract — Phase 1.2 SVG rendering proof v0.12.36

## Goal and Authorization

Authorized slice: implement a fixture-only, deterministic SVG scene model and
renderer using the accepted Variant A vocabulary. The proof page may expose
local selection and reduced-motion controls but may not load or mutate a host.

## Player Questions and Consequences

The proof demonstrates that a player can identify a visible institution,
select a facility, distinguish reported/uncertain/constrained status, and
recover when identity or facility data is unavailable.

## Actor-Visible Source Ledger

| Scene field | Source | Unknown behavior | Client prohibition |
| --- | --- | --- | --- |
| `id`, `name`, `role`, `summary` | Fixture-visible projection | Generic institution label | No private actor inference |
| `status` | Visible status language | Uncertain `?` pattern | No severity formula |
| `facility.kind`, `marker`, `label` | Visible facility/category | Generic marker `•` | No client category engine beyond vocabulary lookup |
| Layout position | Static design slot | Omit/empty state | Not geography or distance |

## Visual, Motion, and Audio Semantics

The renderer uses stable cards, labels, symbols, flat fills, and dashed
uncertainty/delay outlines. The proof has no animation or audio. `data-motion`
records the local reduced-motion choice and never enters a host payload.

## Accessibility and Fallbacks

SVG root title/description, visible text, symbols, `role="button"`, `tabindex=0`,
and keyboard event handling keep the proof operable without color or audio.
Unknown institutions/facilities/statuses use explicit generic/uncertain text.
If SVG is unsupported, the proof page's text fallback explains the same limits.

## Authority, History, and Replay Boundaries

`gui/scene.mjs` consumes only a fixture-shaped visible scene. It does not own
true state, parse commands, resolve outcomes, call the network, or write
history, hashes, replay, audio classification, or debrief data. The proof page
is not part of the live host route.

## Asset Provenance and Release Requirements

The renderer is registered as a project-generated source reference with a
current hash and no release derivative. It uses no external images, fonts,
scripts, or network references. Any future live integration or release asset
requires a new bounded proposal and registry update.

## Verification and Evidence Limits

Node/Python tests assert deterministic SVG snapshot output, keyboard markers,
uncertainty patterns, fallbacks, reduced-motion output, no forbidden authority
markers, and a 500-render local performance target. These are technical proxies,
not human usability, screen-reader, contrast, or lived-accessibility evidence.

## Non-Goals and Open Questions

No live client integration, screenshot capture/upload, facility geometry system,
true geography, animation timeline, or audio cue mapping is included. Phase 1.3
audio direction is a separate slice.
