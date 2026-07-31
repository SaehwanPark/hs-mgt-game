# Implementation Plan — Educational-usability evidence-intake packet v0.13.95

## Task restatement

Prepare the open `Educational usability reviewed` roadmap item with an empty,
privacy-bounded, source-bound intake contract for authorized educational and
classroom usability review. Preserve the existing gameplay, GUI, audio,
evaluation, and release behavior; do not record human results or claim that
educational usability has been reviewed.

## Current understanding

- The evaluation protocol, first-session packet, competitive campaign packet,
  pilot instrument, pilot intake, and debrief intake already define the
  technical tasks, reviewer categories, bounded ratings, accommodations, and
  finding categories needed for an educational review.
- The roadmap checkbox remains open because technical preparation is not human
  educational evidence, accessibility certification, classroom readiness, or a
  release decision.
- The prior pilot, debrief, asset, revision, and expansion packets are empty or
  explicitly pending; this slice should reference their boundaries without
  copying participant results.
- No Rust, GUI, simulation, browser, asset, audio, persistence, or release code
  change is required.

## Assumptions and stop conditions

- All referenced source packets remain empty or explicitly pending human
  evidence/approval. If a source contains human results or a changed decision,
  stop and report the mismatch.
- The intake uses only source-derived task IDs, reviewer categories, review
  statuses, rating dimensions/values, accommodation categories, and finding
  categories. It introduces no names, free text, raw media, private state,
  browser/session locations, or unbounded educational claims.
- Stop if source markers or canonical vocabularies cannot be bound exactly, if
  the packet would need to collect human findings, or if more than the listed
  files need production edits.

## Minimal implementation plan

1. Inspect the evaluation protocol, first-session and competitive review
   packets, pilot instrument/intake, debrief intake, revision intake, and
   preparation boundary to confirm exact source markers and pending states.
2. Add `docs/evaluation/phase13.2-educational-usability-evidence-intake-packet.json`
   with exact source contracts, source-derived educational tasks and rating
   dimensions, bounded review records, zero records, and pending educational
   review/go-no-go fields.
3. Add `scripts/validate_educational_usability_evidence_intake.py` using the
   standard library and existing packet validators; reject source drift,
   unsupported task/reviewer/status/value categories, private/free-text fields,
   numeric coercion, duplicate bounded lists, and premature decisions.
4. Add focused tests for empty/pending state, source and vocabulary parity, one
   representative bounded record, and fail-closed privacy, drift, type, and
   decision-boundary mutations.
5. Bump the patch version to v0.13.95, regenerate existing credits
   projections, and update changelog, SPEC, roadmap, request summary,
   presentation contract, domain QA, presentation QA, final handoff, and
   lessons while leaving the substantive educational-usability checkbox open.
6. Run focused, full Python, serial Rust, formatting/clippy, asset/release,
   and documentation/version checks; then perform exactly one medium-effort
   code review before PR handoff.

## Files and functions likely to change

- `_workspace/173_implementation_plan_visual-audio-phase13-2-educational-usability-evidence-intake-v0.13.95.md`: this plan.
- `docs/evaluation/phase13.2-educational-usability-evidence-intake-packet.json`: empty source-bound packet.
- `scripts/validate_educational_usability_evidence_intake.py`: strict validator.
- `tests/test_phase13_2_educational_usability_evidence_intake.py`: parity and mutation tests.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `tests/test_release_metadata.py`: v0.13.95 projections.
- `CHANGELOG.md`, `SPEC.md`, `docs/visual_audio_enhancement_roadmap.md`: durable project status.
- `_workspace/00_input/request-summary.md`, `_workspace/02_presentation_contract.md`, `_workspace/03_domain_qa.md`, `_workspace/03_presentation_qa.md`, `_workspace/final/handoff.md`, `LESSONS.md`: slice bookkeeping and boundaries.
- `assets/ASSET_CREDITS.md`, `assets/THIRD_PARTY_NOTICES.md`, `gui/asset-credits.mjs`: regenerated existing projections only.

Avoid editing runtime, GUI, simulation, asset-registry, generation, audio,
release, or browser-policy files outside this list.

## Tests and checks

- `python3 -m unittest tests.test_phase13_2_educational_usability_evidence_intake`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/validate_educational_usability_evidence_intake.py`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/validate_assets.py`
- `python3 scripts/verify_asset_release.py --check`
- `cargo fmt --check`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test --quiet -- --test-threads=1`
- `git diff --check`

Expected result: the packet validator passes with `records: 0` and
`pending-authorized-human-review`; focused/full Python and serial Rust tests
pass; no human educational, accessibility, classroom, legal, or public-release
gate is claimed complete.

## Acceptance criteria

- The packet derives its supported tasks, reviewer categories, rating
  dimensions/values, accommodations, finding categories, and privacy boundary
  from canonical existing sources and contains zero records plus a null
  educational-review decision.
- The validator rejects source/task/vocabulary drift, private/free-text fields,
  invalid bounded values, duplicate lists, non-integer counts, and premature
  educational or public-release decisions.
- Version, roadmap, SPEC, contracts, QA, handoff, credits, and lessons agree on
  v0.13.95 and distinguish technical preparation from human authorization.
- No runtime, simulation, GUI, asset, audio, browser, persistence, or release
  behavior changes.

## Non-goals

- Do not perform or claim educational, classroom, accessibility, audio, or
  first-time-user evaluation.
- Do not enter participant findings, identities, raw notes/media, revision
  decisions, expansion approval, legal clearance, or public-release approval.
- Do not add dependencies, free-text storage, raw media, or runtime APIs.

## Handoff requirements

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising. Report
files changed, tests run, deviations, and unresolved risks. Use one reviewer
with medium reasoning effort, merge the authorized PR into `main`, and remove
the temporary branch locally and remotely before re-auditing the roadmap.

## Risk label

Risk: medium

Reason: this slice formalizes a future educational review boundary across
several source contracts, but adds no runtime, participant, or release data.
