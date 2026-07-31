# Implementation Plan — AI preview provenance/human-review packet v0.13.87

## Target slice

Prepare a source-bound technical review packet for the seven preserved,
unverified fictional actor-portrait previews. The packet will make the open
AI-generation metadata, identity, accessibility, resemblance, and release
review work actionable without guessing missing model/seed metadata, recording
human findings, or promoting preview images.

This slice is evaluation and release-boundary infrastructure only. It does not
change the GUI, simulation, visual/audio runtime, asset registries, generated
images, release manifest, or release assets.

## Source and authority boundary

Use these records and validators as the technical authority:

- `docs/evaluation/phase13.1-ai-generation-metadata-boundary.json` for the
  required generation metadata, fail-closed promotion rule, and open gates.
- `docs/evaluation/phase13.1-attribution-boundary.json` for registry/credits/
  manifest parity and attribution limits.
- `assets/generation/generation-workflow.json` and
  `assets/generation/approved-models.json` for required metadata and approved
  local-model scope.
- `assets/generation/portrait-set.json` for the seven role contracts,
  prohibited content, fallback, size, grayscale, and review requirements.
- `assets/generation/portrait-previews.json` for preserved source files,
  hashes, dimensions, prompts, missing model/seed fields, and written
  equivalents.
- `assets/generation/portrait-review-queue.json` for per-preview gate state,
  reviewer fields, release blocking, and registry bridge state.
- `assets/generation/generation-manifest.json`, visual/audio registries,
  generated credits, and `assets/ASSET_RELEASE_MANIFEST.json` for exclusion
  from runtime/release surfaces.
- `scripts/validate_generation_metadata.py`, `scripts/validate_assets.py`,
  `scripts/verify_asset_release.py`, and existing portrait/attribution tests
  for executable evidence.

The packet must keep machine provenance separate from human legal clearance,
training-data provenance, resemblance review, visual quality, accessibility,
educational usefulness, and public-release approval.

## Deliverables

1. Add `docs/evaluation/phase13.1-ai-preview-provenance-review-packet.json`
   with:
   - exact source markers and shared-source paths;
   - all seven preview IDs, role/family, image path, source hash, dimensions,
     written equivalent, generic fallback, and pending gate status;
   - parity-bound generation metadata requirements and approved-model scope;
   - per-preview human review tasks for identity, role, resemblance, marks/text,
     artifact quality, accessibility, small-size, grayscale, provenance,
     release derivative, and registry bridge;
   - explicit release exclusion and no-guessing constraints;
   - pending human-review, legal, training-data, and public-release fields.
2. Add a fail-closed Python validator covering exact source markers, seven-role
   parity, hashes/dimensions/file existence, queue/preview parity, missing
   model/seed enforcement, generation manifest and registry exclusion, release
   manifest exclusion, and human-review pending state.
3. Update roadmap, `SPEC.md`, request/presentation/domain-QA records, final
   handoff, `LESSONS.md`, `CHANGELOG.md`, README/Cargo version metadata, and
   generated asset-credit metadata to v0.13.87.

## Explicit non-goals

- Do not infer or fill model identity, immutable revision, sampler, seed,
  training-data provenance, or license from the preview tool.
- Do not record human resemblance, protected-mark, artifact, accessibility,
  educational, legal, or quality findings.
- Do not approve, register, load, release, or alter any portrait preview.
- Do not claim the AI-generation metadata roadmap item is complete.

## Verification

- Focused packet validator plus existing AI metadata, attribution, portrait,
  asset, security, generation, and release-manifest tests.
- Full Python test discovery, `cargo fmt --check`, `cargo clippy --all-targets
  -- -D warnings`, and serialized `cargo test`.
- Release metadata, documentation-link, credits, provenance/security,
  offline/browser/device, loading, raster, audio, and visual/audio gates.
- Exactly one medium-effort code review; fix actionable findings and obtain a
  clean recheck before PR handoff.

## Acceptance criteria

- The packet records all seven preview candidates and their exact hashes,
  dimensions, roles, fallbacks, and pending review gates.
- Missing model/seed metadata and every release-promotion boundary fail closed.
- No human or legal conclusion is inferred from machine checks.
- The roadmap records the technical packet while leaving AI-generation,
  provenance/legal, and public-release decisions open.
- Version metadata is consistently `0.13.87`.
