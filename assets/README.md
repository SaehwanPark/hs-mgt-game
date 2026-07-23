# Presentation asset repository

This directory separates editable sources from approved distributable assets.
The current GUI continues to use project-generated CSS/SVG tokens and Web Audio
recipes; this foundation does not add third-party files.

```text
assets/
  source/      original/editable inputs
  generated/   preserved generated outputs and generation metadata
  release/     approved derivatives shipped with a release
  registry/    visual/audio manifests and JSON schemas
```

Validate the repository with:

```bash
python3 scripts/validate_assets.py
python3 scripts/validate_asset_security.py
python3 scripts/verify_asset_release.py --check
python3 scripts/generate_asset_credits.py --check
python3 scripts/generate_asset_credits.py --notices
python3 scripts/generate_asset_credits.py --runtime
python3 scripts/check_asset_budget.py
python3 scripts/optimize_release_svg.py --check
python3 scripts/check_raster_scope.py
```

`assets/asset-budget.json` defines the explicit `asset-budget-v1` limits for
the tracked release SVG class and complete release package. The checker emits
a deterministic JSON report with file count, total bytes, largest file, and
pass/fail status. It measures only files under `assets/release`; source
references and generated portrait previews are outside this budget, and a
passing report is not a runtime performance, cache, decode, offline, or device
compatibility claim.

`assets/raster-scope.json` and `scripts/check_raster_scope.py` keep the current
release/preview boundary explicit: supported raster files are prohibited under
`assets/release`, while the seven unverified portrait previews are bounded and
remain outside release eligibility. A passing report is scope evidence, not a
raster-quality, decode, render, cache, device, or browser claim.

`assets/audio-packaging-scope.json` and `scripts/check_audio_packaging.py` keep
the current audio package boundary explicit: no file-backed audio is shipped,
and registered audio remains runtime-generated Web Audio with null release
paths. The compression decision is therefore `not-applicable-runtime-generated`.
The checker fails closed if a known audio file enters the release tree or a
registry entry gains a release path. This is package-scope evidence, not a
codec, loudness, decode, offline, device, browser, or human-quality claim.

`scripts/optimize_release_svg.py --check` verifies that every tracked release
SVG is idempotently normalized and that registry hashes and the release
manifest match. `--write` applies only outer/inter-tag whitespace normalization
to release derivatives, refreshes their registry hashes, and regenerates the
manifest; source SVGs and semantic content are not rewritten.

## Registry contract

Each entry has a stable ID, asset type, known semantic role, source or
generation method, creator, license, attribution, accessibility equivalent,
approval status, provenance, and source/release hash fields. A path-backed
source or release file must exist and match its recorded SHA-256 hash.
Runtime-generated recipes may omit a release path but must record how they are
generated.

The default license allowlist is `project-generated`, `CC0-1.0`, `CC-BY-4.0`,
`CC-BY-SA-4.0`, `MIT`, `Apache-2.0`, `GPL-3.0-or-later`, and `OFL-1.1`.
Unclear, personal-use-only, non-commercial-only, redistribution-hostile,
all-rights-reserved, proprietary-game, and unapproved assets are rejected.

The visual/audio maintainer owns semantic and accessibility review; the PR
reviewer checks the repository and metadata; the project maintainer approves
release use. Contributors must preserve source outputs and modification notes.
The static GUI's in-game credits disclosure is generated from the same registry
projection at `gui/asset-credits.mjs`; it is not a separate source of rights.
The security scanner checks bounded SVG content, binary dimensions, file sizes,
audio signatures, and release-only metadata without rewriting files. The
deterministic `assets/ASSET_RELEASE_MANIFEST.json` projection records the
approved release inventory; regenerate it with
`python3 scripts/verify_asset_release.py` and use `--check` in CI.
