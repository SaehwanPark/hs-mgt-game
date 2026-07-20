![screenshot](https://i.imgur.com/gfmOO3O.png)

# Health Policy Strategy Game

Health Policy Strategy Game is a command-line strategy simulation about leading
a fictional nonprofit US health system through financial pressure, workforce
constraints, payer negotiations, policy oversight, market competition, and
community trust.

The game is built around a simple thesis: health-policy outcomes are not direct
levers. They emerge from strategic responses by institutions with different
authority, incentives, information, and constraints.

The current public milestone is a playable Rust prototype at v0.12.38. Its
visual/audio Phase 8 readiness layer and Phase 9 deterministic capture-matrix
analysis are complete for bounded onboarding, settings, recovery, structured
capture diagnostics, and revision decision logging; Phase 10 adds keyboard
navigation, non-color status language, local text scaling, and optional cue
explanation controls; Phase 11 adds a host-authoritative competitive session
start/load handoff; Phase 12 adds generated visual identity and marker tokens
with explicit provenance; Phase 13 adds a text-first first-month continuity
rail, and v0.12.30 closes the bounded technical first-month contract with
explicit evidence limits. v0.12.31 adds the loopback-only live GUI host and
player troubleshooting guide needed to run that competitive path from a normal
checkout, v0.12.32 reorganizes contributor documentation around current
guidance and indexed historical evidence, and v0.12.33 adds a reusable
presentation-contract and domain-QA agent harness for future visual/audio work
without starting another roadmap milestone, and v0.12.34 adds the product brief
and machine-checked asset provenance foundation for the next presentation
slices. v0.12.35 adds three committed art-direction reference variants and
selects a flat institutional SVG vocabulary for the next rendering proof.
v0.12.36 adds a deterministic, fixture-only SVG scene renderer and keyboard
proof page without changing the live host path. v0.12.37 adds a fixture-only
audio direction board with generated preview recipes, explicit sound
standards, and visible text equivalents without changing the live audio client.
v0.12.38 adds deterministic audio priority, cooldown, mode, and reduced-audio
policy controls to that fixture proof without changing the live audio client.
It is
intended for inspection, playtesting, portfolio review, and future educational design
work. It is not a calibrated policy forecast or a model of any real institution.

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
