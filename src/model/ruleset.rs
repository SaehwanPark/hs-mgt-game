#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Ruleset {
  pub version: &'static str,
  pub max_capital_spend: i32,
  pub max_advocacy_spend: i32,
  pub max_retention_spend: i32,
  pub max_schedule_relief_commitment: i32,
  pub max_coalition_investment: i32,
  pub target_commercial_rate: i32,
  pub minimum_access_commitment: i32,
  pub minimum_retention_spend: i32,
  pub minimum_schedule_relief: i32,
  pub minimum_coalition_investment: i32,
  pub minimum_shared_access_commitment: i32,
  pub max_shared_access_commitment: i32,
  pub max_defensive_capital_commitment: i32,
  pub minimum_defensive_capital_commitment: i32,
  pub minimum_access_posture: i32,
  pub max_access_posture: i32,
}

pub fn default_ruleset() -> Ruleset {
  Ruleset {
    version: "demo-ruleset-0.1.9",
    max_capital_spend: 40,
    max_advocacy_spend: 20,
    max_retention_spend: 25,
    max_schedule_relief_commitment: 20,
    max_coalition_investment: 20,
    target_commercial_rate: 106,
    minimum_access_commitment: 5,
    minimum_retention_spend: 5,
    minimum_schedule_relief: 3,
    minimum_coalition_investment: 4,
    minimum_shared_access_commitment: 4,
    max_shared_access_commitment: 20,
    max_defensive_capital_commitment: 25,
    minimum_defensive_capital_commitment: 4,
    minimum_access_posture: 3,
    max_access_posture: 15,
  }
}
