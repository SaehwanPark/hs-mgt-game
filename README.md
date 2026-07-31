# Health Policy Strategy Game

Health Policy Strategy Game is a strategy simulation about leading a fictional
nonprofit US health system through financial pressure, workforce constraints,
payer negotiations, policy oversight, market competition, and community trust.

The current public milestone is a playable Rust prototype at v0.13.85.

Health-policy outcomes are not direct levers here. Other institutions respond
to your choices based on their own authority, incentives, information, and
constraints. You make tradeoffs with incomplete information, live with delayed
consequences, and review what happened in an educational debrief.

![Terminal view of the game's executive report and competitive command entry](https://i.imgur.com/gfmOO3O.png)

## Start Here

You need a Rust toolchain with Cargo. From the repository root, run:

```bash
cargo run
```

For a friendly first session:

1. Press Enter or choose `1` for `stabilization-v1`.
2. Press Enter for the default deterministic seed.
3. Choose beginner mode.

The stabilization campaign is a short, five-turn introduction. The game
explains the available choices as you play, and `?` or `help` shows guidance
when you need it.

## What You Can Play

- `stabilization-v1` — a five-turn executive stabilization campaign and the
  recommended starting point.
- `competitive-regional-v1` — a 24-month regional-market campaign with AI
  rivals, simultaneous monthly actions, and lagged information.
- `regional-affiliation-v1` — a six-stage affiliation campaign covering
  partner assessment, commitments, review, integration, and debriefing.

Every campaign is deterministic for the same seed and choices. The simulation
keeps actor-visible information separate from its underlying state, records an
append-only history, and supports replay verification.

## Optional GUI

The live GUI currently supports `competitive-regional-v1`,
`stabilization-v1`, and `regional-affiliation-v1`:

```bash
cargo run --bin hs-mgt-game-gui
```

Keep that terminal running and open the printed URL, normally
`http://127.0.0.1:7878`. Choose seed `42`, Normal difficulty, and
**Start competitive session**.

Opening `gui/index.html` directly shows demo data; it does not start a live
scenario.

See [How to Play in GUI Mode](docs/guides/gui-how-to-play.md) for the complete
first month, settings, alternate ports, and troubleshooting.

## Current Boundaries

This is a playable research and educational prototype, not a finished
educational release or a model of any real institution.

- Numerical thresholds and game units are documented abstractions, not
  empirically calibrated parameters or forecasts.
- Rivals are local AI or bounded MCP agents; there is no network multiplayer.
- Automated playtests help evaluate gameplay and explanations, but they are not
  evidence of measured human learning.
- Human accessibility, educational, browser/device, provenance, and
  public-release reviews remain open.

Do not use the game for operational, clinical, financial, regulatory, legal,
or policy decisions.

## Learn More

### Players

- [How to Play in the CLI](docs/guides/how-to-play.md)
- [How to Play in GUI Mode](docs/guides/gui-how-to-play.md)

### Project and contributors

- [Contributor documentation index](docs/README.md)
- [Project specification](SPEC.md)
- [Architecture](ARCHITECTURE.md)
- [Proposal](docs/proposal.md)
- [Roadmap](docs/roadmap.md)
- [Design principles](docs/design_principles.md)
- [Changelog](CHANGELOG.md)

For a longer introduction to the design, read
[A Management Game Where the Market Talks Back](docs/blog-posts/health-policy-strategy-game.md).

## Contributing

The codebase is intentionally CLI-first. Keep core simulation transitions
deterministic and resolve randomness into explicit inputs before evaluating a
transition.

Run the standard checks:

```bash
python3 scripts/check_release_metadata.py
python3 scripts/check_documentation_links.py
cargo fmt --check
cargo clippy --all-targets -- -D warnings
cargo test
```

Start with the [contributor documentation index](docs/README.md) for software,
game and domain design, validation, release, and decision-record guidance.

## License

[GPL-3](LICENSE)
