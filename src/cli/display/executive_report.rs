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
  if calendar.is_annual_tick()
    && let Some(review) = &observation.annual_policy_review
  {
    lines.push("  Year in review".to_string());
    for bullet in review {
      lines.push(format!("  • {bullet}"));
    }
    lines.push(String::new());
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
  // Hierarchical staffing allocation: ICU first, beds second, clinics third (for physicians), ED last
  let target_nurses_icu = observation.icu_capacity;
  let nurses_icu = observation.nurses.min(target_nurses_icu);
  let remaining_nurses_ms = (observation.nurses - nurses_icu).max(0);

  let target_nurses_beds = (observation.staffed_beds + 4) / 5;
  let nurses_beds = remaining_nurses_ms.min(target_nurses_beds);
  let remaining_nurses_ed = (remaining_nurses_ms - nurses_beds).max(0);

  let target_nurses_ed = (observation.emergency_capacity + 1) / 2;
  let nurses_ed = remaining_nurses_ed.min(target_nurses_ed);

  let target_physicians_icu = (observation.icu_capacity + 1) / 2;
  let physicians_icu = observation.physicians.min(target_physicians_icu);
  let remaining_physicians_op = (observation.physicians - physicians_icu).max(0);

  let target_physicians_outpatient = (observation.outpatient_capacity + 9) / 10;
  let physicians_outpatient = remaining_physicians_op.min(target_physicians_outpatient);
  let remaining_physicians_ed = (remaining_physicians_op - physicians_outpatient).max(0);

  let target_physicians_ed = (observation.emergency_capacity + 3) / 4;
  let physicians_ed = remaining_physicians_ed.min(target_physicians_ed);

  let eff_icu = observation
    .icu_capacity
    .min(nurses_icu)
    .min(physicians_icu * 2);
  let eff_beds = observation.staffed_beds.min(nurses_beds * 5);
  let eff_clinics = observation
    .outpatient_capacity
    .min(physicians_outpatient * 10);
  let mut eff_emergency = observation
    .emergency_capacity
    .min(nurses_ed * 2)
    .min(physicians_ed * 4);

  // ED Boarding Calculation
  let critical_admissions = (observation.staffed_beds + 19) / 20;
  let boarded_patients = (critical_admissions - eff_icu).max(0);
  eff_emergency = (eff_emergency - boarded_patients).max(0);

  lines.push(format!(
    "  • Inpatient beds: {} (effective: {}) | Nurses: {}",
    observation.staffed_beds, eff_beds, observation.nurses
  ));
  lines.push(format!(
    "  • Outpatient capacity: {} units (effective: {}) | Physicians: {}",
    observation.outpatient_capacity, eff_clinics, observation.physicians
  ));
  lines.push(format!(
    "  • ICU capacity: {} beds (effective: {})",
    observation.icu_capacity, eff_icu
  ));
  if boarded_patients > 0 {
    lines.push(format!("  • ED boarding: {} patients", boarded_patients));
  }
  lines.push(format!(
    "  • Emergency capacity: {} bays (effective: {})",
    observation.emergency_capacity, eff_emergency
  ));
  lines.push(format!("  • Administrative staff: {}", observation.admins));
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
