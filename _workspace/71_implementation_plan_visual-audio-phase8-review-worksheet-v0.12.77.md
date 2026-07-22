# Implementation Plan — Visual/audio Phase 8.2 review-ready portrait approval worksheet v0.12.77

## 1. Task restatement

Turn the seven preserved Phase 8.2 portrait previews into a review-ready,
per-role approval queue while keeping all approval and release decisions
fail-closed and human-owned.

## 2. Target slice

- Add one queue entry per canonical role, bound to the matching preview asset
  ID, role-derived source path, source hash, accessible equivalent, and
  generic fallback.
- Define explicit gates for identity-only meaning, role consistency,
  real-person resemblance, marks/text, anatomy/artifacts, accessibility,
  small-size, grayscale, approved model/seed provenance, release derivative,
  and registry bridge.
- Keep reviewer identity, review date, notes, decision, release path, release
  hash, and registry ID null/pending until an authorized human completes the
  work.
- Add a no-network static proof showing every role’s pending gates and generic
  fallback, with focused malformed/binding/promotion tests.

## 3. Acceptance criteria

- The queue has exactly seven unique role/asset entries matching the canonical
  portrait set and preview manifest.
- Each entry’s source path/hash, accessible equivalent, and generic fallback
  match the corresponding preview metadata; mismatches fail validation.
- Every gate is boolean and false, reviewer/decision fields are pending/null,
  and the queue cannot approve or register an asset while release eligibility
  is false.
- The proof and tests expose disabled/fallback behavior and do not fetch,
  submit commands, read host state, or add runtime authority.

## 4. Verification target

Queue validator and focused tests, generation/asset/credits/release/
documentation checks, full Python tests, serial Rust tests, formatting,
Clippy, JavaScript syntax, and `git diff --check`.

## 5. Evidence limits

The worksheet makes human review actionable and auditable but does not perform
human review. Automated schema, hash, and rendering checks do not establish
human resemblance, accessibility, legal clearance, training-data provenance,
output ownership, quality, learning, clinical plausibility, or policy validity.
