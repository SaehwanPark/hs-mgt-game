use crate::cli::display::{turn_uncertainty_preview, turn_uncertainty_preview_header};
use crate::inputs::resolve_inputs;
use crate::model::*;
use crate::sim::observe_for_player;

#[test]
fn uncertainty_preview_uses_observation_not_actor_outcomes() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let inputs = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);
  let observation = observe_for_player(&prior, &inputs);
  let preview = turn_uncertainty_preview(&prior, &observation, 1, &ruleset).join("\n");

  assert!(preview.contains("reported"));
  assert!(preview.contains("true access unknown"));
  assert!(!preview.contains("Rejected"));
  assert!(!preview.contains("Accepted"));
  assert!(!preview.contains("State hash"));
}

#[test]
fn uncertainty_preview_reports_turn_spend_bound_from_ruleset() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let observation = Observation {
    actor: "health_system_ceo",
    reported_access_index: 70,
    reported_quality_index: 78,
    prior_access_revision: 0,
    policy_briefing: "state policy attention is stable",
    market_competition_briefing: "",
  };

  let turn_one = turn_uncertainty_preview(&prior, &observation, 1, &ruleset).join("\n");
  let turn_two = turn_uncertainty_preview(&prior, &observation, 2, &ruleset).join("\n");
  let turn_three = turn_uncertainty_preview(&prior, &observation, 3, &ruleset).join("\n");
  let turn_four = turn_uncertainty_preview(&prior, &observation, 4, &ruleset).join("\n");

  assert!(turn_one.contains(&format!("up to ${} spend", ruleset.max_capital_spend)));
  assert!(turn_two.contains(&format!("up to ${} spend", ruleset.max_advocacy_spend)));
  assert!(turn_three.contains(&format!("up to ${} spend", ruleset.max_retention_spend)));
  assert!(turn_four.contains(&format!(
    "up to ${} spend",
    ruleset.max_coalition_investment
  )));
}

#[test]
fn uncertainty_preview_includes_prior_access_revision_note() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let observation = Observation {
    actor: "health_system_ceo",
    reported_access_index: 70,
    reported_quality_index: 78,
    prior_access_revision: -2,
    policy_briefing: "state policy attention is stable",
    market_competition_briefing: "",
  };
  let preview = turn_uncertainty_preview(&prior, &observation, 2, &ruleset).join("\n");

  assert!(preview.contains("Measurement note"));
  assert!(preview.contains("prior-period access revision -2"));
}

#[test]
fn uncertainty_preview_includes_market_context_without_rival_outcome() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let observation = Observation {
    actor: "health_system_ceo",
    reported_access_index: 68,
    reported_quality_index: 78,
    prior_access_revision: 0,
    policy_briefing: "state policy attention is stable",
    market_competition_briefing: "a rival system is signaling outpatient capacity expansion nearby",
  };
  let preview = turn_uncertainty_preview(&prior, &observation, 5, &ruleset).join("\n");

  assert!(preview.contains("rival response unknown"));
  assert!(preview.contains("outpatient capacity expansion"));
  assert!(!preview.contains("Accelerate"));
  assert!(!preview.contains("PartialRetreat"));
}

#[test]
fn uncertainty_preview_header_labels_turn() {
  assert_eq!(
    turn_uncertainty_preview_header(2),
    "Turn 2 uncertainty preview"
  );
}
