use crate::model::{PlayerObservation, PolicyCalendar};

use super::style;

pub fn render_executive_report(
  calendar: PolicyCalendar,
  observation: &PlayerObservation,
  ap_remaining: u32,
  ap_budget: u32,
  pc_remaining: u32,
  pc_cap: u32,
) -> Vec<String> {
  let mut lines = Vec::new();

  lines.push("══════════════════════════════════════════════════════════════".to_string());
  lines.push(format!(
    "  EXECUTIVE REPORT — {}",
    observation.org_name.to_uppercase()
  ));
  lines.push(format!(
    "  Year {}, Month {} ({})          Action points remaining: {}/{}",
    calendar.year,
    calendar.month_in_year,
    calendar.month_name(),
    ap_remaining,
    ap_budget
  ));
  lines.push(format!(
    "  Political capital remaining: {}/{}",
    pc_remaining, pc_cap
  ));
  lines.push(format!(
    "  Cash runway: {}",
    observation.cash_runway_signal.label()
  ));
  lines.push("══════════════════════════════════════════════════════════════".to_string());
  lines.push(String::new());

  lines.push(style::subsection("MARKET SITUATION"));
  for bullet in &observation.market_bullets {
    lines.push(format!("  • {bullet}"));
  }
  lines.push(String::new());

  lines.push(style::subsection("POLICY AND REGULATORY"));
  if calendar.is_annual_tick() {
    if let Some(review) = &observation.annual_policy_review {
      lines.push("  Year in review".to_string());
      for bullet in review {
        lines.push(format!("  • {bullet}"));
      }
      lines.push(String::new());
    }
  }
  for bullet in &observation.policy_bullets {
    lines.push(format!("  • {bullet}"));
  }
  lines.push(String::new());

  lines.push(style::subsection("OWN HEALTH SYSTEM STATUS"));
  lines.push(format!(
    "  • Reported access index: {}",
    observation.reported_access_index
  ));
  if let Some((month, prior)) = observation.prior_access_revision {
    lines.push(format!(
      "  • Prior revision: {prior} in Month {month} (reported)"
    ));
  }
  lines.push(format!(
    "  • Reported quality index: {}",
    observation.reported_quality_index
  ));
  lines.push(format!(
    "  • Workforce trust: {}",
    observation.workforce_trust_summary
  ));
  lines.push(format!(
    "  • Community trust: {}",
    observation.community_trust_summary
  ));
  lines.push(format!("  • In-flight: {}", observation.in_flight_projects));
  lines.push(String::new());

  lines.push(style::subsection(
    "STRATEGY CONSULTANT NOTES — Advisory, not binding",
  ));
  for option in &observation.consultant_options {
    lines.push(format!("  • Option {} — {}:", option.label, option.title));
    for bullet in &option.tradeoff_bullets {
      lines.push(format!("      {bullet}."));
    }
  }
  lines.push(String::new());

  lines.push(style::subsection("INTELLIGENCE GAPS"));
  for bullet in &observation.intel_gaps {
    lines.push(format!("  • {bullet}"));
  }
  lines.push("══════════════════════════════════════════════════════════════".to_string());

  lines
}
