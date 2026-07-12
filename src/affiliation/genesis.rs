use crate::model::{AffiliationWorldState, default_affiliation_ruleset};
use crate::scenario::{Scenario, default_regional_affiliation_scenario};

pub fn genesis_affiliation_world(
  scenario: Option<&Scenario>,
) -> Result<AffiliationWorldState, crate::scenario::ScenarioError> {
  let scenario = match scenario {
    Some(scenario) => scenario.clone(),
    None => default_regional_affiliation_scenario()?,
  };
  let ruleset = default_affiliation_ruleset();
  crate::scenario::validate_regional_affiliation_scenario(&scenario, &ruleset)?;
  scenario.initial_affiliation_world_state()
}
