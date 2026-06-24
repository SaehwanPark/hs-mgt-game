# Health Policy Strategy Game

A turn-based, command-line strategy game about leading a US health system under financial, clinical, regulatory, political, and social constraints.

The project models health-policy outcomes as the result of strategic interaction among health systems, insurers, government, clinicians, employers, labor, patients, and other stakeholders.

## Status

Early research and design phase with a deterministic architecture proof, minimal
playable CLI demo, first scenario design artifacts, stable replay state hash
checks, a starting executive dashboard at v0.1.13, per-turn interactive play
at v0.1.14, deterministic replay artifact export at v0.1.15, library module
boundaries at v0.1.16, GitHub Actions CI at v0.1.18, and Phase 5 bounded-slice
scope register (docs closure) at v0.1.19, and Phase 1 implications memo with
parameter-source ledger at v0.1.20, fifth-turn competitor capacity slice at
v0.1.21, Phase 0 governance docs at v0.1.22, and SPEC/Phase 5 doc reconciliation
at v0.1.23, first ADR and scenario format draft at v0.1.24.

The initial release will focus on a fictional regional US health market and a nonprofit health system led by the player.

## Core Direction

- Rust-based deterministic simulation engine
- Immutable snapshots and append-only history
- Explicit separation of true state, beliefs, and observed measurements
- Seeded stochastic inputs outside the core transition logic
- Strategic non-player actors using game-theoretic and bounded-rationality models
- Data-driven scenarios built from typed, inspectable mechanics
- CLI-first interface
- Educational use in graduate healthcare management and policy programs

## Documentation

Canonical project documents are maintained in [`docs/`](docs/):

- [Project Proposal](docs/proposal.md)
- [Development Roadmap](docs/roadmap.md)
- [Design Principles](docs/design_principles.md)
- [Actor Card Template](docs/actor-cards.md)
- [First Scenario Brief](docs/first-scenario-brief.md)
- [Phase 1 Implications Memo](docs/phase1-implications-memo.md)
- [Glossary](docs/glossary.md)
- [Versioning Policy](docs/versioning-policy.md)
- [Architecture Decision Records](docs/decision-records/README.md)
- [ADR 0001: Deterministic transition boundary](docs/decision-records/0001-deterministic-transition-and-stochastic-input-boundary.md)
- [Scenario Format Draft](docs/scenario-format-draft.md)
- [Phase 5 Scope Register](docs/phase5-scope-register.md)
- [Internal Playtest Findings (v0.1.21)](docs/playtest-findings-v0.1.21.md)

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

1. Forecast/uncertainty CLI preview (Phase 5 hardening).
2. First architecture decision record and scenario format design draft (Phase 6 prep).
3. Scenario data loading runtime only after the format design is approved.

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

To be determined.
