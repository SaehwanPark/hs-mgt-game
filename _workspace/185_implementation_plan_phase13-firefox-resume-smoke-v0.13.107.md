# Implementation plan: v0.13.107 Firefox browser-refresh resume smoke

## Target slice

Add a deterministic, loopback-only Firefox/Marionette probe for the bounded
`gui-session-resume-policy-v1` behavior introduced in v0.13.106. The probe
must exercise only host-visible UI and the opaque active-session storage key;
it must not read or write host save bytes or browser state beyond the one
opaque ID required by the policy observation.

## Design

1. Extend `scripts/check_firefox_runtime_smoke.py` with a refresh-resume step:
   start the host session, perform an explicit checkpoint save, navigate to the
   same loopback URL again, and validate that the resumed session ID matches
   the original and that the shell reaches the loaded state.
2. Keep the probe bounded to one refresh and one host restore attempt. Treat a
   missing checkpoint, changed session ID, missing status, or failed shell
   readiness as a failure.
3. Expand the Firefox evidence packet and its tests to record the new smoke
   observation while retaining every pending certification boundary.
4. Bump the patch version to 0.13.107 and update release, guide, audit, and
   roadmap bookkeeping without changing the canonical browser support policy.

## Files

- `scripts/check_firefox_runtime_smoke.py`
- `docs/evaluation/phase13.1-firefox-runtime-smoke-packet.json`
- `tests/test_phase13_1_firefox_runtime_smoke_packet.py`
- `docs/evaluation/phase13-remaining-gate-technical-audit.json`
- `scripts/validate_remaining_gate_technical_audit.py`
- `tests/test_phase13_remaining_gate_technical_audit.py`
- release metadata and user-facing GUI/runtime evidence docs

## Verification

- Run the live GUI host and the Firefox probe against `127.0.0.1:7878`.
- Run the Firefox packet, browser/device, audit, and release metadata tests.
- Run `cargo fmt`, Clippy, serial Rust tests, the full Python suite, the audit
  validator, and `git diff --check`.
- Obtain the single designated medium-effort code review before merge.

## Exit criteria

- Firefox refresh resume smoke passes with the same opaque session ID after one
  host restore attempt.
- Packet and tests prove the smoke remains non-promotional and fail closed on
  pending full-campaign, WebKit, real-device, human, and release gates.
- Main branch receives the squash merge and the temporary branch is removed
  both locally and remotely.
