# Evidence Map - ASC Project Observation Coverage

## Scope

Validate the concrete observation gap found while extending the v0.10.54
project-limit recovery capture: an accepted ASC project consumed a project
slot and monthly draw but was absent from the actor-visible project label.

## Sources Reviewed

- `README.md`, `docs/roadmap.md`, `docs/design_principles.md`, and `SPEC.md`.
- `docs/playtest-findings-v0.10.54.md` and its generated artifact.
- `docs/agent-playtest-protocol.md` and `docs/mcp-playtesting-guide.md`.
- `src/sim/observe_competitive.rs`, `src/model/competitive_world.rs`, and
  project validation/transition code.

## Mechanisms and Institutions

- Concurrent project limits, monthly project draws, and delayed capacity are
  existing game abstractions, not calibrated real-world constraints.
- The change corrects actor-visible reporting of an existing pending effect; it
  does not add an actor, policy, service line, or transition mechanism.

## Actor Incentives and Information

- True state includes the pending `AscCapacity` effect and active-project
  resource counters.
- The human actor receives only the formatted observation, legal commands, and
  later history/debrief output.
- The missing label created an information mismatch: validation counted the
  project while the observation did not name it.

## Assumptions

- `AscCapacity` should be represented consistently with other project-bearing
  pending effects: name, remaining months, and monthly draw.
- Matching v0.10.54 transition hashes demonstrates that this is an observation
  correction rather than a simulation-rule change.
- Observation visibility is traceability evidence, not proof of comprehension,
  learning, balance, or strategy quality.

## Unresolved Questions

- Whether future evidence identifies a separate need for structured project
  validation hints or broader project guidance.

## Design Implications

- Preserve raw observations before and after rejected commands.
- Keep true state, actor observation, transition history, and debrief evidence
  distinct.
- Keep project validation hints and runtime tuning deferred.

## Risks

- A deterministic three-seed capture cannot establish human learning,
  calibration, winnability, or policy validity.
- Adding only the missing observer branch avoids broadening into a generalized
  project-observation abstraction.
