# Request Summary — Visual/audio Phase 8.1 approved local generation workflow v0.12.74

## Authorized outcome

Complete Milestone 8.1 as an auditable, local-only generation workflow for
future fictional visual/audio assets. Preserve provenance, reproducibility,
human review, and release gates. This slice does not generate or release a
portrait, illustration, texture, or audio source asset.

## Target slice

- List the approved local model and its model-card/license basis with explicit
  scope and access/review conditions.
- Define a versioned generation metadata schema covering model identity and
  revision, license, application, prompts, negative prompts, seed, sampler and
  settings, dimensions, date, contributor, post-processing, source references,
  source/release hashes, and human review.
- Automate capture from a request document and validation of captured records.
- Preserve source-output and optional release-output paths, prevent unapproved
  release records, and bridge approved records to the existing visual/audio
  asset registries.
- Add prompt templates, reviewer checklists, fixture proof, and focused tests.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Milestone 8.1.
- `assets/registry/visual-assets.json` and `assets/registry/audio-assets.json`.
- `scripts/validate_assets.py` and `scripts/generate_asset_credits.py`.
- `docs/design_principles.md` and `LESSONS.md` — actor-visible, provenance,
  accessibility, and evidence boundaries.
- Hugging Face model card for `black-forest-labs/FLUX.1-schnell`, reviewed as
  the primary source for the candidate Apache-2.0 local model listing.

## Non-goals

- Do not download model weights, call a hosted inference API, or create a
  generated asset in this slice.
- Do not approve a generated output without human review, source preservation,
  hash capture, resemblance/logo/trademark/clinical plausibility checks, and
  registry approval.
- Do not add portraits, new visual/audio assets, host fields, simulation state,
  replay artifacts, or network/runtime dependencies.

## Validation target

Capture/validate CLI tests, approved-model and schema fixture checks, registry
bridge checks, prompt/checklist proof checks, existing asset/credits/release/
documentation checks, full Python/Rust tests, formatting, Clippy, and diff
checks.

## Evidence limits

The model-card review supports workflow metadata only; it is not legal advice,
training-data provenance, output ownership, or a human resemblance/clinical
review. Automated hashes and schema checks establish auditability mechanics,
not asset quality, educational value, policy validity, or release clearance.
