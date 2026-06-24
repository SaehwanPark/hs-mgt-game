use crate::cli::display::{turn_executive_briefing, turn_resolution_summary};
use crate::cli::{build_history_interactive, default_interactive_commands};
use crate::inputs::resolve_inputs;
use crate::model::*;
use crate::sim::observe_for_player;

#[test]
fn turn_briefing_includes_prior_access_revision_when_present() {
  let observation = Observation {
    actor: "health_system_ceo",
    reported_access_index: 65,
    reported_quality_index: 78,
    prior_access_revision: -1,
    policy_briefing: "state officials are increasing scrutiny of access and affordability",
  };
  let briefing = turn_executive_briefing(&genesis_state(), &observation, 2).join("\n");

  assert!(briefing.contains("Prior access measurement revision: -1"));
}
#[test]
fn turn_briefing_uses_observation_not_future_actor_outcomes() {
  let ruleset = default_ruleset();
  let prior = genesis_state();
  let inputs = resolve_inputs(DEFAULT_SEED, &prior, &ruleset);
  let observation = observe_for_player(&prior, &inputs);
  let briefing = turn_executive_briefing(&prior, &observation, 1).join("\n");

  assert!(briefing.contains("Reported access"));
  assert!(!briefing.contains("decision:"));
  assert!(!briefing.contains("Rejected"));
  assert!(!briefing.contains("Accepted"));
}
#[test]
fn turn_resolution_summary_includes_actor_rationale_and_hash() {
  let ruleset = default_ruleset();
  let history =
    build_history_interactive(DEFAULT_SEED, &ruleset, default_interactive_commands()).unwrap();
  let summary = turn_resolution_summary(&history.transitions[0]).join("\n");

  assert!(summary.contains("Turn 1 resolved:"));
  assert!(summary.contains("commercial_insurer"));
  assert!(summary.contains("State hash:"));
}
