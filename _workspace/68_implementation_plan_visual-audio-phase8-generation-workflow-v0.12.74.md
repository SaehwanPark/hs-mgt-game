# Implementation Plan — Visual/audio Phase 8.1 approved local generation workflow v0.12.74

## 1. Task restatement

Complete Phase 8.1 as a workflow-only, local-generation provenance slice. Make
future AI-assisted assets reproducible enough for audit and fail closed before
human review and registry approval, without generating or shipping an asset.

## 2. Current understanding

- The repository already validates visual/audio asset registries, source/release
  hashes, allowlisted licenses, attribution, accessible equivalents, and
  approval status.
- Phase 8.1 adds generation-specific metadata that the existing asset registry
  cannot express: model identity/revision/license, prompt settings, seed,
  source references, post-processing, and review checklist.
- A primary Hugging Face model card lists `black-forest-labs/FLUX.1-schnell`
  under Apache-2.0 and documents local-app/Diffusers use, while also requiring
  access conditions. The project records that basis and keeps legal/output
  review explicit rather than treating it as blanket clearance.

## 3. Target slice and assumptions

- Add `assets/generation/approved-models.json` with one conditionally approved
  local prototype model listing and explicit scope/review limitations.
- Add `assets/generation/generation-workflow.json` with required fields,
  allowlisted licenses, prompt/review policy, and registry bridge rules.
- Add `scripts/capture_generation_metadata.py` to capture normalized records and
  hash preserved source/release outputs; add
  `scripts/validate_generation_metadata.py` to validate models, records,
  review/approval gates, paths, hashes, and registry links.
- Add prompt templates, human-review checklist, a fixture-only proof page, and
  focused tests. Keep the committed generation manifest empty until Phase 8.2
  or another explicitly authorized asset slice creates a reviewed output.

## 4. Minimal implementation plan

1. Define JSON schemas/examples for approved models, generation requests,
   captured metadata, human review, and asset-registry bridge fields.
2. Implement capture/validation CLIs with safe repository-relative paths,
   deterministic JSON normalization, SHA-256 source/release hashes, and
   fail-closed errors for incomplete or unapproved records.
3. Add a proof page and tests for complete capture, missing metadata, unknown
   model/license, hash mismatch, pending review, release approval, and registry
   linkage. Keep no generated asset in the manifest.
4. Update roadmap, SPEC, architecture, README, GUI guidance, CHANGELOG,
   LESSONS, version metadata, and QA handoff; cite the primary model-card basis
   in the workflow documentation.

## 5. Acceptance criteria

- Approved local model and license basis are listed with scope and access/
  review limitations.
- Capture records include every roadmap-required field and computed source /
  release hashes; seeds/settings/prompts are never implicit.
- Validation rejects unknown models, denylisted licenses, missing source output,
  hash mismatch, incomplete human review, unapproved releases, and invalid
  registry bridges.
- Prompt template, human review checklist, real-person resemblance, logo/
  trademark, clinical plausibility, accessibility, and post-processing fields
  are explicit and fixture-verifiable.
- The committed generation manifest remains empty and no model weights or
  generated assets are added.
- Existing asset, credits, metadata, docs, Python/Rust, formatting, Clippy,
  syntax, and diff checks pass.

## 6. Non-goals

- Do not download or run a model, invoke a hosted API, or use `image_gen` to
  produce a release asset in this workflow slice.
- Do not create Phase 8.2 fictional portraits or any generated visual/audio
  output.
- Do not alter simulation, host, observation, history, replay, debrief, or
  runtime presentation authority.
- Do not claim legal clearance, training-data provenance, output ownership,
  human quality, clinical plausibility, accessibility, learning, or policy
  validity from metadata automation.

## 7. Stop conditions

- Stop if model terms cannot be documented from a primary source; keep the
  model unapproved and preserve the fail-closed workflow.
- Stop if generation requires network/runtime dependencies or creates an asset.
- Stop on unrelated registry or repository failures rather than weakening the
  release gate.

## 8. Verification target

Focused capture/validation tests; proof/schema checks; existing asset/credits/
release/docs checks; full Python tests; `cargo fmt --check`; Clippy; Rust
tests; and `git diff --check`.

## 9. Risk label

Risk: medium. The main risks are treating a model-card license as complete
legal clearance, losing prompt/seed/hash provenance, approving unreviewed
outputs, or bypassing the existing asset registry. Empty-manifest defaults,
explicit human checklist fields, and fail-closed validation bound those risks.
