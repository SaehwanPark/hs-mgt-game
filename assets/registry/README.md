# Asset registries

`visual-assets.json` and `audio-assets.json` use `asset-registry-v1` and are
checked by `scripts/validate_assets.py`. Their schemas are intentionally
dependency-free documentation and machine-readable guidance for future tooling.

Use `scripts/generate_asset_credits.py` to inspect the deterministic attribution
projection. Do not hand-edit `assets/ASSET_CREDITS.md` without changing the
registries and regenerating the output.
