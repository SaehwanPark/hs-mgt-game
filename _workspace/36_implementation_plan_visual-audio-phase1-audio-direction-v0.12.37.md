# Implementation Plan — Phase 1.3 audio-direction prototype v0.12.37

## Objective

Close the standards and direction-definition portion of Phase 1.3 with a
fixture-only, keyboard-operable preview surface and machine-checkable recipes.

## Scope

- Add seven declarative generated Web Audio recipes.
- Document loudness, peak, duration, loop, ducking, and low-volume targets.
- Provide a static proof page with visible source/equivalent text and preview
  fallback when browser audio is unavailable.
- Check the first seven Phase 1.3 roadmap items.
- Keep priority scheduling, cooldowns, audio modes, and runtime integration out
  of this slice.

## Acceptance criteria

- Every prototype has a visible source, text equivalent, semantic role, and
  bounded recipe.
- Cues use distinct contour/pattern metadata and remain below the peak ceiling.
- Loopable entries fit the documented duration window.
- Environmental and pressure entries cannot claim hidden state in source text.
- Unsupported audio returns a visual-only result.
- Registry hash, credits, roadmap, SPEC, architecture, changelog, LESSONS, and
  handoff records align to v0.12.37.

## Verification

- `python3 -m unittest tests.test_audio_direction`
- `python3 scripts/validate_assets.py`
- `python3 scripts/generate_asset_credits.py --check`
- Full Python, Rust, Clippy, formatting, Node, metadata, documentation-link,
  and diff checks before PR handoff.
