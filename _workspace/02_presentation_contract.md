# Presentation Contract — Phase 1.1 art-direction reference board v0.12.35

## Goal and Authorization

Authorized slice: produce three source-only art-direction reference variants,
score them, select one for future rendering, and record rejected alternatives.
No selected variant is yet a shipped GUI asset or runtime semantic mapping.

## Player Questions and Consequences

The selected direction must make the future player question legible: where is a
visible institution, what facility/process/status is being discussed, and which
relationship deserves attention next. It must support compact executive density
without turning symbolic layout into true geography or hidden-state disclosure.

## Actor-Visible Source Ledger

| Reference element | Source authority | Missingness | Prohibited inference |
| --- | --- | --- | --- |
| Institution name/marker | Visible host or fixture identity | Generic label/token | No private rival identity |
| Facility/status labels | Visible host/fixture category and status | Generic marker/text | No client-derived severity |
| Relationship arrows/lines | Decorative reference vocabulary only | Omit if no visible relationship | No causal or geographic claim |
| Palette/shape treatment | Decorative style decision | Monochrome/text fallback | No color-only meaning |

## Visual, Motion, and Audio Semantics

Variant A uses a flat institutional panel/grid language and is the selected
direction. Variant B uses civic terrain/road motifs and is rejected because it
invites unsupported geography. Variant C uses editorial dashboard tiles and is
rejected because it weakens persistent spatial relationship cues. No motion or
audio is added in this slice.

## Accessibility and Fallbacks

Every SVG includes a title, description, visible labels, shapes, and a
`viewBox`. Meaning is repeated in text and shape, not color alone. Small-size
review uses the compact marker/group in each board; large-text review uses
ordinary text labels rather than rasterized text. Missing or unsupported SVG
rendering falls back to the existing text-first GUI; reduced motion has no
additional behavior because these are static references.

## Authority, History, and Replay Boundaries

The reference board is source/design material only. It does not enter browser
state, commands, transition evaluation, stochastic inputs, history, hashes,
replay, audio classification, or debrief output. Layout slots are not geography.

## Asset Provenance and Release Requirements

The three SVGs are hand-authored project-generated source references under
`assets/source/visual/art-direction/`, registered with hashes and no release
path. They use no external images, fonts, scripts, or network references. A
future release derivative requires a new approved registry entry and hash.

## Verification and Evidence Limits

Focused tests parse all SVGs, require accessibility text and viewBox/role
markers, reject external references and color-only content, and verify the
selection matrix and ADR. This is a technical design proxy, not a human color-
blind, screen-reader, contrast, usability, or art-direction study.

## Non-Goals and Open Questions

No renderer, browser integration, screenshot automation, facility geometry
library, audio motif, or production asset derivative is authorized. Phase 1.2
must prove deterministic SVG rendering with the selected vocabulary before
broader facility/map work.
