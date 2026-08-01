# Request summary: v0.13.110 Firefox all-campaign full-transition smoke

## User objective

Continue the visual/audio enhancement roadmap through bounded implementation,
single-reviewer PR, merge, cleanup, and re-audit loops without converting
technical evidence into human or release approval.

## Selected slice

The v0.13.109 re-audit closes only the competitive Firefox Hold-path smoke.
The existing visible host-shaped campaign coverage forms can also exercise the
remaining supported campaigns:

- five stabilization stages using the rendered numeric decision fields; and
- six regional-affiliation stages using the rendered Commit decision control.

This slice extends the Firefox/Marionette probe to complete both sequences,
requiring host autosave status, committed campaign history, per-stage state
hashes, and the host terminal debrief for each campaign.

This is technical runtime smoke evidence only. It does not certify Firefox
support, alternative decision values, WebKit, real hardware, audio decoding,
accessibility, usability, educational value, provenance, or public release.

## Non-goals

- No simulation, replay, save-artifact, asset, audio, or browser-policy change.
- No new campaign mechanics or client authority.
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
- `CHANGELOG.md`, `Cargo.toml`, `README.md`, `LESSONS.md`, the roadmap, and
  v0.13.110 handoff/plan artifacts

## Validation target

Rebuild the loopback GUI host and run the Firefox 147.0.2 probe against
`http://127.0.0.1:7878/`. Require competitive 24-month evidence plus five
stabilization and six regional-affiliation committed transitions, then run
the focused and full Python/Rust checks and the single designated Archimedes
review at medium reasoning effort.
