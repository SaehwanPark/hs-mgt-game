![screenshot](https://i.imgur.com/gfmOO3O.png)

# Health Policy Strategy Game

Health Policy Strategy Game is a command-line strategy simulation about leading
a fictional nonprofit US health system through financial pressure, workforce
constraints, payer negotiations, policy oversight, market competition, and
community trust.

The game is built around a simple thesis: health-policy outcomes are not direct
levers. They emerge from strategic responses by institutions with different
authority, incentives, information, and constraints.

The current public milestone is a playable Rust prototype at v0.12.28. Its
visual/audio Phase 8 readiness layer and Phase 9 deterministic capture-matrix
analysis are complete for bounded onboarding, settings, recovery, structured
capture diagnostics, and revision decision logging; Phase 10 adds keyboard
navigation, non-color status language, local text scaling, and optional cue
explanation controls; Phase 11 adds a host-authoritative competitive session
start/load handoff; Phase 12 adds generated visual identity and marker tokens
with explicit provenance. It is
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

Run the game:

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

Relevant blog posts:

- [A Management Game Where the Market Talks Back (design essay)](docs/blog-posts/health-policy-strategy-game.md): [Medium](https://medium.com/@saehwanpark/a-management-game-where-the-market-talks-back-388fb2955f26)

Start here:

- [How to Play](docs/how-to-play.md)
- [Core Loop Spec](docs/core-loop-spec.md)
- [Competitive Scenario Brief](docs/competitive-scenario-brief.md)
- [Design Principles](docs/design_principles.md)
- [Architecture](ARCHITECTURE.md)
- [Project Specification](SPEC.md)

Deeper project context:

- [Project Proposal](docs/proposal.md)
- [Roadmap](docs/roadmap.md)
- [Glossary](docs/glossary.md)
- [Evidence Registry](docs/evidence-registry.md)
- [Expansion Proposal Review](docs/expansion-proposal-review.md)
- [Architecture Decision Records](docs/decision-records/README.md)
- [MCP Agent Interface](docs/mcp-agent-interface.md)
- [Agent Playtest Protocol](docs/agent-playtest-protocol.md)
- [Visual/audio Phase 9 evaluation and revision](docs/visual-audio-phase9-ai-agent-evaluation-v0.12.25.md)
- [Visual/audio Phase 10 accessibility and visual-language hardening](docs/visual-audio-phase10-accessibility-v0.12.26.md)
- [Visual/audio Phase 11 first-session launch/load](docs/visual-audio-phase11-session-launch-v0.12.27.md)
- [Visual/audio Phase 12 visual identity and marker provenance](docs/visual-audio-phase12-visual-identity-v0.12.28.md)

Historical and internal development notes, including older playtest findings,
are kept in `docs/` for transparency. The previous developer-focused README is
archived at [docs/README-dev-archive-v0.1.61.md](docs/README-dev-archive-v0.1.61.md).

## Development

Run the standard checks:

```bash
python3 scripts/check_release_metadata.py
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

The release metadata command is documented in
[`docs/contributor-release-check.md`](docs/contributor-release-check.md).

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

A dependency-free browser thin-client proof is available in [`gui/`](gui/). It
can build and submit a host-validated competitive batch, review the committed
monthly resolution, and optionally play visible-only generated audio without
owning simulation state.
It renders injected MCP-shaped session data and, when an action adapter is
provided, builds host-validated canonical command batches. It does not replace
the CLI, host a live server, or own simulation state.

## License

[GPL-3](LICENSE)
