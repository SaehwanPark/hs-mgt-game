# Implementation Plan — Visual/audio Phase 12 visual identity and marker provenance v0.12.28

## 1. Task restatement

Add a small, deterministic visual catalog and use it to label the existing
regional map, entity/facility detail, overlays, and visible process rows. Keep
all host data, simulation behavior, and asset boundaries unchanged. Close the
merged Phase 11 SPEC record while recording Phase 12 as the active bounded
slice.

## 2. Current understanding

`gui/app.mjs` currently renders generic Unicode icons directly from fixture or
host-derived data. `createStatus` already supplies text plus non-color symbols.
`gui/audio-catalog.json` and `gui/ASSET_CREDITS.md` establish the convention for
machine-readable, project-generated presentation provenance. No host or Rust
change is needed.

## 3. Assumptions

- Exact visible IDs `riverside`, `northlake`, and `summit` are the only named
  identity mappings required by this slice.
- Existing fixture and host-derived regional data remain compatible.
- If the implementation needs a new DTO field, hidden-state boundary, or
  dependency, stop and report rather than broadening the slice.

## 4. Minimal implementation plan

1. Add `gui/visual.mjs` with a frozen `visual-catalog-v1` object and pure
   `visualIdentityFor`/`visualMarkerFor` lookup helpers with generic fallback.
2. Add `gui/visual-catalog.json` and extend `gui/ASSET_CREDITS.md` with the
   project-generated visual registry/provenance record.
3. Import the helpers in `gui/app.mjs`; add a small token renderer and attach
   identity/marker tokens to existing map, detail, facility, overlay, and
   process rows without removing source or status text.
4. Add `tests/test_gui_visual_identity.py` for registry coverage, Node behavior,
   semantic labels, unknown fallback, and boundary exclusions.
5. Update GUI/project docs, SPEC Phase 11 closure, Phase 12 active record,
   changelog, lessons, and version metadata to `0.12.28`.

## 5. Files and functions likely to change

- `gui/visual.mjs`: catalog and pure lookup helpers.
- `gui/visual-catalog.json`: machine-readable registry.
- `gui/ASSET_CREDITS.md`: generated visual provenance.
- `gui/app.mjs`: `renderMap`, `renderSelectedEntity`,
  `renderRegionalOverlays`, and visible process rendering; export catalog
  helpers through the existing GUI namespace.
- `gui/index.html`: token styling only, with responsive/accessibility-safe
  text and symbol treatment.
- `tests/test_gui_visual_identity.py`: focused contract and behavior tests.
- `gui/README.md`, `ARCHITECTURE.md`, `README.md`, `SPEC.md`, `CHANGELOG.md`,
  `LESSONS.md`, and Phase 12 protocol/handoff docs.
- `Cargo.toml`, `Cargo.lock`, and release metadata tests: patch version only.

## 6. Tests and checks

- Focused visual identity tests and existing GUI visual/audio/accessibility
  tests.
- `python3 -m unittest discover -s tests -p 'test_*.py'`.
- `node --check gui/visual.mjs && node --check gui/app.mjs`.
- `cargo fmt -- --check`, `cargo test --all -- --test-threads=1`,
  `cargo clippy --all-targets -- -D warnings`.
- `python3 scripts/check_release_metadata.py` and `git diff --check`.

## 7. Acceptance criteria

- The catalog has three named system identities, all required marker categories,
  status entries, stable IDs, and project-generated provenance.
- Known systems render identity label plus symbol; unknown or missing values
  render a generic labeled token rather than a guessed identity.
- Facility, overlay, and process rows expose category markers while retaining
  visible source/status/equivalent text.
- Tokens are semantic and keyboard/screen-reader compatible; color is not the
  sole distinction.
- No Rust/MCP source, host envelope, command, transition, stochastic input,
  history/hash/replay/debrief, network, or external asset changes occur.
- Focused and full checks pass, and Phase 11 is documented as merged/closed.

## 8. Non-goals

- No actual image/audio downloads, licensed asset acquisition, map geometry,
  animation, dynamic status calculation, browser transport, or human study.
- No campaign-specific identity system or new host DTO field.
- No broad UI redesign or opportunistic refactor.

## 9. Stop conditions

- Stop if identity requires hidden or newly authoritative host data.
- Stop if generic fallback cannot preserve explicit missingness.
- Stop if the change requires a public API/MCP schema, dependency, simulation,
  or cross-campaign architecture decision.
- Stop if unrelated tests fail for reasons outside this slice.

## 10. Review checklist

- Verify the diff is limited to visual presentation/provenance and Phase 11
  bookkeeping.
- Verify exact known IDs and conservative fallback do not expose private rival
  state or infer severity.
- Verify symbols always have text/semantic labels and existing source/status
  text remains available.
- Verify registry and credits contain no third-party claims or untracked asset
  paths.
- Verify focused tests exercise known, unknown, empty, and host-shaped paths.
- Run exactly one general code-review pass for this item and fix its findings;
  do not run a second pass.

## 11. Risk label

Medium — multiple existing render call sites and a user-visible semantic
catalog change, but no public host API or simulation state change.
