# Health Policy Strategy Game

A turn-based, command-line strategy game about leading a US health system under financial, clinical, regulatory, political, and social constraints.

The project models health-policy outcomes as the result of strategic interaction among health systems, insurers, government, clinicians, employers, labor, patients, and other stakeholders.

## Status

Early research, design, and vertical-slice development phase. The current build
includes a deterministic five-turn stabilization campaign, replay and state-hash
checks, rich interactive CLI guidance, a stabilization-only TOML scenario loader
with `--scenario` path selection, a bounded three-month competitive regional
preview with AI rivals and Stata-like command entry, and a local stdio MCP server
for bounded agent play of both current campaigns. The v0.1.50 MCP debrief
surface reports final competitive player tradeoff metrics from committed
history, the v0.1.52 scripted MCP batch adds a naive first-time profile across
seeds 42, 43, and 44, and the v0.1.54 free-form agent run records one
observation-driven first-time profile before balance work.
See [`docs/core-loop-spec.md`](docs/core-loop-spec.md),
[`docs/gameplay-competitive-sketch.md`](docs/gameplay-competitive-sketch.md), and
[`docs/competitive-scenario-brief.md`](docs/competitive-scenario-brief.md).

The initial release will focus on a fictional regional US health market and a nonprofit health system led by the player.

## Core Direction

- Rust-based deterministic simulation engine
- Immutable snapshots and append-only history
- Explicit separation of true state, beliefs, and observed measurements
- Seeded stochastic inputs outside the core transition logic
- Strategic non-player actors using game-theoretic and bounded-rationality models
- Data-driven scenarios built from typed, inspectable mechanics
- CLI-first interface (best in a true-color terminal; respects `NO_COLOR`)
- Local MCP stdio interface for AI-agent play of bounded current campaigns
- Educational use in graduate healthcare management and policy programs

## Documentation

Canonical project documents are maintained in [`docs/`](docs/):

- [Project Proposal](docs/proposal.md)
- [Development Roadmap](docs/roadmap.md)
- [Design Principles](docs/design_principles.md)
- [How To Play (New Players)](docs/how-to-play.md)
- [Actor Card Template](docs/actor-cards.md)
- [First Scenario Brief](docs/first-scenario-brief.md)
- [Phase 1 Implications Memo](docs/phase1-implications-memo.md)
- [Glossary](docs/glossary.md)
- [Versioning Policy](docs/versioning-policy.md)
- [Architecture Decision Records](docs/decision-records/README.md)
- [ADR 0001: Deterministic transition boundary](docs/decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md)
- [ADR 0002: Mid-run session save](docs/decision-records/0002-mid-run-session-save.md)
- [Scenario Format Draft](docs/scenario-format-draft.md)
- [Phase 5 Scope Register](docs/phase5-scope-register.md)
- [Internal Playtest Findings (v0.1.25)](docs/playtest-findings-v0.1.25.md)
- [AI-Agent Playtest Findings (v0.1.49)](docs/playtest-findings-v0.1.49.md)
- [AI-Agent Seed-Variation Findings (v0.1.51)](docs/playtest-findings-v0.1.51.md)
- [AI-Agent Naive-Profile Findings (v0.1.52)](docs/playtest-findings-v0.1.52.md)
- [AI-Agent Free-Form Findings (v0.1.54)](docs/playtest-findings-v0.1.54.md)
- [AI-Agent Playtest Protocol](docs/agent-playtest-protocol.md)
- [External Playtest Protocol (Superseded)](docs/external-playtest-protocol.md)
- [MCP Agent Interface](docs/mcp-agent-interface.md)

Detailed subsystem specifications will be added separately as design work progresses.

## Development Approach

The project will proceed through research, conceptual design, technical prototyping, and a narrow vertical slice before expanding into a full MVP.

The first playable slice should demonstrate:

- meaningful executive tradeoffs;
- actor-specific incomplete information;
- at least one strategic negotiation;
- one policy process;
- delayed and stochastic effects;
- deterministic replay;
- and causal explanation of outcomes.

## Non-Goals

The initial version will not attempt to:

- model the entire US healthcare system;
- provide authoritative policy forecasts;
- reproduce every reimbursement or regulatory rule;
- support multiple countries;
- solve global equilibria among all actors;
- or provide a graphical interface.

## Contributing

The project is not yet ready for broad implementation contributions.

Pull requests to `main` run CI checks for `cargo fmt --check` and `cargo test`.
Before opening a PR, run the same commands locally:

```bash
cargo fmt --check
cargo test
```

Current priorities are:

1. Run and synthesize AI-agent playtests against explicit gameplay validity
   hypotheses and strategy-space diagnostics.
2. Treat debrief quality and causal explanation as primary product surfaces.
3. Develop one exemplary scenario before broad scenario tooling.
4. Extend scenario data loading only after the minimal stabilization TOML slice
   has playtest or authoring evidence.
5. Competitive campaign hardening after bounded-loop playtests.
6. Medicare/Medicaid strategic actors only after actor-card and scenario gates.

Before proposing major features or abstractions, review the canonical documents
in [`docs/`](docs/), including the [glossary](docs/glossary.md),
[versioning policy](docs/versioning-policy.md), and
[decision-record template](docs/decision-records/0000-template.md).

## Programming Principles

- Functional programming
- Railway-oriented programming
- Domain-driven design + Carefully designed abstract data types
- Idiomatic Rust code writing
- Careful error handling and resource management
- Thorough and thoughtful code comments and docstrings
- Spec-driven development
- Test-driven development
- Tabsize of 2 spaces

## License

[GPL-3](LICENSE)
