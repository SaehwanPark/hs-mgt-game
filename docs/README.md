# Contributor Documentation

Use this page to enter the project from the kind of contribution you want to
make. The repository root [README](../README.md) remains the player-facing
overview and quickstart.

## Document Roles

- **Canonical direction:** the [proposal](proposal.md), [roadmap](roadmap.md),
  and [design principles](design_principles.md) define durable project intent.
- **Current working documents:** `guides/`, `design/`, `research/`, `reference/`,
  and `validation/` describe the implemented prototype and active workflows.
- **Historical evidence:** `history/` preserves prior findings, milestone
  decisions, and superseded project material. It is evidence, not current
  contributor instruction.

## Software Contributor Path

1. Read the root [project specification](../SPEC.md) and
   [architecture](../ARCHITECTURE.md).
2. Review the [core loop](design/core-loop-spec.md),
   [system boundary](design/system-boundary.md), and
   [MCP interface](reference/mcp-agent-interface.md) relevant to the area you
   will change.
3. Follow the [versioning policy](reference/versioning-policy.md) and
   [release metadata check](guides/contributor-release-check.md).
4. Consult the [architecture decision records](decision-records/README.md)
   before changing an accepted boundary.

## Game and Domain Design Contributor Path

1. Read the canonical [proposal](proposal.md), [roadmap](roadmap.md), and
   [design principles](design_principles.md).
2. Use the [glossary](reference/glossary.md), [actor cards](design/actor-cards.md),
   [action catalog](design/action-catalog-draft.md), and
   [competitive gameplay specification](design/gameplay-competitive-sketch.md).
3. Review the [first](design/first-scenario-brief.md),
   [competitive](design/competitive-scenario-brief.md), and
   [exemplary](design/exemplary-scenario-brief.md) scenario briefs plus the
   [scenario format](design/scenario-format-draft.md).
4. Ground claims in the [evidence registry](research/evidence-registry.md) and
   [workforce ledger](research/workforce-ledger.md); route proposed breadth
   through the [expansion review](design/expansion-proposal-review.md).

Additional current design references:

- [CLI command grammar](design/cli-command-grammar-draft.md)
- [Executive report format](design/executive-report-format.md)

## Validation Contributor Path

1. Start with the active [playtesting protocol](validation/playtesting.md).
2. Follow the [MCP playtesting guide](guides/mcp-playtesting-guide.md) for the
   reproducible local harness.
3. Use the [playtest evidence index](history/playtests/README.md) to find prior
   questions, runs, and limits before opening a new validation slice.
4. Use the [visual/audio initiative index](history/initiatives/visual-audio/README.md)
   when evaluating the bounded GUI first-month presentation contract.

## Player Guides

- [How to play in the CLI](guides/how-to-play.md)
- [How to play in GUI mode](guides/gui-how-to-play.md)

## Historical Context

The [history index](history/README.md) explains which records are retained for
auditability and why they should not be treated as current instructions.

Repository-local agent workflow is documented separately in the
[health-policy strategy-game harness](harness/health-policy-strategy-game/team-spec.md).
