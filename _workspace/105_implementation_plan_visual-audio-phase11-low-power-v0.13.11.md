# Implementation Plan — Visual/audio Phase 11.2 low-power profile evidence v0.13.11

## Task restatement

Define and verify one bounded reduced-capability profile for the existing
dependency-free loopback GUI, closing only the Phase 11.2 low-power test item
without claiming real hardware performance or changing the runtime.

## Current understanding

- `assets/loading-policy.json` defines the current live entrypoint and complete
  local module graph.
- The live surface is source-delivered and uses generated Web Audio; it has no
  file-backed media or speculative preload path.
- A local browser smoke at 1024×768 observed five shell reloads of 49–52 ms,
  818 DOM elements, four SVGs, audio-off text, and written equivalents. The
  live start and adapter probes were 367 ms and 259 ms respectively.
- No standalone low-power device or browser runtime is available, so the
  evidence must be explicitly labeled an emulated proxy.

## Assumptions

- The loading-policy live-file list is the authoritative source-size scope.
- Conservative source/DOM/SVG/time limits are useful regression guardrails for
  the current surface, but do not predict device battery, thermal, or frame
  behavior.
- Existing UI fallbacks already preserve written meaning when audio or motion
  is unavailable.

If an assumption is false, stop and report the mismatch before broadening the
slice.

## Minimal implementation plan

1. Add `assets/device-performance-policy.json` with the named viewport,
   reduced-motion/audio-off/storage-unavailable profile, conservative limits,
   measured proxy values, and explicit evidence limits.
2. Add `scripts/check_device_performance.py` to validate the policy, recompute
   live source bytes from the loading-policy graph, check every measurement
   against limits, and fail closed on a real-device certification claim.
3. Add `tests/test_device_performance.py` covering the green report/CLI,
   source-size drift, exceeded limits, invalid profiles, and forbidden claims.
4. Update the roadmap and project records to describe the exact proxy evidence,
   retain the portrait/human/device limitations, and bump the patch version.
5. Run focused and full checks; stop before adding browser dependencies,
   runtime instrumentation, hardware farms, or simulation changes.

## Files and functions likely to change

- `assets/device-performance-policy.json`: profile, limits, and captured proxy
  observations.
- `scripts/check_device_performance.py`: policy validation and report builder.
- `tests/test_device_performance.py`: focused contract and fail-closed tests.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`,
  `_workspace/03_presentation_qa.md`, and `_workspace/final/handoff.md`:
  additive handoff records.
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `ARCHITECTURE.md`,
  `CHANGELOG.md`, and `LESSONS.md`: synchronized project state.

Avoid editing GUI, Rust, simulation, asset-registry, or host-projection files
unless the plan is found to be incomplete.

## Tests and checks

- `python3 scripts/check_device_performance.py`
- `python3 -m unittest tests.test_device_performance`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/check_documentation_links.py`
- `python3 scripts/validate_assets.py`
- `python3 scripts/validate_asset_security.py`
- `python3 scripts/verify_asset_release.py --check`
- `cargo fmt --check`
- `cargo test`
- `cargo clippy --all-targets --all-features -- -D warnings`

Expected result: the policy report and focused tests pass, current source
measurements remain within the declared proxy limits, and existing runtime and
authority tests remain unchanged.

## Acceptance criteria

- The profile, measurements, limits, and evidence boundaries are machine-
  readable and deterministic.
- The checker recomputes the current live source scope rather than trusting a
  stale count.
- Missing fields, source drift, limit violations, invalid viewport/profile
  values, or `real_device: true` fail closed.
- The report records written and audio-off fallbacks as present and does not
  claim hardware certification, battery, thermal, or human-quality evidence.
- Only Phase 11.2 low-power-profile evidence is updated; portrait approval,
  human evaluation, screenshots, full campaign continuity, and other device
  engines remain open.

## Non-goals

- Do not add Playwright, Selenium, a browser binary, or a device farm.
- Do not add runtime timers, telemetry, frame-rate claims, or client settings.
- Do not change simulation transitions, host DTOs, audio catalog semantics,
  asset bytes, or browser authority boundaries.
- Do not mark the AI portrait human-review gate complete.
- Do not fabricate real-device or participant evidence.

## Stop conditions

Stop and report if the live source graph differs from the loading policy, the
measurement requires a non-loopback or external service, a runtime code change
is needed, or the evidence would need a real device to remain truthful.

## Review checklist

- The policy describes an emulated proxy and never a hardware certification.
- Source bytes are recomputed from the declared live graph.
- Limits and measurements use explicit units and no hidden dynamic inputs.
- Audio/motion/text fallbacks remain part of the measured surface.
- The checker has concrete malformed/escape/drift/claim failure tests.
- Documentation and version projections agree with the bounded evidence.
- The diff contains no unrelated GUI, Rust, simulation, or asset changes.

## Risk label

Risk: low

Reason: The slice adds read-only JSON evidence and a dependency-free checker;
it changes no runtime behavior, public API, asset bytes, or simulation state.
