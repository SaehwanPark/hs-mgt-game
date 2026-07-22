# Implementation Plan — Visual/audio Phase 8.2 first fictional actor portrait slice v0.12.75

## 1. Task restatement

Implement a bounded first slice of the Phase 8.2 fictional actor portrait set:
define one shared portrait contract and prepare the rival-system-executive
candidate for review without allowing an unverified output into release.

## 2. Target slice

- Add a seven-role portrait-set contract with shared editorial style,
  composition, prohibited content, fallback, accessibility, small-size, and
  grayscale requirements.
- Add the first target role, `rival-system-executive`, with an exact prompt
  template and review fields.
- Add a dependency-free proof page and focused tests.
- Keep generation provenance connected to the Phase 8.1 validator. A candidate
  with unknown model identity or incomplete human review remains pending and is
  not added to the approved release manifest.

## 3. Acceptance criteria

- All seven roadmap roles are listed with stable IDs, labels, family, alt-text
  guidance, and generic fallback.
- The first role has chest-up/editorial/consistent-crop/neutral-background
  constraints and no real-person, logo, text, clinical-claim, or hidden-state
  language.
- The proof exposes the portrait contract, first prompt, review checks, and
  pending/release consequence without network or runtime host access.
- Existing generation validation rejects a candidate lacking approved model,
  hashes, human review, or an artifact-bound registry bridge.
- No portrait is promoted to runtime or release without the full Phase 8.1
  gate; no host/simulation/history/replay/debrief behavior changes.

## 4. Verification target

Focused portrait contract tests; generation workflow validation; asset/credits/
release/documentation checks; full Python tests; serial Rust tests; formatting;
Clippy; JavaScript syntax; and `git diff --check`.

## 5. Evidence limits

Contract and fixture checks are not evidence of human recognition,
cross-cultural interpretation, accessibility, quality, legal clearance,
clinical plausibility, or educational benefit. The candidate remains pending
until those reviews are performed and recorded.
