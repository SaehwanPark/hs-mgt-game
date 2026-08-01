# Implementation Plan — Consolidated remaining-gate audit refresh v0.13.101

## Target slice

Bring the consolidated `phase13-remaining-gate-technical-audit-v1` packet
forward to the current repository release and explicitly bind the newer
runtime-boundary evidence packets. This is evidence-governance maintenance;
the eight human/runtime gates remain open.

## Acceptance criteria

1. The audit packet and validator agree on package version v0.13.101.
2. The technical-check inventory includes a current runtime-boundary check with
   sources for runtime capability, first-session/audio, terminal debrief, and
   device evidence.
3. The eight existing gate IDs map every unchecked roadmap marker exactly once.
4. Technical implementation gaps remain false, human/runtime gates remain true,
   promotion remains blocked, and all decision fields remain null.
5. Focused, full, release, asset, documentation, and Rust checks pass.

## Planned files

- `docs/evaluation/phase13-remaining-gate-technical-audit.json`
- `scripts/validate_remaining_gate_technical_audit.py`
- `tests/test_phase13_remaining_gate_technical_audit.py`
- `Cargo.toml`, `Cargo.lock`, `README.md`, `CHANGELOG.md`,
  `tests/test_release_metadata.py`
- `assets/ASSET_CREDITS.md`, `assets/THIRD_PARTY_NOTICES.md`, and
  `gui/asset-credits.mjs`
- `docs/visual_audio_enhancement_roadmap.md`, `SPEC.md`, `LESSONS.md`, and
  `_workspace/final/handoff.md`

## Design boundaries

- Treat packets and validators as source-bound evidence indexes, not human
  findings or release approvals.
- Reuse the current validators and packet paths; do not create duplicate
  simulation, browser-authority, or evidence-capture systems.
- Preserve all eight pending gate authorities, next actions, and null decisions.
- Keep the v0.13.99 terminal packet’s historical package version intact; this
  refresh updates the consolidated index, not the captured observation.

## Verification

- Run `tests.test_phase13_remaining_gate_technical_audit` and every current
  runtime/device evidence validator referenced by the audit.
- Run the full Python suite, serial Rust tests, Clippy, formatting, release,
  asset, browser, device, documentation, and diff checks.
- Complete the one-reviewer PR loop and re-run the consolidated audit on clean
  `main` after merge.
