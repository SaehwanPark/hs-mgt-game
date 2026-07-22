# Presentation Contract — Phase 8.2 fictional actor portrait slice

## Goal and Authorization

Fictional actor portraits must be traceable from an approved local model and
prompt request through preserved source output, post-processing, human review,
and release-asset registry entry. This first slice defines the set and prepares
one reviewable candidate; it does not promote an unverified output into the
runtime or release manifest.

## Player Questions and Consequences

Portraits add only a bounded identity aid. Contributor-facing questions are:

- Can a contributor reproduce how an asset was created?
- Can a reviewer identify the model/license, prompt, seed, settings, source
  output, post-processing, and release derivative?
- Can the project reject resemblance, protected marks, clinical implausibility,
  missing alt text, incomplete provenance, or unreviewed release state?
- Can a portrait be disabled without losing written actor identity or role?
- Does a future asset fail closed when source/release hashes or registry links
  are missing?

## Actor-Visible Source Ledger

| Workflow element | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Model and license | Approved local model registry and primary model card | Capture is rejected if model is not listed or license is not allowlisted | No assumption that model-card license clears training data or every output |
| Prompt/settings | Contributor request file and captured command metadata | Required prompt, negative prompt, seed, sampler, dimensions, and settings must be explicit | No reconstruction from an image or filename |
| Source output | Preserved local source file and hash | No release record without an existing hashed source output | No claim that a release derivative is the original |
| Human review | Checklist fields for resemblance, marks, plausibility, accessibility, and release | Approval remains pending until every required review field is true | No automated proxy for human approval |
| Registry bridge | Existing visual/audio asset registry ID | Approved output must point to a matching registry entry | No asset becomes release-safe merely by being generated |
| Portrait meaning | Explicit actor family/role and written label | Use generic actor marker and role text when the image is absent | No inference of score, severity, intent, outcome, or private action |

## Visual, Motion, and Audio Semantics

The portrait is an optional decorative identity aid, not a new authority or
information channel. The shared set uses non-photorealistic editorial,
chest-up, consistent-crop, neutral-institutional-background output with no
public-figure resemblance, protected marks, readable text, or clinical claim.
Generated assets must retain written labels, alt text, generic fallback,
disabled-asset behavior, small-size behavior, and grayscale behavior. They must
not encode hidden simulation state, future outcomes, clinical severity,
real-person identity, protected logos, or exact simulation parameters.

## Accessibility and Fallbacks

- Every portrait record requires an accessible equivalent/alt-text field and a
  generic actor-marker fallback plan.
- Every portrait must be checked at small size and grayscale before approval.
- Every future audio record requires a written equivalent, mute/unavailable
  fallback, and safe reduced-audio behavior.
- Missing source output, metadata, review, or release derivative blocks release;
  the application uses the existing generic/project-authored fallback.
- Prompt and post-processing records remain readable without an image viewer.

## Authority, History, and Replay Boundaries

Generation requests, seeds, outputs, hashes, approvals, and local model files
are contributor/release artifacts. They never enter simulation transitions,
actor observations, commands, history, state hashes, replay artifacts, or
debrief facts. A future asset may decorate a host-authoritative presentation
only after its asset-registry entry is approved.

## Asset Provenance and Release Requirements

The workflow records model name/version or immutable revision, model license and
source URL, generation application/version, prompt, negative prompt, seed,
sampler/settings, dimensions, date, contributor, post-processing, source image
references, source hash, optional release path/hash, human-review checklist,
approval status, and target visual/audio registry ID. The approved-model file
records the model-card review date, immutable repository revision, and scope
limitations. No model weights or hosted inference outputs are committed by
this first portrait slice.

## Verification and Evidence Limits

Focused tests must cover the role/style contract, prompt constraints, fallback
fields, and pending-review release gate. A fixture proof must show the seven
roles, the first target role, prompt/negative prompt constraints, accessible
equivalent, small/grayscale checks, and fail-closed release rule. Existing
generation, asset, credits, release, docs, Python, Rust, formatting, and
Clippy checks remain required. These checks do not establish legal clearance,
training-data provenance, output ownership, human resemblance, clinical
plausibility, accessibility, learning, or policy validity.

## Non-Goals and Open Questions

- No runtime portrait set or approved output asset is in scope until the
  per-portrait generation and human-review gate passes.
- `FLUX.1-schnell` is listed only as a local prototype candidate under its
  model-card license statement and access conditions; legal review remains
  required before release use.
- Future audio generation needs the same metadata schema but may require extra
  model/license fields and an acoustic human-review track.
