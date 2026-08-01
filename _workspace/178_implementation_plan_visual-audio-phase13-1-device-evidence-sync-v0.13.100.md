# Implementation Plan — Generated device-evidence synchronization v0.13.100

## Target slice

Synchronize the existing low-power browser-proxy evidence measurement with the
post-merge GUI source bytes after the v0.13.99 cross-campaign terminal guard.
This is release/evidence maintenance only; it does not change the roadmap gate
or claim device certification.

## Acceptance criteria

1. The device-performance policy measurement equals the current canonical live
   source byte total.
2. The cross-browser/device review packet and its test fixture use the same
   measurement and remain bounded below the existing limit.
3. Package metadata is bumped from v0.13.99 to v0.13.100 for this follow-up
   PR-equivalent change, with generated asset projections synchronized.
4. Device, asset, release, terminal packet, and remaining-gate validators pass.
5. No support policy, human review, hardware certification, gameplay, or
   public-release status is promoted.

## Planned files

- `assets/device-performance-policy.json`
- `docs/evaluation/phase13.1-cross-browser-device-review-packet.json`
- `tests/test_device_performance.py`
- `assets/ASSET_CREDITS.md`, `assets/THIRD_PARTY_NOTICES.md`, and
  `gui/asset-credits.mjs`
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`, `SPEC.md`, and
  `tests/test_release_metadata.py`
- `docs/visual_audio_enhancement_roadmap.md`, `LESSONS.md`, and this handoff
  record

## Design boundaries

- Treat the byte total as a reproducibility measurement, not a performance or
  device-quality claim.
- Preserve the current 400000-byte limit and all emulated-proxy evidence
  limits.
- Keep v0.13.99 terminal evidence historical and bound to its captured
  package/runtime observation.
- Do not change GUI behavior, simulation, audio, assets, persistence,
  browser-support policy, or human/release decisions.

## Verification

- Run device-performance and cross-browser/device contract tests.
- Run asset, release metadata, formatting, terminal packet, remaining-gate,
  documentation, and full Python/Rust checks as practical.
- Complete one medium-effort code review, merge, delete temporary branches,
  and re-audit the consolidated gate ledger.
