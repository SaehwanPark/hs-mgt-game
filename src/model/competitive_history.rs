use super::{
  AggregatedMonthlyActions, AttributedEffect, CompetitiveValidationError, CompetitiveWorldState,
  Event,
};

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct CompetitiveTransition {
  pub prior: CompetitiveWorldState,
  pub aggregated: AggregatedMonthlyActions,
  pub events: Vec<Event>,
  pub effects: Vec<AttributedEffect>,
  pub next: CompetitiveWorldState,
  pub state_hash: String,
  #[serde(default)]
  pub consultant_options: Vec<crate::model::ConsultantOption>,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum CompetitiveReplayError {
  Validation(CompetitiveValidationError),
  StateHashMismatch {
    turn: u32,
    expected: String,
    actual: String,
  },
}

#[derive(Clone, Debug, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct CompetitiveHistory {
  pub genesis: CompetitiveWorldState,
  pub transitions: Vec<CompetitiveTransition>,
}

impl CompetitiveHistory {
  pub fn final_state(&self) -> &CompetitiveWorldState {
    self
      .transitions
      .last()
      .map(|transition| &transition.next)
      .unwrap_or(&self.genesis)
  }
}
