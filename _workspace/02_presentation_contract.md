# Presentation Contract — Phase 0 foundation v0.12.34

## Goal and Authorization

Authorized slice: close the visual/audio roadmap's Phase 0.1 product brief and
0.2 asset-repository foundation. This contract governs metadata and release
checks; it does not authorize new runtime assets or host changes.

## Player Questions and Consequences

The future first-month presentation must help the player answer: which visible
institution is involved, what changed, what remains in process, what is known or
uncertain, and where the next decision belongs. Registry metadata supports those
surfaces but is not itself player state.

## Actor-Visible Source Ledger

| Semantic family | Source | Timing/missingness | Client prohibition |
| --- | --- | --- | --- |
| Identity, marker, status token | `gui/visual.mjs`, current catalog | Visible fixture/host data; generic fallback | No hidden severity or intent inference |
| UI/event/music cue | `gui/audio.mjs`, visible transition/interaction | Visible event or explicit page stage; mute/unsupported fallback | No private rival or resolved-input mapping |
| Release asset metadata | `assets/registry/*.json` | Build/release time | Never enters commands, transitions, hashes, or replay |

## Visual, Motion, and Audio Semantics

Known semantic roles are validated against a fixed allowlist. Text labels and
symbols remain the meaning-bearing channel. Audio and motion are secondary,
short, and deterministic from visible inputs. The registry records the source,
role, accessible equivalent, and approval state for every registered unit.

## Accessibility and Fallbacks

The product brief requires keyboard operation, non-color status language, large
text support, reduced motion, complete written equivalents, mute, reduced
notifications, and generic missing-asset fallbacks. A registry or asset failure
blocks release validation; a runtime asset failure falls back to text/status
rendering.

## Authority, History, and Replay Boundaries

The asset scripts read files only. They do not parse or mutate simulation state,
call the network, resolve randomness, or affect history, hashes, replay, or
debrief output. Browser presentation remains downstream of actor-visible host
data and committed history.

## Asset Provenance and Release Requirements

Registries require stable IDs, semantic roles, source or generation metadata,
creator, license, attribution, approval, accessible equivalents, and source/
release hash fields. Hashes are checked against paths when present. Release
files under `assets/release/` must be named by a registry entry with approved
license metadata. The allowlist/denylist and AI-generation requirements are in
the product brief and `assets/README.md`.

## Verification and Evidence Limits

Focused Python tests exercise valid and invalid manifests, duplicate IDs,
unknown roles, stale hashes, missing metadata, release coverage, and generated
credits. CI checks the validator and credits. These are technical governance
checks; they do not prove visual quality, human accessibility, license counsel,
or learning outcomes.

## Non-Goals and Open Questions

No actual third-party or recorded assets are acquired here. Phase 1 must decide
the art-direction comparison evidence and SVG rendering proof. Later work must
revisit whether large source files need an external store before adding them.
