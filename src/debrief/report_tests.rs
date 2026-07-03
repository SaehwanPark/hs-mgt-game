use crate::competitive::build_multi_month_resolution_history;
use crate::debrief::{
  competitive_debrief, competitive_instructor_summary, educational_debrief, instructor_run_summary,
};
use crate::model::Difficulty;
use crate::test_support::demo_history;

#[test]
fn debrief_includes_actor_rationales() {
  let history = demo_history();
  let debrief = educational_debrief(&history).join("\n");

  assert!(debrief.contains("commercial_insurer:"));
  assert!(debrief.contains("state_policy_officials:"));
  assert!(debrief.contains("nursing_workforce:"));
  assert!(debrief.contains("regional_provider_coalition:"));
  assert!(debrief.contains("competitor_health_system:"));
  assert!(debrief.contains("Reported access"));
  assert!(debrief.contains("Access commitment"));
  assert!(debrief.contains("coalition investment choice"));
}

#[test]
fn debrief_includes_attributed_tradeoff() {
  let history = demo_history();
  let debrief = educational_debrief(&history).join("\n");

  assert!(debrief.contains("cash moved from 100 to 32"));
  assert!(debrief.contains("access from 70 to 89"));
  assert!(debrief.contains("capacity investment changed cash by -18"));
  assert!(debrief.contains("state policy response changed community_trust by 2"));
  assert!(debrief.contains("workforce response changed cash by"));
  assert!(debrief.contains("coalition response changed cash by"));
  assert!(debrief.contains("competitor response changed cash by"));
}

#[test]
fn identical_histories_produce_identical_debriefs() {
  let first = demo_history();
  let second = demo_history();

  assert_eq!(educational_debrief(&first), educational_debrief(&second));
}

#[test]
fn debrief_notes_observation_revisions_without_rewriting_history() {
  let history = demo_history();
  let debrief = educational_debrief(&history).join("\n");

  assert!(debrief.contains("Observation revision note:"));
  assert!(debrief.contains("Prior committed observations remain unchanged"));
  assert_eq!(history.transitions[0].observation.prior_access_revision, 0);
}

#[test]
fn test_instructor_run_summary_stabilization() {
  let history = demo_history();
  let summary = instructor_run_summary(&history);
  let summary_str = summary.join("\n");

  assert!(summary_str.contains("=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ==="));
  assert!(summary_str.contains("Observed ="));
  assert!(summary_str.contains("True Prior ="));
  assert!(summary_str.contains("Turn 1 (Turn 0 → 1)"));
}

#[test]
fn test_competitive_instructor_summary_and_debrief() {
  let history = build_multi_month_resolution_history(Difficulty::Normal, 42, 3)
    .expect("should build competitive history");

  let summary = competitive_instructor_summary(&history);
  let summary_str = summary.join("\n");

  assert!(summary_str.contains("=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ==="));
  assert!(summary_str.contains("Month 1:"));
  assert!(summary_str.contains("Rival"));
  assert!(summary_str.contains("unobserved during play - REVEALED FOR INSTRUCTOR REVIEW"));

  let debrief = competitive_debrief(&history);
  let debrief_str = debrief.join("\n");
  assert!(debrief_str.contains("=== INSTRUCTOR RUN SUMMARY & DECISION QUALITY REVIEW ==="));
  assert!(debrief_str.contains("Competitive preview completed 3 committed month(s)"));
}
