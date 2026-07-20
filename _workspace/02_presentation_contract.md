# Presentation Contract — Phase 2.1 Riverside identity v0.12.39

## Goal and Authorization

Make fictional Riverside recognizable across required presentation surfaces.
The roadmap authorizes one source/release kit and fixture proof; it does not
authorize live host/render integration or real-world brand resemblance.

## Player Questions and Consequences

- Which recurring system is involved?
- Can I recognize it in a map marker, facility sign, report header, compact
  badge, or audio motif without relying on color?
- What should appear when identity data or the asset is unavailable?

## Actor-Visible Source Ledger

| Surface | Visible source | Prohibited inference | Equivalent |
| --- | --- | --- | --- |
| Riverside identity | Visible system ID/name | True-world affiliation or reputation | Name, mark, monogram |
| Facility/report surfaces | Visible Riverside ownership/source | Hidden facility condition | Sign/header label |
| Audio motif | Visible Riverside identity | Hidden system state | Name, marker, header |
| Missing identity | Missing/unknown visible ID | Guessed actor or real brand | Generic Institution fallback |

## Visual, Motion, and Audio Semantics

- The R silhouette, river-line shape, circular marker, and RV monogram persist
  in color and monochrome.
- Palette is a token, not the sole identity channel.
- Facility signage, report header, and compact badge retain the same mark and
  visible name.
- The existing `audio.direction-riverside-motif` is a visible-identity cue.

## Accessibility and Fallbacks

- Source/release SVGs include title/description and system-ui text.
- The proof shows name, monogram, surface labels, and generic fallback text.
- Unknown IDs use `generic-institution`; missing asset/audio does not erase the
  visible identity label.

## Authority, History, and Replay Boundaries

`identity-kits.mjs` reads only local fixture IDs and labels. It does not load
host DTOs, infer ownership, submit commands, create session state, or alter
transitions, history, hashes, replay, audio state, or debrief output.

## Asset Provenance and Release Requirements

The source kit and release derivative are registry entries with creator,
generation method, project-generated license, modifications, accessible
equivalent, visible source, approval, and source/release hashes. No external
font, URL, or third-party brand is used.

## Verification and Evidence Limits

Focused tests cover SVG labels/variants, asset boundary, identity surfaces,
generic fallback, audio motif linkage, and syntax. These checks do not establish
human art direction, contrast, accessibility experience, learning, or policy
validity.

## Non-Goals and Open Questions

Do not integrate the kit into live map/report/facility rendering, add Northlake
or Summit assets, claim real-world branding, or generate human-evaluation
evidence in this slice.
