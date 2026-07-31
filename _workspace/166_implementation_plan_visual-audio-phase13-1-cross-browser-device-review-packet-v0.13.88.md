# Implementation Plan: Cross-Browser/Device Review Packet v0.13.88

## Target slice

Prepare a source-bound, technical review packet for the open Phase 13.1
cross-browser/device certification gate. The packet will make the current
Chromium compatibility matrix and reduced-capability low-power proxy
inspectable while preserving the explicit non-certification of Firefox,
WebKit, real hardware, battery/thermal/memory/frame-rate behavior, and lived
human accessibility or usability.

## Authorized changes

- Add `docs/evaluation/phase13.1-cross-browser-device-review-packet.json`.
- Add one fail-closed validator test for exact policy, evidence, target, and
  limit parity.
- Update the roadmap, specification, changelog, README version, package
  version, release-version test, lessons, and workspace review/handoff
  records.
- Keep the packet evaluation-only; do not change the GUI, Rust host, browser
  policy, device policy, screenshot assets, runtime behavior, or release
  manifest.

## Source contract

Bind the packet to the browser compatibility policy, device-performance
policy, loading/offline policies, compatibility and device checkers, existing
compatibility/device tests, reproducible-distribution guide, GUI player guide,
and the current technical-coverage ledger. The validator must fail closed on
source-marker drift, policy target/capability drift, measurement drift,
unsupported certification claims, or missing evidence-limit language.

## Technical boundary

- `chromium-evergreen-desktop` remains the only supported browser target,
  with the policy-declared required capabilities and existing static/local
  smoke evidence.
- `low-power-browser-proxy` remains a 1024×768 reduced-motion/audio-off,
  storage-unavailable, loopback-only emulated proxy with its existing measured
  limits and no real-device claim.
- Firefox and WebKit remain `not-certified`; legacy non-module browsers remain
  unsupported.
- Real hardware, battery/thermal/memory/frame-rate/decoder/cache behavior,
  and human accessibility/usability remain pending and must not be inferred.

## Verification target

- Focused v0.13.88 packet validator.
- Existing browser compatibility and device performance tests.
- Existing compatibility/device checker scripts and technical coverage test.
- Full Python/Rust and repository validation.
- Exactly one medium-effort code review, followed by PR merge and temporary
  branch cleanup.

## Non-goals

- No Firefox, WebKit, real-device, battery, thermal, memory, frame-rate, or
  decoder test is claimed or fabricated.
- No browser serialization, runtime, simulation, GUI, asset, audio, screenshot,
  release, participant, accessibility, educational, or legal change.
- No public-release certification or human usability conclusion.
