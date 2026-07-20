# Visual/audio asset contribution checklist

Before opening a pull request that adds or changes a visual or audio asset:

- Put editable inputs under `assets/source/` and approved derivatives under
  `assets/release/`; preserve generated outputs and metadata under
  `assets/generated/`.
- Add a stable ID to the matching visual or audio registry with a known semantic
  role, visible host source, accessible equivalent, creator, method,
  modifications, license, attribution, approval, and hashes.
- Use only the allowlisted license or `project-generated` basis. Do not add
  unclear, non-commercial, personal-use, redistribution-hostile, proprietary,
  or close-imitation assets.
- For AI generation, preserve model/license, prompt, seed or equivalent,
  settings, source output, post-processing, and human review metadata.
- Confirm meaning survives no color, reduced motion, mute, missing assets, and
  large text. Decorative assets must be labeled decorative.
- Run `python3 scripts/validate_assets.py` and
  `python3 scripts/generate_asset_credits.py --check`.

Asset metadata and presentation code must not add simulation state, command
legality, hidden-state inference, randomness, history, hashes, replay, or
debrief semantics to the browser.
