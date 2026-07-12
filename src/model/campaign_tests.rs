use super::{CampaignId, Difficulty, PolicyCalendar};

#[test]
fn campaign_id_matches_scenario_format_strings() {
  assert_eq!(CampaignId::StabilizationV1.as_str(), "stabilization-v1");
  assert_eq!(
    CampaignId::CompetitiveRegionalV1.as_str(),
    "competitive-regional-v1"
  );
  assert_eq!(
    CampaignId::RegionalAffiliationV1.as_str(),
    "regional-affiliation-v1"
  );
}

#[test]
fn difficulty_maps_k_and_ap_budgets() {
  assert_eq!(Difficulty::Easy.k_rivals(), 1);
  assert_eq!(Difficulty::Normal.k_rivals(), 2);
  assert_eq!(Difficulty::Hard.k_rivals(), 3);
  assert_eq!(Difficulty::Expert.k_rivals(), 4);

  assert_eq!(Difficulty::Easy.human_ap_per_month(), 4);
  assert_eq!(Difficulty::Expert.human_ap_per_month(), 2);
  assert_eq!(Difficulty::Expert.cpu_ap_per_month(), 4);
}

#[test]
fn policy_calendar_advances_year_boundary() {
  let month_12 = PolicyCalendar::new_month(12);
  assert_eq!(month_12.year, 1);
  assert_eq!(month_12.month_in_year, 12);
  assert!(month_12.is_annual_tick());

  let month_13 = month_12.advance();
  assert_eq!(month_13.month_index, 13);
  assert_eq!(month_13.year, 2);
  assert_eq!(month_13.month_in_year, 1);
  assert!(!month_13.is_annual_tick());
}
