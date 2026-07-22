# Presentation Contract — Phase 9.2 audio playback fallback v0.12.83

## Goal and Authorization

When optional Web Audio setup or generated cue playback is unavailable, the
client must expose a deterministic local fallback descriptor and preserve the
cue's visible source and written equivalent. This is the bounded v0.12.83
Phase 9.2 runtime slice; it does not add recorded audio or change host
authority.

## Player Questions and Consequences

- Is audio available, muted, unsupported, or failed?
- What visible event or interface meaning remains available when sound cannot
  play?
- Does a playback exception stop only optional audio while the current visual,
  text, and session presentation remains usable?

The player consequence is presentation-only: unavailable sound never hides or
changes the host-reported event, action, observation, or outcome.

## Actor-Visible Source Ledger

| Semantic element | Authorized source | Missing/unknown behavior | Prohibited inference |
| --- | --- | --- | --- |
| Cue/music/ambience identity | Existing local audio catalog entry | Preserve `visible_source` and `equivalent`; use generic audio fallback when the ID is unknown | No inference of severity, intent, or outcome from a sound failure |
| Playback availability | Local Web Audio setup/playback result | Normalize unsupported, missing, failed, malformed, contradictory, and unknown results as unavailable | No host/session or decoder state is synthesized |
| Failure status | Local presentation state and `#audio-state` text | Announce that visual and written equivalents remain active | No command, transition, history, hash, or debrief mutation |

## Visual, Motion, and Audio Semantics

Successful generated tones retain the existing catalog identity and priority
rules. Unsupported setup or thrown playback switches to a visible text status
and an explicit fallback descriptor; no meaning depends on hearing the sound.
Mute, cues-only, reduced-notification, unfocused-page, and missing-audio states
retain the existing visible controls and text equivalents.

## Accessibility and Fallbacks

- Unsupported context creation returns an unavailable fallback without
  throwing through the client.
- Cue playback exceptions clear optional audio work and report the cue's written
  equivalent through the existing status region.
- Unknown or malformed catalog IDs use a generic “Audio unavailable” marker and
  never expose a release path.
- Color, motion, and sound are never the only channel for event meaning.

## Authority, History, and Replay Boundaries

Audio context, timers, playback failures, fallback descriptors, and status text
remain local browser presentation state. They never enter commands, host DTOs,
simulation transitions, stochastic inputs, observations, immutable history,
state hashes, replay artifacts, or debrief facts. A playback failure cannot
replace or retry a host transition.

## Asset Provenance and Release Requirements

No new asset or registry entry is authorized. Existing generated recipes and
written equivalents remain the sole local catalog inputs; pending portraits and
all external/license questions remain unchanged.

## Verification and Evidence Limits

Focused tests must cover unsupported setup, thrown cue playback, successful
recording, fallback descriptor fields, visible status text, and no-authority
markers. Existing audio, asset, release, documentation, Python, Rust,
formatting, Clippy, JavaScript, and diff checks remain required. Automated
checks do not establish measured loudness, browser compatibility, human
accessibility, fatigue, audio quality, learning, or policy validity.

## Non-Goals and Open Questions

- No recorded audio, file decoder, network fetch, audio download, or new audio
  asset is in scope.
- No catalog taxonomy, priority policy, music-state classifier, or host API is
  redesigned.
- Human listening and classroom/accessibility review remain open evidence gates.

---

# Presentation Contract — Phase 8.2 review-ready fictional actor portrait approval worksheet

## Goal and Authorization

Fictional actor portraits must be traceable from an approved local model and
prompt request through preserved source output, post-processing, human review,
and release-asset registry entry. This slice prepares a review-ready worksheet
for all seven preserved previews; it does not perform human review or promote
unverified outputs into the runtime or release manifest.

## Player Questions and Consequences

Portraits add only a bounded identity aid. Contributor-facing questions are:

- Can a contributor reproduce how an asset was created?
- Can a reviewer identify the model/license, prompt, seed, settings, source
  output, post-processing, and release derivative?
- Can the project reject resemblance, protected marks, clinical implausibility,
  missing alt text, incomplete provenance, or unreviewed release state?
- Can each portrait be disabled without losing written actor identity or role?
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
| Review queue | Per-role worksheet bound to preview ID/path/hash | Reviewer identity, date, decision, and every required gate must be explicit | A checked schema is not human approval |
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
this bounded preview slice.

## Verification and Evidence Limits

Focused tests must cover the role/style contract, prompt constraints, fallback
fields, review-queue bindings, and pending-review release gate. A fixture proof
must show all seven roles, per-role review gates, accessible equivalents,
small/grayscale checks, and the fail-closed release rule. Existing
generation, asset, credits, release, docs, Python, Rust, formatting, and
Clippy checks remain required. These checks do not establish legal clearance,
training-data provenance, output ownership, human resemblance, clinical
plausibility, accessibility, learning, or policy validity.

## Non-Goals and Open Questions

- No runtime portrait set or approved output asset is in scope until each
  per-portrait generation and human-review gate passes.
- `FLUX.1-schnell` is listed only as a local prototype candidate under its
  model-card license statement and access conditions; legal review remains
  required before release use.
- Future audio generation needs the same metadata schema but may require extra
  model/license fields and an acoustic human-review track.
