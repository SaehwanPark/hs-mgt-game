# Mechanism Design — Simulation Breadth and Strategic Actors Queue Closure v0.12.12

This slice implements an evidence-boundary audit, not a new simulation
mechanism. The current breadth inventory is:

1. **Service-line and capacity decisions.** The health-system controller and AI
   rivals choose investments, projects, and recruitment. The player observes
   own typed capacity, staffing, demand, treated volume, and unmet demand.
   Cash, Action Points, project delay, access, quality, and operating outcomes
   create the player-facing tradeoff.
2. **Operating and community outcomes.** Access, quality, workforce trust,
   community trust, market share, margin, and unmet demand provide multiple
   outcome dimensions. These are bounded organizational and community proxies,
   not individual patient outcomes.
3. **Capital and market interaction.** Projects draw cash over time; rival
   actions are delayed or partially observed; monitoring costs Action Points;
   payer postures and public commitments create additional strategic timing
   choices.
4. **Public-payer interaction.** Medicare and Medicaid are existing payer
   command/effect surfaces. They are not treated as fully modeled strategic
   actors, and their bounded compliance/access effects are not social-welfare
   estimates.
5. **Strategic rivals and debrief.** AI health-system rivals have style and
   risk posture. Public rival actions, monitor-revealed actions, and private
   actions have different observation paths. Committed history and instructor
   debrief can reveal rationales after play without granting the player
   omniscience during play.

## Boundary decision

The true competitive world contains all systems, effect queues, policy/event
metadata, and private rival actions. `PlayerObservation` contains the human
system's reported metrics and capacity, permitted market signals, lagged public
actions, monitor results, and intelligence gaps. The player does not receive
unobserved rival private actions or rationales during play. Debrief attribution
uses committed events/effects and separates actor responses from player-owned
outcomes.

Because the evidence audit finds no unexplained gap in this bounded surface,
there is no new actor, outcome category, or transition to design in v0.12.12.
