![screenshot](https://i.imgur.com/gfmOO3O.png)

# Health Policy Strategy Game

Health Policy Strategy Game is a command-line strategy simulation about leading
a fictional nonprofit US health system through financial pressure, workforce
constraints, payer negotiations, policy oversight, market competition, and
community trust.

The game is built around a simple thesis: health-policy outcomes are not direct
levers. They emerge from strategic responses by institutions with different
authority, incentives, information, and constraints.

The current public milestone is a playable Rust prototype at v0.10.47. It is intended for
inspection, playtesting, portfolio review, and future educational design work.
It is not a calibrated policy forecast or a model of any real institution.

## What You Can Play

- `stabilization-v1`: a five-turn executive stabilization campaign.
- `competitive-regional-v1`: a 24-month regional-market campaign with
  one human-led system, AI rival health systems, simultaneous monthly actions,
  lagged rival observability, and end-of-run debriefing.

Both campaigns are deterministic for a given seed and set of choices. The
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

Historical and internal development notes, including older playtest findings,
are kept in `docs/` for transparency. The previous developer-focused README is
archived at [docs/README-dev-archive-v0.1.61.md](docs/README-dev-archive-v0.1.61.md).

## Development

Run the standard checks:

```bash
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

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

## License

[GPL-3](LICENSE)
