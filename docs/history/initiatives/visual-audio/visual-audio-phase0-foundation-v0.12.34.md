# Visual/audio Phase 0 — Product brief and asset foundation

**Status:** Implemented, verified, reviewed once, and merged in PR-equivalent
**Scope:** Product brief, asset repository architecture, provenance validation,
and generated credits for the browser presentation track
**Version:** 0.12.34

## Product brief

The presentation direction is a restrained flat-vector, oblique/isometric
executive simulation. It uses compact institutional panels, a schematic
regional board, reusable facility and status tokens, and visible consequence
links. The experience remains serious and information-dense; decorative
richness is subordinate to actor-visible strategic relationships.

The first production slice remains one month of `competitive-regional-v1`:
inspect the market and Riverside, identify a visible bottleneck, choose two
host-shaped actions, submit through the existing boundary, review the committed
resolution, and continue. The browser does not become a second simulation.

### Supported presentation targets

- Baseline review: 1280×720 or larger desktop/laptop viewport.
- Supported narrow desktop: 1024×768 and CSS widths down to 760px using the
  existing responsive layout.
- Large text target: the existing local Large setting at 112.5% root size.
- Mobile, immersive 3-D, and device-specific performance promises are not part
  of this foundation slice.

### Audio direction

Audio is restrained, optional, and hybrid: generated Web Audio recipes provide
short UI/event cues and visible-state music moods; later approved recordings
may supplement them. Audio cannot be the sole signal for pressure, success,
uncertainty, or hidden information. Mute, reduced notifications, and complete
written equivalents remain mandatory.

### Motion and accessibility

Reduced motion removes non-essential transitions and permits immediate review
of committed resolution text. Keyboard navigation, focus visibility, readable
text scaling, non-color status symbols, and text equivalents are part of the
semantic contract. A missing asset, unsupported audio capability, or interrupted
load falls back to the existing text/status surface without changing state.

### Licensing and AI-generation policy

The allowlist is `project-generated`, `CC0-1.0`, `CC-BY-4.0`, `CC-BY-SA-4.0`,
`MIT`, `Apache-2.0`, `GPL-3.0-or-later`, and `OFL-1.1`, subject to the asset's
actual terms and attribution requirements. The denylist includes unclear or
unverified rights, personal-use-only, non-commercial-only, redistribution-
hostile, all-rights-reserved, and proprietary game assets or close imitations.

AI-generated assets may be used only when the model/license, prompt, seed or
equivalent determinism record, source output, post-processing, hashes, and
human review are recorded. Generation cannot imitate a real person, institution,
trademark, or proprietary game asset. Generated runtime glyphs and audio
recipes are approved as project-generated sources and remain registered.

### Ownership and authority

The contributor supplies source and metadata; the visual/audio maintainer
checks semantic role, accessibility fallback, and provenance; the PR reviewer
checks repository integrity; the project maintainer approves release use. The
Rust host remains authoritative for observations, commands, outcomes, history,
replay, and hashes. The browser owns only presentation, playback, and local
preferences.

## Asset repository architecture

```text
assets/
  source/      original or editable inputs
  generated/   preserved generated outputs and metadata
  release/     approved distributable derivatives
  registry/    machine-readable manifests and schemas
  tools/       asset-specific tooling notes
```

`scripts/validate_assets.py` is the dependency-free gate. It validates unique
IDs, known semantic roles, source/generation metadata, license policy,
approval, source/release hashes, and release-file registry coverage. The
registry intentionally permits runtime-generated recipes without a release
file while requiring their generation method and source path.

`scripts/generate_asset_credits.py` renders the checked-in
`assets/ASSET_CREDITS.md` from both registries. CI runs validation and the
credits freshness check. No third-party asset is introduced by this slice.

## Evidence limits and next gate

The foundation establishes governance and technical checks, not artistic
quality, human usability, lived accessibility, audio hardware behavior,
license counsel, or educational effectiveness. Phase 1 art-direction and
rendering prototypes remain the next bounded production candidates.
