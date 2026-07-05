use super::genesis_competitive_world;
use crate::model::{
  CashRunwaySignal, ConsultantOption, Difficulty, PlayerObservation, PlayerResources,
};

fn consultant_options_month1(difficulty: Difficulty) -> Vec<ConsultantOption> {
  let monitor_target = if difficulty.k_rivals() >= 2 {
    "Summit"
  } else {
    "Northlake"
  };
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
      title: format!(
        "Monitor {monitor_target}: spend AP on competitor intelligence before committing capital"
      ),
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
  let world = genesis_competitive_world(difficulty);
  observation_from_genesis(&world)
}

pub fn observation_from_genesis(world: &crate::model::CompetitiveWorldState) -> PlayerObservation {
  let human = world
    .human_system()
    .expect("competitive genesis must include human system");
  let mut obs = observation_from_human_system(human, world.difficulty);
  obs.in_flight_projects = crate::sim::in_flight_projects_label(world, human.system_id);
  obs
}

fn cash_runway_signal(resources: &PlayerResources) -> CashRunwaySignal {
  if resources.cash >= 70 {
    CashRunwaySignal::Comfortable
  } else if resources.cash >= 45 {
    CashRunwaySignal::Watch
  } else {
    CashRunwaySignal::Strained
  }
}

fn workforce_trust_summary(trust: i32) -> String {
  if trust >= 60 {
    "moderate; vacancy rate elevated in nursing".to_string()
  } else {
    "strained; vacancy rate elevated in nursing".to_string()
  }
}

fn observation_from_human_system(
  human: &crate::model::HealthSystemState,
  difficulty: Difficulty,
) -> PlayerObservation {
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
    org_name: human.name.clone(),
    reported_access_index: human.access_index,
    prior_access_revision: None,
    reported_quality_index: human.quality_index,
    workforce_trust_summary: workforce_trust_summary(human.workforce_trust),
    community_trust_summary: if human.community_trust >= 60 {
      "stable".to_string()
    } else {
      "watch".to_string()
    },
    staffed_beds: human.staffed_beds,
    outpatient_capacity: human.outpatient_capacity,
    emergency_capacity: human.emergency_capacity,
    icu_capacity: human.icu_capacity,
    obstetrics_capacity: human.obstetrics_capacity,
    psychiatric_capacity: human.psychiatric_capacity,
    cardiology_capacity: human.cardiology_capacity,
    oncology_capacity: human.oncology_capacity,
    infusion_capacity: human.infusion_capacity,
    nurses: human.nurses,
    physicians: human.physicians,
    admins: human.admins,
    in_flight_projects: "none".to_string(),
    cash_runway_signal: cash_runway_signal(&human.resources),
    market_bullets,
    policy_bullets: vec![
      "State Medicaid director signal: access reporting scrutiny increasing".to_string(),
      "Hospital association lobbying: workforce retention tax credit under committee review"
        .to_string(),
      "No federal rule change this month".to_string(),
    ],
    annual_policy_review: None,
    consultant_options: consultant_options_month1(difficulty),
    intel_gaps,
    rna_strike_active: false,
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

#[cfg(test)]
mod fixtures_tests {
  use super::*;
  use crate::model::Difficulty;

  #[test]
  fn observation_metrics_match_human_genesis_system() {
    for difficulty in [
      Difficulty::Easy,
      Difficulty::Normal,
      Difficulty::Hard,
      Difficulty::Expert,
    ] {
      let world = genesis_competitive_world(difficulty);
      let human = world.human_system().expect("human system");
      let observation = observation_from_genesis(&world);
      assert_eq!(observation.org_name, human.name);
      assert_eq!(observation.reported_access_index, human.access_index);
      assert_eq!(observation.reported_quality_index, human.quality_index);
      assert_eq!(
        observation.cash_runway_signal,
        cash_runway_signal(&human.resources)
      );
    }
  }

  #[test]
  fn easy_consultant_monitor_option_targets_northlake() {
    let observation = mock_observation_month1(Difficulty::Easy);
    let monitor = observation
      .consultant_options
      .iter()
      .find(|option| option.label == 'C')
      .expect("option C");
    assert!(monitor.title.contains("Northlake"));
  }
}
