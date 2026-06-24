use super::{
  ActorDecisionRecord, AttributedEffect, Event, Observation, PlayerCommand, ResolvedInputs,
  ValidationError, WorldState,
};

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Transition {
  pub prior: WorldState,
  pub command: PlayerCommand,
  pub resolved_inputs: ResolvedInputs,
  pub observation: Observation,
  pub actor_decision: ActorDecisionRecord,
  pub events: Vec<Event>,
  pub effects: Vec<AttributedEffect>,
  pub next: WorldState,
  pub state_hash: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ReplayVerification {
  pub final_state: WorldState,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ReplayError {
  InvalidTransition(ValidationError),
  StateHashMismatch {
    turn: u32,
    expected: String,
    actual: String,
  },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct History {
  pub genesis: WorldState,
  pub transitions: Vec<Transition>,
}
