# Presentation Contract — Phase 8.1 approved local generation workflow

## Goal and Authorization

Future generated assets must be traceable from an approved local model and
prompt request through preserved source output, post-processing, human review,
and release-asset registry entry. This slice authorizes the workflow and
validation boundary only; no generated asset is produced or shipped.

## Player Questions and Consequences

This workflow does not add a player-facing signal. Its contributor-facing
questions are:

- Can a contributor reproduce how an asset was created?
- Can a reviewer identify the model/license, prompt, seed, settings, source
  output, post-processing, and release derivative?
- Can the project reject resemblance, protected marks, clinical implausibility,
  missing alt text, incomplete provenance, or unreviewed release state?
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

## Visual, Motion, and Audio Semantics

The workflow is presentation governance, not a new runtime presentation channel.
Prompt templates must describe fictional, non-photorealistic, editorial or
otherwise approved output goals. Generated assets must retain written labels,
alt text, generic fallback, and disabled-asset behavior in their eventual
presentation contract. Assets must not encode hidden simulation state, future
outcomes, clinical severity, real-person identity, protected logos, or exact
simulation parameters.

## Accessibility and Fallbacks

- Every future visual asset record requires an accessible equivalent/alt-text
  field and a generic fallback plan.
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
records the model-card review date and scope limitations. No model weights or
hosted inference outputs are committed.

## Verification and Evidence Limits

Focused tests must capture a complete record, compute source/release hashes,
reject unknown models and missing fields, reject unapproved releases, validate
registry bridges, and preserve a pending-review state. A fixture proof must
show the metadata contract, prompt template, human checklist, model/license
scope, and fail-closed release rule. Existing asset, credits, release, docs,
Python, Rust, formatting, and Clippy checks remain required. These checks do
not establish legal clearance, training-data provenance, output ownership,
human resemblance, clinical plausibility, accessibility, learning, or policy
validity.

## Non-Goals and Open Questions

- No generated portrait set or other output asset is in scope; Phase 8.2 must
  separately authorize roles, prompts, outputs, and per-portrait review.
- `FLUX.1-schnell` is listed only as a local prototype candidate under its
  model-card license statement and access conditions; legal review remains
  required before release use.
- Future audio generation needs the same metadata schema but may require extra
  model/license fields and an acoustic human-review track.
