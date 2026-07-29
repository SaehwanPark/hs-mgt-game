# Implementation Plan — Phase 13.1 AI-generation metadata boundary v0.13.57

## Target slice

Record and test the current technical readiness boundary for AI-generated
portrait metadata. The slice ends at a fail-closed handoff: existing previews
remain pending and unreleased because their actual model identity, immutable
revision, seed, and human review are unavailable.

## Acceptance criteria

1. A versioned evaluation ledger names every source and separates technical
   readiness from unresolved human/release gates.
2. The current approved model registry, workflow, capture validator, portrait
   inventory, review queue, empty generation manifest, and visual registry are
   all source-bound and pass the existing technical validator.
3. Every current preview remains `unverified-preview`/`pending`, with null
   model, revision, license, card, sampler, seed, release path, release hash,
   and registry ID.
4. A promotion-shaped preview mutation fails validation rather than accepting
   guessed or incomplete provenance.
5. No runtime, asset, browser, simulation, history, replay, or authority path
   changes.

## Implementation steps

1. Add `docs/evaluation/phase13.1-ai-generation-metadata-boundary.json`.
2. Add `tests/test_phase13_1_ai_generation_metadata_boundary.py` with positive
   current-state checks and a fail-closed promotion mutation.
3. Update Phase 13.1 roadmap evidence, SPEC Present, CHANGELOG, LESSONS,
   presentation QA, and final handoff.
4. Bump package metadata from v0.13.56 to v0.13.57.
5. Run focused validator/test checks, then the repository's standard checks.

## Non-goals

- No fabricated metadata, image generation, human review, legal approval, or
  portrait promotion.
- No new GUI route, audio behavior, simulation mechanic, persistence, replay,
  asset registry entry, release file, or dependency.

## Review and handoff

The completed branch will receive one independent medium-effort code review,
then be committed, pushed, opened as a PR against `main`, merged, and cleaned
up locally and remotely as requested.
