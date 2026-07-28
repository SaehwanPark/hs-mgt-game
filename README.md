![screenshot](https://i.imgur.com/gfmOO3O.png)

# Health Policy Strategy Game

Health Policy Strategy Game is a command-line strategy simulation about leading
a fictional nonprofit US health system through financial pressure, workforce
constraints, payer negotiations, policy oversight, market competition, and
community trust.

The game is built around a simple thesis: health-policy outcomes are not direct
levers. They emerge from strategic responses by institutions with different
authority, incentives, information, and constraints.

The current public milestone is a playable Rust prototype at v0.13.37.

The current visual/audio evidence also records the supported actor-visible GUI
screenshot surface and its deterministic SVG/structural regression boundary;
full-campaign raster screenshots and human visual-quality review remain open.
Current fictional portrait previews are inventory/hash-bound but remain
unverified and unreleased pending human review.
Their current role, source/hash, and written-equivalent metadata gates are
machine-checked; this does not approve the images.
The current source-checkout technical release contract is also machine-checked;
public-release and human evaluation gates remain open.
The current campaign-specific presentation inventory is recorded for
stabilization and regional affiliation; campaign-specific implementation and
human review remain open.
The reusable-asset matrix now records eligible shared primitives and keeps
direct campaign audio mapping and campaign-specific quality review open.
The current map/facility decision records no new asset requirement under the
present abstract/stage contracts, with future reopen triggers documented.
The current shared pressure/recovery taxonomy is registered against visible
catalogs; campaign-specific pressure design and direct audio mapping remain
open.
The current stabilization tutorial contract covers the CLI beginner flow and
guide; browser-native stabilization integration and human review remain open.
The current stabilization audio-state mapping joins the eight shared visible
pressure/recovery categories to existing optional music, event-cue, and
audio-direction contracts with written equivalents; direct campaign-envelope
audio and human quality review remain open. No runtime or authority boundary
changes.
The current stabilization debrief contract records the deterministic CLI
tradeoff/rationale/effect/revision presentation and host-authored shared
browser/end-session renderers; the live GUI remains competitive-only and
browser-native stabilization debrief quality, instructor-surface decisions,
and human educational review remain open. No runtime or authority boundary
changes.
The current stabilization accessibility evidence records shared technical
keyboard/focus, text/non-color status, text-scale, reduced-motion,
written-equivalent, and audio-fallback checks; the stabilization CLI remains
text-first and the live GUI remains competitive-only. Human accessibility,
screen-reader/device review, and educational usability remain open. No runtime
or authority boundary changes.
The current stabilization provenance audit records repository-authored and
runtime-generated reusable catalog sources, generated credits/notices,
release-manifest checks, the no-new-asset decision, and the unreleased portrait
preview boundary. Legal clearance, future asset provenance, human quality, and
public-release review remain open. No asset, runtime, or authority boundary
changes.
The current regional-affiliation partner identity evidence records host-reported
partner name/condition/stage fields, generic actor fallback, and the
identity-only unverified/unreleased partner portrait boundary. Partner-specific
art/audio, browser integration, and human quality/legal review remain open. No
new asset or runtime authority path changes.

The current regional-affiliation negotiation-stage evidence records the
host-owned `NegotiateCommitments` process label, commitment decision fields,
visible uncertainty, shared process/decision renderers, and optional
affiliation-negotiation audio. Browser-native affiliation integration,
stage-specific art/audio, hidden-state presentation, and human review remain
open. No new asset or runtime authority path changes.

The current regional-affiliation commitment/review evidence records visible
commitment metrics, partner response states, the pending institutional-review
process, submit/await decisions, reported review statuses, and optional
affiliation-negotiation audio. Browser-native review integration, state-specific
art/audio, hidden review deliberation, and human review remain open. No new
asset or runtime authority path changes.

The current regional-affiliation integration-state evidence records the
host-owned `IntegrateOrDecline` stage, integration-obligation process,
begin/decline decision, visible outcome statuses, and written consequence
boundary. Resolved integration drag and continuity shock remain outside the
actor observation; browser-native integration, state-specific art/audio, and
human review remain open. No new asset or runtime authority path changes.
The current regional-affiliation audio-motif evidence records the reusable
`affiliation_negotiation` music state, explicit `event.affiliation-milestone`
cue, visible triggers, generated-audio properties, and written/audio-off
fallback. Direct browser-native affiliation audio integration and human
listening/quality review remain open. No new audio content or runtime
authority path changes.
The current regional-affiliation stage-transition evidence records the typed
Assess partner → Choose posture → Negotiate commitments → Submit review →
Resolve review → Integrate or decline → Affiliation complete sequence, host
successors, legal command gates, visible labels, and replay-aligned history.
Browser-native affiliation sequencing, stage-specific presentation, and human
review remain open. No runtime authority path changes.
The current regional-affiliation replay/debrief evidence records versioned
replay artifact verification, host history/replay metadata, terminal debrief
content, decision-quality language, alternatives, and written rendering.
Browser-native affiliation replay/debrief views, durable persistence, and human
educational review remain open. No runtime authority path changes.
The current regional-affiliation provenance audit records reusable catalog and
registry sources, generated credits, release/security/audio packaging checks,
the no-new-asset decision, and unreleased portrait-preview gates. Legal,
training-data, human quality, and public-release review remain open. No asset
or runtime authority boundary changes.

Key capabilities include:
- **Interactive Campaigns**: Support for 5-turn executive stabilization (`stabilization-v1`), 24-month regional market competition (`competitive-regional-v1`), and 6-stage regional affiliation (`regional-affiliation-v1`) across CLI and GUI surfaces.
- **Deterministic Simulation Core**: Pure state transition core, explicit stochastic input derivation, actor-visible vs. true state separation, append-only history, and stable state hashing for deterministic replay verification.
- **Web-Based Presentation & Audio**: SVG-based regional map and facility rendering, operational overlays, synthesized Web Audio cues and environmental ambience, semantic information containers, and decision-quality debriefing.
- **Host & Packaging Security**: Host-authoritative, loopback-only local web host (`cargo run --bin hs-mgt-game-gui`), automated asset security scanning, manifest auditing, and offline package completeness.

It is intended for inspection, playtesting, portfolio review, and future educational design work. It is not a calibrated policy forecast or a model of any real institution.

## What You Can Play

- `stabilization-v1`: a five-turn executive stabilization campaign.
- `competitive-regional-v1`: a 24-month regional-market campaign with
  one human-led system, AI rival health systems, simultaneous monthly actions,
  lagged rival observability, a recurring operating consequence loop, and
  end-of-run debriefing.
- `regional-affiliation-v1`: an opt-in six-stage regional affiliation campaign
  with explicit partner observations, commitments, review, integration, replay,
  and educational debriefing.

All campaigns are deterministic for a given seed and set of choices. The
simulation separates true state from actor-visible observations, records
append-only history, and verifies replay through stable state hashes.

## Why It Exists

Most health-policy teaching tools make one part of the system legible at a
time: finance, operations, regulation, insurance, labor, or public policy. This
project asks the player to reason across those boundaries.

The design emphasizes:

- tradeoffs rather than a single score;
- incomplete information rather than omniscient dashboards;
- institutional actors rather than passive background conditions;
- delayed and stochastic effects that are resolved outside the deterministic
  transition core;
- debriefs that explain why outcomes happened and what the player knew at the
  time.

## Quickstart

Prerequisites:

- Rust toolchain with Cargo.

### Play in the terminal

Run all three campaigns through the CLI:

```bash
cargo run
```

Then choose:

- Enter or `1` for the stabilization campaign.
- `2` or `c` for the competitive campaign.
- `3` or `a` for the regional affiliation campaign.
- Enter for the default seed, or provide a numeric seed for a different
  deterministic run.

For a first session, start with `stabilization-v1` in beginner mode. For the
competitive campaign, Normal difficulty gives a compact introduction to monthly
action budgeting and rival pressure.

### Play in the GUI

The live GUI currently supports `competitive-regional-v1` only.

```bash
cargo run --bin hs-mgt-game-gui
```

Keep that terminal running, open the printed URL (normally
`http://127.0.0.1:7878`), select seed `42` and Normal difficulty, then choose
**Start competitive session**. Opening `gui/index.html` directly shows the
static demo and does not start a live scenario.

See [How to Play in GUI Mode](docs/guides/gui-how-to-play.md) for the complete first
month, audio controls, alternate ports, session lifetime, and troubleshooting.

See [Reproducible Distribution](docs/guides/reproducible-distribution.md) for
the canonical source-checkout contents, support boundaries, and release checks.

## Competitive Command Examples

Competitive mode uses short Stata-like commands. Commands can be chained with
semicolons.

```text
monitor target=northlake depth=1
recruit role=nurse headcount=4
invest domain=beds amount=20
negotiate payer=carrier_a rate_posture=neutral
commit pledge_type=access level=3
project kind=ehr_epic budget=60
hold
```

Example batch:

```text
monitor target=northlake depth=1; recruit role=nurse headcount=4
```

Type `?` or `help` inside the game for command guidance.

## Current Boundaries

This is a playable prototype, not a finished educational release.

Current limits:

- the campaign features local AI rivals or MCP agents with no network multiplayer;
- current numerical thresholds are documented abstractions, not empirically
  calibrated parameters;
- AI-agent playtest findings are validation aids for gameplay and explanation,
  not evidence of measured human learning.
- Phase 9 capture-matrix findings are deterministic technical/interface-task
  hypotheses; they do not automatically revise the interface or simulation.
- monthly demand, volume, revenue, and cost use visible game units rather than
  calibrated encounters or dollars.

The model should not be used for operational, clinical, financial, regulatory,
or policy decisions.

## Documentation

Contributors should start with the [documentation index](docs/README.md), which
provides separate software, game/domain-design, and validation paths while
keeping historical evidence out of the current instruction flow.

Players can go directly to [How to Play](docs/guides/how-to-play.md) or
[How to Play in GUI Mode](docs/guides/gui-how-to-play.md). The design essay
[A Management Game Where the Market Talks Back](docs/blog-posts/health-policy-strategy-game.md)
is also available on [Medium](https://medium.com/@saehwanpark/a-management-game-where-the-market-talks-back-388fb2955f26).

## Development

Run the standard checks:

```bash
python3 scripts/check_release_metadata.py
python3 scripts/check_documentation_links.py
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

The release metadata command is documented in
[`docs/guides/contributor-release-check.md`](docs/guides/contributor-release-check.md).
The complete source-checkout distribution decision is documented in
[`docs/guides/reproducible-distribution.md`](docs/guides/reproducible-distribution.md).

Run the local MCP server used for bounded agent playtesting:

```bash
cargo run --bin hs-mgt-game-mcp
```

Run the scripted playtest harness:

```bash
python3 scripts/run_automated_playtests.py
```

The codebase is intentionally CLI-first. Core simulation transitions should stay
deterministic, with randomness resolved into explicit inputs before transition
evaluation.

A dependency-free browser client is available in [`gui/`](gui/). The
`hs-mgt-game-gui` binary serves it with a loopback-only, in-memory host so a
player can start and play the competitive campaign. The client builds
host-validated batches, reviews committed resolution, and optionally plays
visible-only generated audio without owning simulation state. Direct static
serving remains available for fixture and externally injected-adapter work.

## License

[GPL-3](LICENSE)
