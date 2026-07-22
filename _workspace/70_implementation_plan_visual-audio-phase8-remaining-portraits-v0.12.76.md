# Implementation Plan — Visual/audio Phase 8.2 remaining actor portrait previews v0.12.76

## 1. Task restatement

Complete the remaining six role previews in the Phase 8.2 fictional actor
portrait set while preserving the identity-only contract and fail-closed
provenance boundary established in v0.12.75.

## 2. Target slice

- Add previews for payer negotiator, regulator, labor representative, community
  leader, board chair, and affiliation partner executive.
- Record a role-specific prompt and negative prompt, source hash, dimensions,
  capture date, contributor, accessible equivalent, generic fallback, and
  portrait review fields for every preview.
- Keep all six previews outside the visual registry, release directory, runtime
  GUI, and generation manifest when the preview tool does not expose approved
  local model/seed provenance.
- Extend proof/tests so all seven canonical roles and all preview boundaries
  remain machine-checked.

## 3. Acceptance criteria

- The preview set has exactly one entry for each of the seven canonical role
  IDs, with no duplicate role or asset ID.
- Each new entry is a valid PNG with matching source hash/dimensions and a
  role-specific identity-only prompt, accessible equivalent, and fallback.
- Every unverified preview remains pending with null model/seed/registry/release
  fields; the validator rejects any attempted unreviewed promotion.
- No host/simulation/history/replay/debrief/runtime GUI authority changes.

## 4. Verification target

Portrait validator, focused malformed/set/hash tests, generation/asset/credits/
release/documentation checks, full Python tests, serial Rust tests, formatting,
Clippy, JavaScript syntax, and `git diff --check`.

## 5. Evidence limits

Preview packaging does not establish human recognition, legal clearance,
training-data provenance, output ownership, quality, lived accessibility,
clinical plausibility, learning, or policy validity. Human review and approved
local generation provenance remain release gates.
