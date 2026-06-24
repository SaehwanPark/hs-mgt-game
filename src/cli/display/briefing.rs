use crate::actors::describe_actor_decision;
use crate::model::{Observation, Transition, WorldState};

pub fn turn_executive_briefing(
  prior: &WorldState,
  observation: &Observation,
  turn_number: u32,
) -> Vec<String> {
  let mut lines = vec![
    format!("Turn {turn_number} executive briefing"),
    format!(
      "  Cash {}, policy pressure {}, workforce trust {}, community trust {}",
      prior.cash, prior.policy_pressure, prior.workforce_trust, prior.community_trust
    ),
    format!(
      "  Reported access {}, quality {}, policy briefing: {}",
      observation.reported_access_index,
      observation.reported_quality_index,
      observation.policy_briefing
    ),
  ];

  if observation.prior_access_revision != 0 {
    lines.push(format!(
      "  Prior access measurement revision: {}",
      observation.prior_access_revision
    ));
  }

  if !observation.market_competition_briefing.is_empty() {
    lines.push(format!(
      "  Market competition briefing: {}",
      observation.market_competition_briefing
    ));
  }

  lines
}

pub fn turn_resolution_summary(transition: &Transition) -> Vec<String> {
  vec![
    format!(
      "Turn {} resolved: {}",
      transition.next.turn,
      describe_actor_decision(&transition.actor_decision.decision)
    ),
    format!(
      "  {} — {}",
      transition.actor_decision.actor, transition.actor_decision.rationale
    ),
    format!("  State hash: {}", transition.state_hash),
  ]
}
