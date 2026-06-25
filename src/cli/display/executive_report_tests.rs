use crate::model::{CashRunwaySignal, Difficulty, PolicyCalendar};

use super::executive_report::render_executive_report;
use crate::competitive::{mock_observation_annual_month, mock_observation_month1};

const SECTION_HEADER: &str = "header";
const SECTION_MARKET: &str = "market";
const SECTION_POLICY: &str = "policy";
const SECTION_OWN_STATUS: &str = "own_status";
const SECTION_CONSULTANT: &str = "consultant";
const SECTION_INTEL_GAPS: &str = "intel_gaps";

fn section_ids_in_report(report: &[String]) -> Vec<&'static str> {
  let mut sections = Vec::new();
  let joined = report.join("\n");

  if joined.contains("EXECUTIVE REPORT") {
    sections.push(SECTION_HEADER);
  }
  if joined.contains("MARKET SITUATION") {
    sections.push(SECTION_MARKET);
  }
  if joined.contains("POLICY AND REGULATORY") {
    sections.push(SECTION_POLICY);
  }
  if joined.contains("OWN HEALTH SYSTEM STATUS") {
    sections.push(SECTION_OWN_STATUS);
  }
  if joined.contains("STRATEGY CONSULTANT NOTES") {
    sections.push(SECTION_CONSULTANT);
  }
  if joined.contains("INTELLIGENCE GAPS") {
    sections.push(SECTION_INTEL_GAPS);
  }

  sections
}

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
  let observation = mock_observation_month1(Difficulty::Hard);
  let report = render_executive_report(calendar, &observation, 3, 3);
  let joined = report.join("\n");

  assert!(joined.contains("Reported access index"));
  assert!(joined.contains("Reported quality index"));
  assert!(!joined.contains("Year in review"));
  assert!(!joined.contains("true_access"));
  assert!(!joined.contains("WorldState"));
}
