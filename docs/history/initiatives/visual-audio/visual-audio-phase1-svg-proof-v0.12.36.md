# Visual/audio Phase 1.2 — SVG rendering proof

**Status:** Implemented, verified, reviewed once, and merged in PR-equivalent
**Scope:** Fixture-only scene model, deterministic SVG renderer, keyboard proof
page, fallbacks, and regression/performance checks
**Version:** 0.12.36

## Result

`gui/scene.mjs` defines a narrow visible scene model and renders the selected
flat institutional vocabulary as deterministic SVG. `gui/svg-proof.html` makes
institution and facility selection reachable by keyboard and exposes a local
reduced-motion control. The page is fixture-only and does not call the live
adapter or create simulation state.

## Contract coverage

- Scene model uses only visible identity, role, summary, status, facility, and
  marker fields; unknown values use generic identity/marker or uncertain status.
- SVG cards and facilities use text, symbols, labels, `role="button"`, and
  `tabindex="0"`; uncertainty/delay uses a dashed outline and `?`/`…` symbol.
- Root title/description, `viewBox`, responsive proof-page styling, and text
  fallback are present. No meaning depends on color, motion, or audio.
- Fixture output has a stable SHA-256 snapshot and the 500-render local proof
  target passes.
- Existing `gui/index.html`, host adapters, simulation, commands, history,
  hashes, replay, audio, and debriefs remain unchanged.

## Evidence limits

The checks are static/technical rendering proxies. They do not establish real
browser viewport behavior, contrast, screen-reader behavior, human usability,
lived accessibility, artistic quality, learning, calibration, balance, or policy
validity. Layout slots remain schematic and are not true geography.

## Next gate

Phase 1.3 is the separate audio-direction prototype. Broader facility and map
production remains gated by the selected vocabulary and later asset contracts.
