use crate::model::{Observation, Ruleset, WorldState};

pub fn turn_uncertainty_preview_header(turn_number: u32) -> String {
  format!("Turn {turn_number} uncertainty preview")
}

pub fn turn_uncertainty_preview(
  prior: &WorldState,
  observation: &Observation,
  turn_number: u32,
  ruleset: &Ruleset,
) -> Vec<String> {
  let mut lines = vec![
    format!(
      "  Access outlook: reported {} (true access unknown); reports may be noisy or revised",
      observation.reported_access_index
    ),
    format!(
      "  Spend flexibility: ${} cash on hand; up to ${} spend bound this turn",
      prior.cash,
      max_spend_for_turn(turn_number, ruleset)
    ),
    format!(
      "  Policy pressure: {} ({})",
      prior.policy_pressure,
      policy_pressure_label(prior.policy_pressure)
    ),
    format!(
      "  Policy briefing: {} (not a forecast of actor response)",
      observation.policy_briefing
    ),
  ];

  if observation.prior_access_revision != 0 {
    lines.push(format!(
      "  Measurement note: prior-period access revision {} already on record",
      observation.prior_access_revision
    ));
  }

  if !observation.market_competition_briefing.is_empty() {
    lines.push(format!(
      "  Market context: {} (rival response unknown)",
      observation.market_competition_briefing
    ));
  }

  lines
}

fn max_spend_for_turn(turn_number: u32, ruleset: &Ruleset) -> i32 {
  match turn_number {
    1 => ruleset.max_capital_spend,
    2 => ruleset.max_advocacy_spend,
    3 => ruleset.max_retention_spend,
    4 => ruleset.max_coalition_investment,
    5 => ruleset.max_defensive_capital_commitment,
    _ => 0,
  }
}

fn policy_pressure_label(pressure: i32) -> &'static str {
  if pressure >= 50 {
    "elevated"
  } else if pressure >= 35 {
    "moderate"
  } else {
    "lower"
  }
}
