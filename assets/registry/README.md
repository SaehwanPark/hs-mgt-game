# Asset registries

`visual-assets.json` and `audio-assets.json` use `asset-registry-v1` and are
checked by `scripts/validate_assets.py`. Their schemas are intentionally
dependency-free documentation and machine-readable guidance for future tooling.

Each entry also contains a `provenance` object. Repository-authored entries
use the local asset licensing policy and have null external URL/retrieval
fields; external and locally generated entries must provide an HTTPS source,
retrieval date, and license reference before they can be release-ready.

Use `scripts/generate_asset_credits.py` to inspect the deterministic attribution
projection. `--notices` renders the third-party notice projection and
`--runtime` renders the GUI's read-only credits module. Do not hand-edit
`assets/ASSET_CREDITS.md`, `assets/THIRD_PARTY_NOTICES.md`, or
`gui/asset-credits.mjs` without changing the registries and regenerating the
outputs.
