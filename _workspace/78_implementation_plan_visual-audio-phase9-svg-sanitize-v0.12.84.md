# Implementation Plan — Visual/audio Phase 9.2 SVG metadata sanitizer v0.12.84

## Task restatement

Add a dependency-free SVG metadata transform and a read-only approved-release
check while preserving current canonical asset bytes, registry hashes, runtime
behavior, and accessibility title/description content.

## Current understanding

- `scripts/validate_asset_security.py` currently rejects `<metadata>` in SVGs;
  it does not provide a transformation.
- `scripts/verify_asset_release.py` owns approved release-path discovery and
  canonical-root/symlink checks.
- All current release files are SVGs and already contain no removable metadata;
  the new check should therefore be a no-op on repository assets.

## Assumptions

- The sanitizer input is UTF-8 XML/SVG and `<metadata>` is the only removable
  element in this slice.
- Sanitized output is written only when the caller supplies a distinct output
  path; `--check-release` never writes.
- Existing title/description elements are accessibility content and must be
  preserved byte-for-byte.

If an assumption is false, stop and report the mismatch before editing.

## Minimal implementation plan

1. Inspect current release-path helpers and security messages; reuse their
   canonical-root and symlink protections rather than duplicating unsafe path
   logic.
2. Add `scripts/sanitize_svg_metadata.py` with pure `sanitize_svg_bytes`, a
   safe explicit-output CLI, and `--check-release` over approved SVG release
   paths.
3. Add `tests/test_svg_metadata_sanitizer.py` for metadata removal,
   title/description preservation, malformed/unbalanced input, output path
   rejection, and current release parity.
4. Wire the read-only release check into CI and update v0.12.84 version,
   roadmap, specification, architecture, QA, changelog, README, lessons, and
   contributor guidance.
5. Run the complete validation matrix and stop if raster/audio transformation,
   canonical asset rewriting, or a new dependency becomes necessary.

## Files and functions likely to change

- `scripts/sanitize_svg_metadata.py`: transform, approved-release discovery,
  safe output CLI, and check reporting.
- `assets/generation/svg-derivatives/.gitkeep`: establishes the empty,
  explicit derivative boundary without approving an asset.
- `tests/test_svg_metadata_sanitizer.py`: focused transform and boundary tests.
- `.github/workflows/ci.yml`: read-only sanitizer release check.
- `_workspace/00_input/request-summary.md`: current slice framing.
- `_workspace/02_presentation_contract.md`: asset transformation contract.
- `_workspace/03_presentation_qa.md`: QA evidence and limits.
- `docs/visual_audio_enhancement_roadmap.md`: v0.12.84 target/evidence.
- `SPEC.md`, `ARCHITECTURE.md`, `README.md`, `CHANGELOG.md`, `LESSONS.md`,
  `docs/guides/asset-contribution-checklist.md`: version and boundary records.

Avoid editing files outside this list unless the plan is incomplete; if that
happens, stop and explain why.

## Tests and checks

- `python3 -m unittest tests.test_svg_metadata_sanitizer tests.test_asset_security tests.test_asset_release`
- `python3 scripts/sanitize_svg_metadata.py --check-release`
- `python3 scripts/validate_assets.py`
- `python3 scripts/validate_asset_security.py`
- `python3 scripts/verify_asset_release.py --check`
- `python3 scripts/generate_asset_credits.py --check`
- `python3 scripts/check_release_metadata.py`
- `python3 scripts/check_documentation_links.py`
- `python3 -m unittest discover -s tests -p 'test_*.py'`
- `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`,
  `cargo test -- --test-threads=1`, and `git diff --check`

Expected result: all checks pass and the canonical release tree plus manifest
remain byte/hash unchanged.

## Acceptance criteria

- Sanitizing a valid SVG removes metadata elements while preserving title,
  description, geometry, and non-metadata bytes.
- Malformed XML, unbalanced metadata, unsafe output paths, symlinked paths,
  missing inputs, and output collisions fail closed without partial output.
- `--check-release` passes on current approved SVGs and never rewrites them.
- CI runs the read-only release check; no registry hash, release manifest,
  runtime module, host field, command, simulation state, history, replay, or
  debrief data changes.
- Documentation states that sanitization is a technical transform, not legal,
  accessibility, decoder, or human-review evidence.

## Non-goals

- Do not transform raster or audio metadata.
- Do not mutate canonical assets, update hashes automatically, promote output,
  or add a dependency.
- Do not redesign security scanning, manifest generation, or asset registries.
- Do not perform opportunistic cleanup or unrelated formatting.

## Stop conditions

Stop and report if the implementation requires XML libraries not already
available, modifies a registry-controlled file, changes release hashes or the
manifest, or needs raster/audio parsing. Stop if more than one production
script or two unrelated documentation areas need expansion.

## Review checklist

- Transform is deterministic and preserves accessibility elements.
- Check mode is read-only and shares canonical release-root safety rules.
- Failure paths cannot create partial/colliding output or approve an asset.
- Tests use concrete malicious/malformed fixtures rather than only happy-path
  current files.
- The diff remains limited to the planned script, tests, CI, and records.
- Exactly one read-only code reviewer will inspect the final worktree before
  PR merge.

## Risk label

Risk: medium

Reason: the change handles release-file transformation and path safety, but does
not alter canonical assets, runtime code, public APIs, or simulation authority.
