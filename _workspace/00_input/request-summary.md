# Request Summary — Visual/audio Phase 8.2 first fictional actor portrait slice v0.12.75

## Authorized outcome

Complete the first bounded Phase 8.2 portrait slice: define the coherent
fictional actor-portrait contract and prepare a reviewable rival-system
executive candidate without leaking outcome, severity, or hidden state through
the image. Preserve provenance, reproducibility, human review, and release
gates. Do not approve a portrait for runtime/release until the Phase 8.1
metadata validator accepts its source/release hashes, model revision, registry
bridge, and human-review fields.

## Target slice

- Define the seven-role portrait set and shared editorial style contract.
- Define the first target role as a rival system executive with a chest-up,
  consistent-crop, neutral institutional-background composition.
- Capture the exact portrait prompt, negative prompt, seed, settings, source
  output, post-processing, accessible equivalent, and fallback requirements.
- Add portrait-set proof and focused contract tests while keeping approval
  fail-closed through the Phase 8.1 generation validator.
- Keep the first candidate outside the approved release manifest if its model
  identity or human review cannot be verified in this environment.

## Sources

- `docs/visual_audio_enhancement_roadmap.md` — Milestone 8.2.
- `assets/registry/visual-assets.json` and `assets/registry/audio-assets.json`.
- `assets/generation/approved-models.json` and the Phase 8.1 capture/validation
  scripts.
- `docs/design_principles.md` and `LESSONS.md` — actor-visible, provenance,
  accessibility, and evidence boundaries.

## Non-goals

- Do not change live GUI authority, host DTOs, simulation, history, replay, or
  debrief behavior.
- Do not treat a portrait as a metric, severity indicator, hidden-state
  channel, future-outcome cue, or real-person representation.
- Do not approve a generated output without human review, source preservation,
  hash capture, resemblance/logo/trademark/clinical plausibility/accessibility
  checks, and registry approval.

## Validation target

Capture/validate CLI tests, approved-model and schema fixture checks, registry
bridge checks, prompt/checklist proof checks, existing asset/credits/release/
documentation checks, full Python/Rust tests, formatting, Clippy, and diff
checks.

## Evidence limits

The model-card review supports workflow metadata only; it is not legal advice,
training-data provenance, output ownership, or a human resemblance/clinical
review. Automated hashes and schema checks establish auditability mechanics,
not asset quality, educational value, policy validity, or release clearance.
