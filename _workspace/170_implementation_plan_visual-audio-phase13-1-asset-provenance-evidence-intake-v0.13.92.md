# Implementation Plan: Asset Provenance Evidence-Intake Packet v0.13.92

## Target slice

Make the open `Complete asset provenance review` and related AI-preview
provenance gates operationally ready for authorized review by adding a strict,
source-bound, empty intake covering the current visual/audio registries and
the seven unreleased portrait previews. The slice does not approve, release,
register, or alter any asset.

## Current repository understanding

- The visual and audio registries already contain the current repository-owned
  inventory with generated credits, hashes, license references, and written
  equivalents.
- The AI-generation boundary and portrait-review queue already record seven
  hash-bound, unreleased previews with missing model/seed metadata and pending
  human gates.
- Existing campaign provenance audits and the AI-preview provenance packet
  establish technical readiness and fail-closed promotion boundaries, but no
  single empty review intake binds all current asset families and future
  provenance findings.

## Authorized changes

- Add `docs/evaluation/phase13.1-asset-provenance-evidence-intake-packet.json`
  with canonical inventory counts/IDs, review gates, zero records, and
  pending approval/release decisions.
- Add `scripts/validate_asset_provenance_evidence_intake.py` using only the
  standard library to enforce exact envelope/source parity, registry/queue
  parity, bounded review records, and no-promotion claims.
- Add `tests/test_phase13_1_asset_provenance_evidence_intake.py` covering
  inventory parity, gate vocabulary, empty/pending status, unknown-field and
  source-redirection rejection, privacy/type safety, and release exclusion.
- Update the roadmap, SPEC, CHANGELOG, README/package version, lessons,
  request summary, presentation contract/QA, domain QA, and final handoff;
  regenerate deterministic credits/notices/runtime metadata after the version
  bump.

## Public and compatibility effects

No Rust, GUI runtime, simulation, persistence, asset content, audio, browser
policy, release manifest, or public API behavior changes are expected. The
packet and validator are repository-local provenance-review evidence only.

## Explicit non-goals and stop conditions

- Do not invent model IDs, revisions, samplers, seeds, licenses, creators,
  legal conclusions, training-data conclusions, or human review results.
- Do not add portrait previews to either registry or release manifest.
- Do not change source/release files, hashes, raster/media artifacts, runtime
  loading, credits policy, or asset approval status.
- Stop and report if the current registry/queue inventories disagree or if a
  review field requires unrestricted identity, legal, or human notes.

## Verification and acceptance criteria

- The validator passes the empty, pending baseline and derives exact inventory
  parity from canonical registries and the portrait review queue.
- Focused tests reject source redirects, inventory drift, unknown fields,
  unsafe identity/private-state fields, numeric coercion, approval promotion,
  and release-manifest inclusion.
- Existing asset, generation, release, documentation, full Python/Rust,
  formatting, and clippy checks remain green.
- Exactly one medium-effort code reviewer performs the final review; findings
  are resolved before the PR is merged and the temporary branch is deleted.

## Risk label

**Medium:** the packet governs provenance and release boundaries, but does not
alter asset content or collect external data.

## Execution instruction

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising. Report
files changed, tests run, deviations, and unresolved risks.
