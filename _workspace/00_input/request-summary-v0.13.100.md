# Request Summary — Generated device-evidence synchronization v0.13.100

## Authorized outcome

Correct the stale source-byte measurement discovered by the v0.13.99
post-merge re-audit. Keep the evidence as an emulated low-power proxy and do
not promote browser/device certification or public release.

## Target slice

- Bind `assets/device-performance-policy.json` and the cross-browser/device
  review packet to the current GUI live-source byte total.
- Synchronize the bounded test expectation and generated asset-credit version
  projections.
- Bump the package patch version for this follow-up PR-equivalent change and
  record the maintenance slice in the roadmap/spec/changelog.

## Non-goals

- No GUI, simulation, gameplay, audio, asset, persistence, support-policy,
  browser-support, hardware, human review, or public-release behavior change.
- No claim that the proxy measurement is a hardware benchmark or certification.
- No revision of the v0.13.99 terminal observation packet's historical package
  version.

## Validation target

Focused device/release/asset checks, full repository verification, exactly one
medium-effort code review, PR merge, temporary-branch deletion, and remaining-
gate re-audit.

## Evidence limits

The synchronized byte count proves only deterministic source-measurement
parity. It does not establish real-device performance, browser certification,
lived accessibility, audio quality, educational usefulness, or release
approval.
