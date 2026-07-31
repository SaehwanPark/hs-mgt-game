# Implementation Plan: Firefox Runtime-Smoke Packet v0.13.89

## Target slice

Record a bounded, host-backed Firefox runtime smoke result now that Firefox
147.0.2 is available in the local verification environment. The result will
cover entrypoint load, DOM readiness, the session-start control, and one
host-adapter start response. It will separately record Safari/WebKit remote
automation as blocked by the local permission setting.

## Authorized changes

- Add a dependency-free Marionette probe script that talks to an already
  running loopback GUI host and emits JSON evidence without writing project
  state.
- Add `docs/evaluation/phase13.1-firefox-runtime-smoke-packet.json` with the
  observed browser version, shell/host observations, command boundary, and
  Safari/WebKit blocker.
- Add a fail-closed validator for probe-source parity, observed fields,
  browser/device limits, and release exclusion.
- Update roadmap, specification, changelog, README/package version, lessons,
  release-version test, generated credits, and workspace review/handoff
  records.
- Keep the canonical browser policy unchanged: one Firefox smoke run does not
  certify the complete engine matrix or authorize support promotion.

## Evidence boundary

- Firefox 147.0.2 headless Marionette loaded `http://127.0.0.1:7878/`, reached
  `readyState=complete`, found the session-start control, and observed
  `competitive regional session loaded: session-1` after a real click.
- Safari/WebKit remains `not-certified`; SafariDriver reported that “Allow
  remote automation” is disabled, so no WebKit runtime result is recorded.
- Full campaign, audio decoder, real-device performance, browser support
  expansion, human accessibility/usability, legal, and public-release claims
  remain open.

## Verification target

- Focused runtime-smoke packet validator.
- Probe syntax and packet-source parity checks.
- Existing browser/device and technical-coverage tests.
- Full Python/Rust and repository validation.
- Exactly one medium-effort code review, followed by PR merge and temporary
  branch cleanup.
