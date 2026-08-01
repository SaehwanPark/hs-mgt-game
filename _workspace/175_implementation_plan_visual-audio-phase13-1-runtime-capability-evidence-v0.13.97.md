# Implementation Plan — Cross-browser runtime capability evidence v0.13.97

## Task restatement

Implement a small, source-bound evidence packet and validator for the current
supported browser runtime and local browser/device capability boundary. Preserve
the existing Chromium support policy and keep Firefox, WebKit, real-device,
human-review, and public-release claims explicitly pending.

## Current understanding

- The canonical support contract is `assets/browser-compatibility-policy.json`
  plus the existing technical review packet and Firefox smoke packet.
- The current Codex in-app browser can load the loopback GUI and start a fresh
  competitive host session. The observed runtime identifies as Chrome 150 on
  macOS; the shell reaches `readyState=complete`, removes the demo fixture,
  and emits no warning/error console entries.
- No Firefox or Chromium command-line binary is installed in this host
  environment. `safaridriver` is present, but it does not open a listener
  without the macOS remote-automation configuration change; that change is out
  of scope for this slice.
- Existing browser/device policies and the remaining-gate audit are already
  authoritative. This slice adds current runtime evidence; it does not promote
  support or close human/runtime gates by inference.

## Assumptions

- The observed browser evidence is a bounded local verification observation,
  not a participant, accessibility, audio-quality, legal, clinical, or release
  decision.
- The packet may record an opaque host session ID only as a bounded observation;
  it must not serialize simulation state or become a browser authority.
- No browser installation, Safari permission change, external upload, or
  networked test service is required.

If any assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. Inspect the existing Phase 13.1 browser/device packet, policy, Firefox smoke
   packet, GUI host contract, and version metadata; confirm the new packet can
   remain additive.
2. Add `docs/evaluation/phase13.1-runtime-capability-evidence.json` with the
   observed Chrome host-backed smoke, safe local capability facts, explicit
   Safari/WebKit and Firefox boundaries, and a no-promotion release boundary.
3. Add `scripts/validate_runtime_capability_evidence.py` with strict schema,
   loopback URL, browser identity/version, shell/host observation, console
   count, capability-status, source-marker, and forbidden-claim checks.
4. Add focused tests for valid evidence, malformed browser identity, non-
   loopback URLs, accidental certification promotion, missing source markers,
   and preservation of the canonical browser/device validators.
5. Update the roadmap, SPEC, changelog, README milestone, lessons, request
   summary, presentation contract, domain/presentation QA, and final handoff;
   bump the package from `0.13.96` to `0.13.97` and regenerate only the
   version-derived credit artifacts.
6. Run focused tests, the full Python suite, serial Rust tests, formatting,
   Clippy, metadata/asset/release checks, and `git diff --check`.

## Files and functions likely to change

- `docs/evaluation/phase13.1-runtime-capability-evidence.json`: new observed
  runtime packet.
- `scripts/validate_runtime_capability_evidence.py`: new dependency-free
  validator; no runtime or simulation mutation.
- `tests/test_phase13_1_runtime_capability_evidence.py`: packet and validator
  regressions.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`, `SPEC.md`: version
  and milestone metadata.
- `docs/visual_audio_enhancement_roadmap.md`, `LESSONS.md`, and the bounded
  `_workspace` handoff/QA records: evidence and remaining-limit updates.
- `assets/ASSET_CREDITS.md`, `assets/THIRD_PARTY_NOTICES.md`, and
  `gui/asset-credits.mjs`: generated version-derived artifacts only.

Avoid editing other files unless the existing version/release checks require a
source-bound companion update. If that happens, stop and explain why before
broadening the plan.

## Public contract and compatibility effects

- Additive evidence schema only; no public Rust, GUI, simulation, host-adapter,
  browser-policy, device-policy, asset, audio, persistence, or release API
  changes.
- The canonical browser policy remains unchanged: Chromium is the only named
  supported target, Firefox/WebKit remain not certified, and the low-power
  profile remains emulated.
- The packet must not contain hidden state, user identity, raw media, browser
  history, or a claim that a human/device/release gate is complete.

## Tests and checks

Focused:

```text
python3 -m unittest tests.test_phase13_1_runtime_capability_evidence
python3 scripts/validate_runtime_capability_evidence.py
```

Repository checks:

```text
python3 -m unittest discover -s tests -p 'test_*.py'
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test --all -- --test-threads=1
python3 scripts/validate_assets.py
python3 scripts/verify_asset_release.py --check
git diff --check
```

Expected result: the new validator and all existing checks pass, with the
packet status remaining pending for Firefox/WebKit, real hardware, human
accessibility/usability, and public release.

## Acceptance criteria

- The packet validates exact Chrome 150 host-backed shell/session-start
  observations from the current loopback GUI and records zero warning/error
  console entries.
- The validator rejects non-loopback URLs, non-Chrome identity, missing or
  malformed host observations, unsupported certification booleans, source
  drift, and forbidden promotion claims.
- Existing browser/device contracts and the remaining-gate audit still pass
  without policy or support-status promotion.
- Version and documentation metadata consistently identify v0.13.97.
- No runtime, simulation, asset, audio, persistence, or public-release behavior
  changes.

## Non-goals

- Do not install or launch a new browser distribution.
- Do not enable Safari remote automation or claim WebKit certification.
- Do not claim Firefox, real-device, battery/thermal, audio-quality,
  accessibility, educational, legal, clinical, or public-release completion.
- Do not change browser/device policy, campaign mechanics, UI presentation, or
  generated assets beyond version-derived metadata.

## Stop conditions

Stop and ask for review if:

- evidence requires changing macOS permissions, installing software, or sending
  data outside the repository;
- the packet requires a new public API or support-policy change;
- more than the listed production/contract files need edits;
- a test exposes a missing human/runtime authority decision rather than a
  source-bound validator defect; or
- the implementation would need to infer a result not directly observed.

## Handoff requirements

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising. Report files
changed, tests run, deviations, and unresolved risks. Before merge, obtain
exactly one medium-effort code review and address or explicitly document every
finding.

## Risk label

Risk: medium

Reason: the change is additive and fail-closed, but it updates release-readiness
evidence and must not accidentally promote an unsupported browser or human gate.
