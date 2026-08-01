# Implementation plan: v0.13.108 Firefox multi-campaign launch smoke

## Target slice

Extend the existing loopback-only Firefox/Marionette probe to cover all three
GUI launch campaigns while preserving the v0.13.107 checkpoint-save and
browser-refresh evidence boundary.

## Design

1. Add a probe helper that selects a campaign through the visible campaign
   control, submits the existing host start action, and validates the returned
   campaign-specific status, opaque session ID, and non-demo shell.
2. Run the helper for competitive regional, stabilization, and regional
   affiliation campaigns in one Firefox session. Keep the competitive
   checkpoint/refresh check bounded to the existing first campaign path.
3. Record the three launch observations in the Firefox packet and add a
   source-bound technical check to the consolidated audit. Keep full-campaign,
   Firefox certification, WebKit, device, human, and release boundaries false.
4. Bump the patch version to 0.13.108 and update roadmap, guide, handoff,
   lessons, and generated device-proxy bookkeeping.

## Files

- `scripts/check_firefox_runtime_smoke.py`
- `docs/evaluation/phase13.1-firefox-runtime-smoke-packet.json`
- `tests/test_phase13_1_firefox_runtime_smoke_packet.py`
- `docs/evaluation/phase13-remaining-gate-technical-audit.json`
- `scripts/validate_remaining_gate_technical_audit.py`
- release metadata and roadmap evidence docs

## Verification

- Rebuild and run the GUI host, then run the Firefox 147.0.2 probe.
- Run Firefox packet, browser/device, audit, release, and full Python tests.
- Run `cargo fmt`, Clippy, serial Rust tests, device and audit validators, and
  `git diff --check`.
- Obtain the one designated medium-effort code review before merging.

## Exit criteria

- All three launch observations pass with opaque host IDs and correct labels.
- The packet explicitly distinguishes launch/read smoke from full-campaign
  certification and leaves all external gates pending.
- The squash merge lands on `main`, and the temporary branch is deleted locally
  and remotely before the next re-audit.
