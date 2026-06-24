use crate::model::{
  ActorDecision, CoalitionDecision, InsurerDecision, LaborDecision, PlayMode, PlayerCommand,
  ReplayArtifact, ResolvedInputs, StatePolicyDecision, StrategyPath, Transition, WorldState,
};

use super::text::escape_artifact_text;

pub const REPLAY_ARTIFACT_VERSION: &str = "replay-artifact-0.1.15";

pub fn serialize_world_state(prefix: &str, state: &WorldState) -> String {
  format!(
    "{prefix}=turn:{turn},cash:{cash},staffed_beds:{staffed_beds},access_index:{access_index},quality_index:{quality_index},workforce_trust:{workforce_trust},community_trust:{community_trust},commercial_rate:{commercial_rate},policy_pressure:{policy_pressure}",
    turn = state.turn,
    cash = state.cash,
    staffed_beds = state.staffed_beds,
    access_index = state.access_index,
    quality_index = state.quality_index,
    workforce_trust = state.workforce_trust,
    community_trust = state.community_trust,
    commercial_rate = state.commercial_rate,
    policy_pressure = state.policy_pressure
  )
}

pub fn serialize_player_command(command: &PlayerCommand) -> String {
  match command {
    PlayerCommand::StabilizeAccess {
      add_staffed_beds,
      capital_spend,
      requested_commercial_rate,
    } => format!(
      "StabilizeAccess,add_staffed_beds:{add_staffed_beds},capital_spend:{capital_spend},requested_commercial_rate:{requested_commercial_rate}"
    ),
    PlayerCommand::RespondToStateAccessMandate {
      advocacy_spend,
      access_commitment,
    } => format!(
      "RespondToStateAccessMandate,advocacy_spend:{advocacy_spend},access_commitment:{access_commitment}"
    ),
    PlayerCommand::RespondToWorkforcePressure {
      retention_spend,
      schedule_relief_commitment,
    } => format!(
      "RespondToWorkforcePressure,retention_spend:{retention_spend},schedule_relief_commitment:{schedule_relief_commitment}"
    ),
    PlayerCommand::JoinRegionalAccessCoalition {
      coalition_investment,
      shared_access_commitment,
    } => format!(
      "JoinRegionalAccessCoalition,coalition_investment:{coalition_investment},shared_access_commitment:{shared_access_commitment}"
    ),
  }
}

pub fn serialize_resolved_inputs(inputs: &ResolvedInputs) -> String {
  format!(
    "measurement_noise:{},delayed_access_report:{},labor_sick_call_delta:{},policy_signal:{},coalition_leverage_signal:{},access_measurement_revision:{}",
    inputs.measurement_noise,
    inputs.delayed_access_report,
    inputs.labor_sick_call_delta,
    inputs.policy_signal,
    inputs.coalition_leverage_signal,
    inputs.access_measurement_revision
  )
}

pub fn serialize_actor_decision(decision: &ActorDecision) -> String {
  match decision {
    ActorDecision::Insurer(InsurerDecision::Accept) => "Insurer:Accept".to_string(),
    ActorDecision::Insurer(InsurerDecision::Counter { offered_rate }) => {
      format!("Insurer:Counter:{offered_rate}")
    }
    ActorDecision::Insurer(InsurerDecision::Reject) => "Insurer:Reject".to_string(),
    ActorDecision::StatePolicy(StatePolicyDecision::GrantFlexibility) => {
      "StatePolicy:GrantFlexibility".to_string()
    }
    ActorDecision::StatePolicy(StatePolicyDecision::ProceedWithMandate) => {
      "StatePolicy:ProceedWithMandate".to_string()
    }
    ActorDecision::StatePolicy(StatePolicyDecision::EscalateOversight) => {
      "StatePolicy:EscalateOversight".to_string()
    }
    ActorDecision::Labor(LaborDecision::Cooperative) => "Labor:Cooperative".to_string(),
    ActorDecision::Labor(LaborDecision::LimitedSupport) => "Labor:LimitedSupport".to_string(),
    ActorDecision::Labor(LaborDecision::WorkAction) => "Labor:WorkAction".to_string(),
    ActorDecision::Coalition(CoalitionDecision::FullPartnership) => {
      "Coalition:FullPartnership".to_string()
    }
    ActorDecision::Coalition(CoalitionDecision::LimitedParticipation) => {
      "Coalition:LimitedParticipation".to_string()
    }
    ActorDecision::Coalition(CoalitionDecision::CoalitionWithdrawal) => {
      "Coalition:CoalitionWithdrawal".to_string()
    }
  }
}

pub fn serialize_play_mode(play_mode: PlayMode) -> String {
  match play_mode {
    PlayMode::Interactive => "interactive".to_string(),
    PlayMode::Preset(StrategyPath::AccessStabilization) => "preset:1".to_string(),
    PlayMode::Preset(StrategyPath::FiscalCaution) => "preset:2".to_string(),
    PlayMode::Preset(StrategyPath::AggressiveBargaining) => "preset:3".to_string(),
  }
}

pub fn serialize_transition(transition: &Transition) -> Vec<String> {
  let mut lines = vec![
    "[transition]".to_string(),
    format!("turn={}", transition.next.turn),
    format!("command={}", serialize_player_command(&transition.command)),
    format!(
      "resolved_inputs={}",
      serialize_resolved_inputs(&transition.resolved_inputs)
    ),
    format!("state_hash={}", transition.state_hash),
    serialize_world_state("prior", &transition.prior),
    serialize_world_state("next", &transition.next),
    format!(
      "observation=actor:{},reported_access_index:{},reported_quality_index:{},prior_access_revision:{},policy_briefing:\"{}\"",
      transition.observation.actor,
      transition.observation.reported_access_index,
      transition.observation.reported_quality_index,
      transition.observation.prior_access_revision,
      escape_artifact_text(transition.observation.policy_briefing)
    ),
    format!(
      "actor_decision=actor:{},decision:{},rationale:\"{}\"",
      transition.actor_decision.actor,
      serialize_actor_decision(&transition.actor_decision.decision),
      escape_artifact_text(&transition.actor_decision.rationale)
    ),
    format!("event_count={}", transition.events.len()),
  ];

  for (index, event) in transition.events.iter().enumerate() {
    lines.push(format!(
      "event={index},actor:{},description:\"{}\"",
      event.actor,
      escape_artifact_text(&event.description)
    ));
  }

  lines.push(format!("effect_count={}", transition.effects.len()));
  for (index, effect) in transition.effects.iter().enumerate() {
    lines.push(format!(
      "effect={index},source:{},metric:{},delta:{}",
      effect.source, effect.metric, effect.delta
    ));
  }

  lines.push("[/transition]".to_string());
  lines
}

pub fn serialize_replay_artifact(artifact: &ReplayArtifact) -> String {
  let mut lines = vec![
    REPLAY_ARTIFACT_VERSION.to_string(),
    format!("ruleset={}", artifact.ruleset_version),
    format!("seed={}", artifact.seed),
    format!("play_mode={}", serialize_play_mode(artifact.play_mode)),
    serialize_world_state("genesis", &artifact.history.genesis),
    format!("transition_count={}", artifact.history.transitions.len()),
  ];

  for transition in &artifact.history.transitions {
    lines.extend(serialize_transition(transition));
  }

  lines.join("\n")
}
