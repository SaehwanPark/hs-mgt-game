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
python3 scripts/generate_asset_credits.py --check
python3 scripts/generate_asset_credits.py --notices
```

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
