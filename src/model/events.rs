#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Observation {
  pub actor: &'static str,
  pub reported_access_index: i32,
  pub reported_quality_index: i32,
  pub prior_access_revision: i32,
  pub policy_briefing: &'static str,
  pub market_competition_briefing: &'static str,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Event {
  pub actor: &'static str,
  pub description: String,
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct AttributedEffect {
  pub source: &'static str,
  pub metric: &'static str,
  pub delta: i32,
}
