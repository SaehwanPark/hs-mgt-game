# Request Summary — Visual/audio Phase 8.2 remaining actor portrait previews v0.12.76

## Authorized outcome

Complete the second bounded Phase 8.2 portrait slice: prepare the remaining
six fictional actor-role previews under the existing coherent portrait
contract, without leaking outcome, severity, or hidden state through the image.
Preserve provenance, reproducibility, human review, and release gates. Do not
approve any portrait for runtime/release until the Phase 8.1 metadata validator
accepts its source/release hashes, model revision, registry bridge, and
portrait-specific review fields.

## Target slice

- Define the seven-role portrait set and shared editorial style contract.
- Prepare payer negotiator, regulator, labor representative, community leader,
  board chair, and affiliation partner executive previews with the same
  chest-up, consistent-crop, neutral institutional-background composition.
- Capture the exact portrait prompt, negative prompt, seed, settings, source
  output, post-processing, accessible equivalent, and fallback requirements.
- Add portrait-set proof and focused contract tests while keeping approval
  fail-closed through the Phase 8.1 generation validator.
- Keep every candidate outside the approved release manifest if its model
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
