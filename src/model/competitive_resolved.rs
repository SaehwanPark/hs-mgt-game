#[derive(Clone, Debug, PartialEq, Eq)]
pub struct CompetitiveResolvedInputs {
  pub monthly_event_signal: i32,
  pub annual_policy_signal: i32,
  pub monthly_event_description: String,
  pub annual_policy_description: Option<String>,
}
