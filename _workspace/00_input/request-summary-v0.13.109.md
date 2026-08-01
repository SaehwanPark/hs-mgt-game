# Request summary: v0.13.109 Firefox competitive full-campaign smoke

## User objective

Continue the visual/audio enhancement roadmap through bounded implementation,
single-reviewer PR, merge, cleanup, and re-audit loops without converting
technical evidence into human or release approval.

## Selected slice

The v0.13.108 re-audit left Firefox full-campaign runtime evidence open. A
live investigation showed that the existing Firefox/Marionette path can use
the visible competitive action builder for all 24 host turns. This slice adds
that bounded probe and records:

- 24 visible Hold decisions added to the DOM draft;
- host validation and submission for every month;
- host autosave status after every committed transition;
- 24 host-backed history/replay rows with state hashes; and
- the host-provided terminal history and written debrief.

This is technical competitive full-campaign smoke evidence only. It does not
certify Firefox support, WebKit, real hardware, audio decoding, accessibility,
usability, educational value, provenance, or public release.

## Non-goals

- No simulation, replay, save-artifact, asset, audio, or browser-policy change.
- No stabilization or regional-affiliation full-campaign automation in this
  slice; their launch/read smoke remains separately recorded.
- No Safari/WebKit permission change or real-device claim.
- No human accessibility, educational, provenance, content, or public-release
  decision.

## Expected files

- `scripts/check_firefox_runtime_smoke.py`
- `docs/evaluation/phase13.1-firefox-runtime-smoke-packet.json`
- `tests/test_phase13_1_firefox_runtime_smoke_packet.py`
- `docs/evaluation/phase13-remaining-gate-technical-audit.json`
- `scripts/validate_remaining_gate_technical_audit.py`
- `docs/guides/gui-how-to-play.md`
- `CHANGELOG.md`, `Cargo.toml`, `docs/visual_audio_enhancement_roadmap.md`,
  `LESSONS.md`, and the v0.13.109 handoff/plan artifacts

## Validation target

Rebuild the loopback GUI host and run the Firefox 147.0.2 probe against
`http://127.0.0.1:7878/`. Validate the evidence packet and audit, run focused
and full Python/Rust checks, and keep the single designated Archimedes review
at medium reasoning effort.
