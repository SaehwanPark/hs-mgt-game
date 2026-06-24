use crate::debrief::educational_debrief;
use crate::test_support::demo_history;

#[test]
fn debrief_includes_actor_rationales() {
  let history = demo_history();
  let debrief = educational_debrief(&history).join("\n");

  assert!(debrief.contains("commercial_insurer:"));
  assert!(debrief.contains("state_policy_officials:"));
  assert!(debrief.contains("nursing_workforce:"));
  assert!(debrief.contains("regional_provider_coalition:"));
  assert!(debrief.contains("Reported access"));
  assert!(debrief.contains("Access commitment"));
  assert!(debrief.contains("coalition investment choice"));
}
#[test]
fn debrief_includes_attributed_tradeoff() {
  let history = demo_history();
  let debrief = educational_debrief(&history).join("\n");

  assert!(debrief.contains("cash moved from 100 to 46"));
  assert!(debrief.contains("access from 70 to 83"));
  assert!(debrief.contains("capacity investment changed cash by -18"));
  assert!(debrief.contains("state policy response changed community_trust by 2"));
  assert!(debrief.contains("workforce response changed cash by"));
  assert!(debrief.contains("coalition response changed cash by"));
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
