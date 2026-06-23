# Repository Agents Guide

Keep this file short and repo-wide. Detailed workflow rules live in
`.agents/skills/` and `docs/harness/`.

## What
- This repository is a Rust, CLI-first health-policy strategy game in early
  research and design. The player leads a fictional nonprofit US health system.
- Canonical project docs are `README.md`, `docs/proposal.md`,
  `docs/roadmap.md`, and `docs/design_principles.md`.
- The durable design boundaries are deterministic core transitions, explicit
  stochastic inputs, true state versus actor observations, immutable history,
  strategic non-player actors, visible assumptions, and educational debriefing.

## Why
- The project models health-policy outcomes as strategic interaction among
  institutions, not as direct policy levers or single-metric optimization.
- Scope control matters: credible vertical slices, inspectable mechanisms, and
  documented assumptions come before broad framework expansion.

## How
- Before major changes, read the canonical docs and the harness team spec at
  `docs/harness/health-policy-strategy-game/team-spec.md`.
- Use repo-local skills only for project-specific health-policy simulation
  workflow. Use global skills for generic functional programming, Rust quality,
  code review, comments, spec maintenance, planning, and release preparation.
- Current Rust commands: `cargo fmt`, `cargo test`, and `cargo run`.
- Do not invent build, CI, scenario, data, or release conventions until the
  roadmap phase calls for them and they are documented.
- You may install any necessary dependencies or tools via `cargo install`.
- When you cannot find CLI tools, use `which <tool>` to find the installed path.
- Do bookkeeping lessons learned into `LESSONS.md` and keep revisitng during development to avoid repeating mistakes.
- You may use **emojis** in the game display when necessary.
- Use tabsize of **2 spaces** throughout the codebase.
- Follow the principle of **simple code writing**
- Bump up project version: increase version number by 0.0.1 for each PR or PR-equivalent change. increase 0.1 for major feature releases or meaningful accumulated changes. no need to carry over, but when bumping up higher digits, reset the lower digits to 0.
