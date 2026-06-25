use crate::model::{CashRunwaySignal, ConsultantOption, Difficulty, PlayerObservation};

fn consultant_options_month1() -> Vec<ConsultantOption> {
  vec![
    ConsultantOption {
      label: 'A',
      title: "Defensive capacity: invest in staffed beds to match Northlake expansion".to_string(),
      tradeoff_bullets: vec!["protects share but strains cash if payer rate unchanged".to_string()],
    },
    ConsultantOption {
      label: 'B',
      title: "Workforce-first: recruit nurses and offer schedule relief".to_string(),
      tradeoff_bullets: vec!["slower share defense but reduces escalation risk".to_string()],
    },
    ConsultantOption {
      label: 'C',
      title: "Monitor Summit: spend AP on competitor intelligence before committing capital"
        .to_string(),
      tradeoff_bullets: vec!["delays response one month".to_string()],
    },
    ConsultantOption {
      label: 'D',
      title: "Public access pledge: commit to ED wait-time target".to_string(),
      tradeoff_bullets: vec!["may pre-empt state scrutiny; rivals will observe".to_string()],
    },
  ]
}

pub fn mock_observation_month1(difficulty: Difficulty) -> PlayerObservation {
  let k = difficulty.k_rivals();
  let mut market_bullets = vec![
    "Regional inpatient demand: stable-to-rising (+0.8% vs prior month, reported)".to_string(),
    "Commercial payer mix: two major carriers; renewal discussions expected Q4".to_string(),
  ];

  if k >= 1 {
    market_bullets.insert(
      1,
      "Rival Northlake Health (observed, prior month): signaled med-surg expansion interest"
        .to_string(),
    );
  }
  if k >= 2 {
    market_bullets.push(
      "Rival Summit Care (observed, prior month): held capacity; increased outpatient marketing"
        .to_string(),
    );
  }
  if k >= 3 {
    market_bullets.push(
      "Rival Valley Regional (observed, prior month): community access pledge under review"
        .to_string(),
    );
  }
  if k >= 4 {
    market_bullets.push(
      "Rival Metro Academic (observed, prior month): lobbying for certificate-of-need flexibility"
        .to_string(),
    );
  }

  let mut intel_gaps =
    vec!["Northlake private payer negotiations (not publicly disclosed)".to_string()];
  if k >= 2 {
    intel_gaps.push("Summit capital budget allocation beyond marketing (unobserved)".to_string());
    intel_gaps.push("Northlake intelligence depth 2 is available (1 AP)".to_string());
  }

  PlayerObservation {
    org_name: "Riverside Community Health".to_string(),
    reported_access_index: 68,
    prior_access_revision: None,
    reported_quality_index: 72,
    workforce_trust_summary: "moderate; vacancy rate elevated in nursing".to_string(),
    community_trust_summary: "stable".to_string(),
    in_flight_projects: "none".to_string(),
    cash_runway_signal: CashRunwaySignal::Watch,
    market_bullets,
    policy_bullets: vec![
      "State Medicaid director signal: access reporting scrutiny increasing".to_string(),
      "Hospital association lobbying: workforce retention tax credit under committee review"
        .to_string(),
      "No federal rule change this month".to_string(),
    ],
    annual_policy_review: None,
    consultant_options: consultant_options_month1(),
    intel_gaps,
  }
}

pub fn mock_observation_annual_month(difficulty: Difficulty) -> PlayerObservation {
  let mut observation = mock_observation_month1(difficulty);
  observation.reported_access_index = 71;
  observation.prior_access_revision = Some((2, 69));
  observation.cash_runway_signal = CashRunwaySignal::Comfortable;
  observation.annual_policy_review = Some(vec![
    "Commercial payer renewals: one carrier signaled tighter rate corridor".to_string(),
    "State workforce grant: partial award; implementation rules pending".to_string(),
    "Medicaid access reporting: new quarterly template effective next year".to_string(),
  ]);
  observation
}
