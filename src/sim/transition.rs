use crate::actors::actor_decision;
use crate::model::hash_state;
use crate::model::*;

use super::effects::push_effect;
use super::observe::observe_for_player;
use super::validate::{requested_commercial_rate, validate_command};

pub fn transition(
  prior: &WorldState,
  command: PlayerCommand,
  resolved_inputs: ResolvedInputs,
  ruleset: &Ruleset,
) -> Result<Transition, ValidationError> {
  validate_command(&command, ruleset)?;

  let observation = observe_for_player(prior, &resolved_inputs);
  let actor_decision = actor_decision(&command, prior, &observation, &resolved_inputs, ruleset);
  let accepted_requested_commercial_rate = requested_commercial_rate(&command);
  let mut next = prior.clone();
  let mut events = Vec::new();
  let mut effects = Vec::new();

  next.turn += 1;
  next.policy_pressure += resolved_inputs.policy_signal;

  match command {
    PlayerCommand::StabilizeAccess {
      add_staffed_beds,
      capital_spend,
      requested_commercial_rate: _,
    } => {
      next.cash -= capital_spend;
      next.staffed_beds += add_staffed_beds;
      push_effect(&mut effects, "capacity investment", "cash", -capital_spend);
      push_effect(
        &mut effects,
        "capacity investment",
        "staffed_beds",
        add_staffed_beds,
      );

      let net_access_delta = add_staffed_beds / 2 + resolved_inputs.labor_sick_call_delta;
      next.access_index += net_access_delta;
      next.workforce_trust -= add_staffed_beds / 4;
      push_effect(
        &mut effects,
        "staffing constraint",
        "access_index",
        net_access_delta,
      );
      push_effect(
        &mut effects,
        "staffing constraint",
        "workforce_trust",
        -(add_staffed_beds / 4),
      );
      events.push(Event {
        actor: "health_system",
        description: format!(
          "Opened {add_staffed_beds} staffed beds while absorbing {capital_spend} capital units."
        ),
      });
    }
    PlayerCommand::RespondToStateAccessMandate {
      advocacy_spend,
      access_commitment,
    } => {
      next.cash -= advocacy_spend;
      next.access_index += access_commitment / 2;
      push_effect(&mut effects, "policy response", "cash", -advocacy_spend);
      push_effect(
        &mut effects,
        "policy response",
        "access_index",
        access_commitment / 2,
      );
      events.push(Event {
        actor: "health_system",
        description: format!(
          "Committed {access_commitment} access units while spending {advocacy_spend} on state engagement."
        ),
      });
    }
    PlayerCommand::RespondToWorkforcePressure {
      retention_spend,
      schedule_relief_commitment,
    } => {
      next.cash -= retention_spend;
      next.workforce_trust += schedule_relief_commitment / 2;
      next.access_index += schedule_relief_commitment / 4;
      push_effect(&mut effects, "workforce response", "cash", -retention_spend);
      push_effect(
        &mut effects,
        "workforce response",
        "workforce_trust",
        schedule_relief_commitment / 2,
      );
      push_effect(
        &mut effects,
        "schedule relief",
        "access_index",
        schedule_relief_commitment / 4,
      );
      events.push(Event {
        actor: "health_system",
        description: format!(
          "Offered {retention_spend} retention units and {schedule_relief_commitment} schedule-relief commitment to address labor pressure."
        ),
      });
    }
    PlayerCommand::JoinRegionalAccessCoalition {
      coalition_investment,
      shared_access_commitment,
    } => {
      next.cash -= coalition_investment;
      next.access_index += shared_access_commitment / 2;
      next.community_trust += shared_access_commitment / 4;
      push_effect(
        &mut effects,
        "coalition response",
        "cash",
        -coalition_investment,
      );
      push_effect(
        &mut effects,
        "coalition response",
        "access_index",
        shared_access_commitment / 2,
      );
      push_effect(
        &mut effects,
        "coalition response",
        "community_trust",
        shared_access_commitment / 4,
      );
      events.push(Event {
        actor: "health_system",
        description: format!(
          "Committed {shared_access_commitment} shared access units and {coalition_investment} coalition investment to join the regional access coalition."
        ),
      });
    }
    PlayerCommand::RespondToCompetitorCapacityMove {
      defensive_capital_commitment,
      access_posture,
    } => {
      next.cash -= defensive_capital_commitment;
      next.access_index += access_posture / 2;
      next.staffed_beds += defensive_capital_commitment / 6;
      push_effect(
        &mut effects,
        "competitor response",
        "cash",
        -defensive_capital_commitment,
      );
      push_effect(
        &mut effects,
        "competitor response",
        "access_index",
        access_posture / 2,
      );
      push_effect(
        &mut effects,
        "defensive capacity",
        "staffed_beds",
        defensive_capital_commitment / 6,
      );
      events.push(Event {
        actor: "health_system",
        description: format!(
          "Committed {defensive_capital_commitment} defensive capital units and access posture {access_posture} in response to rival capacity pressure."
        ),
      });
    }
  }

  match &actor_decision.decision {
    ActorDecision::Insurer(InsurerDecision::Accept) => {
      let requested_commercial_rate =
        accepted_requested_commercial_rate.expect("insurer decision requires rate command");
      let delta = requested_commercial_rate - prior.commercial_rate;
      next.commercial_rate += delta;
      push_effect(&mut effects, "commercial insurer", "commercial_rate", delta);
      events.push(Event {
        actor: "commercial_insurer",
        description: "Accepted the requested rate path to preserve network access.".to_string(),
      });
    }
    ActorDecision::Insurer(InsurerDecision::Counter { offered_rate }) => {
      let delta = *offered_rate - prior.commercial_rate;
      next.commercial_rate += delta;
      next.community_trust -= 1;
      push_effect(&mut effects, "commercial insurer", "commercial_rate", delta);
      push_effect(
        &mut effects,
        "public bargaining friction",
        "community_trust",
        -1,
      );
      events.push(Event {
        actor: "commercial_insurer",
        description: format!("Countered with a rate of {offered_rate}."),
      });
    }
    ActorDecision::Insurer(InsurerDecision::Reject) => {
      next.community_trust -= 3;
      push_effect(&mut effects, "failed negotiation", "community_trust", -3);
      events.push(Event {
        actor: "commercial_insurer",
        description: "Rejected the rate request and signaled a narrow-network threat.".to_string(),
      });
    }
    ActorDecision::StatePolicy(StatePolicyDecision::GrantFlexibility) => {
      next.policy_pressure -= 5;
      next.community_trust += 2;
      push_effect(&mut effects, "state policy response", "policy_pressure", -5);
      push_effect(&mut effects, "state policy response", "community_trust", 2);
      events.push(Event {
        actor: "state_policy_officials",
        description: "Granted implementation flexibility after a credible access commitment."
          .to_string(),
      });
    }
    ActorDecision::StatePolicy(StatePolicyDecision::ProceedWithMandate) => {
      next.policy_pressure += 2;
      next.community_trust += 1;
      push_effect(&mut effects, "state policy response", "policy_pressure", 2);
      push_effect(&mut effects, "state policy response", "community_trust", 1);
      events.push(Event {
        actor: "state_policy_officials",
        description: "Kept the mandate on schedule while acknowledging the access plan."
          .to_string(),
      });
    }
    ActorDecision::StatePolicy(StatePolicyDecision::EscalateOversight) => {
      next.policy_pressure += 6;
      next.community_trust -= 2;
      push_effect(&mut effects, "state policy response", "policy_pressure", 6);
      push_effect(&mut effects, "state policy response", "community_trust", -2);
      events.push(Event {
        actor: "state_policy_officials",
        description: "Escalated oversight after judging the response insufficient.".to_string(),
      });
    }
    ActorDecision::Labor(LaborDecision::Cooperative) => {
      next.workforce_trust += 4;
      next.quality_index += 2;
      next.access_index += 1;
      push_effect(&mut effects, "nursing workforce", "workforce_trust", 4);
      push_effect(&mut effects, "nursing workforce", "quality_index", 2);
      push_effect(&mut effects, "nursing workforce", "access_index", 1);
      events.push(Event {
        actor: "nursing_workforce",
        description: "Accepted the retention package and schedule relief plan.".to_string(),
      });
    }
    ActorDecision::Labor(LaborDecision::LimitedSupport) => {
      next.workforce_trust += 1;
      push_effect(&mut effects, "nursing workforce", "workforce_trust", 1);
      events.push(Event {
        actor: "nursing_workforce",
        description: "Offered limited support while monitoring staffing conditions.".to_string(),
      });
    }
    ActorDecision::Labor(LaborDecision::WorkAction) => {
      next.access_index -= 4;
      next.quality_index -= 2;
      next.community_trust -= 2;
      next.workforce_trust -= 2;
      push_effect(&mut effects, "work action signal", "access_index", -4);
      push_effect(&mut effects, "work action signal", "quality_index", -2);
      push_effect(&mut effects, "work action signal", "community_trust", -2);
      push_effect(&mut effects, "work action signal", "workforce_trust", -2);
      events.push(Event {
        actor: "nursing_workforce",
        description: "Signaled a work action after judging the retention offer insufficient."
          .to_string(),
      });
    }
    ActorDecision::Coalition(CoalitionDecision::FullPartnership) => {
      next.community_trust += 4;
      next.policy_pressure -= 3;
      next.access_index += 2;
      push_effect(
        &mut effects,
        "regional provider coalition",
        "community_trust",
        4,
      );
      push_effect(
        &mut effects,
        "regional provider coalition",
        "policy_pressure",
        -3,
      );
      push_effect(
        &mut effects,
        "regional provider coalition",
        "access_index",
        2,
      );
      events.push(Event {
        actor: "regional_provider_coalition",
        description:
          "Accepted full partnership after a credible coalition investment and access commitment."
            .to_string(),
      });
    }
    ActorDecision::Coalition(CoalitionDecision::LimitedParticipation) => {
      next.community_trust += 1;
      push_effect(
        &mut effects,
        "regional provider coalition",
        "community_trust",
        1,
      );
      events.push(Event {
        actor: "regional_provider_coalition",
        description: "Offered limited participation while monitoring coalition conditions."
          .to_string(),
      });
    }
    ActorDecision::Coalition(CoalitionDecision::CoalitionWithdrawal) => {
      next.community_trust -= 3;
      next.policy_pressure += 4;
      push_effect(&mut effects, "coalition withdrawal", "community_trust", -3);
      push_effect(&mut effects, "coalition withdrawal", "policy_pressure", 4);
      events.push(Event {
        actor: "regional_provider_coalition",
        description: "Withdrew from the coalition after judging the investment and access commitment insufficient.".to_string(),
      });
    }
    ActorDecision::Competitor(CompetitorDecision::AccelerateExpansion) => {
      next.access_index -= 4;
      next.community_trust -= 2;
      next.commercial_rate -= 2;
      push_effect(&mut effects, "competitor health system", "access_index", -4);
      push_effect(
        &mut effects,
        "competitor health system",
        "community_trust",
        -2,
      );
      push_effect(
        &mut effects,
        "competitor health system",
        "commercial_rate",
        -2,
      );
      events.push(Event {
        actor: "competitor_health_system",
        description:
          "Accelerated outpatient capacity expansion after judging the defensive response insufficient."
            .to_string(),
      });
    }
    ActorDecision::Competitor(CompetitorDecision::HoldPosition) => {
      next.access_index -= 1;
      next.policy_pressure += 1;
      push_effect(&mut effects, "competitor health system", "access_index", -1);
      push_effect(
        &mut effects,
        "competitor health system",
        "policy_pressure",
        1,
      );
      events.push(Event {
        actor: "competitor_health_system",
        description: "Held expansion plans steady while monitoring rival commitments.".to_string(),
      });
    }
    ActorDecision::Competitor(CompetitorDecision::PartialRetreat) => {
      next.access_index += 2;
      next.community_trust += 2;
      next.policy_pressure -= 2;
      push_effect(&mut effects, "competitor health system", "access_index", 2);
      push_effect(
        &mut effects,
        "competitor health system",
        "community_trust",
        2,
      );
      push_effect(
        &mut effects,
        "competitor health system",
        "policy_pressure",
        -2,
      );
      events.push(Event {
        actor: "competitor_health_system",
        description:
          "Scaled back expansion plans after a credible defensive capital and access posture."
            .to_string(),
      });
    }
  }

  next.quality_index = clamp_metric(next.quality_index);
  next.access_index = clamp_metric(next.access_index);
  next.workforce_trust = clamp_metric(next.workforce_trust);
  next.community_trust = clamp_metric(next.community_trust);
  next.policy_pressure = clamp_metric(next.policy_pressure);

  let state_hash = hash_state(&next, ruleset);

  Ok(Transition {
    prior: prior.clone(),
    command,
    resolved_inputs,
    observation,
    actor_decision,
    events,
    effects,
    next,
    state_hash,
  })
}
