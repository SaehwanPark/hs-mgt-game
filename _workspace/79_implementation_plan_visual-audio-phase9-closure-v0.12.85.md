# Implementation Plan — Visual/audio Phase 9 technical closure v0.12.85

## Task restatement

Reconcile the Phase 9.1/9.2 roadmap checklist and evidence records with the
implemented technical gates, and add a small regression test that prevents the
roadmap from silently returning to an unchecked technical state.

## Current understanding

- The license/provenance validator, generated credits/notices, in-game credits
  projection, asset security scanner, release metadata audit, deterministic
  manifest, fallback contracts, and SVG derivative sanitizer are implemented.
- The roadmap still marks v0.12.78–v0.12.81 evidence as in progress and leaves
  the Phase 9.1/9.2 technical checklists unchecked.
- Human legal clearance, portrait approval, accessibility quality, decoder
  safety, and asset-quality review are intentionally not established by these
  automated gates.

## Assumptions

- “Complete” means the bounded technical automation and its repository evidence
  are implemented and passing; it does not mean a human legal or design audit.
- Current repository-authored assets have no external URL/retrieval-date
  requirement, while future external entries remain subject to validator rules.
- No registry, release hash, manifest, runtime module, or asset bytes need to
  change for this audit-only slice.

## Minimal implementation plan

1. Add a focused roadmap-evidence test for Phase 9 technical checklist closure,
   required evidence files, and explicit human-review limits.
2. Update the roadmap’s Phase 9.1/9.2 checklist and v0.12.78–v0.12.84 evidence
   statuses to reflect the passing technical gates.
3. Update request, presentation contract, QA, specification, architecture,
   README, changelog, lessons, version projections, and CI documentation.
4. Run the focused and full validation matrix, then hand off to exactly the
   existing sole reviewer before PR merge.

## Files and functions likely to change

- `tests/test_visual_audio_roadmap.py`: machine-checkable Phase 9 closure.
- `.github/workflows/ci.yml`: focused roadmap-evidence test.
- `docs/visual_audio_enhancement_roadmap.md`: checklist/status reconciliation.
- `_workspace/00_input/request-summary.md`,
  `_workspace/02_presentation_contract.md`, `_workspace/03_presentation_qa.md`:
  v0.12.85 audit contract and evidence.
- `SPEC.md`, `ARCHITECTURE.md`, `README.md`, `CHANGELOG.md`, `LESSONS.md`,
  `assets/ASSET_CREDITS.md`, `assets/THIRD_PARTY_NOTICES.md`,
  `gui/asset-credits.mjs`, `Cargo.toml`, `Cargo.lock`, and
  `tests/test_release_metadata.py`: version and release records.

No runtime or asset-registry implementation change is authorized.

## Tests and checks

- `python3 -m unittest tests.test_visual_audio_roadmap`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `python3 scripts/validate_assets.py`
- `python3 scripts/validate_asset_security.py`
- `python3 scripts/sanitize_svg_metadata.py --check-release`
- `python3 scripts/verify_asset_release.py --check`
- `python3 scripts/generate_asset_credits.py --check`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/check_documentation_links.py`
- JavaScript syntax, `cargo fmt --check`, Clippy, Rust tests, and `git diff --check`

## Acceptance criteria

- Phase 9.1 and 9.2 technical checklist entries are checked only where the
  existing validators/tests provide evidence.
- v0.12.78–v0.12.84 technical evidence is recorded as complete, with explicit
  legal, human-review, decoder, accessibility, ownership, and quality limits.
- The new regression test fails if a Phase 9 technical checklist reintroduces
  an unchecked item or drops the evidence/limit language.
- Version projections agree at v0.12.85; no registry/release/runtime bytes
  change except generated package-version projections.

## Non-goals and stop conditions

- Do not approve portraits, declare legal clearance, perform human evaluation,
  add external assets, rewrite registry/release bytes, or change runtime code.
- Stop if any technical checklist cannot be supported by existing evidence, or
  if this audit requires a new asset, dependency, host field, or simulation
  change.

## Review checklist

- Roadmap status language distinguishes automated completion from human gates.
- The regression test is evidence-oriented rather than a tautological count.
- Exactly one existing code reviewer reviews the final worktree.

## Risk label

Risk: low

Reason: this is a documentation/evidence reconciliation with a regression test;
it does not alter runtime, simulation, host authority, or canonical assets.
