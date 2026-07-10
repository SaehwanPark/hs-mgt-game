use super::genesis_competitive_world;
use crate::model::{CashRunwaySignal, Difficulty, PlayerObservation};

pub fn mock_observation_month1(difficulty: Difficulty) -> PlayerObservation {
  let world = genesis_competitive_world(difficulty);
  observation_from_genesis(&world)
}

pub fn observation_from_genesis(world: &crate::model::CompetitiveWorldState) -> PlayerObservation {
  crate::sim::observe_for_human(world, None)
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
        if human.resources.cash >= 70 {
          CashRunwaySignal::Comfortable
        } else if human.resources.cash >= 45 {
          CashRunwaySignal::Watch
        } else {
          CashRunwaySignal::Strained
        }
      );
    }
  }

  #[test]
  fn easy_consultant_monitor_option_is_information_first() {
    let observation = mock_observation_month1(Difficulty::Easy);
    let monitor = observation
      .consultant_options
      .iter()
      .find(|option| option.label == 'C')
      .expect("option C");
    assert!(monitor.title.contains("Information-first"));
  }
}
