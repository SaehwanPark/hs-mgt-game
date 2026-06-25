use crate::model::{CashRunwaySignal, Difficulty, PolicyCalendar};

use super::executive_report::{
  SECTION_CONSULTANT, SECTION_HEADER, SECTION_INTEL_GAPS, SECTION_MARKET, SECTION_OWN_STATUS,
  SECTION_POLICY, render_executive_report, section_ids_in_report,
};
use crate::competitive::{mock_observation_annual_month, mock_observation_month1};

#[test]
fn executive_report_includes_all_six_sections() {
  let calendar = PolicyCalendar::new_month(1);
  let observation = mock_observation_month1(Difficulty::Normal);
  let report = render_executive_report(calendar, &observation, 3, 3);
  let sections = section_ids_in_report(&report);

  assert_eq!(sections.len(), 6);
  assert!(sections.contains(&SECTION_HEADER));
  assert!(sections.contains(&SECTION_MARKET));
  assert!(sections.contains(&SECTION_POLICY));
  assert!(sections.contains(&SECTION_OWN_STATUS));
  assert!(sections.contains(&SECTION_CONSULTANT));
  assert!(sections.contains(&SECTION_INTEL_GAPS));
}

#[test]
fn consultant_section_avoids_optimal_wording() {
  let calendar = PolicyCalendar::new_month(1);
  let observation = mock_observation_month1(Difficulty::Easy);
  let report = render_executive_report(calendar, &observation, 4, 4);
  let joined = report.join("\n").to_lowercase();

  assert!(!joined.contains("optimal"));
  assert!(!joined.contains("correct"));
  assert!(joined.contains("advisory, not binding"));
}

#[test]
fn annual_month_fixture_includes_year_in_review() {
  let calendar = PolicyCalendar::new_month(12);
  let observation = mock_observation_annual_month(Difficulty::Normal);
  let report = render_executive_report(calendar, &observation, 3, 3);
  let joined = report.join("\n");

  assert!(calendar.is_annual_tick());
  assert!(joined.contains("Year in review"));
  assert!(matches!(
    observation.cash_runway_signal,
    CashRunwaySignal::Comfortable
  ));
}

#[test]
fn report_uses_reported_metric_labels() {
  let calendar = PolicyCalendar::new_month(4);
  let observation = mock_observation_annual_month(Difficulty::Hard);
  let report = render_executive_report(calendar, &observation, 3, 3);
  let joined = report.join("\n");

  assert!(joined.contains("Reported access index"));
  assert!(joined.contains("Reported quality index"));
  assert!(!joined.contains("true_access"));
  assert!(!joined.contains("WorldState"));
}
