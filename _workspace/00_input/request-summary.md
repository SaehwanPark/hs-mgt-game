# Request Summary — Live competitive GUI repair v0.12.31

## Objective

Review the current visual/audio GUI, identify why a scenario cannot start from a
normal checkout, repair the live competitive path, and document exact player
steps that minimize launch and recovery failures.

## Classification and scope

- Roadmap/output: bounded technical-prototype repair after a source-backed
  browser-transport gap.
- Runtime: one loopback-only, in-memory GUI host over `GameSessionStore`.
- Player path: `competitive-regional-v1` start through one committed month.
- Documentation: README quickstart plus canonical GUI player guide and
  troubleshooting.

## Root causes

- The shipped page had no injected adapter and browsers cannot call the stdio
  MCP host directly.
- Tests used mock adapters and did not cross the shipped transport boundary.
- Competitive live reads attempted unsupported campaign-coverage calls and
  could show false recovery.

## Non-goals

- No other GUI campaigns, persistence, remote bind, authentication, multiplayer,
  packaging, simulation, balance, or audio-source change.
- No human usability, lived accessibility, learning, calibration, policy, or
  domain-expert claim.

## Validation target

One real loopback transport test must start seed-42 Normal competitive play,
load typed presentation/actions, validate and submit a command, and read the
committed resolution. Player docs must state the exact command, URL, live/demo
distinction, session lifetime, audio gesture, alternate port, and recovery.
