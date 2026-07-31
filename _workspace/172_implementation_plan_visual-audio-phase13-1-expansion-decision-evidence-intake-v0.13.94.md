# Implementation Plan — Campaign-expansion decision evidence-intake packet v0.13.94

## Task restatement

Prepare the open `Approve or reject expansion to full campaign coverage`
roadmap item with an empty, privacy-bounded, source-bound intake for an
authorized expansion decision. Preserve the existing campaign-review,
first-session, pilot, debrief, asset, revision, runtime, and release behavior;
do not record a go/no-go outcome or claim that campaign expansion is approved.

## Current understanding

- The competitive campaign review packet already covers technical 24-month
  continuity and keeps human review, expansion, and public release pending.
- The first-session, pilot, debrief-visual, asset-provenance, and revision-
  decision packets are now separate empty/pending preparation boundaries.
- The roadmap’s expansion checkbox remains open because technical coverage and
  evaluation preparation are not an authorized product decision.
- No Rust, GUI, simulation, browser, asset, audio, persistence, or release
  code change is required.

## Assumptions and stop conditions

- All referenced source packets remain empty or explicitly pending human
  evidence/approval. If a source contains human results or a changed expansion
  decision before implementation, stop and report the mismatch.
- The expansion contract can use only bounded source IDs, gate IDs, outcome
  statuses, evidence-strength labels, blocker codes, and rationale codes; no
  free-text, identity, private-state, or raw-media field is introduced.
- Stop if source markers, campaign catalog, or gate statuses cannot be bound
  exactly, if a new dependency is required, or if more than the listed files
  need production edits.

## Minimal implementation plan

1. Inspect the competitive campaign review, first-session, pilot, debrief,
   asset-provenance, revision-decision, evaluation-protocol, and campaign-
   coverage sources to confirm exact markers and pending boundaries.
2. Add `docs/evaluation/phase13.1-expansion-decision-evidence-intake-packet.json`
   with exact source contracts, the three supported campaign IDs, bounded
   review gates/blockers/outcomes, zero records, and a pending go/no-go field.
3. Add `scripts/validate_expansion_decision_evidence_intake.py` using the
   standard library and existing packet validators; reject source drift,
   unsupported campaigns/gates, private/free-text fields, unknown statuses,
   numeric coercion, and premature expansion/public-release decisions.
4. Add focused tests for empty/pending state, source/gate/campaign parity, one
   representative gate record, and each fail-closed boundary.
5. Bump the patch version to v0.13.94, regenerate existing credits
   projections, and update changelog, SPEC, roadmap, request summary,
   presentation contract, domain QA, presentation QA, final handoff, and
   lessons while leaving the substantive expansion checkbox open.
6. Run focused, full Python, serial Rust, formatting/clippy, asset/release,
   and documentation/version checks; then perform exactly one medium-effort
   code review before PR handoff.

## Files and functions likely to change

- `_workspace/172_implementation_plan_visual-audio-phase13-1-expansion-decision-evidence-intake-v0.13.94.md`: this plan.
- `docs/evaluation/phase13.1-expansion-decision-evidence-intake-packet.json`: empty source-bound packet.
- `scripts/validate_expansion_decision_evidence_intake.py`: strict validator.
- `tests/test_phase13_1_expansion_decision_evidence_intake.py`: parity and mutation tests.
- `Cargo.toml`, `Cargo.lock`, `README.md`, `tests/test_release_metadata.py`: v0.13.94 projections.
- `CHANGELOG.md`, `SPEC.md`, `docs/visual_audio_enhancement_roadmap.md`: durable project status.
- `_workspace/00_input/request-summary.md`, `_workspace/02_presentation_contract.md`, `_workspace/03_domain_qa.md`, `_workspace/03_presentation_qa.md`, `_workspace/final/handoff.md`, `LESSONS.md`: slice bookkeeping and boundaries.
- `assets/ASSET_CREDITS.md`, `assets/THIRD_PARTY_NOTICES.md`, `gui/asset-credits.mjs`: regenerated existing projections only.

Avoid editing runtime, GUI, simulation, asset-registry, generation, audio,
release, or browser-policy files outside this list.

## Tests and checks

- `python3 -m unittest tests.test_phase13_1_expansion_decision_evidence_intake`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/validate_expansion_decision_evidence_intake.py`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/validate_assets.py`
- `python3 scripts/verify_asset_release.py --check`
- `cargo fmt --check`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo test --quiet -- --test-threads=1`
- `git diff --check`

Expected result: the packet validator passes with `records: 0` and
`pending-human-evidence`; focused/full Python and serial Rust tests pass; no
human expansion, campaign, legal, or public-release gate is claimed complete.

## Acceptance criteria

- The packet derives supported campaigns and source statuses from canonical
  existing sources and contains zero records plus a null go/no-go decision.
- The validator rejects source/gate/campaign drift, private/free-text fields,
  invalid bounded values, duplicate lists, non-integer counts, and premature
  expansion/public-release decisions.
- Version, roadmap, SPEC, contracts, QA, handoff, credits, and lessons agree
  on v0.13.94 and distinguish technical preparation from human authorization.
- No runtime, simulation, GUI, asset, audio, browser, persistence, or release
  behavior changes.

## Non-goals

- Do not approve, reject, or infer expansion to the full campaign.
- Do not enter participant, visual, audio, educational, accessibility,
  provenance, legal, or public-release findings.
- Do not add dependencies, free-text storage, raw media, or runtime APIs.

## Handoff requirements

Implement exactly this plan. Do not broaden scope. If the plan conflicts with
the codebase, stop and report the conflict instead of improvising. Report
files changed, tests run, deviations, and unresolved risks. Use one reviewer
with medium reasoning effort, merge the authorized PR into `main`, and remove
the temporary branch locally and remotely before re-auditing the roadmap.

## Risk label

Risk: medium

Reason: this slice joins several evaluation and campaign-coverage boundaries
for a future product decision, but introduces no runtime or release mutation.
