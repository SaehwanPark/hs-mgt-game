# Implementation Plan — Phase 13.1 current technical-release coverage v0.13.20

## Task restatement

Continue the roadmap's release-candidate audit with a bounded technical
contract for the current source-checkout presentation. Join the existing Rust,
GUI, screenshot/structural, asset, hash, accessibility-contract, offline,
replay, in-memory checkpoint, and Chromium checks without claiming that the
product/content/human release gates are complete.

## Current understanding

- The repository already has deterministic Rust tests, the full Python GUI and
  governance suite, release/asset/hash/security checks, offline/package checks,
  device/browser proxy checks, and bounded live history/replay/checkpoint
  evidence.
- `docs/evaluation/phase11.1-campaign-coverage-ledger.json` records the current
  screenshot-surface and continuity limits; the asset/generation policies
  record release and provenance boundaries.
- Phase 13.1's technical checklist is still unchecked as a broad release
  candidate gate even though the current bounded checks pass.

## Target slice

Add `docs/evaluation/phase13.1-technical-coverage.json` and parity tests for:

- current Rust and GUI test suites;
- current screenshot/structural regression;
- asset, license/provenance, and hash/release validation;
- accessibility presentation-contract checks;
- current offline package and Chromium compatibility contracts;
- immutable replay verification; and
- current in-memory save/load visual continuity.

Record each source/check command and explicit limits for full-campaign content,
durable persistence, cross-browser/device certification, human accessibility,
quality, educational usability, and public-release approval.

## Assumptions

- “Technical release coverage” means the current source checkout passes its
  declared automated and bounded local-proxy checks; it is not a release
  candidate approval or a claim that all product/content gates are satisfied.
- Existing scripts/tests remain authoritative. The new ledger only joins their
  scope and must not duplicate or weaken their validators.
- A current in-memory checkpoint and text-first replay projection are recorded
  as bounded capabilities, not durable save/load or playback/regeneration.

## Minimal implementation plan

1. Add the technical-release ledger with exact check sources, status,
   commands, bounded continuity/screenshot references, and limits.
2. Add a focused parity test requiring every named source path and limitation,
   while preserving the existing validators as authoritative.
3. Update the Phase 13.1 technical checklist/status and v0.13.20 evidence;
   synchronize canonical docs, lessons, version metadata, generated credits,
   and additive request/contract/QA/handoff records.
4. Run full Python/Rust/lint/release/documentation/generation/asset/offline/
   browser/device/visual-audio checks.
5. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the remaining roadmap gates.

## Non-goals

- Do not add campaign content, instructor views, durable persistence,
  cross-browser certification, raster goldens, human evaluation, educational
  pilot materials, or a release artifact.
- Do not change simulation, GUI behavior, assets, audio, or authority paths.

## Stop conditions

Stop if the evidence would require product/content completion, human judgment,
external device/browser access, durable storage, or public-release approval.

## Risk label

Risk: low

Reason: This is a read-only evidence aggregation over already passing checks;
it changes governance/documentation and parity tests only.
