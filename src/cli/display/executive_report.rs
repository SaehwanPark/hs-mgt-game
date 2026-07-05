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
  // Hierarchical staffing allocation: ICU first, Obstetrics second, beds third, Cardiology fourth, Psychiatric fifth, clinics sixth (for physicians), ED last
  let target_nurses_icu = observation.icu_capacity;
  let nurses_icu = observation.nurses.min(target_nurses_icu);
  let remaining_nurses_obs = (observation.nurses - nurses_icu).max(0);

  let target_nurses_obs = (observation.obstetrics_capacity + 1) / 2;
  let nurses_obs = remaining_nurses_obs.min(target_nurses_obs);
  let remaining_nurses_ms = (remaining_nurses_obs - nurses_obs).max(0);

  let target_nurses_beds = (observation.staffed_beds + 4) / 5;
  let nurses_beds = remaining_nurses_ms.min(target_nurses_beds);
  let remaining_nurses_cardio = (remaining_nurses_ms - nurses_beds).max(0);

  let target_nurses_cardio = (observation.cardiology_capacity + 2) / 3;
  let nurses_cardio = remaining_nurses_cardio.min(target_nurses_cardio);
  let remaining_nurses_psych = (remaining_nurses_cardio - nurses_cardio).max(0);

  let target_nurses_psych = (observation.psychiatric_capacity + 3) / 4;
  let nurses_psych = remaining_nurses_psych.min(target_nurses_psych);
  let remaining_nurses_oncology = (remaining_nurses_psych - nurses_psych).max(0);

  let target_nurses_oncology = (observation.oncology_capacity + 2) / 3;
  let nurses_oncology = remaining_nurses_oncology.min(target_nurses_oncology);
  let remaining_nurses_infusion = (remaining_nurses_oncology - nurses_oncology).max(0);

  let target_nurses_infusion = (observation.infusion_capacity + 3) / 4;
  let nurses_infusion = remaining_nurses_infusion.min(target_nurses_infusion);
  let remaining_nurses_ed = (remaining_nurses_infusion - nurses_infusion).max(0);

  let target_nurses_ed = (observation.emergency_capacity + 1) / 2;
  let nurses_ed = remaining_nurses_ed.min(target_nurses_ed);

  let target_physicians_icu = (observation.icu_capacity + 1) / 2;
  let physicians_icu = observation.physicians.min(target_physicians_icu);
  let remaining_physicians_obs = (observation.physicians - physicians_icu).max(0);

  let target_physicians_obs = (observation.obstetrics_capacity + 4) / 5;
  let physicians_obs = remaining_physicians_obs.min(target_physicians_obs);
  let remaining_physicians_cardio = (remaining_physicians_obs - physicians_obs).max(0);

  let target_physicians_cardio = (observation.cardiology_capacity + 7) / 8;
  let physicians_cardio = remaining_physicians_cardio.min(target_physicians_cardio);
  let remaining_physicians_psych = (remaining_physicians_cardio - physicians_cardio).max(0);

  let target_physicians_psych = (observation.psychiatric_capacity + 9) / 10;
  let physicians_psych = remaining_physicians_psych.min(target_physicians_psych);
  let remaining_physicians_oncology = (remaining_physicians_psych - physicians_psych).max(0);

  let target_physicians_oncology = (observation.oncology_capacity + 7) / 8;
  let physicians_oncology = remaining_physicians_oncology.min(target_physicians_oncology);
  let remaining_physicians_infusion = (remaining_physicians_oncology - physicians_oncology).max(0);

  let target_physicians_infusion = (observation.infusion_capacity + 14) / 15;
  let physicians_infusion = remaining_physicians_infusion.min(target_physicians_infusion);
  let remaining_physicians_op = (remaining_physicians_infusion - physicians_infusion).max(0);

  let target_physicians_outpatient = (observation.outpatient_capacity + 9) / 10;
  let physicians_outpatient = remaining_physicians_op.min(target_physicians_outpatient);
  let remaining_physicians_ed = (remaining_physicians_op - physicians_outpatient).max(0);

  let target_physicians_ed = (observation.emergency_capacity + 3) / 4;
  let physicians_ed = remaining_physicians_ed.min(target_physicians_ed);

  let mut eff_icu = observation
    .icu_capacity
    .min(nurses_icu)
    .min(physicians_icu * 2);
  let mut eff_obs = observation
    .obstetrics_capacity
    .min(nurses_obs * 2)
    .min(physicians_obs * 5);
  let mut eff_beds = observation.staffed_beds.min(nurses_beds * 5);
  let mut eff_cardio = observation
    .cardiology_capacity
    .min(nurses_cardio * 3)
    .min(physicians_cardio * 8);
  let mut eff_psych = observation
    .psychiatric_capacity
    .min(nurses_psych * 4)
    .min(physicians_psych * 10);
  let mut eff_oncology = observation
    .oncology_capacity
    .min(nurses_oncology * 3)
    .min(physicians_oncology * 8);
  let mut eff_infusion = observation
    .infusion_capacity
    .min(nurses_infusion * 4)
    .min(physicians_infusion * 15);
  let mut eff_clinics = observation
    .outpatient_capacity
    .min(physicians_outpatient * 10);
  let mut eff_emergency = observation
    .emergency_capacity
    .min(nurses_ed * 2)
    .min(physicians_ed * 4);

  if observation.rna_strike_active {
    eff_icu /= 2;
    eff_obs /= 2;
    eff_beds /= 2;
    eff_cardio /= 2;
    eff_psych /= 2;
    eff_oncology /= 2;
    eff_infusion /= 2;
    eff_clinics /= 2;
    eff_emergency /= 2;
  }

  // ED Boarding Calculation
  let critical_admissions = (observation.staffed_beds + 19) / 20;
  let boarded_patients = (critical_admissions - eff_icu).max(0);
  eff_emergency = (eff_emergency - boarded_patients).max(0);

  // Cardiology ED Boarding & Diversion Calculation
  let cardiology_demand = (observation.cardiology_capacity + 9) / 10;
  let cardiology_overflow = (cardiology_demand - eff_cardio).max(0);
  let boarded_cardio = cardiology_overflow.min(eff_emergency);
  eff_emergency = (eff_emergency - boarded_cardio).max(0);
  let diverted_cardio = (cardiology_overflow - boarded_cardio).max(0);

  // Psychiatric ED Boarding & Diversion Calculation
  let psychiatric_demand = (observation.psychiatric_capacity + 9) / 10;
  let psychiatric_overflow = (psychiatric_demand - eff_psych).max(0);
  let boarded_psych = psychiatric_overflow.min(eff_emergency);
  eff_emergency = (eff_emergency - boarded_psych).max(0);
  let diverted_psych = (psychiatric_overflow - boarded_psych).max(0);

  // Oncology ED Boarding & Diversion Calculation
  let oncology_demand = (observation.oncology_capacity + 9) / 10;
  let oncology_overflow = (oncology_demand - eff_oncology).max(0);
  let boarded_oncology = oncology_overflow.min(eff_emergency);
  eff_emergency = (eff_emergency - boarded_oncology).max(0);
  let diverted_oncology = (oncology_overflow - boarded_oncology).max(0);

  // Infusion Center Deferral Calculation
  let infusion_demand = (observation.infusion_capacity + 4) / 5;
  let deferred_infusion = (infusion_demand - eff_infusion).max(0);

  // Obstetric Diversion Calculation
  let obstetric_demand = (observation.obstetrics_capacity + 9) / 10;
  let diverted_patients = (obstetric_demand - eff_obs).max(0);

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
  lines.push(format!(
    "  • Obstetrics capacity: {} beds (effective: {})",
    observation.obstetrics_capacity, eff_obs
  ));
  lines.push(format!(
    "  • Cardiology capacity: {} beds (effective: {})",
    observation.cardiology_capacity, eff_cardio
  ));
  lines.push(format!(
    "  • Psychiatric capacity: {} beds (effective: {})",
    observation.psychiatric_capacity, eff_psych
  ));
  lines.push(format!(
    "  • Oncology capacity: {} beds (effective: {})",
    observation.oncology_capacity, eff_oncology
  ));
  lines.push(format!(
    "  • Infusion Center capacity: {} bays (effective: {})",
    observation.infusion_capacity, eff_infusion
  ));
  if diverted_patients > 0 {
    lines.push(format!(
      "  • Obstetric diversion: {} patients",
      diverted_patients
    ));
  }
  if boarded_patients > 0 {
    lines.push(format!("  • ED boarding: {} patients", boarded_patients));
  }
  if boarded_cardio > 0 {
    lines.push(format!(
      "  • Cardiology ED boarding: {} patients",
      boarded_cardio
    ));
  }
  if diverted_cardio > 0 {
    lines.push(format!(
      "  • Cardiology diversion: {} patients",
      diverted_cardio
    ));
  }
  if boarded_psych > 0 {
    lines.push(format!(
      "  • Psychiatric ED boarding: {} patients",
      boarded_psych
    ));
  }
  if diverted_psych > 0 {
    lines.push(format!(
      "  • Psychiatric diversion: {} patients",
      diverted_psych
    ));
  }
  if boarded_oncology > 0 {
    lines.push(format!(
      "  • Oncology ED boarding: {} patients",
      boarded_oncology
    ));
  }
  if diverted_oncology > 0 {
    lines.push(format!(
      "  • Oncology diversion: {} patients",
      diverted_oncology
    ));
  }
  if deferred_infusion > 0 {
    lines.push(format!(
      "  • Infusion sessions deferred: {} patients",
      deferred_infusion
    ));
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
