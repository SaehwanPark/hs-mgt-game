use crate::cli::display::{executive_dashboard, strategy_previews};
use crate::model::genesis_state;

#[test]
fn executive_dashboard_reports_starting_state() {
  let dashboard = executive_dashboard(&genesis_state()).join("\n");

  assert!(dashboard.contains("Executive dashboard"));
  assert!(dashboard.contains("Cash 100"));
  assert!(dashboard.contains("staffed beds 120"));
  assert!(dashboard.contains("access 70"));
  assert!(dashboard.contains("policy pressure 30"));
}
#[test]
fn strategy_previews_cover_all_compiled_paths() {
  let previews = strategy_previews();

  assert_eq!(previews.len(), 3);
  assert!(previews[0].contains("1. Access stabilization"));
  assert!(previews[0].contains("spends 68 total resource units"));
  assert!(previews[1].contains("2. Fiscal caution"));
  assert!(previews[1].contains("requests commercial rate 104"));
  assert!(previews[2].contains("3. Aggressive bargaining"));
  assert!(previews[2].contains("commits 13 access/workforce/coalition units"));
}
#[test]
fn strategy_previews_do_not_describe_future_actor_outcomes() {
  let previews = strategy_previews().join("\n");

  assert!(!previews.contains("reject"));
  assert!(!previews.contains("grant flexibility"));
  assert!(!previews.contains("work action"));
  assert!(!previews.contains("full partnership"));
  assert!(!previews.contains("state hash"));
}
