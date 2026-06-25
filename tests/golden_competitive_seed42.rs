use hs_mgt_game::competitive::build_month1_resolution_history;
use hs_mgt_game::model::Difficulty;

#[test]
fn competitive_seed42_month1_ai_resolution_is_stable() {
  let history = build_month1_resolution_history(Difficulty::Normal).expect("resolve month 1");
  assert_eq!(history.transitions.len(), 1);

  let transition = &history.transitions[0];
  assert_eq!(transition.prior.turn, 0);
  assert_eq!(transition.next.turn, 1);
  assert_eq!(transition.next.policy_calendar.month_index, 2);
  assert_eq!(
    transition
      .next
      .public_action_log
      .iter()
      .filter(|entry| entry.month_index == 1)
      .count(),
    1
  );
  assert!(
    transition
      .aggregated
      .batches
      .iter()
      .filter(|batch| batch.rationale.is_some())
      .count()
      == 2
  );
  assert_eq!(transition.state_hash, "e68f683da77d7c2f");
}
