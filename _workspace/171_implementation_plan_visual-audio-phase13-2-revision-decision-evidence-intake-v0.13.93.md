# Implementation Plan — Revision-decision evidence-intake packet v0.13.93

## Task restatement

Prepare the open `Record revision decisions` roadmap item with an empty,
privacy-bounded, source-bound intake contract for authorized synthesis of
future pilot, debrief-visual, and asset-provenance findings. Preserve the
existing runtime, presentation, asset, audio, simulation, and release
behavior; do not record or infer human findings, revision decisions, or
expansion approval.

## Current understanding

- `docs/evaluation/phase10.2-revision-log.md` is an empty human-evaluation
  template and explicitly says no participant findings have been collected.
- The pilot, debrief-visual, and asset-provenance packets now provide bounded
  source vocabularies but all contain zero records and pending decisions.
- The roadmap item remains unchecked because preparation is not a human
  revision decision.
- No public API, Rust transition, browser authority, asset registry, release
  manifest, or generated media change is required.

## Assumptions and stop conditions

- The three current evidence-intake packets remain empty, source-bound, and
  pending human evidence. If any source contains human records or a changed
  decision status before implementation, stop and report the mismatch.
- Revision records can use only bounded source IDs, canonical target IDs,
  finding categories, dispositions, priorities, action codes, and rationale
  codes; no free-text observation, identity, private state, or raw media is
  introduced.
- Stop if a source does not expose the target vocabulary needed for exact
  parity, if a new dependency is required, or if more than the listed files
  need production edits.

## Minimal implementation plan

1. Inspect the revision log, the three evidence-intake packets, pilot/debrief
   task catalogs, and current release/version checks to confirm exact markers
   and target IDs.
2. Add `docs/evaluation/phase13.2-revision-decision-evidence-intake-packet.json`
   with exact source contracts, a derived target catalog, bounded decision
   vocabulary, zero records, and a pending human-evidence decision.
3. Add
   `scripts/validate_revision_decision_evidence_intake.py` using only the
   standard library plus source-bound parity checks; reject unknown fields,
   target/source mismatch, private/free-text fields, duplicate categories,
   invalid dispositions/actions, numeric coercion, and premature decisions.
4. Add focused tests covering empty/pending state, source/target parity, one
   representative valid record shape, and each fail-closed boundary.
5. Bump the patch version to v0.13.93, regenerate the existing credits
   projections, and update the changelog, SPEC, roadmap, request summary,
   presentation contract, domain QA, presentation QA, final handoff, and
   lessons without checking the substantive roadmap item complete.
6. Run focused, full Python, serial Rust, formatting/clippy, asset/release,
   and documentation/version checks; then perform exactly one medium-effort
   code review before PR handoff.

## Files and functions likely to change

- `_workspace/171_implementation_plan_visual-audio-phase13-2-revision-decision-evidence-intake-v0.13.93.md`: this plan.
- `docs/evaluation/phase13.2-revision-decision-evidence-intake-packet.json`: empty source-bound packet.
- `scripts/validate_revision_decision_evidence_intake.py`: strict validator.
- `tests/test_phase13_2_revision_decision_evidence_intake.py`: focused parity and mutation tests.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `tests/test_release_metadata.py`: v0.13.93 projections.
- `CHANGELOG.md`, `SPEC.md`, `docs/visual_audio_enhancement_roadmap.md`: durable project status.
- `_workspace/00_input/request-summary.md`, `_workspace/02_presentation_contract.md`, `_workspace/03_domain_qa.md`, `_workspace/03_presentation_qa.md`, `_workspace/final/handoff.md`, `LESSONS.md`: slice bookkeeping and boundaries.
- `assets/ASSET_CREDITS.md`, `assets/THIRD_PARTY_NOTICES.md`, `gui/asset-credits.mjs`: regenerated existing projections only.

Avoid editing runtime, GUI, simulation, asset-registry, generation, audio,
release, or browser-policy files outside this list.

## Tests and checks

- `python3 -m unittest tests.test_phase13_2_revision_decision_evidence_intake`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/validate_revision_decision_evidence_intake.py`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/validate_assets.py`
- `python3 scripts/verify_asset_release.py --check`
- `cargo fmt --check`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test --quiet -- --test-threads=1`
- `git diff --check`

Expected result: the packet validator passes with `records: 0` and
`pending-human-evidence`; focused/full Python and serial Rust tests pass; no
substantive revision, evaluation, expansion, or public-release gate is
claimed complete.

## Acceptance criteria

- The packet derives allowed source/target IDs and finding categories from
  canonical existing sources and contains zero records.
- The validator rejects free text, private/identity/media/browser fields,
  source or target drift, invalid bounded vocabularies, duplicate lists,
  non-integer counts, and non-pending decision fields.
- Version, roadmap, SPEC, contracts, QA, handoff, credits, and lessons agree
  on v0.13.93 and explicitly distinguish preparation from human evidence.
- No runtime, simulation, GUI, asset, audio, browser, persistence, or release
  behavior changes.

## Non-goals

- Do not enter participant, reviewer, provenance, legal, accessibility,
  educational, audio, or visual findings.
- Do not infer or approve a revision, campaign expansion, asset promotion, or
  public release.
- Do not add dependencies, free-text storage, raw media, or new runtime APIs.

## Handoff requirements

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising. Report
files changed, tests run, deviations, and unresolved risks. Use one reviewer
with medium reasoning effort, merge the authorized PR into `main`, and remove
the temporary branch locally and remotely before re-auditing the roadmap.

## Risk label

Risk: medium

Reason: the slice connects three evidence sources and governs future privacy-
bounded decision records, but makes no runtime or release mutation.
