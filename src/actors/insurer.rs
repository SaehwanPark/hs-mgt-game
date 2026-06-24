use crate::model::{ActorDecision, ActorDecisionRecord, InsurerDecision, Observation, Ruleset};

pub fn insurer_decision(
  requested_commercial_rate: i32,
  observation: &Observation,
  ruleset: &Ruleset,
) -> ActorDecisionRecord {
  let (decision, rationale) = if requested_commercial_rate <= ruleset.target_commercial_rate {
    (
      InsurerDecision::Accept,
      format!(
        "Requested rate {requested_commercial_rate} is within target and reported access is {}.",
        observation.reported_access_index
      ),
    )
  } else if observation.reported_access_index < 70 {
    (
      InsurerDecision::Counter {
        offered_rate: ruleset.target_commercial_rate,
      },
      format!(
        "Reported access {} gives the provider leverage, but requested rate {requested_commercial_rate} exceeds target {}.",
        observation.reported_access_index, ruleset.target_commercial_rate
      ),
    )
  } else {
    (
      InsurerDecision::Reject,
      format!(
        "Reported access {} is adequate, so the insurer resists requested rate {requested_commercial_rate}.",
        observation.reported_access_index
      ),
    )
  };

  ActorDecisionRecord {
    actor: "commercial_insurer",
    decision: ActorDecision::Insurer(decision),
    rationale,
  }
}
