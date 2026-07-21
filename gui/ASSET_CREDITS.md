# Generated audio credits

The project ships no third-party audio files. The seven music states/five-stem
recipes, seven environmental ambience recipes, and sixteen interface/event cue
recipes are generated at runtime by [`audio.mjs`](audio.mjs),
[`music-stem-contract.mjs`](music-stem-contract.mjs), and
[`ambience-contract.mjs`](ambience-contract.mjs) with the Web Audio API.

| Registry | Source | Ownership/license | Status |
| --- | --- | --- | --- |
| [`audio-catalog.json`](audio-catalog.json) | `gui/audio.mjs`, `gui/music-stem-contract.mjs`, and `gui/ambience-contract.mjs` generated recipes | Project-generated; no third-party asset | Approved for the Phase 7.3 technical slice |

Any future replacement with recorded or licensed files must add retrieval date,
source URL, hashes, license URL, attribution, modifications, and approval to the
registry before entering the release tree.

# Phase 12 visual credits

Phase 12 ships no third-party visual files, external fonts, or downloadable
images. Identity and marker tokens use project-authored text glyphs and CSS
classes from [`visual.mjs`](visual.mjs); the machine-readable registry is
[`visual-catalog.json`](visual-catalog.json).

| Registry | Source | Ownership/license | Status |
| --- | --- | --- | --- |
| [`visual-catalog.json`](visual-catalog.json) | `gui/visual.mjs` glyph and token definitions | Project-generated; no third-party asset | Approved for the Phase 12 technical slice |

The catalog is a presentation vocabulary, not a source of simulation facts.
Any future replacement with licensed SVG, raster, or font assets must record
retrieval date, source, hashes, license, attribution, modifications, and
approval before entering the release tree.
