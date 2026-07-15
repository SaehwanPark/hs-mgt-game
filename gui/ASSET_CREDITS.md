# Phase 5 audio credits

Phase 5 ships no third-party audio files. The four music recipes, one optional
ambience recipe, and sixteen interface/event cue recipes are generated at
runtime by [`audio.mjs`](audio.mjs) with the browser Web Audio API.

| Registry | Source | Ownership/license | Status |
| --- | --- | --- | --- |
| [`audio-catalog.json`](audio-catalog.json) | `gui/audio.mjs` oscillator recipes | Project-generated; no third-party asset | Approved for the Phase 5 technical slice |

Any future replacement with recorded or licensed files must add retrieval date,
source URL, hashes, license URL, attribution, modifications, and approval to the
registry before entering the release tree.
