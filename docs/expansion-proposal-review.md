# Expansion Proposal Review

**Status:** Phase 7 proposal-review artifact  
**Audience:** Contributors, domain reviewers, playtest designers  
**Scope:** Difficulty expansion, regional merger/acquisition mechanics, and a
future GUI layer

This document reviews three expansion ideas before they are promoted into
runtime work. It is intentionally a gate, not an implementation specification.
Future slices should update this review, then the roadmap, then SDD documents
before changing mechanics or interfaces.

## Review posture

- Treat each idea as a hypothesis about player value and educational value.
- Require evidence or domain review before runtime tuning, new actor classes,
  scenario-schema changes, or GUI architecture.
- Preserve deterministic replay, actor-specific observations, append-only
  history, and debrief traceability.
- Label unsupported mechanics as stylized abstractions or gameplay-driven
  balancing choices.

## Sources reviewed

- Capitalism Lab precedent: higher difficulty makes AI competitors more
  formidable and economic conditions more volatile, with the hardest tier
  treated as clearable by elite players rather than impossible:
  <https://www.capitalismlab.com/amp-up-challenge/>.
- Capitalism Lab settings precedent: competitor aggressiveness can be exposed
  as an explicit setup dimension in addition to a global difficulty label:
  <https://www.capitalismlab.com/scripts/script-dlcs/>.
- DOJ/FTC 2023 Merger Guidelines: merger review depends on law and facts, with
  agencies evaluating whether mergers may substantially lessen competition:
  <https://www.justice.gov/atr/2023-merger-guidelines>.
- HHS consolidation RFI response report: HHS, DOJ, and FTC have treated health
  care consolidation as a cross-government competition issue:
  <https://www.hhs.gov/sites/default/files/hhs-consolidation-health-care-markets-rfi-response-report.pdf>.
- Kenney asset licensing: Kenney asset pages are public-domain CC0 and usable in
  commercial projects without required attribution:
  <https://kenney.nl/support>.
- OpenGameArt license guidance: OpenGameArt supports CC0 and other free
  licenses, but attribution and compatibility vary by asset:
  <https://opengameart.org/content/faq>.

## Proposal 1: Difficulty Expansion

Current competitive difficulty already changes K rivals, human/CPU AP, and AI
ability. The expansion should make difficulty more institutionally expressive:
rivals on harder tiers may have better resource access, better or faster
information, and a higher willingness to take aggressive but risky actions.

Recommended gate:

- Define each tier as a bundle of observable pressures, not just a hidden score
  modifier.
- Keep human AP floors playable and document any Expert-tier restrictions.
- Add rival resource-access and information-access differences only through
  explicit scenario/ruleset fields or documented fixtures.
- Add rival aggressiveness as an actor risk-posture parameter that affects
  decisions and rationales.
- Validate Expert difficulty with repeated scripted and live-agent runs before
  calling it winnable.

Design implications:

- Easy should teach the loop with fewer rivals, more player slack, and lower
  rival information quality.
- Normal should remain the default compact competitive campaign.
- Hard should increase rival pressure and information asymmetry while preserving
  multiple defensible strategies.
- Expert should be framed as severe but clearable: a strong player can survive
  through disciplined cash, monitoring, workforce follow-through, and selective
  growth rather than needing one hidden optimal path.

Risks:

- Difficulty can become arbitrary punishment if it only reduces player
  resources.
- Difficulty can become opaque if rivals receive hidden omniscience.
- Expert can become educationally weak if only one strategy clears it.

## Proposal 2: Regional Merger and Acquisition

The first M&A slice should model realistic regional affiliation or acquisition
choices in US health care, not a full deal-market simulator. Candidate actions
include exploring an affiliation, negotiating a letter of intent, making
community-benefit commitments, seeking regulatory clearance, and integrating
operations after a deal.

Recommended gate:

- Start with one regional nonprofit/community-system affiliation or acquisition
  scenario.
- Model regulatory review as a strategic and legal constraint, not as a direct
  player-controlled lever.
- Include community benefit, labor, payer leverage, integration drag, capital
  access, and service continuity as first-class tradeoffs.
- Treat deal failure, delayed review, conditional approval, and post-close
  integration problems as valid modeled outcomes.
- Keep private equity rollups, national chains, multi-deal portfolios, and
  detailed transaction financing deferred.

Design implications:

- M&A should create a strategic choice among independence, loose affiliation,
  formal acquisition, and partnership alternatives.
- The player should face tradeoffs between solvency, market power, access
  preservation, workforce trust, community legitimacy, and regulator concerns.
- Debrief should separate the player's organizational advantage from regional
  social welfare and distributional effects.

Risks:

- False legal precision if the game implies a calibrated antitrust outcome.
- Normative opacity if consolidation is always good or always bad.
- Scope creep into finance, law, and market modeling before one slice proves
  teachability.

## Proposal 3: GUI Layer

The GUI should be a thin client over the existing deterministic core, not a
second game. It should broaden audience access while preserving the CLI's
strengths: inspectable commands, reproducible histories, and causal debriefs.

Recommended gate:

- Design the GUI around existing observations, command validation, history,
  replay, and debrief outputs.
- Keep rendering, input, layout, asset loading, and settings outside the
  deterministic transition core.
- Use publicly downloadable assets only after license review; prefer CC0 assets
  from sources such as Kenney, or individually audited OpenGameArt/itch.io
  assets.
- Prototype one campaign screen and one end-of-run debrief surface before
  committing to packaging or release workflows.
- Preserve CLI and MCP as first-class interfaces.

Design implications:

- Capitalism is a useful practice example for layered business-simulation UI:
  map-like market context, asset-backed facilities, dashboards, and competitor
  pressure are more useful than decorative graphics.
- A first GUI proof should show the executive report, command selection, rival
  observability, active projects, and debrief attribution from the same data
  used by CLI/MCP.

Risks:

- GUI work can pull attention away from mechanism validation.
- Pixel assets can create licensing or attribution debt.
- A separate UI state model can break replay and observation boundaries.

## Promotion rule

Before any implementation slice begins, the active `SPEC.md` Present entry
should cite:

- the relevant section of this review;
- the roadmap gate it satisfies;
- the narrow artifact or runtime behavior being changed;
- verification evidence needed before the slice can close; and
- explicit non-goals that keep the other two proposals from entering scope.
