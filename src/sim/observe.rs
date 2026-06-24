use crate::model::{Observation, ResolvedInputs, WorldState, clamp_metric};

pub fn observe_for_player(prior: &WorldState, inputs: &ResolvedInputs) -> Observation {
  let policy_briefing = if inputs.policy_signal >= 3 {
    "state officials are increasing scrutiny of access and affordability"
  } else {
    "state policy attention is stable"
  };

  Observation {
    actor: "health_system_ceo",
    reported_access_index: clamp_metric(inputs.delayed_access_report + inputs.measurement_noise),
    reported_quality_index: prior.quality_index,
    prior_access_revision: inputs.access_measurement_revision,
    policy_briefing,
  }
}
