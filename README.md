# Health Policy Strategy Game

Health Policy Strategy Game is a deterministic strategy simulation about
leading a fictional nonprofit US health system through financial pressure,
workforce constraints, payer negotiations, policy oversight, market
competition, and community trust.

The current public milestone is a playable Rust prototype at v0.14.7. The
simulation remains the authority for commands, observations, transitions,
history, replay, checkpoints, and debriefs. The CLI is the reference interface;
the loopback GUI is the active presentation-development surface over the same
host contracts. Its current-task rail switches to an explicit final-debrief
state when the host reports a terminal session.
Visible consequence links also retain timing and existing replay-hash context
with explicit unavailable fallbacks, and committed-effect links show their
host-reported signed deltas.

![Terminal view of the game's executive report and competitive command entry](https://i.imgur.com/gfmOO3O.png)

## Start here

You need a Rust toolchain with Cargo. From the repository root, run:

```bash
cargo run
```

For a friendly first session:

1. Press Enter or choose `1` for `stabilization-v1`.
2. Press Enter for the default deterministic seed.
3. Choose beginner mode.

## Playable campaigns

- `stabilization-v1` — a five-turn executive stabilization campaign.
- `competitive-regional-v1` — a 24-month regional-market campaign with AI
  rivals, simultaneous monthly actions, and lagged information.
- `regional-affiliation-v1` — a six-stage affiliation campaign covering partner
  assessment, commitments, review, integration, and debriefing.

Every campaign is deterministic for the same seed and choices. The simulation
keeps actor-visible information separate from underlying state, records an
append-only history, and supports replay verification.

## GUI mode

The loopback GUI currently launches all three campaigns:

```bash
cargo run --bin hs-mgt-game-gui
```

Keep that terminal running and open the printed URL, normally
`http://127.0.0.1:7878`. Choose seed `42`, Normal difficulty, and
**Start competitive session** for the recommended first GUI session.

The GUI uses a progressive Setup/Brief/Decide/Resolve/Review workspace with
host-ordered actions, event-gated future workspace navigation, host-owned
checkpoints, replay/history reads, and text-first source/uncertainty fallbacks.
`gui/index.html` opened directly shows
demo data; it does not start a live scenario.

The declared default browser target is Chromium evergreen desktop. The Codex in-app browser
is a development inspection surface. Firefox, WebKit/Safari,
mobile, and legacy-browser support are deferred and not certified.

See [How to Play in GUI Mode](docs/guides/gui-how-to-play.md) for launch,
settings, alternate ports, checkpoint recovery, and troubleshooting.

## Current boundaries

This is a playable research and educational prototype, not a finished
educational release or a model of any real institution.

- Numerical thresholds and game units are documented abstractions, not
  empirically calibrated parameters or forecasts.
- Rivals are local AI or bounded MCP agents; there is no network multiplayer.
- Automated and AI-agent playtests support technical and gameplay iteration;
  they do not establish human learning, lived accessibility, classroom
  effectiveness, legal conclusions, or policy validity.
- Asset provenance is machine-checked. Content with incomplete provenance uses
  a generic fallback and is not promoted to runtime release.

Do not use the game for operational, clinical, financial, regulatory, legal, or
policy decisions.

## Learn more

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

Keep core simulation transitions deterministic and resolve randomness into
explicit inputs before evaluating a transition. Treat the host as authoritative
for commands, legality, state, history, replay, checkpoints, and debriefs;
presentation layers must remain actor-visible and reversible.

Run the standard checks:

```bash
python3 scripts/check_documentation_currentness.py
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
