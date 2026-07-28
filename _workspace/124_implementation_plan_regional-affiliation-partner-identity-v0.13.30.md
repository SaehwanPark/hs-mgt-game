# Implementation Plan — Phase 12 regional affiliation partner identity v0.13.30

## Task restatement

Continue Phase 12.2 with a bounded current partner-identity treatment record
for `regional-affiliation-v1`. Bind host-reported partner identity, existing
actor-family/generic fallback language, the identity-only portrait preview
inventory, written equivalents, and the live GUI boundary without promoting an
unverified portrait or inventing a new partner asset.

## Current understanding

- The affiliation campaign coverage projection exposes a host-reported
  partner name, condition, role, and written signal.
- Existing actor-family and generic-actor catalogs provide source-linked
  identity/role markers and fallbacks; the affiliation partner portrait is an
  identity-only preview and remains unverified/unreleased.
- The shared browser campaign renderer can display supplied partner fields, but
  the live GUI launcher remains competitive-regional-v1 only.

## Target slice

Add `docs/evaluation/phase12-regional-affiliation-partner-identity.json` and a
parity test that records:

- host partner identity/condition source and written equivalent;
- actor-family/generic fallback and identity-only portrait-preview boundary;
- current shared GUI campaign-coverage and live-launch boundaries;
- no-new-asset/provenance decision; and
- open work for partner-specific art/audio, quality, and human review.

## Assumptions

- This is current identity-treatment evidence, not a new partner art or audio
  implementation.
- A portrait preview is decoration only and cannot establish identity,
  resemblance, quality, or release eligibility.
- Partner facts and conditions remain host-authored and actor-visible; no
  private intent or future agreement is inferred.

## Minimal implementation plan

1. Add the partner-identity ledger and source-parity test.
2. Check only current regional-affiliation partner-identity evidence in Phase
   12.2 and synchronize canonical docs, lessons, version metadata, generated
   credits, and additive request/contract/QA/handoff records.
3. Run focused/full Python/Rust/lint/release/documentation/generation/asset/
   offline/browser/device/visual-audio checks.
4. Use one reviewer in three passes, open/merge the PR, remove the temporary
   branch locally/remotely, and reassess the next roadmap item.

## Non-goals

- Do not add/promote the portrait preview, new partner art/audio, route,
  runtime field, persistence, screenshot, instructor view, or human study.
- Do not infer partner intent, agreement probability, true condition, quality,
  resemblance, legal clearance, or public release.

## Stop conditions

Stop if current partner identity cannot be source-linked with generic/written
fallbacks without adding an asset, runtime authority path, or human judgment.

## Risk label

Risk: low

Reason: The slice records existing host, actor-family, fallback, and preview
metadata boundaries without changing assets, runtime behavior, or authority.
